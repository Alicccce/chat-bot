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
        'Напиши мне в одном сообщении номера заданий (цифрами через пробел), к которым ты хочешь подготовиться.')
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

    src_theory_filenames = []
    src_filenames = []
    numder = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
              '17',
              '18', '19']

    for i in numder:
        if i in answer:
            src_filenames.append(''.join('pdf_file/number' + i.replace(' ', '') + '.pdf'))
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

    merge_pdf(src_filenames, exe_filename)
    merge_pdf(src_theory_filenames, theory_filename)
    with open(exe_filename, 'rb') as f:
        await update.message.reply_document(exe_filename)
    if sch > 0:
        await update.message.reply_document(theory_filename)
    await update.message.reply_text(f'{src_filenames, src_theory_filenames}')


def merge_pdf(src_filenames, dest_filename):
    merger = PyPDF2.PdfMerger()

    for src_filename in src_filenames:
        merger.append(src_filename)

    merger.write(dest_filename)