from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import email as email_lib
import repository.emails as email_repo
import utils.smtp as email_utils


emojis = {
    "back": "🔙",
    "help": "❓",
    "link": "🔗",  # "🌐",
    "read": "👁",
    "remember": "⏰",
    "delete": "🗑",
    "details": "🔎",
    "archive": "🗃",
    "reply": "↩",
    "label": "🔖",
}


def view_detailed_email(bot, update):
    query = update.callback_query

    data = filter_callback_data(update, "/email/view", 3)
    email = data[0]
    msg_uid = bytes(data[1], 'utf-8')
    folder = data[2]

    msg = email_utils.Message(email_repo.get_emails_servers()[email].get_email_by_uid(msg_uid))
    message = msg.get_body()

    common_sufix = '/' + email + '/' + msg_uid.decode() + '/' + folder

    keyboard = [[
                    InlineKeyboardButton(emojis["back"], callback_data='/email/back' + common_sufix),
                    InlineKeyboardButton(emojis["read"], callback_data='/email/mark_read' + common_sufix),
                    InlineKeyboardButton(emojis["archive"], callback_data='/email/archive'+common_sufix),
                    InlineKeyboardButton(emojis["label"], callback_data='/email/label' + common_sufix),
                    InlineKeyboardButton(emojis["remember"], callback_data='/email/remember'+common_sufix),
                    InlineKeyboardButton(emojis["link"], callback_data='/email/link' + common_sufix),
                    InlineKeyboardButton(emojis["reply"], callback_data='/email/reply' + common_sufix),
                    InlineKeyboardButton(emojis["help"], callback_data='/email/help'),

            ], ]

    bot.edit_message_text(text=message,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=InlineKeyboardMarkup(keyboard))


def view_email(bot, update):
    query = update.callback_query

    data = filter_callback_data(update, "/email/view", 3)
    email = data[0]
    msg_uid = bytes(data[1], 'utf-8')
    folder = data[2]

    response, reply_markup = __load_main_view(email, msg_uid, folder)

    bot.edit_message_text(parse_mode="Markdown",
                          text=response,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)


    # Prefix without last /
def filter_callback_data(update, prefix, fields=1, separator='/'):
    data = update.callback_query.data[len(prefix)+1:]

    return data.split(separator, fields-1)


def send_msg(bot, id_user, user_email, folder, msg_uid):
    response, reply_markup = __load_main_view(user_email, msg_uid, folder)

    msg_send = bot.send_message(chat_id=id_user, parse_mode="Markdown",
                                text=response,
                                reply_markup=reply_markup)
    return msg_send is not None


def __load_main_view(user_email, msg_uid, folder):
    msg = email_utils.Message(email_repo.get_emails_servers()[user_email].get_email_by_uid(msg_uid))
    email_date = email_lib.utils.parsedate_to_datetime(msg.msg['date'])

    email_from = msg.get_header('from')
    email_subject = msg.get_header('subject')

    common_sufix = '/' + user_email + '/' + msg_uid.decode() + '/' + folder

    keyboard = [[
                    InlineKeyboardButton(emojis["details"], callback_data='/email/view'+common_sufix),
                    InlineKeyboardButton(emojis["read"], callback_data='/email/mark_read' + common_sufix),
                    InlineKeyboardButton(emojis["archive"], callback_data='/email/archive'+common_sufix),
                    InlineKeyboardButton(emojis["label"], callback_data='/email/label' + common_sufix),
                    InlineKeyboardButton(emojis["remember"], callback_data='/email/remember'+common_sufix),
                    InlineKeyboardButton(emojis["link"], callback_data='/email/link' + common_sufix),
                    InlineKeyboardButton(emojis["reply"], callback_data='/email/reply' + common_sufix),
                    InlineKeyboardButton(emojis["help"], callback_data='/email/help'),

            # ], [
            #         InlineKeyboardButton(emojis["delete"], callback_data='/email/delete'+common_sufix),
            #         InlineKeyboardButton(emojis["back"], callback_data='/email/back' + common_sufix),
            ], ]

    response = "*"+email_subject + "*\n[" + email_from + "]\n(_" + str(email_date)+"_)"

    return response, InlineKeyboardMarkup(keyboard)

