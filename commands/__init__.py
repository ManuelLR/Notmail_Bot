from telegram.ext import CommandHandler, CallbackQueryHandler

from commands.generic import start, help, error, button
from commands.email import view_email, view_detailed_email


def load_dispatcher(dispatcher):
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CallbackQueryHandler(button, pattern="(\/start\/).+"))

    # EMAIL
    dispatcher.add_handler(CallbackQueryHandler(view_detailed_email, pattern="(\/email\/view\/).+"))
    dispatcher.add_handler(CallbackQueryHandler(view_email, pattern="(\/email\/back\/).+"))

    dispatcher.add_error_handler(error)
