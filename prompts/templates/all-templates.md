# Prompt Templates

> All six production template prompts for the Douyin Fashion AI platform.
> These are appended after the master system prompt for each template-based generation.

---

## Template 1: Runway Walk

**ID:** `runway-walk`
**Best for:** Women's dresses, outerwear, eveningwear, structured garments

```
A confident, high-fashion female model wearing the exact uploaded outfit walks naturally and elegantly toward the camera on a clean premium runway path. The stride is smooth and rhythmic with subtle hip and shoulder motion, natural arm swing, and refined body language. The model maintains direct but elegant camera connection with a composed, charismatic expression. Frame the shot full-body in vertical 9:16 composition. Use cinematic fashion-show lighting: clean, directional, flattering. The garment must move naturally with the walk, showing accurate fabric behavior. No background distractions. Premium commercial runway aesthetic throughout.
```

**Variables:**
- `{MODEL_TYPE}`: female model, male model, androgynous model
- `{WALK_ENERGY}`: composed, confident, editorial, relaxed
- `{LIGHTING}`: runway spotlight, soft studio, editorial daylight

---

## Template 2: Studio Luxury

**ID:** `studio-luxury`
**Best for:** Premium knitwear, silk, tailored pieces, luxury accessories

```
A charismatic premium fashion model presents the exact uploaded outfit in a clean minimalist luxury studio environment. The background is white or softly neutral, completely distraction-free. The model performs slow, graceful turns, refined pose transitions, subtle hand placement, and elegant standing postures that highlight the garment from multiple angles. Lighting is soft, controlled, and professional with clean shadow falloff and realistic skin texture response. Use shallow depth of field for subject separation. Camera moves are slow and deliberate: gentle arc, slow dolly-in, or locked editorial framing. The result must feel like a high-end editorial campaign shoot.
```

**Variables:**
- `{BACKGROUND}`: white cyclorama, warm neutral, light grey
- `{POSE_ENERGY}`: editorial still, slow turn, graceful walk-in-place
- `{LIGHTING}`: soft beauty lighting, Rembrandt, split light

---

## Template 3: Street Style

**ID:** `street-style`
**Best for:** Casual wear, denim, sportswear, youth fashion, contemporary brands

```
A stylish, approachable human model wears the exact uploaded outfit in a clean upscale urban street setting. The environment suggests a modern city: clean pavement, soft architectural background, or a boutique-adjacent outdoor space. The model moves with relaxed confidence: a natural walk, subtle stop-and-look, or casual lean. Lighting is natural daylight or golden-hour warmth with realistic outdoor behavior. The camera follows with smooth handheld-style tracking or gentle static framing. Strong outfit visibility throughout. The aesthetic should feel authentic and commercial without being overly editorial.
```

**Variables:**
- `{SETTING}`: upscale street, shopping district, modern plaza
- `{TIME_OF_DAY}`: golden hour, soft daylight, overcast natural light
- `{MODEL_ENERGY}`: relaxed, confident, casual-chic

---

## Template 4: Product Detail Close-Up

**ID:** `detail-closeup`
**Best for:** Fabric texture showcases, embellishments, knitwear, tailoring details, premium materials

```
A premium fashion presentation video emphasizing the exact garment's detail, texture, stitching, fabric structure, and craftsmanship. The human model wears the uploaded outfit and performs subtle elegant movements that highlight specific garment elements: sleeve drape, collar structure, button detail, knit texture, or hem behavior. Camera uses close-up and macro-style push-ins with smooth focus pulls. Lighting is precise and revealing: crisp fabric micro-texture visibility, realistic material sheen or matte response, and clean highlight behavior. Movement is slow, deliberate, and fabric-focused.
```

**Variables:**
- `{DETAIL_FOCUS}`: fabric texture, stitching, sleeve, collar, hem, embellishment
- `{LIGHTING}`: macro studio, directional texture light, diffused editorial

---

## Template 5: Festive Seasonal Campaign

**ID:** `festive-campaign`
**Best for:** Holiday collections, Chinese New Year, Spring Festival, Valentine's Day, gifting seasons

```
A polished seasonal fashion campaign video with celebratory but refined atmosphere. A charismatic model wears the exact uploaded outfit with premium seasonal energy. Environmental accents are subtle and tasteful: warm color temperature, soft bokeh elements, or delicate festive atmosphere without visual clutter. The model's performance is joyful, confident, and brand-appropriate. Camera work is smooth and commercial. Color grading uses warm, celebratory tones while maintaining premium fashion aesthetics. The garment remains the clear hero of every frame. Suitable for Chinese New Year, holiday campaigns, or seasonal product launches.
```

**Variables:**
prompts: add all 6 video template prompts (runway, studio, street, detail, festive, outdoor)- `{MOOD}`: joyful, celebratory, warm, romantic, fresh
- `{COLOR_GRADE}`: warm gold, soft red, fresh spring

---

## Template 6: Outdoor Cinematic Fashion

**ID:** `outdoor-cinematic`
**Best for:** Outerwear, activewear, travel collections, resort wear, lifestyle brands

```
An ultra-realistic cinematic fashion video set outdoors in a premium natural or architectural environment. The exact uploaded outfit is worn by a charismatic model who moves naturally in the space: walking, turning, or posing with authentic environmental interaction. Natural light behaves realistically: sun direction, shadow movement, wind interaction with fabric. Camera uses premium tracking, slow dolly, or wide editorial framing with cinematic depth of field. Color grading is filmic and premium without losing garment color accuracy. The environment adds atmosphere without distracting from the outfit. Pacing is cinematic and deliberate.
```

**Variables:**
- `{ENVIRONMENT}`: mountain landscape, coastal setting, urban architecture, forest path, desert
- `{LIGHT_CONDITION}`: golden hour, overcast diffused, bright midday, blue hour
- `{CAMERA_STYLE}`: wide cinematic, tracking follow, locked editorial

---

## Template Usage Guidelines

1. Always combine template prompt with the master system prompt (`prompts/system/master.md`).
2. Inject garment reference description between system prompt and template prompt.
3. Append user's custom additions after the template block.
4. Apply negative prompt from `prompts/negative/default.md` to all generations.
5. Run enhanced versions through the rewrite rules in `prompts/enhancers/rewrite-rules.md` for low-quality user inputs.
