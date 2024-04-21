import logging, time
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler
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


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def chek_numder(update, context):
    callback_query = update.callback_query
    answer = update.message.text
    src_filenames = []
    numder = [' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', '10', '11', '12', '14', '15', '16', '17', '18',
              '19']
    for i in numder:
        if i in answer:
            src_filenames.append(''.join('pdf_file/numder' + i))
    dest_filename = "pdf_file/tasks.pdf"
    merge_pdf(src_filenames, dest_filename)
    await callback_query.answer()
    await update.message.reply_text(f'ok{src_filenames}')

def merge_pdf(src_filenames, dest_filename):
    merger = PyPDF2.PdfMerger()

    for src_filename in src_filenames:
        merger.append(src_filename)

    merger.write(dest_filename)


conv_handler2 = ConversationHandler(
    entry_points=[CallbackQueryHandler(person_plan, pattern='remind')],

    states={
        0: [MessageHandler(filters.TEXT & ~filters.COMMAND, chek_numder)]
    },

    fallbacks=[CommandHandler('stop', stop)])
