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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import logging


def account_options(bot, update):
    query = update.callback_query

    keyboard = [[InlineKeyboardButton("Add Account", callback_data='/account/add/servers')],
                 [InlineKeyboardButton("Modify Account", callback_data='/account/modify'),
                 InlineKeyboardButton("Remove Account", callback_data='/account/remove')]]

                #[InlineKeyboardButton("Accounts", callback_data='/account/options')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.message.reply_text('What do you want to do with Accounts?', reply_markup=reply_markup)
    logging.debug(query.message.chat_id)


def account_servers(bot, update):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("GMAIL", callback_data='/account/add/servers/gmail')],
                [InlineKeyboardButton("OUTLOOK - (NOT AVAILABLE)", callback_data='/account/add/servers/outlook')],
                [InlineKeyboardButton("OTHER - (NOT AVAILABLE)", callback_data='/account/add/servers/other')]]

    # [InlineKeyboardButton("Accounts", callback_data='/account/options')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.message.reply_text('On which server do you want to add the Account?', reply_markup=reply_markup)
    logging.debug(query.message.chat_id)


def add_gmail_account(bot, update):
    pass


def add_outlook_account(bot, update):
    query = update.callback_query
    query.message.reply_text('Option not available yet')


def add_other_account(bot, update):
    query = update.callback_query
    query.message.reply_text('Option not available yet')
