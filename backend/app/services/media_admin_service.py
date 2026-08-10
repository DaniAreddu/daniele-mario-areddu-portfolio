"""Admin media library: upload validation, variant generation, and usage
detection before delete.

Security-critical invariants (do not relax without re-reading
docs/admin-guide.md's security review):
  - `storage_key` is always server-generated (`uuid4().hex`), never derived
    from the client filename — `original_filename` is pure display
    metadata and never touches a filesystem path. This eliminates path
    traversal by construction rather than by filtering.
  - The uploaded bytes are validated by actually decoding them as an image
    with Pillow (format allow-list), never by trusting the client-supplied
    Content-Type header or the filename extension.
  - Pillow's default `MAX_IMAGE_PIXELS` decompression-bomb guard is left on.
"""

from __future__ import annotations

import io
import uuid
from typing import Any

from PIL import Image, ImageOps
from sqlalchemy import select

from app.core.config import Settings
from app.core.errors import AppError, NotFoundError
from app.models.admin_user import AdminUser
from app.models.education import Education
from app.models.event import Event
from app.models.experience import Experience
from app.models.media_asset import MediaAsset
from app.models.project import Project
from app.repositories.media_repository import MediaRepository
from app.schemas.media_admin import MediaAssetOut, MediaAssetUpdate, MediaUsageOut
from app.services._admin_common import record_audit_event
from app.services.storage import LocalFilesystemStorage

_ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP", "GIF"}
_VARIANT_SIZES = {"thumbnail": (200, 200), "medium": (800, 800)}


class UnsupportedMediaError(AppError):
    status_code = 415
    code = "unsupported_media_type"


class MediaTooLargeError(AppError):
    status_code = 413
    code = "media_too_large"


def _extension_for(pillow_format: str) -> str:
    return {"JPEG": "jpg", "PNG": "png", "WEBP": "webp", "GIF": "gif"}[pillow_format]


def _to_out(asset: MediaAsset, storage: LocalFilesystemStorage) -> MediaAssetOut:
    return MediaAssetOut(
        id=asset.id,
        storage_key=asset.storage_key,
        url=storage.url_for(asset.storage_key),
        original_filename=asset.original_filename,
        mime_type=asset.mime_type,
        size_bytes=asset.size_bytes,
        width=asset.width,
        height=asset.height,
        alt_text=asset.alt_text,
        caption=asset.caption,
        variants={name: storage.url_for(key) for name, key in asset.variants.items()},
        uploaded_by_email=asset.uploaded_by.email if asset.uploaded_by else None,
        created_at=asset.created_at,
    )


