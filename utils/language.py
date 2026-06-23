"""
Language System
نظام اللغات - عربي + إنجليزي
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
LANG_FILE = os.path.join(DATA_DIR, "languages.json")


def get_lang(guild_id: int) -> str:
    """جلب لغة السيرفر | Get server language"""
    if not os.path.exists(LANG_FILE):
        return "both"
    try:
        with open(LANG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(str(guild_id), "both")
    except:
        return "both"


def set_lang(guild_id: int, lang: str):
    """تعيين لغة السيرفر | Set server language"""
    data = {}
    if os.path.exists(LANG_FILE):
        try:
            with open(LANG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {}
    data[str(guild_id)] = lang
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LANG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ============ الترجمات ============
TRANSLATIONS = {
    # أخطاء عامة
    "no_permission": {
        "ar": "❌ ما عندك صلاحية هالأمر.",
        "en": "❌ You don't have permission for this command.",
    },
    "bot_no_permission": {
        "ar": "❌ البوت ما عنده صلاحية كافية.",
        "en": "❌ Bot doesn't have sufficient permissions.",
    },
    "user_not_found": {
        "ar": "❌ ما لقيت هذا العضو.",
        "en": "❌ User not found.",
    },
    "command_error": {
        "ar": "❌ صار خطأ بالأمر.",
        "en": "❌ An error occurred.",
    },

    # Moderation
    "user_kicked": {
        "ar": "✅ تم طرد {user} | السبب: {reason}",
        "en": "✅ Kicked {user} | Reason: {reason}",
    },
    "user_banned": {
        "ar": "✅ تم حظر {user} | السبب: {reason}",
        "en": "✅ Banned {user} | Reason: {reason}",
    },
    "user_unbanned": {
        "ar": "✅ تم رفع الحظر عن {user}",
        "en": "✅ Unbanned {user}",
    },
    "user_muted": {
        "ar": "✅ تم كتم {user} لمدة {time}",
        "en": "✅ Muted {user} for {time}",
    },
    "user_unmuted": {
        "ar": "✅ تم فك الكتم عن {user}",
        "en": "✅ Unmuted {user}",
    },
    "messages_cleared": {
        "ar": "✅ تم مسح {amount} رسالة",
        "en": "✅ Cleared {amount} messages",
    },
    "channel_locked": {
        "ar": "🔒 تم قفل القناة {channel}",
        "en": "🔒 Channel locked: {channel}",
    },
    "channel_unlocked": {
        "ar": "🔓 تم فتح القناة {channel}",
        "en": "🔓 Channel unlocked: {channel}",
    },
}


def translate(key: str, lang: str = "both", **kwargs) -> str:
    """ترجمة مفتاح | Translate a key"""
    if key not in TRANSLATIONS:
        return key

    translations = TRANSLATIONS[key]
    result = []

    if lang in ["ar", "both"] and "ar" in translations:
        result.append(translations["ar"].format(**kwargs))
    if lang in ["en", "both"] and "en" in translations:
        result.append(translations["en"].format(**kwargs))

    return "\n".join(result) if len(result) > 1 else (result[0] if result else key)