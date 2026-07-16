# Default Negative Prompt

> Version: 1.0.0
> Applied to: All generation routes (economy, standard, premium)
> Usage: Append to every generation call after the positive prompt.

---

## Canonical Negative Prompt (English)

```
low realism, cartoon, anime, CGI look, 3D render, plastic skin, waxy skin, uncanny face, uncanny valley, artificial appearance, synthetic look, deformed hands, extra fingers, missing fingers, fused fingers, broken fingers, wrong number of fingers, deformed limbs, extra limbs, missing limbs, warped body, bad anatomy, incorrect proportions, distorted torso, floating body parts, duplicate body parts, wrong outfit, altered clothing design, clothing mismatch, changed garment structure, missing garment details, wrong fabric color, wrong pattern, unstable garment edges, fabric artifacts, warped fabric, unnatural drape, flicker, jitter, frame inconsistency, temporal inconsistency, motion blur artifacts, bad frame transitions, blurry face, low-detail face, oversharpening, noise, grain, compression artifacts, overexposure, underexposure, harsh fake lighting, flat lighting, neon color cast, desaturated, washed out, bad color grading, cheap advertisement look, low-end AI look, low budget production, distorted background, background artifacts, floating objects in background, cluttered scene, text overlay, watermark, logo, brand mark, NSFW, explicit content, suggestive content, fetish content, minor, ambiguous age, real celebrity likeness, unauthorized public figure, political content, violent content, gore, illegal content
```

---

## Compact Version (for token-limited contexts)

```
low realism, cartoon, CGI, plastic skin, uncanny face, deformed hands, extra fingers, bad anatomy, warped limbs, wrong outfit, altered clothing, unstable garment, flicker, jitter, blurry face, fake lighting, cheap AI look, distorted background, duplicate body parts, visual artifacts, NSFW, watermark
```

---

## Route-Specific Additions

### Economy Route (additional restrictions)
```
low resolution, pixelated, heavily compressed, motion artifacts
```

### Premium Route (heightened requirements)
```
any visible AI artifact, any frame inconsistency, any anatomical imperfection, any fabric instability, any camera jitter
```

---

## Maintenance Notes

- Review and update this prompt quarterly as model capabilities improve.
- Add new artifact categories as they are identified in QA review.
- Do not remove existing entries without full regression testing.
- Changes to this file require PR review and `make test-prompts` passing.
