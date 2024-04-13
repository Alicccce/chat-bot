import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup


BOT_TOKEN = '7131922662:AAFHddt6nU3S-olQtsV7g0dd_nHaMSNafv4'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
reply_keyboard = [['/wrong', '/ready_plan'],
                  ['/person_plan', '/remind']]
reply_keyboard2 = [['/yourself', '/suggestions_from_bot']]
reply_keyboard3 = [['/27_50__scores', '/50_70__scores'],
                  ['/70_85__scores', '/85_100__scores']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
time_for_r = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
scores = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True)

K = ''


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(rf"Привет, {user.mention_html()}! Я чат-бот Гриша, пришёл к вам с планеты Школяриус, чтобы помочь сдать экзамен по профильной математике! С чего начнём?",
                                    reply_markup=markup)
    return 1


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать...")


async def remind(update, context):
    await update.message.reply_text('Как тебе было бы удобнее?', reply_markup=time_for_r)

async def yourself(update, context):
    await update.message.reply_text('Самостоятельно')


async def suggestions_from_bot(update, context):
    await update.message.reply_text('Я могу предложить тебе три универсальных, по-моему, варианта: \n'
                                    '- раз в неделю \n'
                                    '- раз в день \n'
                                    '- через день \n'
                                    'Выбери один и напиши мне его.')
    return 1


async def first_response(update, context):
    global K
    answer = update.message.text
    if 'недел' in answer:
        if ('раз' in answer) or ('кажд' in answer) or \
            ('Раз' in answer) or ('Кажд'in answer):
            await update.message.reply_text('В какой день? Напишите полное или сокращённое название.')
            K = 'нед'
    if 'день' in answer:
        if ('кажд' in answer) or ('раз' in answer) or \
            ('Кажд' in answer) or ('Раз' in answer):
            await update.message.reply_text('В какое время? Напишите слово: утро(8:00), день(13:00), вечер(18:00) или ночь(01:00).')
            K = 'р_день'
    if ('через' in answer) or ('Через' in answer):
        await update.message.reply_text('С какого начать? Напишите полное или сокращённое название.')
        K = 'ч_день'
    return 2


async def second_response(update, context):
    day, time, dayy = '', '', ''
    week = ['вт', 'пн', 'чт', 'ср', 'сб', 'пт', 'вторник'
            'вс', 'четверг', 'понедельник', 'суббота',
            'среда', 'ВТ', 'пятница', 'ВТ', 'воскресенье',
            'Вт', 'Пн', 'Чт', 'Ср', 'Сб', 'Пт', 'Вторник'
            'Вс', 'Четверг', 'Понедельник', 'Суббота',
            'Среда', 'ВТ', 'Пятница', 'ВТ', 'Воскресенье']
    sutki = ['утро', 'вечер', 'день', 'ночь', 'днём',
             'Утро', 'Вечер', 'День', 'Ночь', 'Днём']
    answer = update.message.text
    if K == 'нед':
        for i in week:
            if i in answer:
                day = i
        await update.message.reply_text(f'Хорошо, буду напоминать вам каждый день, а именно - {day}')
    if K == 'р_день':
        for i in sutki:
            if i in answer:
                time = i
        if time == 'утро' or time == 'Утро':
            await update.message.reply_text(f'Хорошо, буду напоминать вам каждый день около 8 утра.')
        elif time == 'днём' or time == 'день' or time == 'Днём' or time == 'День':
            await update.message.reply_text(f'Хорошо, буду напоминать вам каждый день в районе 13.')
        elif time == 'вечер' or time == 'Вечер':
            await update.message.reply_text(f'Хорошо, буду напоминать вам каждый день ближе к 18.')
        elif time == 'ночь' or time == 'Ночь':
            await update.message.reply_text(f'Хорошо, буду напоминать вам каждую ночь.')
    if K == 'ч_день':
        for i in week:
            if i in answer:
                dayy = i
        if week.index(dayy) % 2 != 0:
            await update.message.reply_text('Хорошо буду напоминать вам каждый нечётный день недели. \n'
                                            '(понедельник, среда, пятница, воскресенье)')
        else:
            await update.message.reply_text('Хорошо буду напоминать вам каждый чётный день недели. \n'
                                            '(вторник, четверг, суббота)')

    return 3


async def third_response(update, context):
    answer = update.message.text


async def last_response(update, context):
    answer = update.message.text
    if '?' not in answer:
        await update.message.reply_text("Понял вас")
    else:
        await update.message.reply_text("Извините, я не понял вас")
    return ConversationHandler.END


async def person_plan(update, context):
    await update.message.reply_text('Такое сделаем! pp')


async def ready_plan(update, context):
    await update.message.reply_text('Я помогу, но, даже работая с готовым материалом, ты должен понимать, на что расчитываешь!', reply_markup=scores)


async def wrong(update, context):
    await update.message.reply_text('УЛЮЛЮ, уходи тогда', reply_markup=ReplyKeyboardMarkup([['УЛЮЛЮ, уходи тогда']]))


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


conv_handler = ConversationHandler(
        entry_points=[CommandHandler('suggestions_from_bot', suggestions_from_bot)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response)],
            #4: [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_response)]
        },

        fallbacks=[CommandHandler('stop', stop)])


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)

    application.add_handler(CommandHandler("remind", remind))
    application.add_handler(CommandHandler("person_plan", person_plan))
    application.add_handler(CommandHandler("ready_plan", ready_plan))
    application.add_handler(CommandHandler("wrong", wrong))

    application.add_handler(CommandHandler("yourself", yourself))
    application.add_handler(CommandHandler("suggestions_from_bot", suggestions_from_bot))

    application.run_polling()


if __name__ == '__main__':
    main()