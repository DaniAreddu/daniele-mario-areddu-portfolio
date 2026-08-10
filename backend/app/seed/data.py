"""Structured, factual seed content for the portfolio.

Every fact here traces back to verified information. Fields that are genuinely
unknown are left as ``None`` rather than guessed — see docs/event-management.md
and README "Known content gaps" for the full list of items Daniele should
review before production launch.
"""

from __future__ import annotations

from datetime import date
from typing import Any

PROFILE: dict[str, Any] = {
    "full_name": "Daniele Mario Areddu",
    "roles": [
        "Backend & AI Developer",
        "International Conference Speaker",
        "Founder & Community Lead, Velletri.dev",
    ],
    "location": "Velletri, Italy",
    "base_country": "Italy",
    "availability_en": (
        "Available for international speaking engagements, workshops, panels, "
        "podcasts, and select backend and AI engineering collaborations."
    ),
    "availability_it": (
        "Disponibile per interventi internazionali, workshop, panel, podcast e "
        "collaborazioni selezionate su backend e ingegneria AI."
    ),
    "tagline_en": "Building intelligent systems. Sharing what I learn around the world.",
    "tagline_it": "Costruisco sistemi intelligenti. Condivido ciò che imparo in giro per il mondo.",
    "positioning_statement_en": (
        "Backend & AI Developer, international conference speaker and community "
        "builder working across production AI, distributed backend systems and "
        "modern data platforms."
    ),
    "positioning_statement_it": (
        "Backend & AI Developer, speaker internazionale e community builder, al "
        "lavoro tra AI in produzione, sistemi backend distribuiti e piattaforme "
        "dati moderne."
    ),
    "brand_label": "Backend × AI × Communities",
    "public_email": "danielemario@areddu.it",
    "github_url": None,
    "linkedin_url": None,
    "sessionize_url": None,
    "talks_count_label": "30+",
    "speaking_years_label": "2",
    "speaking_regions_label": "Europe, North America, Central Asia",
}

BIOGRAPHY: dict[str, Any] = {
    "micro_en": (
        "Backend & AI Developer building production-ready systems and sharing "
        "engineering practice at international conferences."
    ),
    "micro_it": (
        "Backend & AI Developer che costruisce sistemi pronti per la produzione "
        "e condivide pratica ingegneristica nelle conferenze internazionali."
    ),
    "short_en": (
        "Daniele Mario Areddu is a Backend & AI Developer at Global Technologies "
        "Italia and a Computer Science student at the University of Calabria. He "
        "builds backend systems and production-oriented AI applications, and has "
        "delivered around thirty technical talks across Europe, North America, "
        "and Central Asia over the past two years. He is also the founder and "
        "community lead of Velletri.dev, a developer community connecting local "
        "talent with the wider international tech ecosystem."
    ),
    "short_it": (
        "Daniele Mario Areddu è Backend & AI Developer presso Global Technologies "
        "Italia e studente di Informatica all'Università della Calabria. Costruisce "
        "sistemi backend e applicazioni AI orientate alla produzione, e negli "
        "ultimi due anni ha tenuto circa trenta interventi tecnici tra Europa, "
        "Nord America e Asia Centrale. È inoltre fondatore e community lead di "
        "Velletri.dev, una community di sviluppatori che collega il talento "
        "locale all'ecosistema tecnologico internazionale."
    ),
    "medium_en": (
        "Daniele Mario Areddu works at the intersection of backend engineering "
        "and applied artificial intelligence. As a Backend & AI Developer at "
        "Global Technologies Italia, he builds REST APIs, data-intensive systems "
        "and production-oriented AI features with Python, FastAPI and "
        "PostgreSQL, while continuing his Computer Science studies at the "
        "University of Calabria.\n\n"
        "Alongside his engineering work, Daniele is an active international "
        "speaker. In the past two years he has delivered roughly thirty "
        "technical talks at conferences and meetups across Europe, North "
        "America and Central Asia, focusing on autonomous AI agents, "
        "production-grade Retrieval-Augmented Generation, context engineering "
        "and backend architecture. He believes the hardest and most valuable "
        "part of working with large language models is not the demo — it is "
        "the engineering required to make an AI system reliable, observable "
        "and maintainable in production.\n\n"
        "In 2023 he founded Velletri.dev, a community initiative that connects "
        "developers, students and technology enthusiasts in his hometown with "
        "national and international developer communities, organizing meetups "
        "and creating opportunities for early-career developers."
    ),
    "medium_it": (
        "Daniele Mario Areddu lavora all'intersezione tra ingegneria backend e "
        "intelligenza artificiale applicata. Come Backend & AI Developer presso "
        "Global Technologies Italia, costruisce API REST, sistemi ad alta "
        "intensità di dati e funzionalità AI orientate alla produzione con "
        "Python, FastAPI e PostgreSQL, proseguendo allo stesso tempo gli studi "
        "in Informatica all'Università della Calabria.\n\n"
        "Accanto al lavoro ingegneristico, Daniele è uno speaker internazionale "
        "attivo. Negli ultimi due anni ha tenuto circa trenta interventi tecnici "
        "in conferenze e meetup tra Europa, Nord America e Asia Centrale, "
        "concentrandosi su agenti AI autonomi, Retrieval-Augmented Generation "
        "in produzione, context engineering e architettura backend. È convinto "
        "che la parte più difficile e preziosa nel lavorare con i modelli "
        "linguistici non sia la demo, ma l'ingegneria necessaria a rendere un "
        "sistema AI affidabile, osservabile e mantenibile in produzione.\n\n"
        "Nel 2023 ha fondato Velletri.dev, un'iniziativa di community che "
        "collega sviluppatori, studenti e appassionati di tecnologia della sua "
        "città natale con le community di sviluppatori nazionali e "
        "internazionali, organizzando meetup e creando opportunità per "
        "sviluppatori a inizio carriera."
    ),
    "long_en": (
        "Daniele Mario Areddu is a Backend & AI Developer, international "
        "technical speaker and community builder based in Italy.\n\n"
        "His engineering path started with a diploma in Informatica e "
        "Telecomunicazioni from ITIS G. Vallauri in Velletri, followed by "
        "independent backend and data-integration work on public-sector "
        "platforms — normalizing territorial data, matching records across "
        "heterogeneous sources, and exposing that work through clean REST "
        "APIs. That early experience shaped a lasting focus on data quality, "
        "typed contracts and systems that hold up outside of a demo "
        "environment. He is currently continuing his education as a Computer "
        "Science student at the University of Calabria, and works as a "
        "Backend & AI Developer at Global Technologies Italia, building "
        "Python and FastAPI services, multi-tenant and role-aware backend "
        "architectures, and production-ready AI features for enterprise and "
        "cybersecurity-related platforms.\n\n"
        "Daniele's technical interests have progressively moved toward applied "
        "artificial intelligence: retrieval-augmented generation, autonomous "
        "agents, tool calling, structured outputs and context engineering — "
        "the discipline of deciding what an AI system actually needs to know, "
        "when, and in what shape, in order to behave reliably. He works with "
        "Gemini, the Agent Development Kit and the Model Context Protocol, and "
        "is particularly interested in systems that move fluidly between "
        "cloud and on-device execution.\n\n"
        "This engineering practice feeds directly into his speaking. In two "
        "years, Daniele has delivered around thirty technical talks at "
        "conferences, DevFests, user groups and meetups across Italy, Spain, "
        "Albania, Romania, Bulgaria, the United States, Kazakhstan and "
        "Kyrgyzstan — always favoring concrete engineering lessons over "
        "abstract hype. His preferred speaking language is English.\n\n"
        "In 2023, Daniele founded Velletri.dev, a grassroots community "
        "initiative in his hometown of Velletri that organizes meetups and "
        "technical events, brings international speakers and ideas into a "
        "smaller local ecosystem, and helps students and early-career "
        "developers find their first opportunities and connections in tech. "
        "For Daniele, backend engineering, applied AI, public speaking and "
        "community building are not separate activities — they are different "
        "expressions of the same habit: build something real, then explain it "
        "clearly enough that someone else can build on it."
    ),
    "long_it": (
        "Daniele Mario Areddu è un Backend & AI Developer, speaker tecnico "
        "internazionale e community builder con base in Italia.\n\n"
        "Il suo percorso ingegneristico è iniziato con il diploma in "
        "Informatica e Telecomunicazioni conseguito all'ITIS G. Vallauri di "
        "Velletri, seguito da esperienze indipendenti di sviluppo backend e "
        "integrazione dati su piattaforme del settore pubblico: normalizzazione "
        "di dati territoriali, confronto di record provenienti da fonti "
        "eterogenee ed esposizione di questo lavoro tramite API REST pulite. "
        "Quella prima esperienza ha consolidato un'attenzione duratura per la "
        "qualità dei dati, i contratti tipizzati e i sistemi che reggono anche "
        "fuori da un ambiente di demo. Attualmente prosegue la propria "
        "formazione come studente di Informatica all'Università della "
        "Calabria e lavora come Backend & AI Developer presso Global "
        "Technologies Italia, costruendo servizi in Python e FastAPI, "
        "architetture backend multi-tenant e role-aware, e funzionalità AI "
        "pronte per la produzione per piattaforme enterprise e legate alla "
        "cybersecurity.\n\n"
        "Gli interessi tecnici di Daniele si sono progressivamente spostati "
        "verso l'intelligenza artificiale applicata: retrieval-augmented "
        "generation, agenti autonomi, tool calling, output strutturati e "
        "context engineering, la disciplina che decide cosa un sistema AI "
        "debba effettivamente sapere, quando e in quale forma, per comportarsi "
        "in modo affidabile. Lavora con Gemini, l'Agent Development Kit e il "
        "Model Context Protocol, ed è particolarmente interessato ai sistemi "
        "che si muovono fluidamente tra cloud ed esecuzione on-device.\n\n"
        "Questa pratica ingegneristica alimenta direttamente la sua attività "
        "di speaker. In due anni, Daniele ha tenuto circa trenta interventi "
        "tecnici in conferenze, DevFest, user group e meetup tra Italia, "
        "Spagna, Albania, Romania, Bulgaria, Stati Uniti, Kazakhstan e "
        "Kirghizistan, privilegiando sempre lezioni ingegneristiche concrete "
        "rispetto all'hype astratto. La sua lingua di lavoro preferita per gli "
        "interventi è l'inglese.\n\n"
        "Nel 2023 Daniele ha fondato Velletri.dev, un'iniziativa di community "
        "dal basso nella sua città natale, Velletri, che organizza meetup ed "
        "eventi tecnici, porta speaker e idee internazionali in un ecosistema "
        "locale più piccolo, e aiuta studenti e sviluppatori a inizio carriera "
        "a trovare le prime opportunità e connessioni nel settore tecnologico. "
        "Per Daniele, ingegneria backend, AI applicata, public speaking e "
        "community building non sono attività separate: sono espressioni "
        "diverse della stessa abitudine — costruire qualcosa di reale, e poi "
        "spiegarlo con abbastanza chiarezza perché qualcun altro possa "
        "costruirci sopra."
    ),
    "speaker_bio_en": (
        "Daniele Mario Areddu is a Backend & AI Developer at Global "
        "Technologies Italia and a Computer Science student at the University "
        "of Calabria. Over the past two years he has delivered around thirty "
        "technical talks at conferences, DevFests and user groups across "
        "Europe, North America and Central Asia, covering autonomous AI "
        "agents, production-grade Retrieval-Augmented Generation, context "
        "engineering, and backend architecture with Python and FastAPI. He is "
        "the founder and community lead of Velletri.dev, a developer community "
        "connecting local talent with the international tech ecosystem. "
        "Daniele speaks in English and is available for conference talks, "
        "workshops, panels, podcasts and community collaborations."
    ),
    "speaker_bio_it": (
        "Daniele Mario Areddu è Backend & AI Developer presso Global "
        "Technologies Italia e studente di Informatica all'Università della "
        "Calabria. Negli ultimi due anni ha tenuto circa trenta interventi "
        "tecnici in conferenze, DevFest e user group tra Europa, Nord America "
        "e Asia Centrale, su agenti AI autonomi, Retrieval-Augmented "
        "Generation in produzione, context engineering e architettura backend "
        "con Python e FastAPI. È fondatore e community lead di Velletri.dev, "
        "una community di sviluppatori che collega il talento locale "
        "all'ecosistema tecnologico internazionale. Daniele tiene i propri "
        "interventi in inglese ed è disponibile per conferenze, workshop, "
        "panel, podcast e collaborazioni con community."
    ),
}

