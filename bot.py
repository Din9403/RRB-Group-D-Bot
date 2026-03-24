import os
import telebot
import google.generativeai as genai

# Hum tokens ko Environment Variables se uthayenge (Security ke liye)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Gemini Setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Bot Setup
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "RRB Group D Assistant Taiyar Hai! Apna sawal likhein ya photo bhejien.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        # Solution generate karna
        response = model.generate_content(f"Solve this RRB Group D question in detail: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Kuch gadbad ho gayi, kripya thodi der baad koshish karein.")

print("Bot is starting...")
bot.infinity_polling()
