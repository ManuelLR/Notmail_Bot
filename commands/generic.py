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
import logging


def start(bot, update):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='/start/1'),
                 InlineKeyboardButton("Option 2", callback_data='/notStart/2')],

                [InlineKeyboardButton("Accounts", callback_data='/account/options')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    logging.debug(update.message.chat_id)


def help(bot, update):
    update.message.reply_text("With this bot you can say goodbye to your ugly email's clients. Feel free of use your "
                              "favorites emails account now in Telegram too!"
                              "\n\nUse /start to start to use this bot!!"
                              "\n\nYou can see the help about Email's buttons at the ❓ option")


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: %s" % query.data,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


