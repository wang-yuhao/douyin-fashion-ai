import random

ENHANCEMENT_RULES = {
    "runway_walk": {
        "prefix_en": "Ultra-realistic 9:16 vertical fashion video. ",
        "suffix_en": " T-stage runway, dramatic directional lighting, slow-motion fabric movement, photorealistic skin texture, editorial color grade, Douyin-ready.",
        "prefix_zh": "超写实9:16竖屏时尚大片。",
        "suffix_zh": "T台走秀场景，戏剧性定向灯光，慢动作面料飘动，皮肤质感逼真，杂志级色调，抖音竖屏标准。",
    },
    "studio_luxury": {
        "prefix_en": "Premium studio fashion video, 9:16 vertical. ",
        "suffix_en": " Clean white cyclorama backdrop, three-point studio lighting, full-body outfit reveal, luxury brand aesthetic, sharp garment detail.",
        "prefix_zh": "高端棚拍时尚视频，9:16竖屏。",
        "suffix_zh": "纯白弧形背景，三点棚拍灯光，全身服装展示，奢侈品牌美学，服装细节清晰锐利。",
    },
    "street_style": {
        "prefix_en": "Urban street style fashion video, 9:16. ",
        "suffix_en": " Bustling city background, natural daylight, candid movement, contemporary lifestyle mood, social-media optimized.",
        "prefix_zh": "都市街头风格时尚视频，9:16竖屏。",
        "suffix_zh": "繁华城市背景，自然日光，随性自然动作，现代生活方式氛围，社交媒体优化。",
    },
    "detail_closeup": {
        "prefix_en": "Macro detail fashion video, 9:16 vertical. ",
        "suffix_en": " Extreme close-up on fabric weave, stitching quality, button detail and texture. Soft diffused lighting, product photography standard.",
        "prefix_zh": "服装细节特写视频，9:16竖屏。",
        "suffix_zh": "面料纹理极致特写，缝制工艺，纽扣细节与质感。柔和散射灯光，产品摄影标准。",
    },
    "festive_campaign": {
        "prefix_en": "Festive fashion campaign video, 9:16 vertical. ",
        "suffix_en": " Vibrant seasonal backdrop, warm celebratory lighting, dynamic movement, campaign-grade production value.",
        "prefix_zh": "节庆时尚营销视频，9:16竖屏。",
        "suffix_zh": "鲜艳节日背景，温暖庆典灯光，动感十足，广告级制作水准。",
    },
    "outdoor_cinematic": {
        "prefix_en": "Cinematic outdoor fashion video, 9:16 vertical. ",
        "suffix_en": " Golden hour natural light, shallow depth of field, cinematic LUT color grade, natural wind movement, editorial quality.",
        "prefix_zh": "户外电影感时尚视频，9:16竖屏。",
        "suffix_zh": "黄金时段自然光，浅景深虚化，电影级LUT色调，自然风吹动效果，杂志大片品质。",
    },
}

PERSONA_ADDITIONS = {
    "east_asian": {"en": "East Asian female model, natural makeup, ", "zh": "东亚女模特，自然妆容，"},
    "international": {"en": "International diverse model, confident posture, ", "zh": "国际多元化模特，自信姿态，"},
    "luxury_editorial": {"en": "High-fashion editorial model, haute couture expression, ", "zh": "高级时装杂志模特，高定表情，"},
    "casual_commercial": {"en": "Approachable commercial model, friendly expression, ", "zh": "亲和力商业模特，友好自然表情，"},
}


def detect_language(text: str) -> str:
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    return "zh-CN" if chinese_chars > len(text) * 0.2 else "en"


def enhance_prompt(prompt: str, template: str, persona: str, language: str) -> dict:
    rules = ENHANCEMENT_RULES.get(template, ENHANCEMENT_RULES["studio_luxury"])
    persona_add = PERSONA_ADDITIONS.get(persona, PERSONA_ADDITIONS["east_asian"])
    detected_lang = detect_language(prompt) if language == "auto" else language

    if detected_lang == "zh-CN":
        enhanced = rules["prefix_zh"] + persona_add["zh"] + (prompt or "展示服装") + rules["suffix_zh"]
    else:
        enhanced = rules["prefix_en"] + persona_add["en"] + (prompt or "showcase the outfit") + rules["suffix_en"]

    # Simulate token count
    tokens_used = random.randint(180, 380)

    return {
        "original": prompt,
        "enhanced": enhanced,
        "tokens_used": tokens_used,
        "language_detected": detected_lang,
    }
