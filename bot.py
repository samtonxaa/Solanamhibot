import os
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace these with your actual questions and answers
QUESTIONS = [
    {"q": "Question 1: What is digital marketing?", "a": "advertising"},
    {"q": "Question 2: Name a social platform.", "a": "instagram"},
    {"q": "Question 3: What does SEO stand for?", "a": "search engine optimization"},
    {"q": "Question 4: Is email marketing dead?", "a": "no"},
    {"q": "Question 5: Best time to post?", "a": "evening"},
]

# Simple in-memory database (Note: Render free tier restarts will clear this)
user_data = {}

def get_week_number():
    return datetime.datetime.now().isocalendar()[1]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Type /ask to start your 5 weekly questions.")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current_week = get_week_number()
    
    # Initialize or Reset user if it's a new week
    if user_id not in user_data or user_data[user_id]['week'] != current_week:
        user_data[user_id] = {'count': 0, 'week': current_week}

    count = user_data[user_id]['count']

    if count >= 5:
        await update.message.reply_text("Limit reached! Please come back next week for new channeling.")
    else:
        question = QUESTIONS[count]['q']
        await update.message.reply_text(f"{question}")
        user_data[user_id]['count'] += 1

if __name__ == '__main__':
    # Render uses environment variables for security
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    
    print("Bot is running...")
    app.run_polling()
