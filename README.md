# douyin-fashion-ai

> Production-grade B2B SaaS platform for generating ultra-realistic Douyin fashion videos from garment images. Built for Chinese apparel factories, OEM/ODM manufacturers, and fashion brands.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Stack](https://img.shields.io/badge/stack-Next.js%20%7C%20FastAPI%20%7C%20Python-informational)
![Status](https://img.shields.io/badge/status-MVP%20Development-orange)

---

## What It Does

A user uploads one or more garment images, selects a video template or writes a free-form prompt in Chinese or English, and the platform generates a polished 9:16 vertical fashion video featuring an ultra-realistic human model naturally presenting the outfit, ready for Douyin, e-commerce listings, and digital marketing.

**Core workflow:**

1. Upload garment images (front, back, detail)
2. Select template or write a free-form prompt
3. Choose AI model persona or upload a reference
4. Generate video via Standard or Premium route
5. Preview, regenerate, or approve
6. Export Douyin-ready vertical video

---

## Who It Is For

| Customer | Use Case |
|---|---|
| Chinese garment factories | High-volume SKU video production |
| OEM / ODM manufacturers | Buyer-facing product videos |
| Apparel exporters | Multilingual campaign assets |
| Private-label fashion brands | Seasonal and launch content |
| E-commerce content teams | Douyin / Tmall / JD channel creatives |

---

## Key Features

- Garment-first upload pipeline with front, back, and detail shots plus auto quality checks
- Template library: Runway Walk, Studio Luxury, Street Style, Detail Close-up, Festive Campaign, Outdoor Cinematic
- Free-form prompt mode accepting Chinese or English natural language
- Prompt enhancement engine that rewrites weak prompts into high-performing production prompts
- AI model persona selection: East Asian, international, luxury editorial, casual commercial
- Tiered inference routing: Economy / Standard / Premium routes for cost and quality control
- Preview and regenerate loop with one-click variation control
- Batch mode via CSV or folder-driven bulk generation
- Bilingual UI: Simplified Chinese and English
- Douyin-ready export in 9:16 vertical format
- Team workspaces with multi-user RBAC and shared brand presets
- Admin panel with queue monitoring, cost telemetry, and moderation console

---

## Model Strategy (July 2026)

| Layer | Approach |
|---|---|
| Primary video model | Kling 3.x image-to-video route |
| Secondary fallback | Mid-tier bulk generation route |
| Premium tier | Veo 3.1-class high-realism route |
| Character / image layer | High-fidelity image model with identity locking |
| Garment binding | Fashion-specific try-on / garment-transfer stage |
| Identity consistency | Face embedding and locked reference seed bank |
| Audio (optional) | Music bed, voiceover, and beat sync |
| Moderation | Multi-stage prompt, image, and output review |

All model calls are routed through an abstraction layer. Providers can be swapped without rewriting application logic.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind CSS |
| Backend services | Python 3.12, FastAPI |
| Job queue | Redis and async worker pools |
| Storage | S3-compatible object store (Alibaba OSS or AWS S3) |
| Database | PostgreSQL 15 |
| Inference routing | Custom Python router with provider abstraction |
| Containerization | Docker and Docker Compose for dev, Kubernetes for prod |
| CI/CD | GitHub Actions |
| Observability | Structured logging, OpenTelemetry tracing |
| Cloud primary | Alibaba Cloud or Tencent Cloud for China |
| Cloud global | AWS or GCP for premium inference routes |

---

## Repository Structure

```
douyin-fashion-ai/
├── apps/
│   ├── web/                     # Customer-facing SaaS frontend (Next.js)
│   ├── admin/                   # Internal ops and admin console
│   └── docs-site/               # Product and API documentation site
├── services/
│   ├── api-gateway/             # Unified public API entrypoint
│   ├── auth-service/            # Auth, orgs, RBAC, sessions
│   ├── billing-service/         # Plans, credits, invoices, usage
│   ├── asset-service/           # Uploads, storage metadata, transforms
│   ├── prompt-service/          # Prompt enhancement and template logic
│   ├── orchestration-service/   # Job lifecycle and workflow state
│   ├── inference-router/        # Model and provider selection logic
│   ├── moderation-service/      # Prompt, image, and output compliance
│   ├── qa-service/              # Automated quality scoring
│   ├── analytics-service/       # Product and business analytics
│   └── export-service/          # Render packaging and delivery
├── workers/
│   ├── preprocess-worker/       # Cleanup, segmentation, normalization
│   ├── tryon-worker/            # Garment binding and virtual try-on
│   ├── video-worker/            # Video generation runners
│   ├── retry-worker/            # Retry and failover jobs
│   └── thumbnail-worker/        # Preview assets and poster frames
├── packages/
│   ├── ui/                      # Shared UI component library
│   ├── config/                  # Shared config and env schema
│   ├── types/                   # Shared TypeScript and Pydantic contracts
│   ├── sdk/                     # Partner and API client SDK
│   └── observability/           # Logging and tracing helpers
├── prompts/
│   ├── system/                  # Master system prompts
│   ├── templates/               # Per-template prompt variants
│   ├── negative/                # Negative prompt blocks
│   ├── enhancers/               # Rewrite and expansion rules
│   ├── localization/            # zh-CN and en prompt variants
│   └── tests/                   # Prompt regression test cases
├── infra/
│   ├── terraform/               # Infrastructure as code
│   ├── kubernetes/              # Helm charts and manifests
│   ├── alicloud/                # Alibaba Cloud specific modules
│   ├── tencent/                 # Tencent Cloud specific modules
│   └── monitoring/              # Dashboards and alerting
├── docs/
│   ├── architecture/            # System design documents
│   ├── product/                 # PRDs and roadmap
│   ├── compliance/              # China compliance policies
│   ├── pricing/                 # Pricing and margin logic
│   ├── runbooks/                # On-call and support procedures
│   └── adr/                     # Architecture decision records
├── examples/
│   ├── sample-garments/         # Example garment input sets
│   ├── sample-prompts/          # Example user and enhanced prompts
│   ├── sample-outputs/          # Example output metadata
│   └── partner-api/             # Example API integration payloads
├── scripts/
│   ├── seed/                    # Seed templates and demo tenants
│   ├── migrations/              # Database migration tooling
│   ├── benchmark/               # Latency and cost benchmark scripts
│   └── smoke/                   # End-to-end smoke tests
├── tests/
│   ├── e2e/
│   ├── integration/
│   ├── unit/
│   ├── load/
│   └── regression/
├── .github/
│   ├── workflows/               # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── configs/
│   ├── tenants/
│   ├── feature-flags/
│   └── pricing/
├── .env.example
├── docker-compose.yml
├── Makefile
├── turbo.json
└── package.json
```

---

## Prompt Framework

The `prompts/` directory is a fully versioned prompt engineering system:

- `system/master.md` - Master system prompt for the video generation pipeline
- `templates/` - Runway Walk, Studio Luxury, Street Style, Detail Close-up, Festive, Outdoor Cinematic
- `negative/default.md` - Canonical negative prompt block
- `enhancers/rewrite-rules.md` - Rules for converting weak user prompts into production-grade prompts
- `localization/zh-CN.md` - Full Chinese-language prompt system
- `tests/` - Prompt regression test cases with expected quality thresholds

All prompts are treated as versioned code. Changes require review and regression testing.

---

## Pricing Model

| Plan | Target | Monthly Fee |
|---|---|---|
| Starter Factory | Small factory teams | $299-$499 |
| Growth Brand | Mid-sized brands and exporters | $999-$2,499 |
| Scale Enterprise | Large factories and groups | $5,000+ |
| Custom Enterprise+ | Strategic accounts | Custom |

**Generation cost bands:**

| Route | Internal Cost / Video | Customer Price / Video | Target Margin |
|---|---|---|---|
| Economy | $0.80-$2.00 | $3-$6 | >60% |
| Standard | $2.50-$6.00 | $8-$18 | >60% |
| Premium | $8-$20+ | $25-$60+ | >55% |

---

## MVP Roadmap

### Phase 1 - MVP
- Garment upload pipeline
- 5 core video templates
- AI model persona selection
- Prompt enhancement engine
- Standard route generation
- Preview and regenerate loop
- Vertical video export
- Basic billing and credits

### Phase 2 - Paid Beta
- Batch mode
- Shared brand model presets
- QA scoring and auto-retry
- Workspace roles and RBAC
- Subscription plans
- Chinese-first onboarding flow
- Analytics dashboard

### Phase 3 - Factory Workflow Automation
- SKU folder ingestion
- API and ERP integrations
- Bulk approval workflows
- Collection export bundles
- Template performance recommendations

### Phase 4 - API and Enterprise Scale
- Full partner API
- SSO and enterprise procurement pack
- Region-aware deployment options
- Advanced analytics and custom workflows
- Strategic account routing policies

---

## Key Success Metrics

| Metric | Target |
|---|---|
| Generation success rate | >85% |
| First-pass realism satisfaction | >70% |
| Garment fidelity score | >80% |
| Time to first usable output | <10 minutes |
| Cost per successful video (standard) | <$6 internal |
| Monthly retained factory accounts | Growing MoM |
| Gross margin on standard route | >60% |

---

## China Compliance

- AI-generated content labeling per deep-synthesis regulations (effective 2023)
- Multi-stage prompt, image, and output moderation
- Identity misuse controls and full audit logging
- Regional data hosting options for enterprise accounts
- No unauthorized real-person likeness cloning
- Complete policy audit trail per generation job

---

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.12+
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7+

### Local Development

```bash
# Clone the repo
git clone https://github.com/wang-yuhao/douyin-fashion-ai.git
cd douyin-fashion-ai

# Copy environment config
cp .env.example .env

# Install all dependencies
npm install

# Start all services
docker-compose up -d

# Run database migrations
make migrate

# Seed demo data and templates
make seed

# Start the development server
make dev
```

### Run Tests

```bash
make test           # unit tests
make test-int       # integration tests
make test-e2e       # end-to-end tests
make test-load      # load tests
```

---

## Contributing

This is a private commercial repository. Internal contributors should follow branching and review guidelines in `docs/runbooks/contributing.md`.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

> Built for the 2026 Chinese apparel market. Optimized for garment fidelity, Douyin-ready output, and B2B factory workflows.
