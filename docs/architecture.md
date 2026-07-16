# System Architecture

## Overview

Douyin Fashion AI is a cloud-native, event-driven B2B SaaS platform. A merchant uploads a garment image; the platform returns a 5–15 second ultra-realistic fashion video ready for Douyin publishing.

```
┌───────────────────────────────────────────────────────────────┐
│  Merchant Browser / WeChat Mini-Program                   │
└──────────────────────────────┬─────────────────────────────┘
                               │ HTTPS
                    ┌─────────┴─────────┐
                    │  Cloudflare CDN   │
                    │  + WAF + DDoS     │
                    └─────────┬─────────┘
                               │
                    ┌─────────┴─────────┐
                    │  API Gateway      │
                    │  (Fastify / EKS)  │
                    └─────────┬─────────┘
                    ┌─────────┴─────────┐
                    │  BullMQ Queue     │
                    │  (Redis / Upstash)│
                    └─────────┬─────────┘
                    ┌─────────┴─────────┐
                    │ Video-Gen Worker  │
                    │ (Model Router)    │
                    └──┬─────────────┬┘
              ┌─────┤              ├──────┐
         Kling 3.x         Veo 3.1    Runway
         (Primary)      (Secondary) (Fallback)
```

## Key Design Decisions

### 1. Model Router Strategy
- **Default**: Kling 3.x via KuaiShou API (lowest latency in CN, $0.04/video-second)
- **Overflow**: Veo 3.1 via Google Vertex AI (best quality, $0.09/video-second)
- **Fallback**: Runway Gen-4 (most stable, $0.06/video-second)
- Router selects based on: queue depth, cost budget per tenant, model health

### 2. Job Lifecycle
```
UPLOAD → PREPROCESSING → QUEUED → GENERATING → POSTPROCESSING → READY → DELIVERED
```
- Each state transition emits a webhook event to the merchant
- SLA targets: QUEUED→READY in <90 seconds (p95)

### 3. Multi-Tenancy
- Row-level security in PostgreSQL via `tenant_id`
- Separate BullMQ queues per pricing tier (Starter / Pro / Enterprise)
- Rate limits enforced at API Gateway + Redis layer

### 4. Storage Architecture
- **Input images**: S3 / Cloudflare R2 (merchant uploads)
- **Generated videos**: S3 with pre-signed URLs (72h TTL), then Cloudflare Stream for delivery
- **Thumbnails**: Sharp-generated, stored on R2, served via CDN

### 5. Database Schema (Core Tables)
```sql
tenants        -- org, plan, credits, settings
users          -- auth, roles, tenant_id FK
garments       -- image_url, metadata, processed_url
jobs           -- garment_id, status, model, prompt, video_url, cost_credits
webhooks       -- job_id, url, secret, last_attempt, status
billing_events -- tenant_id, type, amount, stripe_id
```

## Infrastructure

| Component       | Service                  | Region         |
|----------------|--------------------------|----------------|
| Compute         | AWS EKS                  | ap-east-1 HK   |
| Database        | AWS RDS PostgreSQL 16    | ap-east-1 HK   |
| Cache / Queue   | AWS ElastiCache Redis 7  | ap-east-1 HK   |
| Object Storage  | AWS S3 + Cloudflare R2   | Multi-region   |
| Video Delivery  | Cloudflare Stream        | Global CDN     |
| CDN / WAF       | Cloudflare               | Global         |
| Monitoring      | Grafana + Prometheus     | In-cluster     |
| Logging         | Loki + Pino              | In-cluster     |
| Tracing         | OpenTelemetry + Tempo    | In-cluster     |

## Security

- JWT (RS256) for API auth, 15min access tokens + 7-day refresh
- Webhook signatures: HMAC-SHA256
- All secrets in AWS Secrets Manager
- ICP license compliance for .cn domain serving
- GDPR-equivalent handling: no PII stored beyond account data