class MediaAdminService:
    def __init__(
        self,
        repository: MediaRepository,
        storage: LocalFilesystemStorage,
        settings: Settings,
    ) -> None:
        self.repository = repository
        self.storage = storage
        self.settings = settings

    async def list_all(self) -> list[MediaAssetOut]:
        assets = await self.repository.list_all()
        return [_to_out(asset, self.storage) for asset in assets]

    async def get(self, media_id: int) -> MediaAssetOut:
        asset = await self._get_or_404(media_id)
        return _to_out(asset, self.storage)

    async def _get_or_404(self, media_id: int) -> MediaAsset:
        asset = await self.repository.get_by_id(media_id)
        if asset is None:
            raise NotFoundError("Media asset not found.")
        return asset

    async def upload(
        self, *, filename: str, content_type: str, data: bytes, actor: AdminUser
    ) -> MediaAssetOut:
        if len(data) > self.settings.media_max_upload_bytes:
            max_mb = self.settings.media_max_upload_bytes // (1024 * 1024)
            raise MediaTooLargeError(f"File exceeds the {max_mb} MB limit.")

        # The actual decode is the validation — never trust `content_type`
        # or the filename extension for this.
        try:
            with Image.open(io.BytesIO(data)) as probe:
                probe.verify()
            with Image.open(io.BytesIO(data)) as image:
                image_format = image.format
                if image_format not in _ALLOWED_FORMATS:
                    raise UnsupportedMediaError(f"Unsupported image format: {image_format}")
                # Re-open after verify() (which leaves the file unusable for
                # further ops) and normalize orientation/strip EXIF by
                # re-encoding through a fresh buffer.
                image = ImageOps.exif_transpose(image) or image
                width, height = image.size
                variants = self._build_variants(image, image_format)
        except UnsupportedMediaError:
            raise
        except Exception as exc:
            raise UnsupportedMediaError("The uploaded file is not a valid image.") from exc

        extension = _extension_for(image_format)
        storage_key = f"{uuid.uuid4().hex}.{extension}"
        await self.storage.save(storage_key, data)

        variant_keys: dict[str, str] = {}
        for variant_name, variant_bytes in variants.items():
            variant_key = f"{uuid.uuid4().hex}-{variant_name}.webp"
            await self.storage.save(variant_key, variant_bytes)
            variant_keys[variant_name] = variant_key

        asset = MediaAsset(
            storage_key=storage_key,
            original_filename=filename[:255],
            mime_type=f"image/{extension}",
            size_bytes=len(data),
            width=width,
            height=height,
            variants=variant_keys,
            uploaded_by_id=actor.id,
        )
        await self.repository.create(asset)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="media.upload",
            entity_type="media_asset",
            entity_id=asset.id,
            summary=f"Uploaded '{asset.original_filename}'",
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(asset, attribute_names=["uploaded_by"])
        return _to_out(asset, self.storage)

    def _build_variants(self, image: Image.Image, image_format: str) -> dict[str, bytes]:
        variants: dict[str, bytes] = {}
        rgb_image = image.convert("RGB") if image.mode not in ("RGB", "RGBA") else image
        for name, size in _VARIANT_SIZES.items():
            if image.width <= size[0] and image.height <= size[1]:
                continue  # never upscale a smaller original
            resized = rgb_image.copy()
            resized.thumbnail(size, Image.Resampling.LANCZOS)
            buffer = io.BytesIO()
            resized.save(buffer, format="WEBP", quality=82)
            variants[name] = buffer.getvalue()
        return variants

    async def update(
        self, media_id: int, payload: MediaAssetUpdate, actor: AdminUser
    ) -> MediaAssetOut:
        asset = await self._get_or_404(media_id)
        asset.alt_text = payload.alt_text
        asset.caption = payload.caption
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="media.update",
            entity_type="media_asset",
            entity_id=asset.id,
            summary=f"Updated metadata for '{asset.original_filename}'",
        )
        await self.repository.session.commit()
        return _to_out(asset, self.storage)

    async def check_usage(self, media_id: int) -> MediaUsageOut:
        asset = await self._get_or_404(media_id)
        url = self.storage.url_for(asset.storage_key)
        session = self.repository.session
        references: list[str] = []

        checks: list[tuple[type[Any], Any, str]] = [
            (Event, Event.image, "event"),
            (Project, Project.cover_image_url, "project"),
            (Experience, Experience.logo_media_url, "experience"),
            (Education, Education.logo_media_url, "education"),
        ]
        for model, column, label in checks:
            result = await session.execute(select(model.id).where(column == url))
            references.extend(f"{label}:{row[0]}" for row in result)

        return MediaUsageOut(reference_count=len(references), referenced_in=references)

    async def delete(self, media_id: int, actor: AdminUser, *, force: bool = False) -> None:
        asset = await self._get_or_404(media_id)
        usage = await self.check_usage(media_id)
        if usage.reference_count > 0 and not force:
            raise AppError(
                f"This file is used by {usage.reference_count} item(s). "
                "Pass force=true to delete it anyway.",
                code="media_in_use",
            )
        await self.storage.delete(asset.storage_key)
        for variant_key in asset.variants.values():
            await self.storage.delete(variant_key)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="media.delete",
            entity_type="media_asset",
            entity_id=asset.id,
            summary=f"Deleted '{asset.original_filename}'",
        )
        await self.repository.delete(asset)
        await self.repository.session.commit()
