from telegram.ext import CommandHandler, CallbackQueryHandler

from commands.generic import start, help, error, button
from commands.email import view_email, view_detailed_email, mark_read_email, mark_unread_email,\
    help_email, archive_email, label_list_email, delete_email
from commands.account import account_options, account_servers


bot = None


def load_dispatcher(dispatcher):
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CallbackQueryHandler(button, pattern="(\/start\/).+"))

    # EMAIL
    dispatcher.add_handler(CallbackQueryHandler(view_detailed_email, pattern="(\/email\/view\/).+"))
    dispatcher.add_handler(CallbackQueryHandler(view_email, pattern="(\/email\/back\/).+"))
    dispatcher.add_handler(CallbackQueryHandler(mark_read_email, pattern="(\/email\/mark_read\/).+"))
    dispatcher.add_handler(CallbackQueryHandler(mark_unread_email, pattern="(\/email\/mark_unread\/).+"))
    dispatcher.add_handler(CallbackQueryHandler(archive_email, pattern="(\/email\/archive\/).+"))
    dispatcher.add_handler(CallbackQueryHandler(label_list_email, pattern="(\/email\/label_l\/).+"))
    dispatcher.add_handler(CallbackQueryHandler(delete_email, pattern="(\/email\/delete\/).+"))

    dispatcher.add_handler(CallbackQueryHandler(help_email, pattern="(\/email\/help)"))


    dispatcher.add_handler(CommandHandler('list_folders', help))

    # ACCOUNTS
    dispatcher.add_handler(CallbackQueryHandler(account_options, pattern="(\/account\/options)"))
    dispatcher.add_handler(CallbackQueryHandler(account_servers, pattern="(\/account\/add\/servers)"))

    dispatcher.add_error_handler(error)


def get_bot():
    return bot

def set_bot(inp):
    global bot
    bot = inp