EDUCATION: list[dict[str, Any]] = [
    {
        "institution": "ITIS G. Vallauri, Velletri",
        "degree_en": "Diploma in Informatica e Telecomunicazioni (Computer Science & Telecommunications)",
        "degree_it": "Diploma in Informatica e Telecomunicazioni",
        "location": "Velletri, Italy",
        "start_year": None,
        "end_year": 2025,
        "is_ongoing": False,
        "description_en": (
            "Technical secondary education in computer science and "
            "telecommunications, providing the foundation for Daniele's later "
            "backend and systems work."
        ),
        "description_it": (
            "Percorso di istruzione tecnica superiore in informatica e "
            "telecomunicazioni, alla base del successivo lavoro di Daniele su "
            "backend e sistemi."
        ),
        "sort_order": 1,
    },
    {
        "institution": "University of Calabria",
        "degree_en": "Bachelor's Degree in Computer Science",
        "degree_it": "Laurea in Informatica",
        "location": "Rende (Cosenza), Italy",
        "start_year": 2025,
        "end_year": None,
        "is_ongoing": True,
        "description_en": (
            "Undergraduate studies in Computer Science, pursued alongside "
            "professional backend and AI engineering work."
        ),
        "description_it": (
            "Studi triennali in Informatica, portati avanti parallelamente "
            "all'attività professionale come backend e AI engineer."
        ),
        "sort_order": 2,
    },
]

EXPERIENCE: list[dict[str, Any]] = [
    {
        "organization": "Global Technologies Italia",
        "role_en": "Backend & AI Developer",
        "role_it": "Backend & AI Developer",
        "location": "Italy",
        "start_date": date(2026, 3, 1),
        "end_date": None,
        "is_current": True,
        "summary_en": (
            "Backend and AI engineering for enterprise and cybersecurity-related "
            "platforms, focused on typed REST APIs, multi-tenant architecture "
            "and production-ready AI features."
        ),
        "summary_it": (
            "Ingegneria backend e AI per piattaforme enterprise e legate alla "
            "cybersecurity, con focus su API REST tipizzate, architettura "
            "multi-tenant e funzionalità AI pronte per la produzione."
        ),
        "highlights_en": [
            "Design and build REST APIs with Python, FastAPI and Flask for enterprise data systems.",
            "Work with PostgreSQL and PostGIS across data-intensive and geospatial workloads.",
            "Contribute to multi-tenant, role-aware backend architectures with typed API contracts.",
            "Apply automated testing and OpenAPI documentation as part of the delivery process.",
            "Bring production-ready AI architecture patterns into enterprise and cybersecurity-related platforms.",
        ],
        "highlights_it": [
            "Progettazione e sviluppo di API REST con Python, FastAPI e Flask per sistemi dati enterprise.",
            "Utilizzo di PostgreSQL e PostGIS su carichi di lavoro ad alta intensità di dati e geospaziali.",
            "Contributo ad architetture backend multi-tenant e role-aware con contratti API tipizzati.",
            "Applicazione di test automatizzati e documentazione OpenAPI nel processo di delivery.",
            "Introduzione di pattern di architettura AI pronti per la produzione in piattaforme enterprise e legate alla cybersecurity.",
        ],
        "technologies": [
            "Python", "FastAPI", "Flask", "PostgreSQL", "PostGIS", "Docker",
            "REST APIs", "OpenAPI",
        ],
        "sort_order": 1,
    },
]

