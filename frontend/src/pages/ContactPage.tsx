import { useTranslation } from "react-i18next";

import { ContactForm } from "@/features/contact/ContactForm";
import { useProfile } from "@/hooks/usePortfolioQueries";
import { useSeo } from "@/hooks/useSeo";

export default function ContactPage() {
  const { t } = useTranslation();
  const profile = useProfile();

  useSeo({
    title: "Contact — Daniele Mario Areddu",
    description:
      "Invite Daniele Mario Areddu to speak, or start a conversation about a project.",
    path: "/contact",
  });

  return (
    <div className="container-editorial max-w-3xl py-16 sm:py-24">
      <p className="eyebrow">{t("nav.contact")}</p>
      <h1 className="mt-4 text-balance font-serif text-4xl leading-tight text-ink sm:text-5xl">
        {t("contact.title")}
      </h1>
      <p className="mt-4 max-w-xl text-lg text-ink-soft">{t("contact.intro")}</p>

      {profile.data ? (
        <p className="mt-4 text-sm text-ink-faint">
          {t("contact.emailLabel")}{" "}
          <a
            href={`mailto:${profile.data.public_email}`}
            className="font-medium text-ink underline"
          >
            {profile.data.public_email}
          </a>
        </p>
      ) : null}

      <div className="mt-10">
        <ContactForm />
      </div>
    </div>
  );
}
