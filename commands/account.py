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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from repository.repository import DBC
from repository.account import Account

import logging

ACCOUNT, PASSWORD, REFRESH_TIME = range(3)

def account_options(bot, update):
    query = update.callback_query

    keyboard = [[InlineKeyboardButton("Add Account", callback_data='/account/add/servers')],
                 [InlineKeyboardButton("Modify Account", callback_data='/account/modify'),
                 InlineKeyboardButton("Remove Account", callback_data='/account/remove')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.message.reply_text('What do you want to do with Accounts?', reply_markup=reply_markup)
    logging.debug(query.message.chat_id)


def account_servers(bot, update):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("GMAIL", callback_data='/account/add/servers/gmail')],
                [InlineKeyboardButton("OUTLOOK - (NOT AVAILABLE)", callback_data='/account/add/servers/outlook')],
                [InlineKeyboardButton("OTHER - (NOT AVAILABLE)", callback_data='/account/add/servers/other')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.message.reply_text('On which server do you want to add the Account?', reply_markup=reply_markup)
    logging.debug(query.message.chat_id)


def add_gmail_account(bot, update):
    query = update.callback_query

    db = DBC()

    try:
        db.search_user(str(query.message.chat_id))
    except:
        db.insert_user(str(query.message.chat_id), [])

    query.message.reply_text('Type your email address:')
    logging.debug(query.message.chat_id)

    return ACCOUNT


def add_outlook_account(bot, update):
    query = update.callback_query
    query.message.reply_text('Option not available yet')


def add_other_account(bot, update):
    query = update.callback_query
    query.message.reply_text('Option not available yet')


def add_gmail_username_account(bot, update, user_data):
    db = DBC()
    email_server = db.search_email_server('GMAIL', 'IMAP')
    account = Account('GMAIL', None, None, email_server.host, email_server.port, email_server.protocol, None)
    account.username = update.message.text
    user_data['account'] = account

    update.message.reply_text('Type your password:')

    return PASSWORD


def add_password_account(bot, update, user_data):
    account = user_data['account']
    account.password = update.message.text
    user_data['account'] = account

    update.message.reply_text('Type your desired refresh_time in seconds (type 0 to set Default):')

    return REFRESH_TIME


def add_refresh_time_account(bot, update, user_data):
    db = DBC()
    user = db.search_user(str(update.message.chat_id))
    account = user_data['account']
    if int(update.message.text) != 0:
        account.refresh_time = int(update.message.text)
    db.add_account_to_user(user, account)

    update.message.reply_text('Great! Your account has been saved.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logging.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Operation cancelled, you have stopped the Account process.')

    return ConversationHandler.END


def modify_account(bot, update):
    query = update.callback_query

    keyboard = [[InlineKeyboardButton("Modify Password", callback_data='/account/modify/password')],
                [InlineKeyboardButton("Modify Refresh Time", callback_data='/account/modify/refresh_time')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.message.reply_text('What do you want to modify on your Accounts?', reply_markup=reply_markup)
    logging.debug(query.message.chat_id)


def modify_password(bot, update):
    query = update.callback_query

    query.message.reply_text('Okay. Type the email address of the account you want to modify your password:')

    return ACCOUNT


def modify_account_password(bot, update, user_data):
    query = update.callback_query

    user_data['username'] = update.message.text

    query.message.reply_text('Now type your new password:')

    return PASSWORD

def modify_password_password(bot, update, user_data):
    pass


def modify_refresh_time(bot, update):
    pass


def modify_account_refresh_time(bot, update, user_data):
    pass


def modify_refresh_time_refresh_time(bot, update, user_data):
    pass
