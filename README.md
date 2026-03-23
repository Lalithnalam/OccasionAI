# ✨ OccasionAI — AI-Powered Greeting & Invitation Platform

> Never miss a moment — generate personalized AI greeting cards and send or schedule them at midnight, automatically.

🔗 **Live Demo:** [occasionai-pvmftopj6jry3xhzhs9pvq.streamlit.app](https://occasionai-pvmftopj6jry3xhzhs9pvq.streamlit.app)

---

## 📌 What is OccasionAI?

OccasionAI is a full-stack AI web application that generates personalized greeting cards and invitations using Google Gemini AI.
Users can instantly send or schedule emails to be delivered automatically at midnight on any special occasion — birthdays, anniversaries, festivals, weddings, and more.

---

## 🚀 Live Demo

👉 [https://occasionai-pvmftopj6jry3xhzhs9pvq.streamlit.app](https://occasionai-pvmftopj6jry3xhzhs9pvq.streamlit.app)

---

## ✦ Features

- **AI Greeting Cards** — Generates 3 unique card variations (emotional, playful, elegant) using Gemini AI based on the person, occasion, and relationship
- **Beautiful Email Design** — Cards are delivered as stunning HTML emails with a physical greeting card aesthetic
- **Midnight Scheduler** — Schedule emails to auto-send at exactly 12:00 AM on the chosen date using Python threading
- **Live Card Preview** — Preview exactly how the card looks in the inbox before sending
- **Send Instantly** — Option to send the card immediately via Gmail SMTP
- **WhatsApp Reminder** — One-click WhatsApp message pre-filled with the card content
- **Bulk Invitations** — Upload an Excel file and send personalized cards to multiple people at once
- **Invitation Sender** — Create elegant event invitations and send to all guests simultaneously
- **Birthday Calendar** — Visual calendar showing all upcoming scheduled occasions
- **Cancel Scheduled Mails** — Delete any pending scheduled greeting before it sends

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI Engine | Google Gemini 2.5 Flash |
| Email Delivery | Gmail SMTP |
| Scheduling | Python Threading |
| Database | SQLite |
| Data Processing | Pandas, OpenPyXL |
| Deployment | Streamlit Cloud |
| Language | Python 3.14 |

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- A Gmail account with App Password enabled
- A Gemini API key (free at [aistudio.google.com](https://aistudio.google.com/app/apikey))

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Lalithnalam/OccasionAI.git
cd OccasionAI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your .env file
echo GEMINI_API_KEY=your_key_here > .env

# 4. Run the app
python -m streamlit run app.py
```

---

## 📖 Usage

1. **Greetings Tab** — Enter the person's name, email, occasion, and relationship → Click Generate → Pick a card → Send Now or Schedule at Midnight
2. **Invitations Tab** — Fill event details and guest emails → Generate invitation → Send to all guests at once
3. **Bulk Send Tab** — Upload an Excel file with columns: `name`, `email`, `occasion`, `relationship` → AI generates and sends personalized cards to everyone
4. **Scheduled Tab** — View all pending scheduled emails, with option to cancel any
5. **Calendar Tab** — See all upcoming occasions in a month-wise calendar view

### Gmail App Password Setup
1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Go to App Passwords → Create one for OccasionAI
4. Use this 16-digit password in the app

---

## 📁 Project Structure

```
OccasionAI/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── occasions.db         # SQLite database (auto-created)
├── .env                 # API keys (not pushed to GitHub)
├── .gitignore           # Protects sensitive files
├── .streamlit/
│   ├── config.toml      # Theme configuration
│   └── secrets.toml     # Streamlit Cloud secrets (not pushed)
└── README.md            # This file
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Nalam Naga Venkata Sai Sri Lalith**

- 🎓 B.Tech CSE — SRM AP University (CGPA: 9.52)
- 💼 LinkedIn: [linkedin.com/in/lalithnalam](https://linkedin.com/in/lalithnalam)
- 🐙 GitHub: [github.com/Lalithnalam](https://github.com/Lalithnalam)
- 📧 Email: nalamlalith@gmail.com

---

