import { useState } from "react";

import { AdminApiError } from "@/admin/api/adminApiClient";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { ConfirmDialog } from "@/admin/components/ui/ConfirmDialog";
import { Input } from "@/admin/components/ui/Input";
import { useAdminToast } from "@/admin/components/ui/Toast";
import {
  useAdminSkillCategories,
  useCreateSkill,
  useCreateSkillCategory,
  useDeleteSkill,
  useDeleteSkillCategory,
  useUpdateSkill,
  useUpdateSkillCategory,
} from "@/admin/hooks/useAdminSkills";
import type { SkillAdmin, SkillCategoryAdmin } from "@/admin/types/skill";

function describeError(error: unknown): string {
  if (error instanceof AdminApiError) return error.message;
  return "Something went wrong. Please try again.";
}

function slugify(value: string): string {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function NewCategoryForm() {
  const [name, setName] = useState("");
  const { showToast } = useAdminToast();
  const createCategory = useCreateSkillCategory();

  async function handleCreate() {
    if (!name.trim()) return;
    try {
      await createCategory.mutateAsync({
        slug: slugify(name),
        name_en: name.trim(),
        name_it: "",
        description_en: null,
        description_it: null,
        sort_order: 0,
        enabled: true,
      });
      setName("");
      showToast({ title: "Category added" });
    } catch (error) {
      showToast({
        title: "Could not add category",
        description: describeError(error),
        variant: "error",
      });
    }
  }

  return (
    <Card className="flex flex-wrap items-end gap-3">
      <div className="flex-1">
        <label htmlFor="new-category-name" className="eyebrow">
          New category name
        </label>
        <div className="mt-2">
          <Input
            id="new-category-name"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Languages & Frameworks"
          />
        </div>
      </div>
      <Button onClick={() => void handleCreate()} disabled={createCategory.isPending}>
        Add category
      </Button>
    </Card>
  );
}

function SkillRow({ skill }: { skill: SkillAdmin }) {
  const { showToast } = useAdminToast();
  const updateSkill = useUpdateSkill();
  const deleteSkill = useDeleteSkill();

  async function toggle(field: "enabled" | "is_featured") {
    try {
      await updateSkill.mutateAsync({
        id: skill.id,
        payload: {
          category_id: skill.category_id,
          name: skill.name,
          context_en: skill.context_en,
          context_it: skill.context_it,
          is_featured: field === "is_featured" ? !skill.is_featured : skill.is_featured,
          enabled: field === "enabled" ? !skill.enabled : skill.enabled,
          sort_order: skill.sort_order,
        },
      });
    } catch (error) {
      showToast({
        title: "Could not update skill",
        description: describeError(error),
        variant: "error",
      });
    }
  }

  return (
    <li className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-ink/10 p-3 text-sm">
      <span className={skill.enabled ? "text-ink" : "text-ink-faint line-through"}>
        {skill.name}
      </span>
      <div className="flex items-center gap-4">
        <label className="flex items-center gap-2 text-xs text-ink-soft">
          <input
            type="checkbox"
            className="h-4 w-4 rounded border-ink/30"
            checked={skill.is_featured}
            onChange={() => void toggle("is_featured")}
          />
          Featured
        </label>
        <label className="flex items-center gap-2 text-xs text-ink-soft">
          <input
            type="checkbox"
            className="h-4 w-4 rounded border-ink/30"
            checked={skill.enabled}
            onChange={() => void toggle("enabled")}
          />
          Enabled
        </label>
        <ConfirmDialog
          trigger={
            <Button variant="danger" className="px-3 py-1 text-xs">
              Delete
            </Button>
          }
          title="Delete this skill?"
          description="This cannot be undone."
          confirmLabel="Delete"
          onConfirm={() => void deleteSkill.mutateAsync(skill.id)}
        />
      </div>
    </li>
  );
}

function NewSkillForm({ categoryId }: { categoryId: number }) {
  const [name, setName] = useState("");
  const { showToast } = useAdminToast();
  const createSkill = useCreateSkill();

  async function handleCreate() {
    if (!name.trim()) return;
    try {
      await createSkill.mutateAsync({
        category_id: categoryId,
        name: name.trim(),
        context_en: null,
        context_it: null,
        is_featured: false,
        enabled: true,
        sort_order: 0,
      });
      setName("");
    } catch (error) {
      showToast({
        title: "Could not add skill",
        description: describeError(error),
        variant: "error",
      });
    }
  }

  return (
    <div className="flex items-center gap-3">
      <Input
        value={name}
        onChange={(event) => setName(event.target.value)}
        placeholder="Skill name"
        aria-label="New skill name"
        className="max-w-xs"
        onKeyDown={(event) => {
          if (event.key === "Enter") {
            event.preventDefault();
            void handleCreate();
          }
        }}
      />
      <Button
        variant="secondary"
        onClick={() => void handleCreate()}
        disabled={createSkill.isPending}
      >
        Add skill
      </Button>
    </div>
  );
}

function CategoryCard({ category }: { category: SkillCategoryAdmin }) {
  const { showToast } = useAdminToast();
  const updateCategory = useUpdateSkillCategory();
  const deleteCategory = useDeleteSkillCategory();

  async function toggleEnabled() {
    try {
      await updateCategory.mutateAsync({
        id: category.id,
        payload: {
          slug: category.slug,
          name_en: category.name_en,
          name_it: category.name_it,
          description_en: category.description_en,
          description_it: category.description_it,
          sort_order: category.sort_order,
          enabled: !category.enabled,
        },
      });
    } catch (error) {
      showToast({
        title: "Could not update category",
        description: describeError(error),
        variant: "error",
      });
    }
  }

  return (
    <Card className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="font-serif text-lg text-ink">{category.name_en}</h2>
          <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">
            {category.slug}
          </p>
        </div>
        <div className="flex items-center gap-4">
          <label className="flex items-center gap-2 text-xs text-ink-soft">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-ink/30"
              checked={category.enabled}
              onChange={() => void toggleEnabled()}
            />
            Enabled
          </label>
          <ConfirmDialog
            trigger={
              <Button variant="danger" className="px-3 py-1 text-xs">
                Delete category
              </Button>
            }
            title="Delete this category?"
            description="Skills inside it must be removed first."
            confirmLabel="Delete"
            onConfirm={() => void deleteCategory.mutateAsync(category.id)}
          />
        </div>
      </div>

      {category.skills.length > 0 ? (
        <ul className="space-y-2">
          {category.skills.map((skill) => (
            <SkillRow key={skill.id} skill={skill} />
          ))}
        </ul>
      ) : (
        <p className="text-sm text-ink-faint">No skills in this category yet.</p>
      )}

      <NewSkillForm categoryId={category.id} />
    </Card>
  );
}

export default function SkillsPage() {
  const { data: categories, isLoading, isError } = useAdminSkillCategories();

  return (
    <div className="max-w-3xl">
      <div>
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Skills</p>
        <h1 className="mt-2 font-serif text-3xl text-ink">Skills & categories</h1>
        <p className="mt-2 text-sm text-ink-soft">
          Skills have no draft/publish lifecycle — changes here are live immediately. Disabled
          skills and categories are hidden from the public site but not deleted.
        </p>
      </div>

      <div className="mt-6">
        <NewCategoryForm />
      </div>

      <div className="mt-6 space-y-6">
        {isLoading ? (
          <p className="text-sm text-ink-faint">Loading…</p>
        ) : isError ? (
          <p className="text-sm text-red-700">Could not load skills.</p>
        ) : categories && categories.length > 0 ? (
          categories
            .slice()
            .sort((a, b) => a.sort_order - b.sort_order)
            .map((category) => <CategoryCard key={category.id} category={category} />)
        ) : (
          <div className="rounded-2xl border border-dashed border-ink/15 p-10 text-center">
            <p className="text-ink-soft">No categories yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}
