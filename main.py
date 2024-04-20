import logging, time
import asyncio, aioschedule
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = '7131922662:AAFHddt6nU3S-olQtsV7g0dd_nHaMSNafv4'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)



reply_keyboard1 = [[InlineKeyboardButton("Готовый план", callback_data="ready_plan"),
                InlineKeyboardButton("Персональный план", callback_data="person_plan")],
                    [InlineKeyboardButton("База заданий", callback_data="wrong"),
                    InlineKeyboardButton("Напомнить", callback_data="remind")]]

reply_keyboard2 = [[InlineKeyboardButton('27-50 баллов', callback_data='niz'), InlineKeyboardButton('50-70 баллов', callback_data='nser')],
                  [InlineKeyboardButton('70-85 баллов', callback_data='vser'), InlineKeyboardButton('85-100 баллов', callback_data='verch')]]

reply_keyboard3 = [[InlineKeyboardButton('Знаю лучше алгебру', callback_data='algebra'), InlineKeyboardButton('Знаю лучше геометрию', callback_data='geometria')],
                    [InlineKeyboardButton('Всем владею хорошо', callback_data='alll')]]

reply_keyboard4 = [[InlineKeyboardButton('Первая часть', callback_data='z112'), InlineKeyboardButton('18 задание', callback_data='z18')],
                   [InlineKeyboardButton('13 задание', callback_data='z13'), InlineKeyboardButton('15 задание', callback_data='z15')],
                   [InlineKeyboardButton('14 задание', callback_data='z14'), InlineKeyboardButton('17 задание', callback_data='z17')],
                   [InlineKeyboardButton('16 задание', callback_data='z16'), InlineKeyboardButton('19 задание', callback_data='z19')]]

markup = InlineKeyboardMarkup(reply_keyboard1)
scores = InlineKeyboardMarkup(reply_keyboard2)
alg_geom = InlineKeyboardMarkup(reply_keyboard3)
zdn = InlineKeyboardMarkup(reply_keyboard4)

K = ''


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(rf"Привет, {user.mention_html()}! Я чат-бот Гриша, пришёл к вам с планеты Школяриус, чтобы помочь сдать экзамен по профильной математике! С чего начнём?",
                                    reply_markup=markup)


async def help_command(update, context):
    await update.message.reply_text("С божьей помощью.. удачи!")


async def job(update, message = 'Сообщение', n=1):
    await update.message.reply_text("Сообщение (%s)" % n, message)