SKILL_CATEGORIES: list[dict[str, Any]] = [
    {
        "slug": "backend-engineering",
        "name_en": "Backend Engineering",
        "name_it": "Ingegneria Backend",
        "description_en": "Typed, tested, production-oriented backend systems.",
        "description_it": "Sistemi backend tipizzati, testati e orientati alla produzione.",
        "sort_order": 1,
        "skills": [
            ("Python", "Primary language across all backend and AI work, including Global Technologies Italia and independent projects.", "Linguaggio principale in tutto il lavoro backend e AI, inclusi Global Technologies Italia e progetti indipendenti."),
            ("FastAPI", "Primary framework for typed, async REST APIs, including this portfolio's own backend.", "Framework principale per API REST tipizzate e asincrone, incluso il backend di questo stesso portfolio."),
            ("Flask", "Used for backend services at Global Technologies Italia.", "Utilizzato per servizi backend presso Global Technologies Italia."),
            ("REST APIs", "Designed and documented across enterprise, cybersecurity-related and public-sector platforms.", "Progettate e documentate su piattaforme enterprise, legate alla cybersecurity e del settore pubblico."),
            ("OpenAPI", "Used to keep API contracts explicit and consumable by clients and tooling.", "Utilizzato per mantenere espliciti i contratti API e renderli fruibili da client e strumenti."),
            ("PostgreSQL", "Core database for backend systems and the municipal data reconciliation platform.", "Database centrale per i sistemi backend e per la piattaforma di riconciliazione dati comunale."),
            ("PostGIS", "Applied to geographic and street-level data normalization and matching.", "Applicato alla normalizzazione e al matching di dati geografici e stradali."),
            ("Docker", "Used to containerize backend services for development and deployment.", "Utilizzato per containerizzare i servizi backend in sviluppo e produzione."),
            ("Multi-tenant architectures", "Designed for enterprise platforms requiring tenant isolation.", "Progettate per piattaforme enterprise che richiedono isolamento tra tenant."),
            ("Authentication & authorization", "Implemented role-aware access control on enterprise APIs.", "Implementati controlli di accesso role-aware su API enterprise."),
            ("Automated testing", "Applied with pytest and HTTPX across API, service and repository layers.", "Applicati con pytest e HTTPX su livelli API, servizio e repository."),
        ],
    },
    {
        "slug": "artificial-intelligence",
        "name_en": "Artificial Intelligence",
        "name_it": "Intelligenza Artificiale",
        "description_en": "Moving LLM applications from prototype to production.",
        "description_it": "Portare le applicazioni LLM dal prototipo alla produzione.",
        "sort_order": 2,
        "skills": [
            ("LLM-powered applications", "Core focus of Daniele's current engineering and speaking work.", "Focus centrale del lavoro ingegneristico e divulgativo attuale di Daniele."),
            ("Retrieval-Augmented Generation", "Subject of multiple international talks on production-grade RAG.", "Argomento di diversi interventi internazionali su RAG in produzione."),
            ("Autonomous agents", "Explored through talks such as \"Stop Fine-Tuning. Start Thinking\" at AgentCamp Sofia.", "Approfondito in interventi come \"Stop Fine-Tuning. Start Thinking\" ad AgentCamp Sofia."),
            ("Context engineering", "A recurring theme across Daniele's 2025–2026 speaking circuit.", "Tema ricorrente nel percorso di speaking di Daniele nel 2025–2026."),
            ("Tool calling & structured outputs", "Applied when designing agents that need reliable, machine-readable results.", "Applicati nella progettazione di agenti che richiedono risultati affidabili e leggibili da macchina."),
            ("Agent orchestration", "Covered in talks on coordinating multi-step, multi-tool agent tasks.", "Trattato in interventi sul coordinamento di task agentici multi-step e multi-tool."),
            ("Gemini", "Used to build cloud-to-edge agent demos presented internationally.", "Utilizzato per costruire demo di agenti cloud-to-edge presentate a livello internazionale."),
            ("Agent Development Kit", "Featured in the talk \"From Cloud to Edge\" delivered at GDG Almaty.", "Presente nell'intervento \"From Cloud to Edge\" tenuto al GDG Almaty."),
            ("Model Context Protocol", "Used to connect agents to external tools and context sources.", "Utilizzato per collegare gli agenti a strumenti esterni e fonti di contesto."),
            ("Cloud-to-edge & on-device AI", "Central topic of Daniele's most requested international talk.", "Argomento centrale dell'intervento internazionale più richiesto a Daniele."),
        ],
    },
    {
        "slug": "data-platforms",
        "name_en": "Data Platforms",
        "name_it": "Piattaforme Dati",
        "description_en": "ETL/ELT, data quality and geospatial data at scale.",
        "description_it": "ETL/ELT, qualità dei dati e dati geospaziali su larga scala.",
        "sort_order": 3,
        "skills": [
            ("Microsoft Fabric", "Part of Daniele's data-platform toolkit.", "Parte del toolkit di Daniele per le piattaforme dati."),
            ("Azure Data Factory", "Used for orchestrating data pipelines.", "Utilizzato per orchestrare pipeline dati."),
            ("Databricks & PySpark", "Applied to larger-scale data transformation workloads.", "Applicati a carichi di trasformazione dati su larga scala."),
            ("ETL / ELT", "Core discipline behind the municipal data reconciliation platform.", "Disciplina centrale della piattaforma di riconciliazione dati comunale."),
            ("Data normalization & matching", "Applied to heterogeneous territorial and street-level datasets.", "Applicati a dataset territoriali e stradali eterogenei."),
            ("Deduplication & data-quality pipelines", "Delivered matching quality above 70% in a municipal reconciliation workflow.", "Hanno raggiunto una qualità di matching superiore al 70% in un flusso di riconciliazione comunale."),
            ("PostgreSQL / PostGIS", "Shared foundation between backend engineering and data platform work.", "Base condivisa tra ingegneria backend e lavoro sulle piattaforme dati."),
        ],
    },
    {
        "slug": "engineering-practices",
        "name_en": "Engineering Practices",
        "name_it": "Pratiche Ingegneristiche",
        "description_en": "The discipline that makes systems trustworthy over time.",
        "description_it": "La disciplina che rende i sistemi affidabili nel tempo.",
        "sort_order": 4,
        "skills": [
            ("Clean architecture", "Applied through repository/service/API layering, including in this portfolio's own backend.", "Applicata tramite la separazione in livelli repository/service/API, anche nel backend di questo portfolio."),
            ("Automated testing", "Unit, integration and API-level tests as a standard part of delivery.", "Test unitari, di integrazione e a livello API come parte standard della delivery."),
            ("Observability", "Structured logging and health/readiness checks built into backend services.", "Logging strutturato e controlli di health/readiness integrati nei servizi backend."),
            ("Security-aware development", "Input validation, rate limiting and role-aware access as default practice.", "Validazione degli input, rate limiting e accesso role-aware come pratica di default."),
            ("API documentation", "OpenAPI-first approach to keeping contracts explicit.", "Approccio OpenAPI-first per mantenere espliciti i contratti."),
            ("Incremental delivery", "Shipping in small, verifiable increments rather than large untested batches.", "Rilasci in incrementi piccoli e verificabili invece di grandi batch non testati."),
            ("Git & Dockerized development", "Standard workflow across all professional and personal projects.", "Workflow standard in tutti i progetti professionali e personali."),
            ("Technical documentation", "Practiced both in engineering work and in preparing international talks.", "Praticata sia nel lavoro ingegneristico sia nella preparazione di interventi internazionali."),
        ],
    },
]

