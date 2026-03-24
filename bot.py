import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- Render Port Error Fix (Flask Setup) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "RRB Bot is Running!"

def run_flask():
    # Render default port 8080 ya 10000 use karta hai
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- RRB Bot Logic Starts Here ---
# Keys ko Environment Variables se uthana (Security ke liye)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Gemini Setup (Latest Model)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Telegram Bot Setup
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 Namaste! Main aapka RRB Group D Assistant hoon.\n\n"
        "📖 Aap mujhse Maths, Science, Reasoning ya GK ka koi bhi sawal puch sakte hain.\n"
        "✍️ Bas apna sawal yahan likhein aur main uska detail solution dunga."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def get_ai_solution(message):
    try:
        # User ko batana ki process ho raha hai
        sent_msg = bot.reply_to(message, "Soch raha hoon... 🤔")
        
        # Gemini se answer mangna (RRB context ke saath)
        prompt = f"Solve this RRB Group D exam question with step-by-step details in Hindi/English: {message.text}"
        response = model.generate_content(prompt)
        
        # Jawab ko edit karke bhejna
        bot.edit_message_text(response.text, chat_id=sent_msg.chat.id, message_id=sent_msg.message_id)
        
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Maaf kijiye, abhi response nahi mil raha. Kripya apni Gemini API Key Render par check karein.")

# --- Flask aur Bot ko saath mein chalan ---
if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    print("Bot is starting...")
    bot.infinity_polling()
    
