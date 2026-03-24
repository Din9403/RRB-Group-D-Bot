import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# Flask setup taaki Render 'Port' error na de
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    # Render default port 10000 ya 8080 use karta hai
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- RRB Bot Logic ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "RRB Group D Assistant Taiyar Hai! 📚\n\nApna sawal likhein ya photo bhejien.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        # User ko 'Thinking' ka feeling dene ke liye
        response = model.generate_content(f"Solve this RRB Group D question in detail: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Maaf kijiye, abhi response nahi mil raha. Kripya apni Gemini API Key check karein.")

if __name__ == "__main__":
    # Flask ko alag thread mein chalana
    t = Thread(target=run_flask)
    t.start()
    print("Bot is starting...")
    bot.infinity_polling()
    
