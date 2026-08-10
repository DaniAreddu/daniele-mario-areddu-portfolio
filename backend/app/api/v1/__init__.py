from fastapi import APIRouter

from app.api.v1 import (
    admin_auth,
    admin_events,
    admin_projects,
    admin_tags,
    biography,
    community,
    contact,
    education,
    events,
    experiences,
    journey,
    passions,
    profile,
    projects,
    skills,
    talks,
)

router = APIRouter()
router.include_router(profile.router, tags=["profile"])
router.include_router(biography.router, tags=["profile"])
router.include_router(education.router, tags=["education"])
router.include_router(journey.router, tags=["journey"])
router.include_router(experiences.router, tags=["experience"])
router.include_router(projects.router, tags=["projects"])
router.include_router(skills.router, tags=["skills"])
router.include_router(events.router, tags=["events"])
router.include_router(talks.router, tags=["talks"])
router.include_router(passions.router, tags=["passions"])
router.include_router(community.router, tags=["community"])
router.include_router(contact.router, tags=["contact"])
router.include_router(admin_auth.router, tags=["admin-auth"])
router.include_router(admin_events.router, tags=["admin-events"])
router.include_router(admin_projects.router, tags=["admin-projects"])
router.include_router(admin_tags.router, tags=["admin-tags"])
