from telegram.ext import CommandHandler, CallbackQueryHandler

from Commands.generic import start, help, error, button


def load_dispatcher(dispatcher):
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CallbackQueryHandler(button, pattern="(\/start\/).+"))
    dispatcher.add_error_handler(error)
