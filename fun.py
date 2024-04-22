from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import PyPDF2

done = [[InlineKeyboardButton('Готово!', callback_data='start')]]
donee = InlineKeyboardMarkup(done)

numder_for_person_plan = []


async def person_plan(update, context):
    callback_query = update.callback_query
    await callback_query.answer()
    await callback_query.message.reply_text(
        'Напиши мне в одном сообещнии номера заданий (цифрами через пробел), к которым ты хочешь подготовиться.')
    return 5


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def chek_numder(update, context):
    answer = update.message.text
    answer = answer.split()
    exe_filename = "pdf_file/tasks.pdf"
    theory_filename = "pdf_theory_file/theory.pdf"
    sch = 0

    link = ''
    src_theory_filenames = []
    src_filenames = []
    numder = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
              '17',
              '18', '19']
    sl_link = {
        '13': "13 задание - https://www.youtube.com/live/ygd5VKNjRiQ?si=TSC9rsNk2Pyiynkk, https://www.youtube.com/live/Xx9v3PDEt4s?si=EoABsdPa4--3WcYV\n",
        '14': '14 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaza0FRUCDpuwRYXnoF9ySIc&si=C4K_wN8PW-FGISwS\n',
        '15': '15 задание - https://youtu.be/eB0HFxJSXzA?si=0G3ELCDMHZ-ggh9u, https://www.youtube.com/live/OVjkcHzls_g?si=ojzYCBq2khYIupwM\n',
        '16': '16 задание - все типы https://www.youtube.com/live/1UFpGeuXPNE?si=piETyUIoBXbQbzGk, диффдифференцированный https://www.youtube.com/live/LUJcuxJtKBE?si=RuXsNqMG52rXUSTB, аннуитетный https://www.youtube.com/live/_YrXlFDEIw0?si=C5pA7F0xb8UT8GP6\n',
        '17': '17 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaz5YJeBpJugoQ7FkyL0HxS9&si=iuOHpxih1grtmVVB\n',
        '18': '18 задание - https://youtube.com/playlist?list=PL3BJnp-dNqaw31jYk5qqKX7ivCdWwPYRZ&si=n15mo7E1XiF2O64f, https://www.youtube.com/live/JJT28hxRvP0?si=9UcGGCntKfcUqmcU, https://www.youtube.com/live/t3NTVw73rvw?si=VyOIfqFizMeUfQeG + https://www.youtube.com/live/U-jw8tTBZu4?si=EFT9r8YV52oz9LH4\n',
        '19': '19 задание - https://www.youtube.com/live/xHj_NbgOWiY?si=JdLYcpt7lq9a4wqp, https://youtube.com/playlist?list=PL3BJnp-dNqazRHFnGVeZBDi7M5h9gdGxk&si=BPIE9PdJEABob2RP, https://www.youtube.com/live/A7Qrm63EdEI?si=LDUZgeUldmMyBuBJ\n'
    }

    for i in numder:
        if i in answer:
            src_filenames.append(''.join('pdf_file/number' + i.replace(' ', '') + '.pdf'))
            if int(i) > 12:
                link += sl_link[i]
            if int(i) < 13:
                if int(i) == 5 and 'pdf_theory_file/theory4.pdf' not in src_theory_filenames:
                    src_theory_filenames.append(''.join('pdf_theory_file/theory' + '4' + '.pdf'))
                    sch += 1
                if int(i) == 7 and 'pdf_theory_file/theory6.pdf' not in src_theory_filenames:
                    src_theory_filenames.append(''.join('pdf_theory_file/theory' + '6' + '.pdf'))
                    sch += 1
                if int(i) == 12 and 'pdf_theory_file/theory8.pdf' not in src_theory_filenames:
                    src_theory_filenames.append(''.join('pdf_theory_file/theory' + '8' + '.pdf'))
                    sch += 1
                elif int(i) != 5 and int(i) != 7 and int(i) != 12 and int(i) != 9:
                    sch += 1
                    src_theory_filenames.append(''.join('pdf_theory_file/theory' + i.replace(' ', '') + '.pdf'))
    if len(src_filenames) == 0 and len(src_theory_filenames) == 0:
        await update.message.reply_text('Извините, что-то пошло не так. попробуйте снова.')

    merge_pdf(src_filenames, exe_filename)
    merge_pdf(src_theory_filenames, theory_filename)
    if len(link) != 0:
        await update.message.reply_text('Эти видео помогут тебе при подготовки! \n' + link)
    if len(src_filenames) != 0 and len(src_theory_filenames) != 0:
        await update.message.reply_text('Эти файлы помогут тебе подготовиться к заданиям и потренеровать свои навыки.')
    if len(src_filenames) != 0 and len(src_theory_filenames) == 0:
        await update.message.reply_text('Этот файл поможет тебе отточить свои умения на практике.')
    if len(src_filenames) != 0:
        with open(exe_filename, 'rb') as f:
            await update.message.reply_document(exe_filename)

    if len(src_theory_filenames) != 0:
        if sch > 0:
            await update.message.reply_document(theory_filename)



def merge_pdf(src_filenames, dest_filename):
    merger = PyPDF2.PdfMerger()

    for src_filename in src_filenames:
        merger.append(src_filename)

    merger.write(dest_filename)
