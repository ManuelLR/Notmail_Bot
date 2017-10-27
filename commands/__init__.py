# Copyright 2017 by Notmail Bot contributors. All rights reserved.
#
# This file is part of Notmail Bot.
#
#     Notmail Bot is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Notmail Bot is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Notmail Bot.  If not, see <http:#www.gnu.org/licenses/>.
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, \
    RegexHandler, Filters

from commands.generic import start, help, error, button
from commands.email import view_email, view_detailed_email, mark_read_email, mark_unread_email,\
    help_email, archive_email, label_list_email, delete_email
from commands.account import account_options, account_servers, add_gmail_account, add_outlook_account,\
    add_other_account, add_gmail_username_account, add_password_account, add_refresh_time_account, \
    cancel


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
    dispatcher.add_handler(CallbackQueryHandler(account_servers, pattern="(\/account\/add\/servers)$"))
    # dispatcher.add_handler(CallbackQueryHandler(add_gmail_account, pattern="(\/account\/add\/servers\/gmail)"))
    # dispatcher.add_handler(CallbackQueryHandler(add_outlook_account, pattern="(\/account\/add\/servers\/outlook)"))
    # dispatcher.add_handler(CallbackQueryHandler(add_other_account, pattern="(\/account\/add\/servers\/other)"))

    ACCOUNT, PASSWORD, REFRESH_TIME = range(3)

    conv_gmail_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_gmail_account, pattern="(\/account\/add\/servers\/gmail)")],

        states={
            ACCOUNT: [RegexHandler('^.*?@.*?\..*$', add_gmail_username_account, pass_user_data=True)],

            PASSWORD: [MessageHandler(Filters.text, add_password_account, pass_user_data=True)],

            REFRESH_TIME: [MessageHandler(Filters.text, add_refresh_time_account, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_gmail_handler)

    dispatcher.add_error_handler(error)