PROJECTS: list[dict[str, Any]] = [
    {
        "slug": "municipal-data-reconciliation-platform",
        "title_en": "Municipal Data Reconciliation Platform",
        "title_it": "Piattaforma di Riconciliazione Dati Comunale",
        "summary_en": (
            "A backend and data-processing platform that integrates "
            "heterogeneous territorial datasets, normalizes geographic and "
            "street-level information, and identifies duplicates and "
            "inconsistencies through REST APIs."
        ),
        "summary_it": (
            "Una piattaforma backend e di elaborazione dati che integra "
            "dataset territoriali eterogenei, normalizza informazioni "
            "geografiche e stradali, e individua duplicati e incongruenze "
            "tramite API REST."
        ),
        "problem_en": (
            "Public-sector organizations often hold territorial and address "
            "data across multiple, independently maintained sources — with "
            "inconsistent formats, spellings and geographic references. This "
            "makes it hard to know, with confidence, whether two records "
            "describe the same real-world place or entity."
        ),
        "problem_it": (
            "Le organizzazioni del settore pubblico gestiscono spesso dati "
            "territoriali e anagrafici su fonti multiple e mantenute in modo "
            "indipendente, con formati, grafie e riferimenti geografici "
            "incoerenti. Questo rende difficile stabilire con sicurezza se due "
            "record descrivano lo stesso luogo o la stessa entità reale."
        ),
        "challenge_en": (
            "The engineering challenge was twofold: normalize noisy, "
            "inconsistent geographic and street-related data at scale, and "
            "design a matching approach precise enough to be genuinely useful "
            "without requiring manual review of every record."
        ),
        "challenge_it": (
            "La sfida ingegneristica era duplice: normalizzare su larga scala "
            "dati geografici e stradali rumorosi e incoerenti, e progettare un "
            "approccio di matching sufficientemente preciso da essere "
            "realmente utile senza richiedere una revisione manuale di ogni "
            "record."
        ),
        "approach_en": (
            "Territorial records were normalized into a consistent schema, "
            "then compared using a combination of deterministic rules and "
            "similarity-based matching on street and locality fields. "
            "PostGIS was used to validate and enrich geographic references, "
            "and the result was exposed as a set of REST APIs that downstream "
            "systems could query for reconciled, deduplicated data."
        ),
        "approach_it": (
            "I record territoriali sono stati normalizzati in uno schema "
            "coerente, quindi confrontati tramite una combinazione di regole "
            "deterministiche e matching basato sulla similarità su campi "
            "stradali e di località. PostGIS è stato utilizzato per validare "
            "e arricchire i riferimenti geografici, e il risultato è stato "
            "esposto tramite un insieme di API REST interrogabili dai sistemi "
            "a valle per ottenere dati riconciliati e deduplicati."
        ),
        "architecture_en": (
            "A FastAPI service layered over PostgreSQL and PostGIS, with a "
            "dedicated normalization and matching pipeline running as part of "
            "the data ingestion path, and REST endpoints exposing reconciled "
            "records with confidence indicators. The whole stack was "
            "containerized with Docker for consistent deployment."
        ),
        "architecture_it": (
            "Un servizio FastAPI stratificato su PostgreSQL e PostGIS, con una "
            "pipeline dedicata di normalizzazione e matching eseguita "
            "all'interno del flusso di ingestion dei dati, ed endpoint REST "
            "che espongono record riconciliati con indicatori di confidenza. "
            "L'intero stack è stato containerizzato con Docker per un "
            "deployment coerente."
        ),
        "key_decisions_en": [
            "Prioritized deterministic normalization rules before introducing similarity-based matching, to keep results explainable.",
            "Used PostGIS rather than external geocoding services to keep geographic validation self-hosted and predictable.",
            "Optimized selected SQL operations after profiling, rather than optimizing the whole pipeline speculatively.",
        ],
        "key_decisions_it": [
            "Priorità alle regole di normalizzazione deterministiche prima di introdurre il matching basato sulla similarità, per mantenere i risultati spiegabili.",
            "Uso di PostGIS invece di servizi di geocodifica esterni per mantenere la validazione geografica self-hosted e prevedibile.",
            "Ottimizzazione di operazioni SQL selezionate dopo il profiling, invece di ottimizzare speculativamente l'intera pipeline.",
        ],
        "outcome_en": (
            "In the relevant matching workflow, the system reached matching "
            "quality above 70%. After targeted SQL optimizations, selected "
            "processing operations ran approximately 40% faster. These figures "
            "describe specific workflows and operations within the platform, "
            "not its performance as a whole."
        ),
        "outcome_it": (
            "Nel flusso di matching considerato, il sistema ha raggiunto una "
            "qualità di matching superiore al 70%. Dopo ottimizzazioni SQL "
            "mirate, alcune operazioni di elaborazione sono diventate circa il "
            "40% più veloci. Questi dati descrivono flussi e operazioni "
            "specifiche della piattaforma, non le sue prestazioni complessive."
        ),
        "lessons_en": (
            "Data quality work rewards patience: most of the value came from "
            "getting normalization right before investing in more elaborate "
            "matching logic. Measuring performance on specific, representative "
            "operations — rather than the system as a whole — made "
            "optimization work far more targeted and defensible."
        ),
        "lessons_it": (
            "Il lavoro sulla qualità dei dati premia la pazienza: gran parte "
            "del valore è arrivata dal fare bene la normalizzazione prima di "
            "investire in logiche di matching più elaborate. Misurare le "
            "prestazioni su operazioni specifiche e rappresentative, invece "
            "che sul sistema nel suo complesso, ha reso il lavoro di "
            "ottimizzazione molto più mirato e difendibile."
        ),
        "confidentiality_note_en": (
            "Described generically to respect the confidentiality of the "
            "public-sector context in which this work was carried out. No "
            "client names, internal systems, or non-public details are shared."
        ),
        "confidentiality_note_it": (
            "Descritto in forma generica per rispettare la riservatezza del "
            "contesto pubblico in cui questo lavoro è stato svolto. Non "
            "vengono condivisi nomi di clienti, sistemi interni o dettagli non "
            "pubblici."
        ),
        "technologies": ["FastAPI", "PostgreSQL", "PostGIS", "SQL", "Docker", "REST APIs"],
        "related_skills": ["Data normalization", "Data matching", "Deduplication", "PostgreSQL", "PostGIS"],
        "external_url": None,
        "is_featured": True,
        "sort_order": 1,
    },
    {
        "slug": "production-ai-agent-architectures",
        "title_en": "Production AI Agent Architectures",
        "title_it": "Architetture di Agenti AI in Produzione",
        "summary_en": (
            "An ongoing engineering, research and speaking focus on designing "
            "AI agents that retrieve context, use tools, produce structured "
            "outputs and coordinate tasks reliably in production."
        ),
        "summary_it": (
            "Un focus continuativo di ingegneria, ricerca e speaking sulla "
            "progettazione di agenti AI in grado di recuperare contesto, "
            "usare strumenti, produrre output strutturati e coordinare task in "
            "modo affidabile in produzione."
        ),
        "problem_en": (
            "Most AI agent demos work well in a controlled setting and break "
            "down under real-world conditions: ambiguous input, tool "
            "failures, missing context, or tasks that require several "
            "coordinated steps. Moving from an impressive demo to a system "
            "that behaves predictably is a distinct engineering problem."
        ),
        "problem_it": (
            "La maggior parte delle demo di agenti AI funziona bene in un "
            "contesto controllato e si rompe in condizioni reali: input "
            "ambigui, fallimenti degli strumenti, contesto mancante o task che "
            "richiedono più passaggi coordinati. Passare da una demo "
            "impressionante a un sistema che si comporta in modo prevedibile "
            "è un problema ingegneristico a sé."
        ),
        "challenge_en": (
            "The core challenge is context engineering: deciding what "
            "information an agent actually needs, in what form, and at which "
            "step — plus designing for graceful failure when a tool call or "
            "retrieval step does not return what was expected."
        ),
        "challenge_it": (
            "La sfida principale è il context engineering: decidere quali "
            "informazioni servano davvero a un agente, in quale forma e in "
            "quale passaggio, oltre a progettare una gestione elegante dei "
            "fallimenti quando una chiamata a uno strumento o un passaggio di "
            "retrieval non restituisce quanto atteso."
        ),
        "approach_en": (
            "This work combines Retrieval-Augmented Generation for grounded "
            "context, explicit tool calling and structured outputs for "
            "predictable agent behavior, and orchestration logic to coordinate "
            "multi-step tasks — built with Gemini, the Agent Development Kit "
            "and the Model Context Protocol, and explored across both cloud "
            "and on-device execution."
        ),
        "approach_it": (
            "Questo lavoro combina Retrieval-Augmented Generation per un "
            "contesto ancorato ai fatti, tool calling esplicito e output "
            "strutturati per un comportamento prevedibile dell'agente, e "
            "logica di orchestrazione per coordinare task multi-step — "
            "costruito con Gemini, l'Agent Development Kit e il Model Context "
            "Protocol, ed esplorato sia in esecuzione cloud sia on-device."
        ),
        "architecture_en": (
            "A modular agent architecture separating retrieval, tool access, "
            "reasoning and output validation, designed so individual pieces — "
            "the retrieval layer, a given tool, the execution target — can be "
            "swapped or moved between cloud and edge without rewriting the "
            "agent's core logic."
        ),
        "architecture_it": (
            "Un'architettura di agente modulare che separa retrieval, accesso "
            "agli strumenti, ragionamento e validazione dell'output, "
            "progettata in modo che i singoli componenti — il livello di "
            "retrieval, un determinato strumento, il target di esecuzione — "
            "possano essere sostituiti o spostati tra cloud ed edge senza "
            "riscrivere la logica centrale dell'agente."
        ),
        "key_decisions_en": [
            "Treated context engineering as a first-class design activity rather than an afterthought to prompting.",
            "Required structured outputs at agent boundaries to make failures detectable instead of silent.",
            "Designed for cloud-to-edge portability from the start, rather than retrofitting on-device support later.",
        ],
        "key_decisions_it": [
            "Trattato il context engineering come attività di design di prima classe, non come ripensamento del prompting.",
            "Richiesti output strutturati ai confini dell'agente per rendere i fallimenti rilevabili invece che silenziosi.",
            "Progettata fin dall'inizio la portabilità cloud-to-edge, invece di aggiungere il supporto on-device in un secondo momento.",
        ],
        "outcome_en": (
            "This focus area has directly shaped Daniele's most requested "
            "international talk, \"From Cloud to Edge: Building Autonomous AI "
            "Agents with Gemini, ADK and On-Device AI,\" and continues to "
            "inform his engineering work on production AI features."
        ),
        "outcome_it": (
            "Questo ambito ha modellato direttamente l'intervento "
            "internazionale più richiesto a Daniele, \"From Cloud to Edge: "
            "Building Autonomous AI Agents with Gemini, ADK and On-Device AI\", "
            "e continua a orientare il suo lavoro ingegneristico su "
            "funzionalità AI in produzione."
        ),
        "lessons_en": (
            "Reliability in agent systems comes less from a smarter model and "
            "more from disciplined engineering around it: what context it "
            "sees, how failures are surfaced, and how outputs are validated "
            "before they reach a user or another system."
        ),
        "lessons_it": (
            "L'affidabilità nei sistemi agentici deriva meno da un modello più "
            "intelligente e più da un'ingegneria disciplinata attorno ad esso: "
            "quale contesto vede, come vengono segnalati i fallimenti e come "
            "gli output vengono validati prima di raggiungere un utente o un "
            "altro sistema."
        ),
        "confidentiality_note_en": (
            "Presented as an engineering, research and speaking focus rather "
            "than a named commercial product; no proprietary system details "
            "are disclosed."
        ),
        "confidentiality_note_it": (
            "Presentato come ambito di ingegneria, ricerca e speaking e non "
            "come prodotto commerciale con un nome proprio; non vengono "
            "divulgati dettagli su sistemi proprietari."
        ),
        "technologies": [
            "Gemini", "Agent Development Kit", "Model Context Protocol",
            "Retrieval-Augmented Generation", "Context engineering", "Tool calling",
        ],
        "related_skills": ["Autonomous agents", "Structured outputs", "Agent orchestration", "Cloud-to-edge AI"],
        "external_url": None,
        "is_featured": True,
        "sort_order": 2,
    },
    {
        "slug": "enterprise-backend-cybersecurity-systems",
        "title_en": "Enterprise Backend & Cybersecurity Systems",
        "title_it": "Sistemi Backend Enterprise e Cybersecurity",
        "summary_en": (
            "Backend engineering for enterprise and cybersecurity-related "
            "platforms, covering multi-tenant APIs, tenant isolation, "
            "role-aware access, search, and typed contracts."
        ),
        "summary_it": (
            "Ingegneria backend per piattaforme enterprise e legate alla "
            "cybersecurity, con API multi-tenant, isolamento tra tenant, "
            "accesso role-aware, ricerca e contratti tipizzati."
        ),
        "problem_en": (
            "Enterprise and cybersecurity-related platforms typically serve "
            "many organizations from a shared codebase, where a single data "
            "leak or authorization mistake between tenants is unacceptable — "
            "while still needing to move fast on new features."
        ),
        "problem_it": (
            "Le piattaforme enterprise e legate alla cybersecurity servono "
            "tipicamente molte organizzazioni da una base di codice comune, "
            "dove anche una singola fuga di dati o un errore di autorizzazione "
            "tra tenant è inaccettabile, pur dovendo mantenere un ritmo "
            "sostenuto sulle nuove funzionalità."
        ),
        "challenge_en": (
            "Building APIs where tenant isolation and role-aware access are "
            "structurally enforced — not just checked ad hoc in individual "
            "endpoints — while keeping the system testable, documented and "
            "fast to extend."
        ),
        "challenge_it": (
            "Costruire API in cui l'isolamento tra tenant e l'accesso "
            "role-aware siano imposti a livello strutturale, e non solo "
            "verificati ad hoc nei singoli endpoint, mantenendo al contempo il "
            "sistema testabile, documentato e veloce da estendere."
        ),
        "approach_en": (
            "This work applied typed Pydantic schemas and OpenAPI contracts "
            "across notification, search and pagination features, backed by "
            "automated tests, and layered authorization checks so that tenant "
            "boundaries hold even as new endpoints are added."
        ),
        "approach_it": (
            "Questo lavoro ha applicato schemi Pydantic tipizzati e contratti "
            "OpenAPI su funzionalità di notifica, ricerca e paginazione, "
            "supportati da test automatizzati, con controlli di autorizzazione "
            "stratificati affinché i confini tra tenant reggano anche "
            "all'aggiunta di nuovi endpoint."
        ),
        "architecture_en": (
            "Layered FastAPI-style services (API, service, repository) with "
            "tenant context resolved once per request and propagated "
            "consistently, typed request/response schemas, and search and "
            "pagination built as shared, reusable building blocks."
        ),
        "architecture_it": (
            "Servizi in stile FastAPI organizzati a livelli (API, service, "
            "repository) con il contesto del tenant risolto una sola volta per "
            "richiesta e propagato in modo coerente, schemi di richiesta e "
            "risposta tipizzati, e ricerca e paginazione costruite come "
            "componenti condivisi e riutilizzabili."
        ),
        "key_decisions_en": [
            "Resolved tenant context centrally rather than re-deriving it in each endpoint.",
            "Standardized pagination and search response shapes across the API surface.",
            "Kept authorization logic close to the service layer, not scattered across route handlers.",
        ],
        "key_decisions_it": [
            "Contesto del tenant risolto centralmente invece di essere ridedotto in ogni endpoint.",
            "Standardizzazione della forma delle risposte di paginazione e ricerca su tutta la superficie API.",
            "Logica di autorizzazione mantenuta vicina al livello di servizio, non dispersa nei route handler.",
        ],
        "outcome_en": (
            "Consistent tenant isolation and role-aware access across the "
            "platform's API surface, with typed contracts and automated tests "
            "reducing regressions as new features were added."
        ),
        "outcome_it": (
            "Isolamento coerente tra tenant e accesso role-aware su tutta la "
            "superficie API della piattaforma, con contratti tipizzati e test "
            "automatizzati che hanno ridotto le regressioni all'aggiunta di "
            "nuove funzionalità."
        ),
        "lessons_en": (
            "Structural enforcement beats convention: isolating tenant logic "
            "in one place made the system safer than trusting every new "
            "endpoint to remember the rules."
        ),
        "lessons_it": (
            "L'imposizione strutturale batte la convenzione: isolare la logica "
            "del tenant in un unico punto ha reso il sistema più sicuro che "
            "affidarsi al fatto che ogni nuovo endpoint ricordasse le regole."
        ),
        "confidentiality_note_en": (
            "Described without internal product names or confidential "
            "implementation details, in line with the non-disclosure "
            "boundaries of enterprise and cybersecurity-related work."
        ),
        "confidentiality_note_it": (
            "Descritto senza nomi di prodotti interni o dettagli implementativi "
            "riservati, nel rispetto dei vincoli di riservatezza propri del "
            "lavoro enterprise e legato alla cybersecurity."
        ),
        "technologies": ["Python", "FastAPI", "Flask", "PostgreSQL", "OpenAPI", "REST APIs"],
        "related_skills": ["Multi-tenant architectures", "Authentication & authorization", "Automated testing"],
        "external_url": None,
        "is_featured": False,
        "sort_order": 3,
    },
    {
        "slug": "velletri-dev",
        "title_en": "Velletri.dev — A Local Developer Community",
        "title_it": "Velletri.dev — Una Community di Sviluppatori Locale",
        "summary_en": (
            "A community initiative founded by Daniele to connect developers, "
            "students and technology enthusiasts in Velletri with the wider "
            "national and international developer ecosystem."
        ),
        "summary_it": (
            "Un'iniziativa di community fondata da Daniele per collegare "
            "sviluppatori, studenti e appassionati di tecnologia a Velletri "
            "con il più ampio ecosistema di sviluppatori nazionale e "
            "internazionale."
        ),
        "problem_en": (
            "Smaller Italian towns rarely have direct access to the technical "
            "events, speakers and peer networks concentrated in larger cities, "
            "leaving local developers and students with fewer chances to "
            "learn from and connect with the wider community."
        ),
        "problem_it": (
            "Le città italiane più piccole raramente hanno accesso diretto "
            "agli eventi tecnici, agli speaker e alle reti di pari concentrati "
            "nelle grandi città, lasciando sviluppatori e studenti locali con "
            "meno occasioni di imparare e connettersi con la community più "
            "ampia."
        ),
        "challenge_en": (
            "Building a sustainable local community from zero: attracting a "
            "consistent audience, organizing recurring events, and creating a "
            "credible bridge to national and international speakers and "
            "communities."
        ),
        "challenge_it": (
            "Costruire una community locale sostenibile partendo da zero: "
            "attrarre un pubblico costante, organizzare eventi ricorrenti e "
            "creare un ponte credibile verso speaker e community nazionali e "
            "internazionali."
        ),
        "approach_en": (
            "Daniele founded Velletri.dev to organize technical meetups and "
            "events in Velletri, using his own growing international speaking "
            "network to bring outside speakers and ideas into the local "
            "ecosystem, while creating a welcoming entry point for students "
            "and early-career developers."
        ),
        "approach_it": (
            "Daniele ha fondato Velletri.dev per organizzare meetup ed eventi "
            "tecnici a Velletri, sfruttando la propria rete di speaking "
            "internazionale in crescita per portare speaker e idee esterne "
            "nell'ecosistema locale, creando al contempo un punto di ingresso "
            "accogliente per studenti e sviluppatori a inizio carriera."
        ),
        "architecture_en": (
            "Not applicable — this is a community initiative rather than a "
            "software system. Its \"architecture\" is the recurring cadence of "
            "meetups, the relationships with regional and international "
            "developer communities, and the pipeline it creates from student "
            "to contributor to speaker."
        ),
        "architecture_it": (
            "Non applicabile: si tratta di un'iniziativa di community e non di "
            "un sistema software. La sua \"architettura\" è la cadenza "
            "ricorrente dei meetup, le relazioni con le community di "
            "sviluppatori regionali e internazionali, e il percorso che crea "
            "da studente a contributore a speaker."
        ),
        "key_decisions_en": [
            "Kept the community hyper-local in focus while deliberately connecting it to national and international networks.",
            "Used Daniele's own speaking travel as a channel to invite international speakers and ideas back to Velletri.",
            "Prioritized recurring, low-friction meetups over infrequent large-scale events.",
        ],
        "key_decisions_it": [
            "Community mantenuta iper-locale nel focus, ma deliberatamente connessa a reti nazionali e internazionali.",
            "Utilizzo dei viaggi di speaking di Daniele come canale per invitare speaker e idee internazionali a Velletri.",
            "Priorità a meetup ricorrenti e a bassa frizione rispetto a eventi su larga scala ma poco frequenti.",
        ],
        "outcome_en": (
            "An active local meetup series (see the Community page for "
            "specific events) and a direct link between a small Italian town "
            "and Daniele's international speaking network."
        ),
        "outcome_it": (
            "Una serie attiva di meetup locali (vedi la pagina Community per "
            "gli eventi specifici) e un collegamento diretto tra una piccola "
            "città italiana e la rete di speaking internazionale di Daniele."
        ),
        "lessons_en": (
            "Community building rewards the same discipline as engineering: "
            "consistency beats spectacle, and small recurring commitments "
            "compound faster than occasional large ones."
        ),
        "lessons_it": (
            "Costruire una community premia la stessa disciplina "
            "dell'ingegneria: la costanza batte lo spettacolo, e piccoli "
            "impegni ricorrenti si moltiplicano più rapidamente di eventi "
            "occasionali di grande portata."
        ),
        "confidentiality_note_en": (
            "All information here is public community activity; no external "
            "link is shown unless a verified URL has been configured."
        ),
        "confidentiality_note_it": (
            "Tutte le informazioni qui riportate riguardano attività pubbliche "
            "della community; nessun link esterno viene mostrato finché non "
            "sia configurato un URL verificato."
        ),
        "technologies": ["Community organizing", "Event curation", "Public speaking"],
        "related_skills": ["Developer communities", "Public speaking", "Knowledge sharing"],
        "external_url": None,
        "is_featured": False,
        "sort_order": 4,
    },
]

