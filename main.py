import logging
import os
import requests
from dotenv import load_dotenv, find_dotenv
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler

load_dotenv(find_dotenv())

URL = 'https://jsonplaceholder.typicode.com/todos/'
# HEADERS = {"Authorization": "Bearer 19efbdc8ee723b7eb9e6dae1f7a20ca4378b288c"}

def get(id: int):
    if id:
        return (requests.get(URL + id)).json()
    logging.info(f"type {type(id)}")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"update: {update.message.text}")
    result = get(update.message.text)
    msg = str(result["id"]) + ' ' + result["title"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    
    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    application.add_handler(start_handler)
    application.add_handler(inline_caps_handler)    
    application.add_handler(caps_handler)
    application.add_handler(echo_handler)

    # must be added last. If you added it before the other handlers, it would be triggered before the CommandHandlers had a chance to look at the update. 
    application.add_handler(unknown_handler)
    
    application.run_polling()