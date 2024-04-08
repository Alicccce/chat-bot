import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


BOT_TOKEN = '7131922662:AAFHddt6nU3S-olQtsV7g0dd_nHaMSNafv4'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
reply_keyboard = [['/ошибся чатом', '/ready_plan'],
                  ['/person_plan', '/remind']]
reply_keyboard2 = [['/задать самому', '/преложение бота']]
reply_keyboard3 = [['/27-50 баллов', '/50-70 баллов'],
                  ['/70-85 баллов', '/85-90+ баллов']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
time_for_r = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
scores = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)

async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(rf"Привет, {user.mention_html()}! Я чат-бот Гриша, пришёл к вам с планеты Школяриус, чтобы помочь сдать экзамен по профильной математике! С чего начнём?",
                                    reply_markup=markup)


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать...")


async def remind(update, context):
    await update.message.reply_text('Как тебе было бы удобнее?', reply_markup=time_for_r)

async def yourself(update, context):
    await update.message.reply_text('Самостоятельно')


async def suggestion_from_bot(update, context):
    await update.message.reply_text('Вот так, вот так')


async def person_plan(update, context):
    await update.message.reply_text('Такое сделаем! pp')


async def ready_plan(update, context):
    await update.message.reply_text('Я помогу, но, даже работая с готовым материалом, ты должен понимать, на что расчитываешь!', reply_markup=scores)


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

    application.add_handler(CommandHandler("yourself", yourself))
    application.add_handler(CommandHandler("suggestion_from_bot", suggestion_from_bot))

    application.run_polling()


if __name__ == '__main__':
    main()