TALKS: list[dict[str, Any]] = [
    {
        "slug": "stop-fine-tuning-start-thinking",
        "title": "Stop Fine-Tuning. Start Thinking: The Rise of Self-Evolving AI Agents",
        "language": "en",
        "summary_en": (
            "Why the future of practical AI systems favors agents that reason "
            "and adapt over ones that are endlessly fine-tuned, and what that "
            "means for how we engineer them."
        ),
        "summary_it": (
            "Perché il futuro dei sistemi AI pratici favorisce agenti che "
            "ragionano e si adattano invece di essere continuamente "
            "fine-tuned, e cosa questo comporta per il modo in cui li "
            "progettiamo."
        ),
        "topics": ["Autonomous AI agents", "Context engineering"],
        "is_featured": True,
    },
    {
        "slug": "cloud-to-edge-autonomous-agents",
        "title": "From Cloud to Edge: Building Autonomous AI Agents with Gemini, ADK and On-Device AI",
        "language": "en",
        "summary_en": (
            "A practical look at building autonomous AI agents that move "
            "fluidly between cloud and on-device execution using Gemini and "
            "the Agent Development Kit."
        ),
        "summary_it": (
            "Uno sguardo pratico alla costruzione di agenti AI autonomi che si "
            "muovono fluidamente tra esecuzione cloud e on-device usando "
            "Gemini e l'Agent Development Kit."
        ),
        "topics": ["Cloud-to-edge AI", "Gemini", "Agent Development Kit", "On-device AI"],
        "is_featured": True,
    },
    {
        "slug": "parla-pensa-risponde",
        "title": "Parla, Pensa, Risponde: Costruire App Flutter IA con Gemini, anche Offline",
        "language": "it",
        "summary_en": (
            "Building AI-powered Flutter apps with Gemini that keep working "
            "offline, presented in Italian."
        ),
        "summary_it": (
            "Costruire app Flutter potenziate dall'IA con Gemini che "
            "continuano a funzionare anche offline."
        ),
        "topics": ["Gemini", "Flutter", "On-device AI"],
        "is_featured": True,
    },
]

