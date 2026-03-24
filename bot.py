import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- Render Port Fix (Flask Setup) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "RRB Bot is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Bot Configuration ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Gemini Setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Telegram Bot Setup
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Namaste Zara! Main aapka RRB Group D Assistant hoon. Apna sawal yahan likhein.")

@bot.message_handler(func=lambda message: True)
def get_solution(message):
    try:
        # Thinking message
        sent_msg = bot.reply_to(message, "Soch raha hoon... 🧠")
        
        # AI Solution
        prompt = f"Explain this RRB Group D question in detail with step-by-step solution: {message.text}"
        response = model.generate_content(prompt)
        
        # Reply with solution
        bot.edit_message_text(response.text, chat_id=sent_msg.chat.id, message_id=sent_msg.message_id)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Maaf kijiye, abhi response nahi mil raha. Kripya Gemini API Key check karein.")

# --- Start Everything ---
if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    print("Bot is starting...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    
