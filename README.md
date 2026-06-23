# 🤖 System Discord Bot | بوت ديسكورد سيستم

بوت ديسكورد كامل بنظام الإدارة، الترحيب، اللوجز، التذاكر، والرتب التفاعلية.

---

## ✨ المميزات | Features

- 🛡️ **Moderation** - طرد، حظر، كتم، تحذيرات
- 📊 **Utility** - معلومات السيرفر والأعضاء
- 👋 **Welcome System** - ترحيب تلقائي + Auto-role
- 📝 **Logging** - مراقبة كل شي
- 🎫 **Tickets** - نظام تذاكر دعم
- 📌 **Reaction Roles** - رتب بالتفاعل
- 🌍 **Bilingual** - عربي + English

---

## 📦 التثبيت | Installation

### 1. Install Python
حمّل Python 3.8+ من [python.org](https://python.org)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. إعداد البوت على Discord Developer Portal

1. روح لـ [Discord Developer Portal](https://discord.com/developers/applications)
2. اعمل **New Application**
3. روح لـ **Bot** → اضغط **Add Bot**
4. انسخ الـ **Token**
5. فعّل الخيارات:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

### 4. إعداد `.env`
```bash
cp .env.example .env
```
عدّل `.env`:
```
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
PREFIX=!
OWNER_ID=YOUR_USER_ID
```

### 5. Invite Bot to Server

روح لـ **OAuth2 → URL Generator**:
- Scopes: `bot`, `applications.commands`
- Bot Permissions:
  - ✅ Kick Members
  - ✅ Ban Members
  - ✅ Moderate Members
  - ✅ Manage Roles
  - ✅ Manage Channels
  - ✅ Manage Messages
  - ✅ Send Messages
  - ✅ Read Messages
  - ✅ View Audit Log

انسخ الرابط وافتحه بالمتصفح.

### 6. تشغيل البوت | Run

```bash
python main.py
```

---

## 📋 الأوامر | Commands

### 🛡️ Moderation
```
!kick @user [reason]
!ban @user [reason]
!unban [user_id]
!mute @user [duration] [reason]    (مثال: 10m, 1h, 1d)
!unmute @user
!warn @user [reason]
!warnings @user
!clear [number]
!lockdown [#channel]
!unlock [#channel]
```

### 📊 Utility
```
!ping
!serverinfo
!userinfo [@user]
!avatar [@user]
!roleinfo @role
!channelinfo [#channel]
```

### 👋 Welcome Setup
```
!setup welcome #channel
!setup leave #channel
!setup autorole @role
```

### 📝 Logs Setup
```
!setup logs #channel
```

### 🎫 Tickets
```
!ticket       (في أي قناة)
!close        (داخل التكت)
```

### 📌 Reaction Roles
```
!rr add [message_id] [emoji] @role
!rr remove [message_id]
!rr list
```

---

## 🗂️ هيكل المشروع | Project Structure

```
discord-bot/
├── main.py                  ← الملف الرئيسي
├── requirements.txt
├── .env.example
├── cogs/
│   ├── moderation.py        ← الإدارة
│   ├── utility.py           ← المعلومات
│   ├── welcome.py           ← الترحيب
│   ├── logging_system.py    ← اللوجز
│   ├── tickets.py           ← التذاكر
│   ├── setup.py             ← الإعداد
│   └── reaction_roles.py    ← الرتب التفاعلية
├── utils/
│   └── language.py          ← نظام اللغات
└── data/                    ← ملفات JSON (تتسوى أوتوماتيك)
```

---

## 🚀 نشر على سيرفر مجاني | Deploy Free

### Railway.app
1. سوي حساب على [Railway](https://railway.app)
2. اربط الـ GitHub repo
3. ضيف Environment Variable: `DISCORD_TOKEN`
4. Deploy

### Replit
1. اعمل Repl جديد (Python)
2. انسخ الملفات
3. شغّل

### Oracle Cloud Free Tier
- سيرفر مجاني 24/7

---

## ❓ مشاكل شائعة | Common Issues

### البوت ما يشتغل؟
- ✅ تأكد إن الـ Token صحيح
- ✅ فعّلت Intents كلها
- ✅ شغّلت `pip install -r requirements.txt`

### البوت ما يرد؟
- ✅ تأكد من الـ Prefix (الافتراضي `!`)
- ✅ البوت عنده صلاحية يقرأ ويكتب بالقناة

### اللوجز ما تشتغل؟
- ✅ تأكد عملت `!setup logs #channel`

---

## 📝 الترخيص | License

Free to use and modify.

---

صنع بـ ❤️ للمجتمع العربي
Made with ❤️ for the Arabic community