# City coordinates confirmed in the source brief. Never guessed for other cities.
CITY_COORDINATES: dict[str, tuple[float, float]] = {
    "Pisa": (43.7228, 10.4017),
    "Vicenza": (45.5455, 11.5354),
    "Tirana": (41.3275, 19.8187),
    "Velletri": (41.6867, 12.7775),
    "Dallas": (32.7767, -96.7970),
    "Ponferrada": (42.5466, -6.5962),
    "Turin": (45.0703, 7.6869),
    "Modena": (44.6471, 10.9252),
    "Madrid": (40.4168, -3.7038),
    "Bucharest": (44.4268, 26.1025),
    "Sofia": (42.6977, 23.3219),
    "New York": (40.7128, -74.0060),
    "Bishkek": (42.8746, 74.5698),
    "Almaty": (43.2389, 76.8897),
    "Catania": (37.5079, 15.0830),
    # Added for the expanded 2023-2026 speaking history.
    "Bari": (41.1171, 16.8719),
    "Naples": (40.8518, 14.2681),
    "Ancona": (43.6158, 13.5189),
    "Lecce": (40.3515, 18.1750),
    "Pordenone": (45.9564, 12.6605),
    "Potenza": (40.6420, 15.8059),
    "Gela": (37.0639, 14.2478),
    "Niscemi": (37.1439, 14.3866),
    "Toronto": (43.6532, -79.3832),
    "Washington, D.C. Area": (38.9072, -77.0369),
    "Chișinău": (47.0105, 28.8638),
}


def _coords(city: str | None) -> tuple[float | None, float | None]:
    if city and city in CITY_COORDINATES:
        return CITY_COORDINATES[city]
    return (None, None)


def _event(
    slug: str,
    event_name: str,
    *,
    year: int,
    month: int | None = None,
    city: str | None = None,
    country: str | None = None,
    continent: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    venue: str | None = None,
    format: str = "conference",
    status: str = "completed",
    sessions_count: int = 1,
    talk_slug: str | None = None,
    topics: list[str] | None = None,
    event_url: str | None = None,
    session_title: str | None = None,
    is_international_milestone: bool = False,
) -> dict[str, Any]:
    lat, lon = _coords(city)
    return {
        "slug": slug,
        "event_name": event_name,
        "year": year,
        # A start_date implies its own month; otherwise fall back to the
        # explicitly known month (many engagements here are only confirmed
        # to the month, without an exact day — see docs/event-management.md).
        "month": start_date.month if start_date else month,
        "city": city,
        "country": country,
        "continent": continent,
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date or start_date,
        "venue": venue,
        "format": format,
        "language": "en",
        "topics": topics or [],
        "status": status,
        "sessions_count": sessions_count,
        "talk_slug": talk_slug,
        "session_title": session_title,
        "event_url": event_url,
        "is_featured": talk_slug is not None,
        "is_international_milestone": is_international_milestone,
    }


EVENTS: list[dict[str, Any]] = [
    # --- 2023 -----------------------------------------------------------
    _event(
        "pybari-2023", "PyBari",
        year=2023, month=12, city="Bari", country="Italy", continent="Europe",
        format="user_group", event_url="https://bari.python.it/",
        topics=["Python"],
    ),
    # --- 2024 -------------------------------------------------------------
    _event(
        "devfest-gela-2024", "Google Developers Group DevFest — Gela, Sicily",
        year=2024, month=12, city="Gela", country="Italy", continent="Europe",
        format="devfest",
        event_url="https://gdg.community.dev/events/details/google-gdg-gela-presents-devfest-2024/",
    ),
    _event(
        "devfest-catania-2024", "DevFest Catania",
        year=2024, month=11, city="Catania", country="Italy", continent="Europe",
        format="devfest",
    ),
    # --- 2025 ---------------------------------------------------------------
    _event(
        # Verified exact date preserved from earlier data. Session title and
        # event URL added from the confirmed dataset.
        "pisa-dev-lightning-talk-2025", "Pisa.dev Lightning Talk Night",
        year=2025, city="Pisa", country="Italy", continent="Europe",
        start_date=date(2025, 3, 17), format="lightning_talk",
        event_url="https://gdg.community.dev/events/details/google-gdg-pisa-presents-pisadev-lightning-talk-night-with-gdg-pisa/",
        session_title="Può l'IA trasformarti in un 10x Developer?",
    ),
    _event(
        "devfest-pisa-2025", "GDG DevFest Pisa 2025",
        year=2025, city="Pisa", country="Italy", continent="Europe",
        start_date=date(2025, 4, 12), format="devfest",
    ),
    _event(
        "agile-oday-2025", "Agile O'Day 2025",
        year=2025, month=5, city="Naples", country="Italy", continent="Europe",
        format="conference",
        event_url="http://www.agilecommunitycampania.it/agile-oday?view=article&id=43:agile-oday-2024&catid=12",
        topics=["Agile"],
    ),
    _event(
        # Location and month added from the confirmed dataset; exact day still
        # unknown.
        "sql-start-2025", "SQL Start!",
        year=2025, month=6, city="Ancona", country="Italy", continent="Europe",
        format="conference", topics=["Data", "SQL"],
    ),
    _event(
        "devfest-vicenza-2025", "DevFest Vicenza 2025",
        year=2025, city="Vicenza", country="Italy", continent="Europe",
        start_date=date(2025, 6, 14), format="devfest",
        event_url="https://gdg.community.dev/gdg-vicenza",
    ),
    _event(
        "ppug-tirana-2025", "Power Platform User Group Albania",
        year=2025, city="Tirana", country="Albania", continent="Europe",
        start_date=date(2025, 7, 30), format="user_group",
        event_url="https://ppug.al/", topics=["Microsoft Power Platform"],
        is_international_milestone=True,
    ),
    _event(
        "devfest-lecce-2025", "DevFest Lecce 2025",
        year=2025, month=9, city="Lecce", country="Italy", continent="Europe",
        format="devfest", event_url="https://gdg.community.dev/gdg-lecce/",
    ),
    _event(
        # Location and month added from the confirmed dataset.
        "1nn0vai-2025", "1nn0vAI 2025",
        year=2025, month=9, city="Pordenone", country="Italy", continent="Europe",
        format="conference", event_url="https://1nn0vai2025.1nn0va.it/",
        topics=["AI"],
    ),
    _event(
        "global-game-jam-catania-2025", "Global Game Jam Catania 2025",
        year=2025, month=1, city="Catania", country="Italy", continent="Europe",
        format="community", event_url="https://globalgamejam.it/",
        topics=["Game Development"],
    ),
    _event(
        "velletri-dev-meetup-2025", "Velletri Dev Meetup",
        year=2025, city="Velletri", country="Italy", continent="Europe",
        start_date=date(2025, 9, 6), format="meetup",
    ),
    _event(
        "devfest-modena-2025", "DevFest Modena 2025",
        year=2025, month=10, city="Modena", country="Italy", continent="Europe",
        format="devfest", event_url="https://devfest.modena.it/",
    ),
    _event(
        # City added from the confirmed dataset (Potenza).
        "devfest-basilicata-2025", "DevFest Basilicata 2025",
        year=2025, month=10, city="Potenza", country="Italy", continent="Europe",
        format="devfest",
        event_url="https://gdg.community.dev/events/details/google-gdg-basilicata-presents-devfest-basilicata-2025/",
    ),
    _event(
        "omniopencon-bucharest-2025", "OmniOpenCon 2025",
        year=2025, month=10, city="Bucharest", country="Romania", continent="Europe",
        format="conference", event_url="https://omniopencon.org/",
        is_international_milestone=True,
    ),
    _event(
        "techcon365-dallas-2025",
        "TechCon 365 Dallas — A Microsoft 365 & Power Platform Conference",
        year=2025, city="Dallas", country="United States", continent="North America",
        start_date=date(2025, 11, 5), end_date=date(2025, 11, 7),
        format="conference", sessions_count=3,
        event_url="https://www.techcon365.com/Dallas",
        topics=["Microsoft 365", "Power Platform"],
        is_international_milestone=True,
    ),
    _event(
        # Merged with the previously separate "Nerdearla" / "Nerdearla Madrid"
        # entry — one appearance, canonical name per the confirmed dataset.
        # Slug kept stable rather than renamed (see docs/event-management.md).
        "nerdearla-madrid-2025", "Nerdearla España 2025",
        year=2025, month=11, city="Madrid", country="Spain", continent="Europe",
        format="conference", event_url="https://nerdearla.es/",
        is_international_milestone=True,
    ),
    _event(
        "devfest-ponferrada-2025", "DevFest Ponferrada 2025",
        year=2025, month=11, city="Ponferrada", country="Spain", continent="Europe",
        format="devfest",
        event_url="https://gdg.community.dev/events/details/google-gdg-ponferrada-presents-devfest-ponferrada-2025/",
    ),
    _event(
        "devfest-alps-2025", "DevFest Alps 2025",
        year=2025, month=11, city="Turin", country="Italy", continent="Europe",
        format="devfest",
    ),
    # --- 2026 -----------------------------------------------------------
    _event(
        # Official branding retains "2025" even though the event took place
        # in February 2026 — kept as-is per the confirmed dataset. Location
        # is Niscemi, distinct from the 2024 Gela DevFest above.
        "gdg-gela-devfest-2025", "GDG Gela DevFest 2025",
        year=2026, month=2, city="Niscemi", country="Italy", continent="Europe",
        format="devfest", event_url="https://gdg.community.dev/e/m5n7yp/",
    ),
    _event(
        "flutter-catania-meetup-2026", "Flutter Catania Meetup",
        year=2026, month=4, city="Catania", country="Italy", continent="Europe",
        format="meetup", topics=["Flutter"],
    ),
    _event(
        "agentcamp-sofia-2026", "AgentCamp",
        year=2026, city="Sofia", country="Bulgaria", continent="Europe",
        start_date=date(2026, 5, 16), format="conference",
        event_url="http://bsc.technology/AIBootcamp/",
        talk_slug="stop-fine-tuning-start-thinking",
        topics=["Autonomous AI agents", "Context engineering"],
        is_international_milestone=True,
    ),
    _event(
        "devfest-vicenza-2026", "DevFest Vicenza 2026",
        year=2026, month=6, city="Vicenza", country="Italy", continent="Europe",
        format="devfest", event_url="https://devfestvicenza.it/",
        talk_slug="parla-pensa-risponde",
        topics=["Gemini", "Flutter", "On-device AI"],
    ),
    _event(
        "ai-community-conference-nyc-2026", "AI Community Conference",
        year=2026, city="New York", country="United States", continent="North America",
        start_date=date(2026, 6, 26), venue="Microsoft, Times Square",
        format="conference", topics=["AI"],
        is_international_milestone=True,
    ),
    _event(
        "gdg-bishkek-2026", "GDG Bishkek Community Meetup",
        year=2026, city="Bishkek", country="Kyrgyzstan", continent="Central Asia",
        start_date=date(2026, 7, 12), format="meetup",
        event_url="https://gdg.community.dev/events/details/google-gdg-bishkek-presents-from-cloud-to-edge-building-production-ready-ai-agents-with-gemini-adk-and-on-device-ai/cohost-gdg-bishkek/",
        topics=["Cloud-to-edge AI", "Gemini", "Agent Development Kit", "On-device AI"],
        is_international_milestone=True,
    ),
    _event(
        # Merged with the previously separate generic "GDG Almaty" entry —
        # one appearance; this is its official, more complete name from the
        # confirmed dataset, with the real event URL. Exact date and talk
        # link preserved from the earlier record.
        "gdg-almaty-2026", "Qazaq IT Community Conference",
        year=2026, city="Almaty", country="Kazakhstan", continent="Central Asia",
        start_date=date(2026, 7, 15), format="conference",
        event_url="https://qazaqitcom.kz/ru/events/from-cloud-to-edge-building-autonomous-ai-agents-with-gemini-adk-and-on-device-ai",
        talk_slug="cloud-to-edge-autonomous-agents",
        topics=["Cloud-to-edge AI", "Gemini", "Agent Development Kit", "On-device AI"],
        is_international_milestone=True,
    ),
    # --- Upcoming / incoming (not yet delivered) -------------------------
    _event(
        "gdg-chisinau-first-meetup-2026", "GDG Chișinău First Meetup",
        year=2026, month=9, city="Chișinău", country="Moldova", continent="Europe",
        format="meetup", status="upcoming",
    ),
    _event(
        "m365-toronto-2026", "M365 Toronto",
        year=2026, month=9, city="Toronto", country="Canada", continent="North America",
        format="conference", status="incoming", topics=["Microsoft 365"],
    ),
    _event(
        "sql-saturday-toronto-2026", "SQL Saturday Toronto",
        year=2026, month=9, city="Toronto", country="Canada", continent="North America",
        format="conference", status="incoming", topics=["Data", "SQL"],
    ),
    _event(
        "data-saturday-sofia-2026", "Data Saturday Sofia 2026",
        year=2026, month=10, city="Sofia", country="Bulgaria", continent="Europe",
        format="conference", status="upcoming",
        event_url="https://datasaturdayssofia.eventbrite.com/", topics=["Data"],
    ),
    _event(
        # Exact date not yet known; only that it is expected in 2026.
        "bsides-nova-2026", "BSides NOVA",
        year=2026, city="Washington, D.C. Area", country="United States",
        continent="North America", format="conference", status="incoming",
        topics=["Cybersecurity"],
    ),
]

