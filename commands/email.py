from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import email as email_lib
import repository.emails as email_repo


emojis = {
    "back": "🔙",
    "help": "❓",
    "link": "🔗",  # "🌐",
    "is_read": "👁",
    "is_unread": "❗️",
    "remember": "⏰",
    "delete": "🗑",
    "details": "🔎",
    "archive": "🗃",
    "reply": "↩",
    "label": "🏷",
}


def view_detailed_email(bot, update):
    query = update.callback_query

    data = filter_callback_data(update, "/email/view", 3)
    user_email = data[0]
    msg_uid = bytes(data[1], 'utf-8')
    folder = data[2]

    msg = email_repo.get_emails_servers()[user_email].get_email_by_uid(folder, msg_uid)
    message = msg.get_body()

    response, reply_markup = __load_main_view(user_email, msg_uid, folder, back="details")

    bot.edit_message_text(text=message,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)


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


def mark_read_email(bot, update):
    query = update.callback_query

    data = filter_callback_data(update, "/email/mark_read", 3)
    user_email = data[0]
    msg_uid = bytes(data[1], 'utf-8')
    folder = data[2]

    email_repo.get_emails_servers()[user_email].mark_as_read(folder, msg_uid, True)

    response, reply_markup = __load_main_view(user_email, msg_uid, folder)

    bot.edit_message_text(parse_mode="Markdown",
                          text=response + "--",
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)


def mark_unread_email(bot, update):
    query = update.callback_query
    try:
        data = filter_callback_data(update, "/email/mark_unread", 3)
        user_email = data[0]
        msg_uid = bytes(data[1], 'utf-8')
        folder = data[2]
        email_repo.get_emails_servers()[user_email].mark_as_read(folder, msg_uid, False)

        response, reply_markup = __load_main_view(user_email, msg_uid, folder)
        bot.edit_message_text(parse_mode="Markdown",
                              text=response + "++",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup)
    except:
        logging.error("mark_unread_email error")


def help_email(bot, update):
    text = emojis["back"] + " previous content\n"
    text += emojis["help"] + " show this menu\n"
    text += emojis["link"] + " link to web email\n"
    text += emojis["details"] + " show additionals details\n"
    text += emojis["archive"] + " archive the message\n"
    text += emojis["reply"] + " reply to the message\n"
    text += emojis["remember"] + " remember in the future\n"
    text += emojis["label"] + " manage labels\n"
    text += emojis["is_read"] + "/" + emojis["is_unread"] + " mark as unread/read\n"
    bot.send_message(chat_id=update.effective_chat.id, parse_mode="Markdown",
                                text=text)


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


def __load_main_view(user_email, msg_uid, folder, back=None):
    msg = email_repo.get_emails_servers()[user_email].get_email_by_uid(folder, msg_uid)
    a = msg.msg
    email_date = email_lib.utils.parsedate_to_datetime(a["date"])

    email_from = msg.get_header('from')
    email_subject = msg.get_header('subject')

    common_sufix = '/' + user_email + '/' + msg_uid.decode() + '/' + folder

    if msg.get_flag("Seen"):
        read_button = InlineKeyboardButton(emojis["is_read"], callback_data='/email/mark_unread' + common_sufix)
    else:
        read_button = InlineKeyboardButton(emojis["is_unread"], callback_data='/email/mark_read' + common_sufix)

    if back == "details":
        details_button = InlineKeyboardButton(emojis["back"], callback_data='/email/back' + common_sufix)
    else:
        details_button = InlineKeyboardButton(emojis["details"], callback_data='/email/view'+common_sufix)

    keyboard = [[
                    details_button,
                    read_button,
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

