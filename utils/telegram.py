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
import email as email_lib


emojis = {
    "back": "🔙",
    "help": "❓",
    "link": "🔗",  # "🌐",
    "mark_as_unread": "❗️",
    "mark_as_read": "👁",
    "remember": "⏰",
    "delete": "🗑",
    "details": "🔎",
    "archive": "🗄",  # 🗃
    "reply": "↩",
    "label": "🗂",  # 🏷
    "previous_page": "⏪",
    "next_page": "⏩",
}


def notify_new_email(bot, id_user, msg):
    response, reply_markup = load_main_view(msg)

    msg_send = bot.send_message(chat_id=id_user, parse_mode="Markdown",
                                text=response,
                                reply_markup=reply_markup)
    return msg_send is not None


def load_main_view(msg, back=None):
    # msg = get_email_server(user_email).get_email_by_uid(folder, msg_uid)
    # a = msg.msg
    email_date = email_lib.utils.parsedate_to_datetime(msg.msg["date"])

    email_from = msg.get_header('from')
    email_subject = msg.get_header('subject')

    common_sufix = '/' + msg.email + '/' + msg.uid.decode() + '/' + msg.folders[0]

    if msg.get_flag("Seen"):
        read_button = InlineKeyboardButton(emojis["mark_as_unread"], callback_data='/email/mark_unread' + common_sufix)
    else:
        read_button = InlineKeyboardButton(emojis["mark_as_read"], callback_data='/email/mark_read' + common_sufix)

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

    if len(email_subject) > 500:
        email_subject = email_subject[:500] + " ..."

    response = "*"+email_subject + "*\n[" + email_from + "]\n(_" + str(email_date)+"_)"

    return response, InlineKeyboardMarkup(keyboard)