PASSIONS: list[dict[str, Any]] = [
    {
        "slug": "ai-beyond-demos",
        "title_en": "AI Beyond Demos",
        "title_it": "L'IA Oltre le Demo",
        "text_en": (
            "What genuinely interests Daniele is not the impressive demo but "
            "the unglamorous engineering that makes an AI system trustworthy "
            "on the hundredth run, not just the first."
        ),
        "text_it": (
            "Ciò che interessa davvero a Daniele non è la demo impressionante, "
            "ma l'ingegneria poco appariscente che rende un sistema AI "
            "affidabile alla centesima esecuzione, non solo alla prima."
        ),
        "motif_label": None,
        "sort_order": 1,
    },
    {
        "slug": "backend-systems-and-architecture",
        "title_en": "Backend Systems & Architecture",
        "title_it": "Sistemi Backend & Architettura",
        "text_en": (
            "There is a particular satisfaction in a well-typed API contract "
            "and a database schema that still makes sense a year later. "
            "Daniele treats architecture as a form of long-term care for a "
            "system's future maintainers."
        ),
        "text_it": (
            "C'è una soddisfazione particolare in un contratto API ben "
            "tipizzato e in uno schema di database che ha ancora senso un "
            "anno dopo. Daniele considera l'architettura una forma di cura a "
            "lungo termine per i futuri manutentori di un sistema."
        ),
        "motif_label": None,
        "sort_order": 2,
    },
    {
        "slug": "public-speaking-and-communities",
        "title_en": "Public Speaking & Developer Communities",
        "title_it": "Public Speaking & Community di Sviluppatori",
        "text_en": (
            "Explaining a hard technical idea clearly, to a room of strangers "
            "who might use it the next day, is one of Daniele's favorite kinds "
            "of engineering work — which is also why Velletri.dev exists."
        ),
        "text_it": (
            "Spiegare con chiarezza un'idea tecnica complessa a una sala di "
            "sconosciuti che magari la useranno il giorno dopo è uno dei tipi "
            "di lavoro ingegneristico preferiti da Daniele — ed è anche per "
            "questo che esiste Velletri.dev."
        ),
        "motif_label": "Velletri · 41.6867° N, 12.7775° E",
        "sort_order": 3,
    },
    {
        "slug": "travel-and-cultures",
        "title_en": "International Travel & Discovering Cultures",
        "title_it": "Viaggi Internazionali & Scoperta di Culture",
        "text_en": (
            "Two years of international speaking have taken Daniele from "
            "Central European user groups to conferences in Central Asia and "
            "North America — and every trip reshapes how he thinks about "
            "building for a genuinely international audience."
        ),
        "text_it": (
            "Due anni di speaking internazionale hanno portato Daniele da "
            "user group dell'Europa centrale a conferenze in Asia Centrale e "
            "Nord America — e ogni viaggio ridefinisce il suo modo di pensare "
            "a come costruire per un pubblico davvero internazionale."
        ),
        "motif_label": "Velletri → Almaty · 5,600+ km",
        "sort_order": 4,
    },
    {
        "slug": "aviation-and-route-networks",
        "title_en": "Aviation & Airline Route Networks",
        "title_it": "Aviazione & Reti di Rotte Aeree",
        "text_en": (
            "A long-standing fascination with how airline networks connect "
            "the world — hubs, routes, and the logistics behind getting to a "
            "conference stage on another continent on time."
        ),
        "text_it": (
            "Un interesse di lunga data per il modo in cui le reti aeree "
            "connettono il mondo — hub, rotte, e la logistica che sta dietro "
            "l'arrivare puntuali su un palco in un altro continente."
        ),
        "motif_label": None,
        "sort_order": 5,
    },
    {
        "slug": "geography-and-cartography",
        "title_en": "Geography & Maps",
        "title_it": "Geografia & Cartografia",
        "text_en": (
            "Maps, coordinates and routes show up throughout this site for a "
            "reason: geography is one of Daniele's quiet, long-running "
            "interests, and speaking internationally has only deepened it."
        ),
        "text_it": (
            "Mappe, coordinate e rotte ricorrono in tutto questo sito per un "
            "motivo: la geografia è uno degli interessi discreti e duraturi "
            "di Daniele, e lo speaking internazionale non ha fatto che "
            "approfondirlo."
        ),
        "motif_label": None,
        "sort_order": 6,
    },
    {
        "slug": "continuous-learning",
        "title_en": "Continuous Learning",
        "title_it": "Apprendimento Continuo",
        "text_en": (
            "Between university coursework, professional engineering and "
            "conference preparation, Daniele treats staying technically "
            "current as a daily practice, not an occasional effort."
        ),
        "text_it": (
            "Tra i corsi universitari, il lavoro ingegneristico professionale "
            "e la preparazione delle conferenze, Daniele considera il "
            "restare tecnicamente aggiornato una pratica quotidiana, non uno "
            "sforzo occasionale."
        ),
        "motif_label": None,
        "sort_order": 7,
    },
    {
        "slug": "digital-ethics-and-knowledge-sharing",
        "title_en": "Digital Ethics & Knowledge Sharing",
        "title_it": "Etica Digitale & Condivisione della Conoscenza",
        "text_en": (
            "As AI systems take on more responsibility, Daniele cares about "
            "building and talking about them honestly — including their "
            "limits — and about making that understanding freely accessible "
            "through talks, community events and open discussion."
        ),
        "text_it": (
            "Man mano che i sistemi AI assumono più responsabilità, a Daniele "
            "sta a cuore costruirli e raccontarli con onestà, inclusi i loro "
            "limiti, e rendere quella comprensione liberamente accessibile "
            "tramite interventi, eventi di community e discussione aperta."
        ),
        "motif_label": None,
        "sort_order": 8,
    },
]

