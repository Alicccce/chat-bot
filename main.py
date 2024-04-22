import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from fun import person_plan, chek_numder, merge_pdf

BOT_TOKEN = '7131922662:AAFHddt6nU3S-olQtsV7g0dd_nHaMSNafv4'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

reply_keyboard1 = [[InlineKeyboardButton("Готовый план", callback_data="ready_plan"),
                    InlineKeyboardButton("Персональный план", callback_data="person_plan")],
                   [InlineKeyboardButton("База заданий", callback_data="wrong"),
                    InlineKeyboardButton("Напомнить", callback_data="remind")]]

reply_keyboard2 = [[InlineKeyboardButton('27-50 баллов', callback_data='niz'),
                    InlineKeyboardButton('50-70 баллов', callback_data='nser')],
                   [InlineKeyboardButton('70-85 баллов', callback_data='vser'),
                    InlineKeyboardButton('85-100 баллов', callback_data='verch')]]

reply_keyboard3 = [[InlineKeyboardButton('Знаю лучше алгебру', callback_data='algebra'),
                    InlineKeyboardButton('Знаю лучше геометрию', callback_data='geometria')],
                   [InlineKeyboardButton('Всем владею хорошо', callback_data='alll'),
                    InlineKeyboardButton('Ничего не знаю', callback_data='noth')]]

reply_keyboard4 = [[InlineKeyboardButton('Первая часть', callback_data='z112'),
                    InlineKeyboardButton('18 задание', callback_data='z18')],
                   [InlineKeyboardButton('13 задание', callback_data='z13'),
                    InlineKeyboardButton('15 задание', callback_data='z15')],
                   [InlineKeyboardButton('14 задание', callback_data='z14'),
                    InlineKeyboardButton('17 задание', callback_data='z17')],
                   [InlineKeyboardButton('16 задание', callback_data='z16'),
                    InlineKeyboardButton('19 задание', callback_data='z19')]]

reply_keyboard5 = [[InlineKeyboardButton('Давай в начало', callback_data='nachalo'),
                    InlineKeyboardButton('Нет, пока', callback_data='byee')]]

markup = InlineKeyboardMarkup(reply_keyboard1)
scores = InlineKeyboardMarkup(reply_keyboard2)
alg_geom = InlineKeyboardMarkup(reply_keyboard3)
zdn = InlineKeyboardMarkup(reply_keyboard4)
nazad = InlineKeyboardMarkup(reply_keyboard5)

K1, K2 = '', ''  # переменные для запоминания необходимых данных


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я чат-бот Гриша, пришёл к вам с планеты Школяриус, чтобы помочь сдать экзамен по профильной математике! С чего начнём?",
        reply_markup=markup)


async def help_command(update, context):
    await update.message.reply_text("С божьей помощью.. удачи!")


async def nachalo(update, context):
    user = update.effective_user
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_html(
        rf"Привет, {user.mention_html()}! Я чат-бот Гриша, пришёл к вам с планеты Школяриус, чтобы помочь сдать экзамен по профильной математике! С чего начнём?",
        reply_markup=markup)


