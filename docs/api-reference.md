# API Reference

Base URL: `https://api.douyinfashion.ai/v1`

All requests require `Authorization: Bearer <access_token>` header.

---

## Authentication

### POST /auth/login
Issue access + refresh tokens.

**Body**
```json
{ "email": "string", "password": "string" }
```

**Response 200**
```json
{
  "accessToken": "eyJ...",
  "refreshToken": "eyJ...",
  "expiresIn": 900
}
```

### POST /auth/refresh
Rotate refresh token.

**Body**: `{ "refreshToken": "string" }`

---

## Garments

### POST /garments/upload
Get a pre-signed S3 URL to upload a garment image.

**Body**
```json
{
  "filename": "jacket-front.jpg",
  "contentType": "image/jpeg",
  "sizeBytes": 2048000
}
```

**Response 200**
```json
{
  "garmentId": "grm_01j2abc...",
  "uploadUrl": "https://s3.ap-east-1.amazonaws.com/...",
  "expiresAt": "2026-07-01T12:15:00Z"
}
```

### POST /garments/:id/confirm
Confirm upload complete and trigger preprocessing.

**Response 200**: `{ "status": "processing" }`

### GET /garments/:id
Get garment metadata and processed status.

---

## Jobs

### POST /jobs
Create a video generation job.

**Body**
```json
{
  "garmentId": "grm_01j2abc...",
  "templateId": "lifestyle-outdoor",
  "duration": 8,
  "aspectRatio": "9:16",
  "modelOverride": null,
  "webhookUrl": "https://yourshop.com/webhooks/fashion-ai"
}
```

**Response 201**
```json
{
  "jobId": "job_01j2xyz...",
  "status": "queued",
  "estimatedSeconds": 75,
  "creditsConsumed": 8
}
```

### GET /jobs/:id
Poll job status.

**Response**
```json
{
  "jobId": "job_01j2xyz...",
  "status": "ready",
  "videoUrl": "https://stream.cloudflare.com/...",
  "thumbnailUrl": "https://cdn.douyinfashion.ai/...",
  "durationSeconds": 8,
  "model": "kling-3.x",
  "completedAt": "2026-07-01T12:01:23Z"
}
```

**Job statuses**: `queued` | `preprocessing` | `generating` | `postprocessing` | `ready` | `failed`

### GET /jobs
List jobs with pagination.

**Query params**: `?page=1&limit=20&status=ready&garmentId=grm_...`

---

## Credits & Billing

### GET /billing/balance
Get current credit balance.

**Response**: `{ "credits": 450, "plan": "pro", "renewsAt": "2026-08-01" }`

### POST /billing/topup
Initiate a Stripe checkout session for credit top-up.

**Body**: `{ "packageId": "credits_500" }`

**Response**: `{ "checkoutUrl": "https://checkout.stripe.com/..." }`

---

## Webhooks

All webhook payloads are signed with `X-Signature-256: sha256=<HMAC-SHA256>`.

**Job completed payload**
```json
{
  "event": "job.completed",
  "jobId": "job_01j2xyz...",
  "videoUrl": "https://stream.cloudflare.com/...",
  "timestamp": "2026-07-01T12:01:23Z"
}
```

**Job failed payload**
```json
{
  "event": "job.failed",
  "jobId": "job_01j2xyz...",
  "reason": "model_timeout",
  "creditsRefunded": 8,
  "timestamp": "2026-07-01T12:02:00Z"
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 400  | Validation error |
| 401  | Unauthorized |
| 402  | Insufficient credits |
| 404  | Resource not found |
| 429  | Rate limit exceeded |
| 503  | All AI models unavailable |
