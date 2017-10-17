from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

def account_options(bot, update):
    query = update.callback_query

    keyboard = [[InlineKeyboardButton("Add Account", callback_data='/account/add')],
                 [InlineKeyboardButton("Modify Account", callback_data='/account/modify'),
                 InlineKeyboardButton("Remove Account", callback_data='/account/remove')]]

                #[InlineKeyboardButton("Accounts", callback_data='/account/options')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.message.reply_text('What do you want to do with Accounts?', reply_markup=reply_markup)
    logging.debug(query.message.chat_id)