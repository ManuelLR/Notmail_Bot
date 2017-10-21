from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import email as email_lib


emojis = {
    "back": "🔙",
    "help": "❓",
    "link": "🔗",  # "🌐",
    "is_read": "👁",
    "is_unread": "❗️",
    "remember": "⏰",
    "delete": "🗑",
    "details": "🔎",
    "archive": "🗄",  # 🗃
    "reply": "↩",
    "label": "🗂",  # 🏷
    "previous_page": "⏪",
    "next_page": "⏩",
}


def send_msg(bot, id_user, user_email, folder, msg_uid, msg):
    response, reply_markup = load_main_view(user_email, msg_uid, msg, folder)

    msg_send = bot.send_message(chat_id=id_user, parse_mode="Markdown",
                                text=response,
                                reply_markup=reply_markup)
    return msg_send is not None


def load_main_view(user_email, msg_uid, msg, folder, back=None):
    # msg = get_email_server(user_email).get_email_by_uid(folder, msg_uid)
    # a = msg.msg
    email_date = email_lib.utils.parsedate_to_datetime(msg.msg["date"])

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
                    InlineKeyboardButton(emojis["label"], callback_data='/email/label_l/0' + common_sufix),
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

