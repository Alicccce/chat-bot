import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup


BOT_TOKEN = '7131922662:AAFHddt6nU3S-olQtsV7g0dd_nHaMSNafv4'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
reply_keyboard = [['/wrong', '/ready_plan'],
                  ['/person_plan', '/remind']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(rf"Привет, {user.mention_html()}! Я чат-бот Гриша, пришёл к вам с планеты Школяриус, чтобы помочь сдать экзамен по профильной математике! С чего начнём?",
                                    reply_markup=markup)


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать...")


async def remind(update, context):
    await update.message.reply_text('Такое сделаем! r')


async def person_plan(update, context):
    await update.message.reply_text('Такое сделаем! pp')


async def ready_plan(update, context):
    await update.message.reply_text('Такое сделаем! rp')


async def wrong(update, context):
    await update.message.reply_text('Такое сделаем! w')


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("remind", remind))
    application.add_handler(CommandHandler("person_plan", person_plan))
    application.add_handler(CommandHandler("ready_plan", ready_plan))
    application.add_handler(CommandHandler("wrong", wrong))

    application.run_polling()


if __name__ == '__main__':
    main()