async def byee(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('Рад был помочь, обращайтесь. До свидания!')


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
    global K1
    answer = update.message.text
    if '1' in answer:
        await update.message.reply_text('В какой день? Напишите полное или сокращённое название.')
        K1 = 'нед'
        return 4
    if '2' in answer:
        await update.message.reply_text(
            'В какое время? Напишите слово: утро(8:00), день(13:00), вечер(18:00) или ночь(01:00).')
        K1 = 'р_день'
        return 4
    if '3' in answer:
        await update.message.reply_text('С какого начать? Напишите полное или сокращённое название.')
        K1 = 'ч_день'
        return 4

    if 'недел' in answer:
        if ('раз' in answer) or ('кажд' in answer) or \
                ('Раз' in answer) or ('Кажд' in answer):
            await update.message.reply_text('В какой день? Напишите полное или сокращённое название.')
            K1 = 'нед'
            return 4
    if 'день' in answer:
        if ('кажд' in answer) or ('раз' in answer) or \
                ('Кажд' in answer) or ('Раз' in answer):
            await update.message.reply_text(
                'В какое время? Напишите слово: утро(8:00), день(13:00), вечер(18:00) или ночь(01:00).')
            K1 = 'р_день'
            return 4
    if ('через' in answer) or ('Через' in answer):
        await update.message.reply_text('С какого начать? Напишите полное или сокращённое название.')
        K1 = 'ч_день'
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
    if K1 == 'нед':
        for i in week:
            if i in answer:
                day = i
        await update.message.reply_text(f'Хорошо, буду напоминать вам раз в неделю, в конкретный день - {day}')
    if K1 == 'р_день':
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
    if K1 == 'ч_день':
        for i in week:
            if i in answer:
                dayy = i
        if week.index(dayy) % 2 != 0:
            await update.message.reply_text('Хорошо буду напоминать вам каждый нечётный день недели. \n'
                                            '(понедельник, среда, пятница, воскресенье)')
        else:
            await update.message.reply_text('Хорошо буду напоминать вам каждый чётный день недели. \n'
                                            '(вторник, четверг, суббота)')
    await update.message.reply_text('Ещё что-то?', reply_markup=nazad)


async def ready_plan(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text(
        'Я помогу, но, даже работая с готовым материалом, ты должен понимать, на что расчитываешь, и знать, что умеешь!',
        reply_markup=scores)


async def niz(update, context):
    global K2
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('Теперь мне важно понять, в чём ты хорош больше. Выбери;)',
                                            reply_markup=alg_geom)
    K2 = 2750


async def nser(update, context):
    global K2
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('Теперь мне важно понять, в чём ты хорош больше. Выбери;)',
                                            reply_markup=alg_geom)
    K2 = 5070


async def vser(update, context):
    global K2
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('Теперь мне важно понять, в чём ты хорош больше. Выбери;)',
                                            reply_markup=alg_geom)
    K2 = 7085


async def verch(update, context):
    global K2
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text('Теперь мне важно понять, в чём ты хорош больше. Выбери;)',
                                            reply_markup=alg_geom)
    K2 = 85100


async def algebra(update, context):  # остальное
    callback_query = update.callback_query
    await callback_query.answer()
    if K2 == 2750:
        await callback_query.message.reply_text(
            'Знаешь лучше алгебру, значит надо подтянуть геометрию! Затачивай 1, 2, 3 номера! \n\n'
            'Смотри два разбора в неделю по 1, 2, 3 заданиям, один на повтор по алгебре и ещё один по всей первой части. Вот неплохие вебинары на решение различных прототипов:\n'
            '1 задание - https://youtu.be/40ixsuhZC44?si=2vQbPKqNPq0YSEs5 \n'
            '2 задание - https://www.youtube.com/live/1sPClRa2PuY?si=zLahMBPqngN4dKox \n'
            '3 задание - https://youtu.be/UPa5fHk161k?si=UrMcTvS_7lW4sW9C \n\n'
            'И не забывай продолжать работать над алгеброй, ещё пока не время расслабляться, даже если хорошо получается. С целью 27-50 баллов лучше набивать руку на первую часть.\n'
            'https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)
    if K2 == 5070:
        await callback_query.message.reply_text(
            'Знаешь лучше алгебру, значит надо подтянуть геометрию! Затачивай 1, 2, 3 номера и пробуй получать 1 балл за пункт а) в 17 задании:) \n\n'
            'Смотри вебинар по 17 один-два раза в неделю, разбор 1, 2, 3 один день в неделю и ещё денёк на повторы.\n'
            '1 задание - https://youtu.be/40ixsuhZC44?si=2vQbPKqNPq0YSEs5 \n'
            '2 задание - https://www.youtube.com/live/1sPClRa2PuY?si=zLahMBPqngN4dKox \n'
            '3 задание - https://youtu.be/UPa5fHk161k?si=UrMcTvS_7lW4sW9C \n'
            '17 задание - https://www.youtube.com/live/tlOTaiad36Q?si=Sp2_Z07Ai4SWRkBp\n'
            'повторы - https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n\n'
            'Но нельзя забывать про алгебру, например, решив 13 можно заработать достаточно легко 2 балла. Лови вебинарчик по разбору 13, разбирайся в нём хотя бы один раз в неделю;)\n'
            '13 задание - https://www.youtube.com/live/ygd5VKNjRiQ?si=TSC9rsNk2Pyiynkk')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)
    if K2 == 7085:
        await callback_query.message.reply_text(
            'А ты хорош! Надо много работать на такой результат. Раз лучше знаешь алгебру, нужно большее внимание уделить геометрии, но и работать над тем, что хорошо получается.\n\n'
            'Предлагаю два дня уделять заданиям 14, 17, два - 13, 15, 18, один - первой части\n'
            '14 задание - https://www.youtube.com/live/eJAc8z0DjrY?si=7JaVERKevmcBs9np\n'
            '17 задание - https://www.youtube.com/live/tlOTaiad36Q?si=Sp2_Z07Ai4SWRkBp\n'
            '13 задание - https://www.youtube.com/live/ygd5VKNjRiQ?si=TSC9rsNk2Pyiynkk'
            '15 задание -  https://youtu.be/eB0HFxJSXzA?si=0G3ELCDMHZ-ggh9u\n'
            '18 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaw31jYk5qqKX7ivCdWwPYRZ&si=n15mo7E1XiF2O64f, https://www.youtube.com/live/t3NTVw73rvw?si=VyOIfqFizMeUfQeG + https://www.youtube.com/live/U-jw8tTBZu4?si=EFT9r8YV52oz9LH4\n'
            'первая часть - https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)
    if K2 == 85100:
        await callback_query.message.reply_text(
            'Ого! Вот это цели! Так держать. Раз лучше знаешь алгебру, нужно большее внимание уделить геометрии, но я советую разбирать задание 19, если лучше с алгеброй, будет проще понять его:)\n\n'
            'Смотри вебинар по 17 два раза в неделю, 14 хотя бы раз в неделю, один день уделяй 18, один - 19 и ещё денёк на повторы первй части и 13, 15, 16. Главное - продолжай работать!\n'
            '14 задание -  https://youtube.com/playlist?list=PL3BJnp-dNqaza0FRUCDpuwRYXnoF9ySIc&si=C4K_wN8PW-FGISwS\n'
            '17 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaz5YJeBpJugoQ7FkyL0HxS9&si=iuOHpxih1grtmVVB + https://www.youtube.com/live/axMFeOWP6x8?si=MY7QzcCSSKVgiWfv\n'
            '😄💪\n'
            'первая часть - https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n'
            'повтор 13, 15, 16 - https://www.youtube.com/live/eHTWv7sIpbI?si=p1z-tvDo1y3BIwaH\n'
            '18 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaw31jYk5qqKX7ivCdWwPYRZ&si=n15mo7E1XiF2O64f, https://www.youtube.com/live/t3NTVw73rvw?si=VyOIfqFizMeUfQeG + https://www.youtube.com/live/U-jw8tTBZu4?si=EFT9r8YV52oz9LH4\n'
            '19 задание - https://youtube.com/playlist?list=PL3BJnp-dNqazRHFnGVeZBDi7M5h9gdGxk&si=BPIE9PdJEABob2RP')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)


async def geometria(update, context):  # 1, 2, 3, 14, 17
    callback_query = update.callback_query
    await callback_query.answer()
    if K2 == 2750:
        await callback_query.message.reply_text(
            'Знаешь лучше геометрию, значит надо подтянуть алгебру! Затачивай 4-12 номера! \n\n'
            'Смотри два-три разбора в неделю 4-12 заданиям (ниже по ним вебинары), один на повтор по геометрии и ещё один по всей первой части. Вот неплохие вебинары на решение различных прототипов:\n'
            '- https://youtu.be/H5w-Ppy5ez0?si=dxIP436_vP_epd69\n'
            '- https://www.youtube.com/live/0aGIDlgzHCU?si=m7SdbUmITtncpUap\n'
            '- https://www.youtube.com/live/oRWQtlPOyww?si=4N-UAkdvXP7C_uJS\n'
            '- https://youtu.be/17axkC5JxFM?si=R3zdp0m4kHhbHa9g\n'
            '- https://youtu.be/qHKEcOJ_Z3U?si=dsPJSfwPpmVRquZe\n\n'
            'И не забывай продолжать работать над геометрией, ещё пока не время расслабляться, даже если хорошо получается. С целью 27-50 баллов лучше набивать руку на первую часть.\n'
            'https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)
    if K2 == 5070:
        await callback_query.message.reply_text(
            'Знаешь лучше геометрию, значит надо подтянуть алгебру! Затачивай 4-12 номера и тренируйся в решении 13, 15, 16, чтобы получить желаемый результат:) \n\n'
            'Уделяй хотя бы три дня разбору заданий, практике по тому, в чём ты не слишком силён и ещё день на повторы.\n'
            '13 задание - https://www.youtube.com/live/ygd5VKNjRiQ?si=TSC9rsNk2Pyiynkk\n'
            '15 задание - https://youtu.be/eB0HFxJSXzA?si=0G3ELCDMHZ-ggh9u, https://www.youtube.com/live/OVjkcHzls_g?si=ojzYCBq2khYIupwM\n'
            '16 задание - https://www.youtube.com/live/1UFpGeuXPNE?si=piETyUIoBXbQbzGk\n'
            'повтор - https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)
    if K2 == 7085:
        await callback_query.message.reply_text(
            'А ты хорош! Надо много работать на такой результат. Раз лучше знаешь геометрию, нужно большее внимание уделить алгебре, но и работать над тем, что хорошо получается.\n\n'
            'Предлагаю два дня уделять заданиям 13, 15, 16, два - 14, 17, один - первой части\n'
            '13 задание - https://www.youtube.com/live/ygd5VKNjRiQ?si=TSC9rsNk2Pyiynkk'
            '15 задание -  https://youtu.be/eB0HFxJSXzA?si=0G3ELCDMHZ-ggh9u\n'
            '16 задание - https://www.youtube.com/live/1UFpGeuXPNE?si=piETyUIoBXbQbzGk\n'
            '14 задание - https://www.youtube.com/live/eJAc8z0DjrY?si=7JaVERKevmcBs9np\n'
            '17 задание - https://www.youtube.com/live/tlOTaiad36Q?si=Sp2_Z07Ai4SWRkBp\n'
            'первая часть - https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n\n'
            'Но я думаю, есть резон познакомиться и с 18 заданием. Если разобраться, оно бывает не очень сложным, а приносит целых 4 балла:)\n'
            '18 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaw31jYk5qqKX7ivCdWwPYRZ&si=n15mo7E1XiF2O64f, https://www.youtube.com/live/t3NTVw73rvw?si=VyOIfqFizMeUfQeG + https://www.youtube.com/live/U-jw8tTBZu4?si=EFT9r8YV52oz9LH4\n')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)
    if K2 == 85100:
        await callback_query.message.reply_text(
            'Ого! Вот это цели! Так держать. Раз лучше знаешь геометрию, нужно большее внимание уделить алгебре, но я советую не пропускать 17 и 14 задания в подготовке, если лучше с геометрией, то здорово было бы получить по 3 балла за эти задания:)\n\n'
            'Тебе решать и решать. По три дня в неделю разбирать 13, 15, 16, в отдельные два-три дня разбирать 18 и 19, а также два дня на тренировку первой части и двух заданий на геометрию из второй!'
            'разбор 13, 15, 16 - https://www.youtube.com/live/sXEJWaOZeGs?si=Wy3P5kkuUtm5Iv2X, https://www.youtube.com/live/eHTWv7sIpbI?si=xukbWDSloAtxBsx6, https://www.youtube.com/live/svbIsEvFhdw?si=bC5mpmJGzx20qJqU, https://www.youtube.com/live/I2RTzRXVaKU?si=t8Y7zL8CwDUODvmX\n'
            '18 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaw31jYk5qqKX7ivCdWwPYRZ&si=n15mo7E1XiF2O64f, https://www.youtube.com/live/t3NTVw73rvw?si=VyOIfqFizMeUfQeG + https://www.youtube.com/live/U-jw8tTBZu4?si=EFT9r8YV52oz9LH4\n'
            '19 задание - https://youtube.com/playlist?list=PL3BJnp-dNqazRHFnGVeZBDi7M5h9gdGxk&si=BPIE9PdJEABob2RP\n'
            '😄💪\n'
            'первая часть - https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n'
            '14 задание -  https://youtube.com/playlist?list=PL3BJnp-dNqaza0FRUCDpuwRYXnoF9ySIc&si=C4K_wN8PW-FGISwS\n'
            '17 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaz5YJeBpJugoQ7FkyL0HxS9&si=iuOHpxih1grtmVVB + https://www.youtube.com/live/axMFeOWP6x8?si=MY7QzcCSSKVgiWfv\n')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)


async def alll(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    if K2 == 2750:
        await callback_query.message.reply_text(
            'Даже если всё знаешь, не переставай тренировать первую часть, решив её полносью правильно можно получить до 60-70 баллов, представляешь! Смотри эти разборы:\n'
            '- https://youtu.be/DyDN94omS8I?si=LI9rqBUJ6ijXGPaU\n'
            '- https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n'
            '- https://www.youtube.com/live/4wKw-BzjTUQ?si=ESjEwQUP4i1vQL1Z\n'
            'Но можно подстраховаться для такого результата и разобрать 13 задание, за которое дают 2 балла (https://www.youtube.com/live/ygd5VKNjRiQ?si=TSC9rsNk2Pyiynkk).\n'
            'Удачи:):):):):)')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)
    if K2 == 5070:
        await callback_query.message.reply_text(
            'Даже если всё знаешь, не переставай тренировать первую часть, решив её полносью правильно можно получить до 60-70 баллов, представляешь! Смотри эти разборы:\n'
            '- https://youtu.be/DyDN94omS8I?si=LI9rqBUJ6ijXGPaU\n'
            '- https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n'
            '- https://www.youtube.com/live/4wKw-BzjTUQ?si=ESjEwQUP4i1vQL1Z\n'
            'Но чем больше, тем лучше, потренируй 13, 15, они не слишком сложные. Разбирай 16 задание, 17, в котором пункт а) часто нетрудный\n'
            '13 задание - https://www.youtube.com/live/ygd5VKNjRiQ?si=TSC9rsNk2Pyiynkk\n'
            '15 задание - https://youtu.be/eB0HFxJSXzA?si=0G3ELCDMHZ-ggh9u, https://www.youtube.com/live/OVjkcHzls_g?si=ojzYCBq2khYIupwM\n'
            '16 задание - https://www.youtube.com/live/1UFpGeuXPNE?si=piETyUIoBXbQbzGk\n'
            '17 задание - https://www.youtube.com/live/GWOGTZvRYjc?si=lTd4a2ZebPZny0a4\n'
            'Выдели для подготовки 3+ дня. Удачи:):):):):)')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)
    if K2 == 7085:
        await callback_query.message.reply_text(
            'Вот это цели! Не забывай про первую часть, даже если думаешь, что всё знаешь, решив её полносью правильно можно получить до 60-70 баллов, представляешь! Для этого разборы по первой части:\n'
            '- https://youtu.be/DyDN94omS8I?si=LI9rqBUJ6ijXGPaU\n'
            '- https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n'
            '- https://www.youtube.com/live/4wKw-BzjTUQ?si=ESjEwQUP4i1vQL1Z\n'
            'Чем больше работаешь, тем выше результат, для достижения 70-85 баллов нужно точно уметь решать 13, 15 и 16 задания, а также можно браться за пункт а) 17 или 19 задания.\n'
            '13 задание - https://www.youtube.com/live/ygd5VKNjRiQ?si=TSC9rsNk2Pyiynkk, https://www.youtube.com/live/Xx9v3PDEt4s?si=EoABsdPa4--3WcYV\n'
            '15 задание - https://youtu.be/eB0HFxJSXzA?si=0G3ELCDMHZ-ggh9u, https://www.youtube.com/live/OVjkcHzls_g?si=ojzYCBq2khYIupwM\n'
            '16 задание - все типы https://www.youtube.com/live/1UFpGeuXPNE?si=piETyUIoBXbQbzGk, диффдифференцированный https://www.youtube.com/live/LUJcuxJtKBE?si=RuXsNqMG52rXUSTB, аннуитетный https://www.youtube.com/live/_YrXlFDEIw0?si=C5pA7F0xb8UT8GP6\n'
            '17 задание - https://www.youtube.com/live/GWOGTZvRYjc?si=lTd4a2ZebPZny0a4\n'
            '19 задание - https://www.youtube.com/live/xHj_NbgOWiY?si=JdLYcpt7lq9a4wqp\n'
            'Тренируйся хотя бы 4 дня в неделю, не забывая отдыхать. Удачи:):):):):)')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)
    if K2 == 85100:
        await callback_query.message.reply_text(
            'Ох, надо усердно работать для такого результата. Твоя уверенность в себе - это хорошо!\n Не забывай про первую часть, решив её полносью правильно можно получить до 60-70 баллов, представляешь! Для этого разборы по первой части:\n'
            '- https://youtu.be/DyDN94omS8I?si=LI9rqBUJ6ijXGPaU\n'
            '- https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n'
            '- https://www.youtube.com/live/4wKw-BzjTUQ?si=ESjEwQUP4i1vQL1Z\n'
            'Работа, работа и ещё раз работа. Решать и решать, смотреть и смотреть. Задания первой части ты должен щёлкать как орешки, достаточно быстро решать 13, 15, 16, знать разные конструкции 18 и, безусловно, практиковаться в решении 14, 17, 19.\n'
            '13 задание - https://www.youtube.com/live/ygd5VKNjRiQ?si=TSC9rsNk2Pyiynkk, https://www.youtube.com/live/Xx9v3PDEt4s?si=EoABsdPa4--3WcYV\n'
            '15 задание - https://youtu.be/eB0HFxJSXzA?si=0G3ELCDMHZ-ggh9u, https://www.youtube.com/live/OVjkcHzls_g?si=ojzYCBq2khYIupwM\n'
            '16 задание - все типы https://www.youtube.com/live/1UFpGeuXPNE?si=piETyUIoBXbQbzGk, диффдифференцированный https://www.youtube.com/live/LUJcuxJtKBE?si=RuXsNqMG52rXUSTB, аннуитетный https://www.youtube.com/live/_YrXlFDEIw0?si=C5pA7F0xb8UT8GP6\n'
            '14 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaza0FRUCDpuwRYXnoF9ySIc&si=C4K_wN8PW-FGISwS\n'
            '17 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaz5YJeBpJugoQ7FkyL0HxS9&si=iuOHpxih1grtmVVB\n'
            '18 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaw31jYk5qqKX7ivCdWwPYRZ&si=n15mo7E1XiF2O64f, https://www.youtube.com/live/JJT28hxRvP0?si=9UcGGCntKfcUqmcU, https://www.youtube.com/live/t3NTVw73rvw?si=VyOIfqFizMeUfQeG + https://www.youtube.com/live/U-jw8tTBZu4?si=EFT9r8YV52oz9LH4\n'
            '19 задание - https://www.youtube.com/live/xHj_NbgOWiY?si=JdLYcpt7lq9a4wqp, https://youtube.com/playlist?list=PL3BJnp-dNqazRHFnGVeZBDi7M5h9gdGxk&si=BPIE9PdJEABob2RP, https://www.youtube.com/live/A7Qrm63EdEI?si=LDUZgeUldmMyBuBJ\n'
            'Тренируйся хотя бы 4 дня в неделю, не забывая отдыхать. Всё получается сейчас, получится и потом! Удачи:):):):):)')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)