COMMUNITY_PROFILE: dict[str, Any] = {
    "name": "Velletri.dev",
    "role_en": "Founder & Community Lead",
    "role_it": "Fondatore & Community Lead",
    "mission_en": (
        "Connect developers, students and technology enthusiasts in Velletri "
        "and the surrounding area with each other, and with the national and "
        "international developer community."
    ),
    "mission_it": (
        "Connettere sviluppatori, studenti e appassionati di tecnologia a "
        "Velletri e dintorni tra loro, e con la community di sviluppatori "
        "nazionale e internazionale."
    ),
    "description_en": (
        "Velletri.dev is a grassroots community initiative founded by Daniele "
        "Mario Areddu to bring technical events, meetups and knowledge "
        "sharing to Velletri — organizing sessions, inviting speakers, and "
        "creating a local entry point into the wider tech ecosystem for "
        "students and early-career developers."
    ),
    "description_it": (
        "Velletri.dev è un'iniziativa di community dal basso fondata da "
        "Daniele Mario Areddu per portare eventi tecnici, meetup e "
        "condivisione di conoscenza a Velletri, organizzando sessioni, "
        "invitando speaker e creando un punto di accesso locale al più ampio "
        "ecosistema tecnologico per studenti e sviluppatori a inizio "
        "carriera."
    ),
    "vision_en": (
        "A local tech ecosystem where geography is not a barrier to learning "
        "from — and eventually speaking alongside — the wider international "
        "developer community."
    ),
    "vision_it": (
        "Un ecosistema tecnologico locale in cui la geografia non sia una "
        "barriera per imparare dalla, e infine parlare accanto alla, più "
        "ampia community di sviluppatori internazionale."
    ),
    "collaboration_en": (
        "Velletri.dev welcomes collaboration with speakers, communities and "
        "organizations interested in supporting local developer ecosystems — "
        "reach out through the contact page."
    ),
    "collaboration_it": (
        "Velletri.dev è aperta a collaborazioni con speaker, community e "
        "organizzazioni interessate a sostenere gli ecosistemi di "
        "sviluppatori locali — è possibile scrivere tramite la pagina "
        "contatti."
    ),
    "founded_year": 2023,
    "website_url": None,
}

COMMUNITY_ACTIVITIES: list[dict[str, Any]] = [
    {
        "slug": "velletri-dev-founding",
        "title_en": "Velletri.dev is founded",
        "title_it": "Nasce Velletri.dev",
        "description_en": (
            "Daniele founds Velletri.dev to bring regular technical meetups "
            "and knowledge sharing to his hometown."
        ),
        "description_it": (
            "Daniele fonda Velletri.dev per portare meetup tecnici regolari e "
            "condivisione di conoscenza nella sua città natale."
        ),
        "activity_date": date(2023, 1, 1),
        "activity_type": "milestone",
        "url": None,
        "sort_order": 1,
    },
    {
        "slug": "velletri-dev-meetup-2025",
        "title_en": "Velletri Dev Meetup",
        "title_it": "Velletri Dev Meetup",
        "description_en": (
            "A community meetup in Velletri, part of the ongoing local "
            "meetup series."
        ),
        "description_it": (
            "Un meetup di community a Velletri, parte della serie di eventi "
            "locali in corso."
        ),
        "activity_date": date(2025, 9, 6),
        "activity_type": "meetup",
        "url": None,
        "sort_order": 2,
    },
]

# ---------------------------------------------------------------------------
# Journey milestones for the frontend's editorial timeline. These reference
# only facts established elsewhere in this file and in the product brief.
# ---------------------------------------------------------------------------
JOURNEY_MILESTONES: list[dict[str, Any]] = [
    {
        "year": None,
        "title_en": "An early interest in computing",
        "title_it": "Un interesse precoce per l'informatica",
        "text_en": "Daniele's interest in how computers and networks work takes root, ahead of formal technical studies.",
        "text_it": "L'interesse di Daniele per il funzionamento di computer e reti prende forma, prima degli studi tecnici formali.",
        "kind": "education",
    },
    {
        "year": 2025,
        "title_en": "Diploma in Informatica e Telecomunicazioni",
        "title_it": "Diploma in Informatica e Telecomunicazioni",
        "text_en": "Completes technical secondary education at ITIS G. Vallauri, Velletri.",
        "text_it": "Completa gli studi tecnici superiori all'ITIS G. Vallauri di Velletri.",
        "kind": "education",
    },
    {
        "year": None,
        "title_en": "Early backend & data-integration work",
        "title_it": "Primi lavori di backend e integrazione dati",
        "text_en": "Independent work on public-sector data platforms: normalizing territorial data and building REST APIs.",
        "text_it": "Lavoro indipendente su piattaforme dati del settore pubblico: normalizzazione di dati territoriali e sviluppo di API REST.",
        "kind": "project",
    },
    {
        "year": 2023,
        "title_en": "Velletri.dev is founded",
        "title_it": "Nasce Velletri.dev",
        "text_en": "Daniele founds Velletri.dev to bring technical meetups and knowledge sharing to his hometown.",
        "text_it": "Daniele fonda Velletri.dev per portare meetup tecnici e condivisione di conoscenza nella sua città natale.",
        "kind": "community",
    },
    {
        "year": 2023,
        "title_en": "First community speaking activity",
        "title_it": "Primi interventi in community",
        "text_en": "Daniele's speaking journey begins with the Python community at PyBari, in Bari.",
        "text_it": "Il percorso da speaker di Daniele inizia con la community Python di PyBari, a Bari.",
        "kind": "speaking",
        "event_slug": "pybari-2023",
    },
    {
        "year": 2024,
        "title_en": "The Italian GDG / DevFest circuit",
        "title_it": "Il circuito italiano GDG / DevFest",
        "text_en": "Talks at DevFest Catania and the Gela DevFest connect Daniele with Italy's Google Developer Group community.",
        "text_it": "Gli interventi a DevFest Catania e al DevFest di Gela collegano Daniele alla community italiana dei Google Developer Group.",
        "kind": "speaking",
        "event_slug": "devfest-catania-2024",
    },
    {
        "year": 2025,
        "title_en": "First talks in local developer communities",
        "title_it": "Primi interventi nelle community locali",
        "text_en": "Speaking journey begins with a lightning talk at Pisa.dev, followed by DevFest Pisa and DevFest Vicenza.",
        "text_it": "Il percorso da speaker inizia con un lightning talk a Pisa.dev, seguito da DevFest Pisa e DevFest Vicenza.",
        "kind": "speaking",
        "event_slug": "pisa-dev-lightning-talk-2025",
    },
    {
        "year": 2025,
        "title_en": "Expansion into European events",
        "title_it": "Espansione verso eventi europei",
        "text_en": "Talks follow in Tirana, Ponferrada, Madrid, Bucharest and across Italy.",
        "text_it": "Seguono interventi a Tirana, Ponferrada, Madrid, Bucarest e in diverse città italiane.",
        "kind": "speaking",
        "event_slug": "ppug-tirana-2025",
    },
    {
        "year": 2025,
        "title_en": "First talks in North America",
        "title_it": "Primi interventi in Nord America",
        "text_en": "Three sessions at TechCon365 in Dallas mark Daniele's first speaking trip to the United States.",
        "text_it": "Tre sessioni al TechCon365 di Dallas segnano il primo viaggio da speaker di Daniele negli Stati Uniti.",
        "kind": "speaking",
        "event_slug": "techcon365-dallas-2025",
    },
    {
        "year": 2026,
        "title_en": "Joining Global Technologies Italia",
        "title_it": "L'ingresso in Global Technologies Italia",
        "text_en": "Daniele joins Global Technologies Italia as a Backend & AI Developer.",
        "text_it": "Daniele entra in Global Technologies Italia come Backend & AI Developer.",
        "kind": "experience",
    },
    {
        "year": 2025,
        "title_en": "Computer Science at the University of Calabria",
        "title_it": "Informatica all'Università della Calabria",
        "text_en": "Begins a Bachelor's Degree in Computer Science at the University of Calabria.",
        "text_it": "Inizia la Laurea in Informatica all'Università della Calabria.",
        "kind": "education",
    },
    {
        "year": 2026,
        "title_en": "Speaking experiences in Central Asia",
        "title_it": "Interventi in Asia Centrale",
        "text_en": "Talks at AgentCamp Sofia, GDG Bishkek and GDG Almaty extend Daniele's speaking map into Central Asia.",
        "text_it": "Gli interventi ad AgentCamp Sofia, GDG Bishkek e GDG Almaty estendono la mappa di speaking di Daniele fino all'Asia Centrale.",
        "kind": "speaking",
        "event_slug": "gdg-almaty-2026",
    },
    {
        "year": 2026,
        "title_en": "Next stops: Moldova, Canada and the United States",
        "title_it": "Prossime tappe: Moldova, Canada e Stati Uniti",
        "text_en": "Incoming and upcoming appearances continue the expansion — GDG Chișinău, M365 Toronto, SQL Saturday Toronto, Data Saturday Sofia and BSides NOVA.",
        "text_it": "I prossimi interventi, in programma o in via di conferma, proseguono l'espansione — GDG Chișinău, M365 Toronto, SQL Saturday Toronto, Data Saturday Sofia e BSides NOVA.",
        "kind": "speaking",
        "event_slug": "m365-toronto-2026",
    },
    {
        "year": None,
        "title_en": "Toward AI agents, RAG and context engineering",
        "title_it": "Verso agenti AI, RAG e context engineering",
        "text_en": "Daniele's technical and speaking focus evolves toward production AI: autonomous agents, RAG and context engineering.",
        "text_it": "Il focus tecnico e divulgativo di Daniele evolve verso l'AI in produzione: agenti autonomi, RAG e context engineering.",
        "kind": "focus",
    },
]
