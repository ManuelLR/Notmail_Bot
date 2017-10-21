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

    keyboard = [["GMAIL"],
                ["OUTLOOK - (NOT AVAILABLE)"],
                ["OTHER - (NOT AVAILABLE)"]]

    # [InlineKeyboardButton("Accounts", callback_data='/account/options')]]

    reply_markup = ReplyKeyboardMarkup(keyboard)
    reply_markup.one_time_keyboard = True
    
    query.message.reply_text('On which server do you want to add the Account?', reply_markup=reply_markup)
    logging.debug(query.message.chat_id)