async def noth(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    if K2 == 2750:
        await callback_query.message.reply_text(
            'Конечно, тренируем первую часть, решив полносью её правильно можно получить до 60-70 баллов, представляешь! Смотри эти разборы:\n'
            '- https://youtu.be/DyDN94omS8I?si=LI9rqBUJ6ijXGPaU\n'
            '- https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n'
            '- https://www.youtube.com/live/4wKw-BzjTUQ?si=ESjEwQUP4i1vQL1Z\n'
            'Удачи:):):):):)')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)
    if K2 == 5070:
        await callback_query.message.reply_text(
            'Конечно, мы начинаем с первой части, решив полносью её правильно можно получить до 60-70 баллов, представляешь! Для этого разборы по первой части:\n'
            '- https://youtu.be/DyDN94omS8I?si=LI9rqBUJ6ijXGPaU\n'
            '- https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n'
            '- https://www.youtube.com/live/4wKw-BzjTUQ?si=ESjEwQUP4i1vQL1Z\n'
            'Но чем больше, тем лучше, подстрахуйся и потренируй 13, 15, они не слишком сложные.\n'
            '13 задание - https://www.youtube.com/live/ygd5VKNjRiQ?si=TSC9rsNk2Pyiynkk'
            '15 задание - https://youtu.be/eB0HFxJSXzA?si=0G3ELCDMHZ-ggh9u, https://www.youtube.com/live/OVjkcHzls_g?si=ojzYCBq2khYIupwM\n'
            'Выдели для подготовки 3+ дня. Удачи:):):):):)')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)
    if K2 == 7085:
        await callback_query.message.reply_text(
            'Вот это цели! Конечно, мы начинаем с первой части, решив полносью её правильно можно получить до 60-70 баллов, представляешь! Для этого разборы по первой части:\n'
            '- https://youtu.be/DyDN94omS8I?si=LI9rqBUJ6ijXGPaU\n'
            '- https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n'
            '- https://www.youtube.com/live/4wKw-BzjTUQ?si=ESjEwQUP4i1vQL1Z\n'
            'Чем больше работаешь, тем выше результат, для достижения 70-85 баллов нужно точно уметь решать 13, 15 и 16 задания, а также можно браться за пункт а) 17 или 19 задания.\n'
            '13 задание - https://www.youtube.com/live/ygd5VKNjRiQ?si=TSC9rsNk2Pyiynkk, https://www.youtube.com/live/Xx9v3PDEt4s?si=EoABsdPa4--3WcYV\n'
            '15 задание - https://youtu.be/eB0HFxJSXzA?si=0G3ELCDMHZ-ggh9u, https://www.youtube.com/live/OVjkcHzls_g?si=ojzYCBq2khYIupwM\n'
            '16 задание - все типы https://www.youtube.com/live/1UFpGeuXPNE?si=piETyUIoBXbQbzGk, диффдифференцированный https://www.youtube.com/live/LUJcuxJtKBE?si=RuXsNqMG52rXUSTB, аннуитетный https://www.youtube.com/live/_YrXlFDEIw0?si=C5pA7F0xb8UT8GP6\n'
            '17 задание - https://www.youtube.com/live/GWOGTZvRYjc?si=lTd4a2ZebPZny0a4\n'
            '19 задание - https://www.youtube.com/live/xHj_NbgOWiY?si=JdLYcpt7lq9a4wqp\n'
            'Тренируйся хотя бы 4 дня в неделю, не забывая отдыхать. Удачи:):):):):)')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)
    if K2 == 85100:
        await callback_query.message.reply_text(
            'Ох, надо усердно работать для такого результата. Давай начинать:)\n Конечно, поначалу с первой части, решив полносью её правильно можно получить до 60-70 баллов, представляешь! Для этого разборы по первой части:\n'
            '- https://youtu.be/DyDN94omS8I?si=LI9rqBUJ6ijXGPaU\n'
            '- https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9\n'
            '- https://www.youtube.com/live/4wKw-BzjTUQ?si=ESjEwQUP4i1vQL1Z\n'
            'Работа, работа и ещё раз работа. Решать и решать, смотреть и смотреть. Задания первой части ты должен щёлкать как орешки, достаточно быстро решать 13, 15, 16, знать разные конструкции 18 и, безусловно, практиковаться в решении 14, 17, 19.\n'
            '13 задание - https://www.youtube.com/live/ygd5VKNjRiQ?si=TSC9rsNk2Pyiynkk, https://www.youtube.com/live/Xx9v3PDEt4s?si=EoABsdPa4--3WcYV\n'
            '15 задание - https://youtu.be/eB0HFxJSXzA?si=0G3ELCDMHZ-ggh9u, https://www.youtube.com/live/OVjkcHzls_g?si=ojzYCBq2khYIupwM\n'
            '16 задание - все типы https://www.youtube.com/live/1UFpGeuXPNE?si=piETyUIoBXbQbzGk, диффдифференцированный https://www.youtube.com/live/LUJcuxJtKBE?si=RuXsNqMG52rXUSTB, аннуитетный https://www.youtube.com/live/_YrXlFDEIw0?si=C5pA7F0xb8UT8GP6\n'
            '14 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaza0FRUCDpuwRYXnoF9ySIc&si=C4K_wN8PW-FGISwS\n'
            '17 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaz5YJeBpJugoQ7FkyL0HxS9&si=iuOHpxih1grtmVVB\n'
            '18 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaw31jYk5qqKX7ivCdWwPYRZ&si=n15mo7E1XiF2O64f, https://www.youtube.com/live/JJT28hxRvP0?si=9UcGGCntKfcUqmcU, https://www.youtube.com/live/t3NTVw73rvw?si=VyOIfqFizMeUfQeG + https://www.youtube.com/live/U-jw8tTBZu4?si=EFT9r8YV52oz9LH4\n'
            '19 задание - https://www.youtube.com/live/xHj_NbgOWiY?si=JdLYcpt7lq9a4wqp, https://youtube.com/playlist?list=PL3BJnp-dNqazRHFnGVeZBDi7M5h9gdGxk&si=BPIE9PdJEABob2RP, https://www.youtube.com/live/A7Qrm63EdEI?si=LDUZgeUldmMyBuBJ\n'
            'Тренируйся хотя бы 4 дня в неделю, не забывая отдыхать. Удачи:):):):):)')
        await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)


