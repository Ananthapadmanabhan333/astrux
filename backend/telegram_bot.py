import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

client = None
if os.getenv("OPENAI_API_KEY"):
    client = openai.OpenAI()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Namaste! 🙏 I am Astrus, your AI Vedic Astrologer on Telegram.\n\n"
        "Ask me any question about your life, career, or relationships, "
        "and I will guide you using the stars."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text
    
    dataset_context = ""
    dataset_path = os.path.join(os.path.dirname(__file__), "vedic_astra_dataset.md")
    if os.path.exists(dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            dataset_context = f.read()

    if client:
        prompt = f"""
        You are Astrus, a traditional Vedic astrologer chatbot on Telegram.
        Base your answers on this highly accurate core Vedic dataset:
        <vedic_dataset>
        {dataset_context}
        </vedic_dataset>
        
        User asks: {user_query}
        Provide comforting, honest Vedic guidance strictly aligned with classical Parashari principles.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a traditional Vedic astrologer."},
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"(AI Error) {str(e)}"
    else:
        reply = f"Namaste! I have received your message: '{user_query}'. " \
                "Please configure OPENAI_API_KEY in the env to activate AI predictions."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set. Please set it to run the bot.")
        return

    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)

    print("Starting Astrus Telegram Bot...")
    application.run_polling()

if __name__ == '__main__':
    main()
