import { useTranslation } from "react-i18next";

import { useLocale } from "@/app/LocaleContext";
import { useSeo } from "@/hooks/useSeo";

const EN_COPY = {
  intro:
    "This page explains, in plain terms, what happens to the information you share through the contact form on this site.",
  sections: [
    {
      title: "What is collected",
      body: "When you submit the contact form, this site stores your name, email address, organization (if provided), the type of request, an optional event or project reference, an optional indicative date, and your message. A hidden field is used only to detect automated spam and is never shown to real visitors.",
    },
    {
      title: "Why it is collected",
      body: "This information is used solely to respond to your enquiry — for example, a speaking invitation, workshop request, or collaboration proposal. It is not used for marketing, profiling, or shared with third parties.",
    },
    {
      title: "How it is stored",
      body: "Submissions are stored in a private database that is never exposed through any public API endpoint, and are not included in this site's source code or public repository.",
    },
    {
      title: "Email delivery",
      body: "A notification email is sent to Daniele's inbox so he can respond. In local development this is routed to a test mailbox (Mailpit) rather than any real address.",
    },
    {
      title: "Your rights",
      body: "You may ask for your submitted information to be reviewed or deleted at any time by writing to the contact email address published on this site.",
    },
  ],
  note: "This page is a plain-language summary provided in good faith and does not constitute formal legal advice. Daniele should review this page against applicable regulations (such as the GDPR, if targeting EU visitors) before relying on it in production.",
};

const IT_COPY = {
  intro:
    "Questa pagina spiega, in termini semplici, cosa succede alle informazioni condivise tramite il modulo di contatto di questo sito.",
  sections: [
    {
      title: "Cosa viene raccolto",
      body: "Quando invii il modulo di contatto, il sito memorizza nome, indirizzo email, organizzazione (se fornita), tipo di richiesta, un riferimento opzionale a un evento o progetto, una data indicativa opzionale e il messaggio. Un campo nascosto viene utilizzato solo per rilevare spam automatizzato e non è mai visibile ai visitatori reali.",
    },
    {
      title: "Perché viene raccolto",
      body: "Queste informazioni sono utilizzate esclusivamente per rispondere alla tua richiesta, ad esempio un invito a parlare, una richiesta di workshop o una proposta di collaborazione. Non vengono utilizzate per marketing, profilazione, né condivise con terze parti.",
    },
    {
      title: "Come viene conservato",
      body: "Le richieste inviate sono conservate in un database privato, mai esposto tramite alcun endpoint API pubblico, e non incluse nel codice sorgente o nel repository pubblico di questo sito.",
    },
    {
      title: "Consegna via email",
      body: "Una email di notifica viene inviata alla casella di Daniele per permettergli di rispondere. In sviluppo locale questa viene indirizzata a una casella di test (Mailpit) e non a un indirizzo reale.",
    },
    {
      title: "I tuoi diritti",
      body: "Puoi richiedere in qualsiasi momento la revisione o la cancellazione delle informazioni inviate scrivendo all'indirizzo email di contatto pubblicato su questo sito.",
    },
  ],
  note: "Questa pagina è un riepilogo in linguaggio semplice fornito in buona fede e non costituisce una consulenza legale formale. Daniele dovrebbe verificarne la conformità alle normative applicabili (come il GDPR, se il sito si rivolge a visitatori nell'UE) prima di considerarla definitiva in produzione.",
};

export default function PrivacyPage() {
  const { t } = useTranslation();
  const { locale } = useLocale();
  const copy = locale === "it" ? IT_COPY : EN_COPY;

  useSeo({
    title: "Privacy — Daniele Mario Areddu",
    description: "How contact form submissions are collected, used and stored on this site.",
    path: "/privacy",
  });

  return (
    <div className="container-editorial max-w-3xl py-16 sm:py-24">
      <h1 className="eyebrow">{t("privacy.title")}</h1>
      <p className="mt-4 text-lg text-ink-soft">{copy.intro}</p>

      <div className="mt-10 space-y-8">
        {copy.sections.map((section) => (
          <section key={section.title}>
            <h2 className="font-serif text-xl text-ink">{section.title}</h2>
            <p className="mt-2 text-ink-soft">{section.body}</p>
          </section>
        ))}
      </div>

      <p className="mt-12 rounded-2xl border border-ink/10 bg-paper-warm p-5 text-sm text-ink-faint">
        {copy.note}
      </p>
    </div>
  );
}
