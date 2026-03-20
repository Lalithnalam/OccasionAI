import streamlit as st
from google import genai
import smtplib
import sqlite3
import os
import threading
import time
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, date
from dotenv import load_dotenv

# ── Load API Key ──────────────────────────────────────────────────────────────
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="OccasionAI", page_icon="✨", layout="wide")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,500&family=DM+Sans:wght@300;400;500;600&display=swap');
:root {
    --bg: #080810; --surface: #0f0f1a; --card: #13131e; --card2: #1a1a28;
    --border: #252535; --accent: #c084fc; --accent2: #f472b6;
    --green: #34d399; --text: #eeeef5; --muted: #7070a0;
}
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; background-color: var(--bg) !important; color: var(--text) !important; }
.stApp { background-color: var(--bg) !important; }
.stApp > header { background: transparent !important; }
.hero { text-align: center; padding: 3rem 0 2rem; position: relative; }
.hero::before { content: ''; position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 700px; height: 350px; background: radial-gradient(ellipse, rgba(192,132,252,0.07) 0%, transparent 70%); pointer-events: none; }
.hero-badge { display: inline-block; background: rgba(192,132,252,0.1); border: 1px solid rgba(192,132,252,0.25); color: var(--accent); font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase; padding: 0.3rem 1rem; border-radius: 999px; margin-bottom: 1.2rem; }
.hero h1 { font-family: 'Playfair Display', serif !important; font-size: 4rem; font-weight: 700; background: linear-gradient(135deg, #e0aaff 0%, #c084fc 40%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 0.6rem 0; line-height: 1.1; }
.hero p { color: var(--muted); font-size: 1.05rem; font-weight: 300; margin: 0; }
.stTabs [data-baseweb="tab-list"] { background: var(--card) !important; border-radius: 14px !important; padding: 0.4rem !important; border: 1px solid var(--border) !important; gap: 0.2rem !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; border-radius: 10px !important; color: var(--muted) !important; font-weight: 500 !important; padding: 0.5rem 1.2rem !important; font-size: 0.9rem !important; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, rgba(192,132,252,0.18), rgba(244,114,182,0.12)) !important; color: var(--text) !important; border: 1px solid rgba(192,132,252,0.25) !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem !important; }
div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea { background: var(--card2) !important; border: 1px solid var(--border) !important; color: var(--text) !important; border-radius: 12px !important; }
div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(192,132,252,0.1) !important; }
div[data-testid="stFileUploader"] { background: var(--card2) !important; border: 2px dashed var(--border) !important; border-radius: 14px !important; }
.stButton > button { background: linear-gradient(135deg, #c084fc, #f472b6) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.65rem 1.5rem !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; width: 100% !important; transition: all 0.25s ease !important; }
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 10px 30px rgba(192,132,252,0.35) !important; }
.glass-card { background: var(--card); border: 1px solid var(--border); border-radius: 20px; padding: 1.8rem; margin-bottom: 1.2rem; position: relative; overflow: hidden; }
.glass-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(192,132,252,0.3), transparent); }
.section-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.15em; color: var(--muted); margin-bottom: 0.5rem; font-weight: 600; }
.success-box { background: rgba(52,211,153,0.08); border: 1px solid rgba(52,211,153,0.25); border-radius: 12px; padding: 0.9rem 1.2rem; color: #34d399; font-size: 0.92rem; margin-top: 0.5rem; }
.info-box { background: rgba(192,132,252,0.08); border: 1px solid rgba(192,132,252,0.2); border-radius: 12px; padding: 0.9rem 1.2rem; color: var(--accent); font-size: 0.9rem; }
.pill { display: inline-block; padding: 0.25rem 0.8rem; border-radius: 999px; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
.pill-pending { background: rgba(192,132,252,0.15); color: #c084fc; border: 1px solid rgba(192,132,252,0.3); }
.pill-sent { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.pill-failed { background: rgba(244,63,94,0.15); color: #f43f5e; border: 1px solid rgba(244,63,94,0.3); }
.wa-btn { display: inline-block; background: #25D366; color: white !important; padding: 0.5rem 1.2rem; border-radius: 10px; font-size: 0.85rem; font-weight: 600; text-decoration: none !important; }
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Database ───────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("occasions.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scheduled_mails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipient_name TEXT, recipient_email TEXT, recipient_phone TEXT,
        occasion TEXT, send_date TEXT, subject TEXT, body TEXT,
        sender_email TEXT, sender_password TEXT, status TEXT DEFAULT 'pending'
    )''')
    for col in ["sender_email TEXT", "sender_password TEXT", "recipient_phone TEXT"]:
        try:
            c.execute(f"ALTER TABLE scheduled_mails ADD COLUMN {col}")
        except:
            pass
    conn.commit()
    conn.close()

init_db()

# ── Email HTML ─────────────────────────────────────────────────────────────────
def build_email_html(subject, body):
    return f"""
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Sacramento&display=swap" rel="stylesheet">
</head>
<body style="margin:0;padding:30px 20px;background:#f5f0eb;">
  <div style="max-width:520px;margin:0 auto;">
    <div style="background:#fffdf9;border-radius:6px;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,0.13);">
      <div style="height:5px;background:linear-gradient(90deg,#c084fc,#f472b6,#fb923c);"></div>
      <div style="padding:3.5rem 3rem 2.5rem;">
        <div style="text-align:center;margin-bottom:2.5rem;">
          <div style="display:inline-flex;align-items:center;gap:12px;">
            <div style="width:35px;height:1px;background:#d4b8a0;"></div>
            <span style="color:#c9a882;font-size:0.65rem;letter-spacing:0.3em;text-transform:uppercase;font-family:'Cormorant Garamond',serif;">OccasionAI</span>
            <div style="width:35px;height:1px;background:#d4b8a0;"></div>
          </div>
        </div>
        <h1 style="font-family:'Sacramento',cursive;font-size:3rem;color:#2d1b4e;text-align:center;margin:0 0 2rem 0;font-weight:400;line-height:1.2;">{subject}</h1>
        <div style="text-align:center;margin-bottom:2rem;color:#ddc9b8;font-size:1rem;letter-spacing:0.3em;">✦ ✦ ✦</div>
        <div style="font-size:5rem;color:#f0e4f7;line-height:0.6;font-family:'Cormorant Garamond',serif;margin-bottom:0.8rem;">"</div>
        <p style="font-family:'Cormorant Garamond',serif;font-size:1.18rem;line-height:2;color:#3d2c1e;margin:0;text-align:center;font-style:italic;">{body.replace(chr(10), '<br>')}</p>
        <div style="font-size:5rem;color:#f0e4f7;line-height:0.6;font-family:'Cormorant Garamond',serif;text-align:right;margin-top:0.8rem;">"</div>
        <div style="text-align:center;margin:2.5rem 0 0;color:#ddc9b8;font-size:1rem;letter-spacing:0.3em;">✦ ✦ ✦</div>
      </div>
      <div style="background:linear-gradient(135deg,#fdf8f3,#fdf4f8);padding:1.2rem 2rem;text-align:center;border-top:1px solid #eeddd0;">
        <p style="margin:0;font-family:'Cormorant Garamond',serif;color:#c4a898;font-size:0.78rem;letter-spacing:0.18em;text-transform:uppercase;">
          Crafted with care &nbsp;·&nbsp; <span style="color:#c084fc;font-weight:600;">OccasionAI</span>
        </p>
      </div>
    </div>
  </div>
</body>
</html>"""

# ── Send Email ─────────────────────────────────────────────────────────────────
def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg.attach(MIMEText(build_email_html(subject, body), "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True
    except Exception as e:
        return str(e)

# ── DB Ops ─────────────────────────────────────────────────────────────────────
def schedule_mail(name, email, phone, occasion, send_date, subject, body, sender_email, sender_password):
    conn = sqlite3.connect("occasions.db")
    c = conn.cursor()
    c.execute("""INSERT INTO scheduled_mails
              (recipient_name,recipient_email,recipient_phone,occasion,send_date,subject,body,sender_email,sender_password)
              VALUES (?,?,?,?,?,?,?,?,?)""",
              (name, email, phone, occasion, f"{send_date} 00:00:00", subject, body, sender_email, sender_password))
    conn.commit()
    conn.close()

def delete_mail(mail_id):
    conn = sqlite3.connect("occasions.db")
    c = conn.cursor()
    c.execute("DELETE FROM scheduled_mails WHERE id=?", (mail_id,))
    conn.commit()
    conn.close()

def get_all_scheduled():
    conn = sqlite3.connect("occasions.db")
    c = conn.cursor()
    c.execute("SELECT id,recipient_name,recipient_email,recipient_phone,occasion,send_date,subject,status FROM scheduled_mails ORDER BY send_date")
    rows = c.fetchall()
    conn.close()
    return rows

# ── Midnight Scheduler ─────────────────────────────────────────────────────────
def run_scheduler():
    while True:
        now = datetime.now()
        if now.hour == 0 and now.minute == 0:
            try:
                conn = sqlite3.connect("occasions.db")
                c = conn.cursor()
                today = now.strftime("%Y-%m-%d")
                c.execute("""SELECT id,recipient_email,subject,body,sender_email,sender_password
                           FROM scheduled_mails WHERE send_date LIKE ? AND status='pending'""", (f"{today}%",))
                for row in c.fetchall():
                    id_, to_email, subj, body, s_email, s_pass = row
                    result = send_email(s_email, s_pass, to_email, subj, body)
                    c.execute("UPDATE scheduled_mails SET status=? WHERE id=?",
                              ("sent" if result is True else "failed", id_))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Scheduler error: {e}")
        time.sleep(60)

if "scheduler_started" not in st.session_state:
    threading.Thread(target=run_scheduler, daemon=True).start()
    st.session_state["scheduler_started"] = True

# ── Gemini ─────────────────────────────────────────────────────────────────────
def generate_cards(name, occasion, relationship, extra=""):
    prompt = f"""Generate 3 greeting card messages for:
- Name: {name}, Occasion: {occasion}, Relationship: {relationship}, Extra: {extra or 'None'}
Rules:
- Use 1-2 classy tasteful emojis per card only from: 🌸 ✨ 🥂 💫 🌟 🎂 💐 🕊️ 🌙 🍀 🌺
- Card 1: Deeply emotional and heartfelt
- Card 2: Fun, warm and playful  
- Card 3: Short, poetic and elegant
Format EXACTLY (no extra text):
CARD1_TITLE: [title]
CARD1_BODY: [message]
CARD2_TITLE: [title]
CARD2_BODY: [message]
CARD3_TITLE: [title]
CARD3_BODY: [message]"""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return parse_cards(response.text)

def parse_cards(text):
    cards = []
    for i in range(1, 4):
        try:
            title = text.split(f"CARD{i}_TITLE:")[1].split("\n")[0].strip()
            body = text.split(f"CARD{i}_BODY:")[1].split(f"CARD{i+1}_TITLE:")[0].strip() if i < 3 else text.split(f"CARD{i}_BODY:")[1].strip()
            cards.append({"title": title, "body": body})
        except:
            cards.append({"title": f"Card {i}", "body": "Could not generate."})
    return cards

def generate_invitation(occasion, host_name, date_str, venue, extra=""):
    prompt = f"""Write a beautiful elegant invitation for:
- Occasion: {occasion}, Host: {host_name}, Date: {date_str}, Venue: {venue}, Extra: {extra or 'None'}
One warm heartfelt invitation. Start directly, no preamble."""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text.strip()

def generate_bulk_card(name, occasion, relationship):
    prompt = f"""Write one short elegant greeting for {name} on {occasion}. Relationship: {relationship}.
Use 1 classy emoji from 🌸✨💫🌟💐. Keep under 3 sentences. Start directly."""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text.strip()

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI-Powered Occasions</div>
    <h1>OccasionAI</h1>
    <p>Never miss a moment — beautiful greetings & invitations, delivered at midnight ✨</p>
</div>
<hr>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💌 Greetings", "🎊 Invitations", "📦 Bulk Send", "📅 Scheduled", "🗓️ Calendar"
])

# ══════════════════════════════════════════════════════════
# TAB 1 — GREETINGS
# ══════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💌 Send a Greeting")
    st.markdown("<p style='color:var(--muted);margin-top:-0.5rem;'>Fill details → AI generates 3 cards → Preview → Send now or Schedule at midnight 🌙</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<p class="section-label">Person\'s Name</p>', unsafe_allow_html=True)
        g_name = st.text_input("", placeholder="e.g. Hemanth", key="g_name", label_visibility="collapsed")
        st.markdown('<p class="section-label">Their Email</p>', unsafe_allow_html=True)
        g_email = st.text_input("", placeholder="hemanth@gmail.com", key="g_email", label_visibility="collapsed")
        st.markdown('<p class="section-label">Their WhatsApp Number (Optional)</p>', unsafe_allow_html=True)
        g_phone = st.text_input("", placeholder="+91 9876543210", key="g_phone", label_visibility="collapsed")
        st.markdown('<p class="section-label">Occasion</p>', unsafe_allow_html=True)
        g_occasion = st.selectbox("", ["Birthday 🎂", "Anniversary 💍", "Congratulations 🏆",
                                        "Festival 🪔", "Get Well Soon 🌸", "Thank You 🙏",
                                        "Farewell 🕊️", "Wedding 💐", "Other ✨"],
                                   key="g_occ", label_visibility="collapsed")
    with col2:
        st.markdown('<p class="section-label">Your Relationship</p>', unsafe_allow_html=True)
        g_rel = st.selectbox("", ["Best Friend", "Close Friend", "Family", "Colleague",
                           "Partner 💑", "Crush 😄", "Boss/Senior", "Mentor", "Classmate"],
                              key="g_rel", label_visibility="collapsed")
        st.markdown('<p class="section-label">Schedule Date</p>', unsafe_allow_html=True)
        g_date = st.date_input("", min_value=date.today(), key="g_date", label_visibility="collapsed")
        st.markdown('<p class="section-label">Your Gmail</p>', unsafe_allow_html=True)
        g_sender = st.text_input("", placeholder="yourmail@gmail.com", key="g_sender", label_visibility="collapsed")
        st.markdown('<p class="section-label">Gmail App Password</p>', unsafe_allow_html=True)
        g_pass = st.text_input("", type="password", placeholder="16-digit app password",
                                key="g_pass", label_visibility="collapsed",
                                help="Google Account → Security → App Passwords")
        st.markdown('<p class="section-label">Extra Info (Optional)</p>', unsafe_allow_html=True)
        g_extra = st.text_input("", placeholder="e.g. loves cricket, turning 21",
                                 key="g_extra", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✨ Generate 3 Cards", key="gen_greeting"):
        if not g_name or not g_email:
            st.error("Please fill in Name and Email!")
        else:
            with st.spinner("✨ Crafting your personalized cards..."):
                cards = generate_cards(g_name, g_occasion, g_rel, g_extra)
                st.session_state["cards"] = cards
                st.session_state["g_info"] = {
                    "name": g_name, "email": g_email, "phone": g_phone,
                    "occasion": g_occasion, "date": str(g_date),
                    "sender": g_sender, "password": g_pass
                }

    if "cards" in st.session_state:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Pick your favourite card:")

        for i, card in enumerate(st.session_state["cards"]):
            with st.expander(f"✦ Card {i+1} — {card['title']}", expanded=(i == 0)):

                # Preview
                st.markdown("**📬 How it looks in inbox:**")
                st.markdown(f"""
                <div style="background:#f5f0eb;border-radius:12px;padding:1.5rem;margin:0.5rem 0 1rem;">
                  <div style="background:#fffdf9;border-radius:6px;overflow:hidden;
                              box-shadow:0 4px 20px rgba(0,0,0,0.1);max-width:460px;margin:auto;">
                    <div style="height:4px;background:linear-gradient(90deg,#c084fc,#f472b6,#fb923c);"></div>
                    <div style="padding:2rem 2rem 1.5rem;">
                      <div style="text-align:center;margin-bottom:1rem;">
                        <span style="color:#c9a882;font-size:0.6rem;letter-spacing:0.25em;text-transform:uppercase;">OccasionAI</span>
                      </div>
                      <h3 style="font-family:Georgia,serif;color:#2d1b4e;text-align:center;
                                 margin:0 0 0.8rem;font-size:1.5rem;font-style:italic;">{card['title']}</h3>
                      <div style="text-align:center;color:#ddc9b8;margin-bottom:1rem;font-size:0.9rem;letter-spacing:0.2em;">✦ ✦ ✦</div>
                      <p style="color:#3d2c1e;font-size:0.95rem;line-height:1.85;
                                text-align:center;font-style:italic;margin:0;
                                font-family:Georgia,serif;">
                        {card['body'].replace(chr(10), '<br>')}
                      </p>
                      <div style="text-align:center;color:#ddc9b8;margin-top:1rem;font-size:0.9rem;letter-spacing:0.2em;">✦ ✦ ✦</div>
                    </div>
                    <div style="background:#fdf8f3;padding:0.8rem;text-align:center;border-top:1px solid #eeddd0;">
                      <span style="color:#c4a898;font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;">
                        Crafted with care · OccasionAI
                      </span>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                info = st.session_state.get("g_info", {})
                b1, b2, b3 = st.columns(3)

                with b1:
                    if st.button("📨 Send Now", key=f"send_{i}"):
                        if not info.get("sender") or not info.get("password"):
                            st.error("Enter Gmail & App Password!")
                        else:
                            result = send_email(info["sender"], info["password"],
                                                info["email"], card["title"], card["body"])
                            if result is True:
                                st.markdown('<div class="success-box">✅ Sent successfully!</div>', unsafe_allow_html=True)
                            else:
                                st.error(f"❌ {result}")

                with b2:
                    if st.button("🌙 Schedule Midnight", key=f"sched_{i}"):
                        if not info.get("sender") or not info.get("password"):
                            st.error("Enter Gmail & App Password!")
                        else:
                            schedule_mail(info["name"], info["email"], info.get("phone",""),
                                          info["occasion"], info["date"],
                                          card["title"], card["body"],
                                          info["sender"], info["password"])
                            st.markdown(f'<div class="success-box">🌙 Scheduled! Sends at midnight on {info["date"]}</div>',
                                        unsafe_allow_html=True)

                with b3:
                    if info.get("phone"):
                        phone_clean = info["phone"].replace(" ","").replace("+","")
                        wa_msg = f"Hey {info['name']}! {card['body'][:100]}..."
                        wa_url = f"https://wa.me/{phone_clean}?text={wa_msg}"
                        st.markdown(f'<br><a href="{wa_url}" target="_blank" class="wa-btn">💬 WhatsApp</a>',
                                    unsafe_allow_html=True)
                    else:
                        st.caption("Add phone for WhatsApp")

# ══════════════════════════════════════════════════════════
# TAB 2 — INVITATIONS
# ══════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎊 Send Invitations")
    st.markdown("<p style='color:var(--muted);margin-top:-0.5rem;'>Create a beautiful invitation and send to multiple guests at once!</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<p class="section-label">Occasion Name</p>', unsafe_allow_html=True)
        i_occasion = st.text_input("", placeholder="e.g. My Sister's Wedding", key="i_occ", label_visibility="collapsed")
        st.markdown('<p class="section-label">Hosted By</p>', unsafe_allow_html=True)
        i_host = st.text_input("", placeholder="e.g. Lalith & Family", key="i_host", label_visibility="collapsed")
        st.markdown('<p class="section-label">Event Date</p>', unsafe_allow_html=True)
        i_date = st.date_input("", min_value=date.today(), key="i_date", label_visibility="collapsed")
    with col2:
        st.markdown('<p class="section-label">Venue</p>', unsafe_allow_html=True)
        i_venue = st.text_input("", placeholder="e.g. Vysya Kalyana Mandapam, Guntur", key="i_venue", label_visibility="collapsed")
        st.markdown('<p class="section-label">Guest Emails (one per line)</p>', unsafe_allow_html=True)
        i_emails_raw = st.text_area("", placeholder="friend1@gmail.com\nfriend2@gmail.com",
                                     height=100, key="i_emails_raw", label_visibility="collapsed")
        st.markdown('<p class="section-label">Extra Details (Optional)</p>', unsafe_allow_html=True)
        i_extra = st.text_input("", placeholder="e.g. Dress code: Traditional", key="i_extra", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-label">Your Gmail</p>', unsafe_allow_html=True)
        inv_sender = st.text_input("", placeholder="yourmail@gmail.com", key="inv_sender", label_visibility="collapsed")
    with col2:
        st.markdown('<p class="section-label">App Password</p>', unsafe_allow_html=True)
        inv_pass = st.text_input("", type="password", placeholder="16-digit app password", key="inv_pass", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✨ Generate Invitation", key="gen_inv"):
        if not i_occasion or not i_host or not i_venue:
            st.error("Fill Occasion, Host and Venue!")
        else:
            with st.spinner("✨ Crafting your invitation..."):
                invitation = generate_invitation(i_occasion, i_host, str(i_date), i_venue, i_extra)
                st.session_state["invitation"] = invitation
                st.session_state["i_emails_list"] = [e.strip() for e in i_emails_raw.split("\n") if e.strip()]
                st.session_state["i_occasion"] = i_occasion

    if "invitation" in st.session_state:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("**📬 Preview:**")
        st.markdown(f"""
        <div style="background:#f5f0eb;border-radius:12px;padding:1.5rem;margin:0.5rem 0 1rem;">
          <div style="background:#fffdf9;border-radius:6px;overflow:hidden;
                      box-shadow:0 4px 20px rgba(0,0,0,0.1);max-width:460px;margin:auto;">
            <div style="height:4px;background:linear-gradient(90deg,#c084fc,#f472b6,#fb923c);"></div>
            <div style="padding:2rem;">
              <h3 style="font-family:Georgia,serif;color:#2d1b4e;text-align:center;font-style:italic;margin:0 0 1rem;">
                You're Invited ✦
              </h3>
              <div style="text-align:center;color:#ddc9b8;margin-bottom:1rem;letter-spacing:0.2em;">✦ ✦ ✦</div>
              <p style="color:#3d2c1e;font-size:0.95rem;line-height:1.85;text-align:center;font-style:italic;font-family:Georgia,serif;margin:0;">
                {st.session_state['invitation'].replace(chr(10), '<br>')}
              </p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        emails_list = st.session_state.get("i_emails_list", [])
        st.markdown(f'<div class="info-box">📧 Will be sent to {len(emails_list)} guest(s)</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📨 Send to All Guests", key="send_inv"):
            if not inv_sender or not inv_pass:
                st.error("Enter Gmail & App Password!")
            elif not emails_list:
                st.error("Add at least one guest email!")
            else:
                success, failed = 0, 0
                prog = st.progress(0)
                for idx, email in enumerate(emails_list):
                    result = send_email(inv_sender, inv_pass, email,
                                        f"You're Invited: {st.session_state['i_occasion']}",
                                        st.session_state["invitation"])
                    if result is True: success += 1
                    else: failed += 1
                    prog.progress((idx + 1) / len(emails_list))
                st.markdown(f'<div class="success-box">✅ Sent to {success} guests!{f" ❌ {failed} failed." if failed else ""}</div>',
                            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# TAB 3 — BULK SEND
# ══════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📦 Bulk Greetings via Excel")
    st.markdown("<p style='color:var(--muted);margin-top:-0.5rem;'>Upload Excel → AI generates personal card for each person → Sends all at once!</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    📋 <strong>Excel columns required:</strong>
    &nbsp;<code>name</code> &nbsp;|&nbsp; <code>email</code> &nbsp;|&nbsp; <code>occasion</code> &nbsp;|&nbsp; <code>relationship</code>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    bulk_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-label">Your Gmail</p>', unsafe_allow_html=True)
        bulk_sender = st.text_input("", placeholder="yourmail@gmail.com", key="bulk_sender", label_visibility="collapsed")
    with col2:
        st.markdown('<p class="section-label">App Password</p>', unsafe_allow_html=True)
        bulk_pass = st.text_input("", type="password", placeholder="16-digit app password", key="bulk_pass", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    if bulk_file:
        df = pd.read_excel(bulk_file)
        st.markdown(f'<div class="info-box">✅ Found {len(df)} people in your file</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df.head(5), use_container_width=True)

        if st.button("🚀 Generate & Send All", key="bulk_send"):
            if not bulk_sender or not bulk_pass:
                st.error("Enter Gmail & App Password!")
            else:
                success, failed = 0, 0
                prog = st.progress(0)
                status_text = st.empty()
                for idx, row in df.iterrows():
                    try:
                        name = str(row.get("name", "Friend"))
                        email = str(row.get("email", ""))
                        occasion = str(row.get("occasion", "Special Day"))
                        relationship = str(row.get("relationship", "Friend"))
                        if not email: continue
                        status_text.markdown(f"✨ Generating card for **{name}**...")
                        body = generate_bulk_card(name, occasion, relationship)
                        result = send_email(bulk_sender, bulk_pass, email,
                                            f"A Special Message for You, {name} ✨", body)
                        if result is True: success += 1
                        else: failed += 1
                    except:
                        failed += 1
                    prog.progress((idx + 1) / len(df))
                status_text.empty()
                st.markdown(f'<div class="success-box">✅ Done! Sent to {success} people.{f" ❌ {failed} failed." if failed else ""}</div>',
                            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# TAB 4 — SCHEDULED
# ══════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 📅 Scheduled Greetings")
    st.markdown("<p style='color:var(--muted);margin-top:-0.5rem;'>All emails scheduled to auto-send at midnight 🌙</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    rows = get_all_scheduled()
    if rows:
        for row in rows:
            id_, name, email, phone, occasion, send_date, subject, status = row
            col1, col2 = st.columns([6, 1])
            with col1:
                pill_class = f"pill-{status}"
                st.markdown(f"""
                <div class="glass-card" style="margin-bottom:0.8rem;">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem;">
                    <div>
                      <strong style="font-size:1.05rem;">{name}</strong>
                      <span class="pill {pill_class}" style="margin-left:0.8rem;">{status}</span>
                    </div>
                  </div>
                  <div style="color:var(--muted);font-size:0.85rem;margin-top:0.3rem;">📧 {email}{f' · 📱 {phone}' if phone else ''}</div>
                  <div style="color:var(--muted);font-size:0.85rem;margin-top:0.4rem;">
                    🌙 Midnight on <strong style="color:var(--text);">{send_date[:10]}</strong>
                    &nbsp;·&nbsp; {occasion} &nbsp;·&nbsp; ✉️ {subject}
                  </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if status == "pending":
                    if st.button("🗑️", key=f"del_{id_}", help="Cancel this scheduled mail"):
                        delete_mail(id_)
                        st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:var(--muted);">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">🌙</div>
            No scheduled greetings yet.<br>Go to Greetings tab to schedule one!
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# TAB 5 — CALENDAR
# ══════════════════════════════════════════════════════════
with tab5:
    st.markdown("### 🗓️ Occasion Calendar")
    st.markdown("<p style='color:var(--muted);margin-top:-0.5rem;'>All your upcoming occasions at a glance</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    rows = get_all_scheduled()
    if rows:
        from collections import defaultdict
        months = defaultdict(list)
        for row in rows:
            id_, name, email, phone, occasion, send_date, subject, status = row
            try:
                dt = datetime.strptime(send_date[:10], "%Y-%m-%d")
                months[dt.strftime("%B %Y")].append({
                    "name": name, "occasion": occasion,
                    "date": dt.strftime("%d %b"), "day": dt.strftime("%a"),
                    "status": status
                })
            except:
                pass

        for month, events in sorted(months.items()):
            st.markdown(f"<p style='color:var(--accent);font-weight:600;font-size:0.8rem;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.8rem;'>📅 {month}</p>", unsafe_allow_html=True)
            for ev in events:
                pill = "pill-sent" if ev["status"] == "sent" else "pill-pending"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:1rem;
                            background:var(--card);border:1px solid var(--border);
                            border-radius:14px;padding:0.9rem 1.2rem;margin-bottom:0.5rem;">
                  <div style="min-width:52px;height:52px;border-radius:12px;
                              background:linear-gradient(135deg,rgba(192,132,252,0.15),rgba(244,114,182,0.15));
                              display:flex;flex-direction:column;align-items:center;
                              justify-content:center;border:1px solid rgba(192,132,252,0.2);">
                    <span style="font-size:0.6rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.05em;">{ev['day']}</span>
                    <span style="font-size:1rem;font-weight:700;color:var(--accent);">{ev['date'][:2]}</span>
                    <span style="font-size:0.6rem;color:var(--muted);">{ev['date'][3:]}</span>
                  </div>
                  <div style="flex:1;">
                    <strong style="font-size:1rem;">{ev['name']}</strong>
                    <span style="color:var(--muted);font-size:0.85rem;margin-left:0.5rem;">{ev['occasion']}</span>
                  </div>
                  <span class="pill {pill}">{ev['status']}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:var(--muted);">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">🗓️</div>
            No occasions yet.<br>Schedule greetings to see them here!
        </div>
        """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<br><br>
<div style="text-align:center;color:#2a2a44;font-size:0.75rem;letter-spacing:0.1em;">
    ✦ &nbsp; OccasionAI — Gemini AI · Streamlit · Gmail SMTP &nbsp; ✦
</div>
""", unsafe_allow_html=True)