async def remind(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('Я готов предложить тебе три универсальных, по-моему, варианта: \n'
                                    '- раз в неделю \n'
                                    '- раз в день \n'
                                    '- через день \n'
                                    'Выбери один и напиши мне его.')
    return 0


async def first_response(update, context):
    global K
    answer = update.message.text
    if '1' in answer:
        await update.message.reply_text('В какой день? Напишите полное или сокращённое название.')
        K = 'нед'
        return 4
    if '2' in answer:
        await update.message.reply_text(
            'В какое время? Напишите слово: утро(8:00), день(13:00), вечер(18:00) или ночь(01:00).')
        K = 'р_день'
        return 4
    if '3' in answer:
        await update.message.reply_text('С какого начать? Напишите полное или сокращённое название.')
        K = 'ч_день'
        return 4

    if 'недел' in answer:
        if ('раз' in answer) or ('кажд' in answer) or \
                ('Раз' in answer) or ('Кажд' in answer):
            await update.message.reply_text('В какой день? Напишите полное или сокращённое название.')
            K = 'нед'
            return 4
    if 'день' in answer:
        if ('кажд' in answer) or ('раз' in answer) or \
                ('Кажд' in answer) or ('Раз' in answer):
            await update.message.reply_text(
                'В какое время? Напишите слово: утро(8:00), день(13:00), вечер(18:00) или ночь(01:00).')
            K = 'р_день'
            return 4
    if ('через' in answer) or ('Через' in answer):
        await update.message.reply_text('С какого начать? Напишите полное или сокращённое название.')
        K = 'ч_день'
        return 4


async def second_response(update, context):
    answer = update.message.text
    day, time, dayy = '', '', ''
    week = ['вт', 'пн', 'чт', 'ср', 'сб', 'пт', 'вторник'
            'вс', 'четверг', 'понедельник', 'суббота',
            'среда', 'ВТ', 'пятница', 'ЧТ', 'воскресенье',
            'Вт', 'Пн', 'Чт', 'Ср', 'Сб', 'Пт', 'Вторник'
            'Вс', 'Четверг', 'Понедельник', 'Суббота',
            'Среда', 'СБ', 'Пятница', 'ВТ', 'Воскресенье',
            'ВТ', 'ПН', 'ВТ', 'СР', 'ВТ', 'ПТ', 'ВС']
    sutki = ['утро', 'вечер', 'день', 'ночь', 'днём',
             'Утро', 'Вечер', 'День', 'Ночь', 'Днём']
    if K == 'нед':
        for i in week:
            if i in answer:
                day = i
        await update.message.reply_text(f'Хорошо, буду напоминать вам раз в неделю, в конкретный день - {day}')
    if K == 'р_день': #aioschedule.every().day.at("19:19").do(job, n=1)
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


async def ready_plan(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('Я помогу, но, даже работая с готовым материалом, ты должен понимать, на что расчитываешь, и знать, что умеешь!', reply_markup=scores)


async def niz(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('Теперь мне важно понять, в чём ты хорош больше. Выбери;)', reply_markup=alg_geom)


async def nser(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('5070', reply_markup=alg_geom)


async def vser(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('7085', reply_markup=alg_geom)


async def verch(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('85100', reply_markup=alg_geom)


async def algebra(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('fku')


async def geometria(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('utjv')


async def alll(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('la')


async def person_plan(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('Такое сделаем!')


async def wrong(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("будем", reply_markup=zdn)


async def z112(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("Держи на разбор и отработку первой части три вебнарчика!\n"
                                            "- https://youtu.be/DyDN94omS8I?si=LI9rqBUJ6ijXGPaU \n"
                                            "- https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9 \n"
                                            "- https://www.youtube.com/live/4wKw-BzjTUQ?si=ESjEwQUP4i1vQL1Z")


async def z13(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("Лови три крутых разбора тригонометрии, которая понадобится и в первой части, которую не стоит забывать.\n"
                                            "• https://youtu.be/H5w-Ppy5ez0?si=Vvx949txRgeRuSn3 \n"
                                            "• https://www.youtube.com/live/BZORLZhj388?si=zHa9T7KuC2_LWo6D \n"
                                            "• https://www.youtube.com/live/J-HwyFrwVbU?si=jisUKUGOoylGlEW1")


async def z14(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("УЛЮЛЮ")


async def z15(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("Держи классные видео разборы неравенств!\n"
                                            "• https://www.youtube.com/live/sjxLxV0rA1s?si=IzYLTMoTv7kZnAJA \n"
                                            "• https://youtu.be/eB0HFxJSXzA?si=0G3ELCDMHZ-ggh9u \n"
                                            "• https://www.youtube.com/live/OVjkcHzls_g?si=ojzYCBq2khYIupwM")


async def z16(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("Вот два супер-вебинара по экономическим задачам. Всё на пальцах объясняют.\n"
                                            "• дифференцированный платёж - https://www.youtube.com/live/LUJcuxJtKBE?si=RuXsNqMG52rXUSTB \n"
                                            "• аннуитетный платёж - https://www.youtube.com/live/_YrXlFDEIw0?si=C5pA7F0xb8UT8GP6")


async def z17(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("Лови жёсткую разборы планиматрии, в которых не забывают и про первое задание, ведь без такой основы не надо браться и за 17!:)\n"
                                            "• https://www.youtube.com/live/GWOGTZvRYjc?si=lTd4a2ZebPZny0a4 \n"
                                            "• https://youtu.be/nMhVd0kXvVY?si=sMPvA1Yx_B06_qN2 \n"
                                            "• https://www.youtube.com/live/geuUNU6fy4E?si=Yp1chrOtlEIDx98N")


async def z18(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("УЛЮЛЮ")


async def z19(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("УЛЮЛЮ")


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END



conv_handler1 = ConversationHandler(
        entry_points=[CallbackQueryHandler(remind, pattern='remind')],

        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
        },

        fallbacks=[CommandHandler('stop', stop)])


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(conv_handler1)
    application.add_handler(CallbackQueryHandler(remind, pattern='remind'))

    application.add_handler(CallbackQueryHandler(person_plan, pattern='person_plan'))

    application.add_handler(CallbackQueryHandler(ready_plan, pattern='ready_plan'))
    application.add_handler(CallbackQueryHandler(niz, pattern='niz'))
    application.add_handler(CallbackQueryHandler(nser, pattern='nser'))
    application.add_handler(CallbackQueryHandler(vser, pattern='vser'))
    application.add_handler(CallbackQueryHandler(verch, pattern='verch'))
    application.add_handler(CallbackQueryHandler(algebra, pattern='algebra'))
    application.add_handler(CallbackQueryHandler(geometria, pattern='geometria'))
    application.add_handler(CallbackQueryHandler(alll, pattern='alll'))

    application.add_handler(CallbackQueryHandler(wrong, pattern='wrong'))
    application.add_handler(CallbackQueryHandler(z112, pattern='z112'))
    application.add_handler(CallbackQueryHandler(z13, pattern='z13'))
    application.add_handler(CallbackQueryHandler(z14, pattern='z14'))
    application.add_handler(CallbackQueryHandler(z15, pattern='z15'))
    application.add_handler(CallbackQueryHandler(z16, pattern='z16'))
    application.add_handler(CallbackQueryHandler(z17, pattern='z17'))
    application.add_handler(CallbackQueryHandler(z18, pattern='z18'))
    application.add_handler(CallbackQueryHandler(z19, pattern='z19'))



    application.run_polling()


if __name__ == '__main__':
    main()

'''loop = asyncio.get_event_loop()
while True:
    loop.run_until_complete(aioschedule.run_pending())
    time.sleep(0.1)'''