async def wrong(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("Выберите то, что хотели бы разобрать отдельно.", reply_markup=zdn)


async def z112(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("Держи на разбор и отработку первой части три вебнарчика и теорию по ней же!\n"
                                            "- https://youtu.be/DyDN94omS8I?si=LI9rqBUJ6ijXGPaU \n"
                                            "- https://www.youtube.com/live/esUmA8mlJGc?si=2TQSp5fjnTHDO_j9 \n"
                                            "- https://www.youtube.com/live/4wKw-BzjTUQ?si=ESjEwQUP4i1vQL1Z")
    await callback_query.message.reply_document('pdf_theory_file/theory1.pdf')
    await callback_query.message.reply_document('pdf_theory_file/theory2.pdf')
    await callback_query.message.reply_document('pdf_theory_file/theory3.pdf')
    await callback_query.message.reply_document('pdf_theory_file/theory4.pdf')
    await callback_query.message.reply_document('pdf_theory_file/theory6.pdf')
    await callback_query.message.reply_document('pdf_theory_file/theory8.pdf')
    await callback_query.message.reply_document('pdf_theory_file/theory10.pdf')
    await callback_query.message.reply_document('pdf_theory_file/theory11.pdf')
    await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)


async def z13(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text(
        "Лови три крутых разбора тригонометрии, которая понадобится и в первой части, которую не стоит забывать. А также задания для практики!\n"
        "• https://youtu.be/H5w-Ppy5ez0?si=Vvx949txRgeRuSn3 \n"
        "• https://www.youtube.com/live/BZORLZhj388?si=zHa9T7KuC2_LWo6D \n"
        "• https://www.youtube.com/live/J-HwyFrwVbU?si=jisUKUGOoylGlEW1")
    await callback_query.message.reply_document('pdf_file/number6.pdf')
    await callback_query.message.reply_document('pdf_file/number7.pdf')
    await callback_query.message.reply_document('pdf_file/number13.pdf')
    await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)


async def z14(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text(
        "Лови классные разборы 14 задания, в которых не забывают и про 3 задание, ведь там основы стереометрии. А также задания для практики!\n"
        "• https://www.youtube.com/live/QIdzj5haquI?si=NWm27jl5593LSgew \n"
        "• https://youtube.com/playlist?list=PL3BJnp-dNqaza0FRUCDpuwRYXnoF9ySIc&si=C4K_wN8PW-FGISwS \n"
        "• https://www.youtube.com/live/eKpUiqUk1BI?si=kd4LTpB5l0zF19K3")
    await callback_query.message.reply_document('pdf_file/number3.pdf')
    await callback_query.message.reply_document('pdf_file/number14.pdf')
    await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)


async def z15(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("Держи классные видео разборы неравенств и задания для практики!\n"
                                            "• https://www.youtube.com/live/sjxLxV0rA1s?si=IzYLTMoTv7kZnAJA \n"
                                            "• https://youtu.be/eB0HFxJSXzA?si=0G3ELCDMHZ-ggh9u \n"
                                            "• https://www.youtube.com/live/OVjkcHzls_g?si=ojzYCBq2khYIupwM")
    await callback_query.message.reply_document('pdf_file/number15.pdf')
    await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)


async def z16(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text(
        "Вот два супер-вебинара по экономическим задачам. Всё на пальцах объясняют. И не забывай про прктику!\n"
        "• дифференцированный платёж - https://www.youtube.com/live/LUJcuxJtKBE?si=RuXsNqMG52rXUSTB \n"
        "• аннуитетный платёж - https://www.youtube.com/live/_YrXlFDEIw0?si=C5pA7F0xb8UT8GP6")
    await callback_query.message.reply_document('pdf_file/number16.pdf')
    await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)


async def z17(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text(
        "Лови жёсткие разборы планиматрии, в которых не забывают и про первое задание, ведь без такой основы не надо браться и за 17! Тренируй себя в практических заданиях:)\n"
        "• https://www.youtube.com/live/GWOGTZvRYjc?si=lTd4a2ZebPZny0a4 \n"
        "• https://youtu.be/nMhVd0kXvVY?si=sMPvA1Yx_B06_qN2 \n"
        "• https://www.youtube.com/live/geuUNU6fy4E?si=Yp1chrOtlEIDx98N")
    await callback_query.message.reply_document('pdf_file/number1.pdf')
    await callback_query.message.reply_document('pdf_file/number17.pdf')
    await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)


async def z18(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text(
        "Теперь у тебя есть подробные разборы 18 задания. Проводи время с толком и с практикой;) \n"
        "• https://youtube.com/playlist?list=PL3BJnp-dNqaw31jYk5qqKX7ivCdWwPYRZ&si=n15mo7E1XiF2O64f \n"
        "• https://www.youtube.com/live/JJT28hxRvP0?si=9UcGGCntKfcUqmcU \n"
        "• https://www.youtube.com/live/t3NTVw73rvw?si=VyOIfqFizMeUfQeG + https://www.youtube.com/live/U-jw8tTBZu4?si=EFT9r8YV52oz9LH4")
    await callback_query.message.reply_document('pdf_file/number18.pdf')
    await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)


async def z19(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text("Жёстко ботаем 19 задание! Лови вебинары и задания на практику.\n"
                                            "• https://www.youtube.com/live/xHj_NbgOWiY?si=JdLYcpt7lq9a4wqp \n"
                                            "• https://youtube.com/playlist?list=PL3BJnp-dNqazRHFnGVeZBDi7M5h9gdGxk&si=BPIE9PdJEABob2RP \n"
                                            "• https://www.youtube.com/live/A7Qrm63EdEI?si=LDUZgeUldmMyBuBJ")
    await callback_query.message.reply_document('pdf_file/number19.pdf')
    await callback_query.message.reply_text('Ещё что-то?', reply_markup=nazad)


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

conv_handler2 = ConversationHandler(
    entry_points=[CallbackQueryHandler(person_plan, pattern='person_plan')],

    states={
        5: [MessageHandler(filters.TEXT & ~filters.COMMAND, chek_numder)]
    },

    fallbacks=[CommandHandler('stop', stop)])


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CallbackQueryHandler(nachalo, pattern='nachalo'))
    application.add_handler(CallbackQueryHandler(byee, pattern='byee'))

    application.add_handler(conv_handler1)
    application.add_handler(CallbackQueryHandler(remind, pattern='remind'))

    application.add_handler(conv_handler2)
    application.add_handler(CallbackQueryHandler(person_plan, pattern='chek_numder'))
    application.add_handler(CallbackQueryHandler(person_plan, pattern='person_plan'))

    application.add_handler(CallbackQueryHandler(ready_plan, pattern='ready_plan'))
    application.add_handler(CallbackQueryHandler(niz, pattern='niz'))
    application.add_handler(CallbackQueryHandler(nser, pattern='nser'))
    application.add_handler(CallbackQueryHandler(vser, pattern='vser'))
    application.add_handler(CallbackQueryHandler(verch, pattern='verch'))
    application.add_handler(CallbackQueryHandler(algebra, pattern='algebra'))
    application.add_handler(CallbackQueryHandler(geometria, pattern='geometria'))
    application.add_handler(CallbackQueryHandler(alll, pattern='alll'))
    application.add_handler(CallbackQueryHandler(noth, pattern='noth'))

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