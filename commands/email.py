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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
import logging
from services.email import get_email_server
from utils.telegram import emojis, load_main_view

folders_by_page = 8


def view_detailed_email(bot, update):
    query = update.callback_query
    try:
        data = filter_callback_data(update, "/email/view", 3)
        user_email = data[0]
        msg_uid = bytes(data[1], 'utf-8')
        folder = data[2]

        msg = get_email_server(user_email).get_email_by_uid(folder, msg_uid)
        message = msg.get_body()

        response, reply_markup = load_main_view(msg, back="details")

        if len(message) > 4000:
            message = message[:4000] + " ..."

        bot.edit_message_text(text=message,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup)
        query.answer()
    except:
        logging.error("view_detailed_email error")
        query.answer(text="view_detailed_email error")


def view_email(bot, update):
    query = update.callback_query

    data = filter_callback_data(update, "/email/view", 3)
    email = data[0]
    msg_uid = bytes(data[1], 'utf-8')
    folder = data[2]

    response, reply_markup = load_main_view(get_email_server(email).get_email_by_uid(folder, msg_uid))

    bot.edit_message_text(parse_mode="Markdown",
                          text=response,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)
    query.answer()


def mark_read_email(bot, update):
    query = update.callback_query
    try:
        data = filter_callback_data(update, "/email/mark_read", 3)
        user_email = data[0]
        msg_uid = bytes(data[1], 'utf-8')
        folder = data[2]

        get_email_server(user_email).mark_as_read(folder, msg_uid, True)

        response, reply_markup = load_main_view(get_email_server(user_email).get_email_by_uid(folder, msg_uid))

        bot.edit_message_text(parse_mode="Markdown",
                              text=response + "--",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup)
        query.answer()
    except:
        logging.error("mark_read_email error")
        query.answer(text="mark_read_email error")


def mark_unread_email(bot, update):
    query = update.callback_query
    try:
        data = filter_callback_data(update, "/email/mark_unread", 3)
        user_email = data[0]
        msg_uid = bytes(data[1], 'utf-8')
        folder = data[2]
        get_email_server(user_email).mark_as_read(folder, msg_uid, False)

        response, reply_markup = load_main_view(get_email_server(user_email).get_email_by_uid(folder, msg_uid))
        bot.edit_message_text(parse_mode="Markdown",
                              text=response + "++",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup)
        query.answer()
    except:
        logging.error("mark_unread_email error")
        query.answer(text="mark_unread_email error")


def archive_email(bot, update):
    query = update.callback_query
    try:
        data = filter_callback_data(update, "/email/archive", 3)
        user_email = data[0]
        msg_uid = bytes(data[1], 'utf-8')
        folder = data[2]
        get_email_server(user_email).delete_from_folder(msg_uid, folder)

        previous_response = query.message.text_markdown
        bot.edit_message_text(parse_mode="Markdown",
                              text=previous_response+"\n\n"+emojis["archive"]+"Archived! "+emojis["archive"],
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        query.answer()
    except Exception as e:
        logging.error(e)
        logging.error("archive_email error")
        query.answer(text="archive_email error")


def label_list_email(bot, update):
    query = update.callback_query
    try:
        data = filter_callback_data(update, "/email/label_l", 4)
        user_email = data[1]
        msg_uid = bytes(data[2], 'utf-8')
        page = data[0]
        folder = data[3]
        folders = get_email_server(user_email).get_folders()

        common_sufix = '/' + user_email + '/' + msg_uid.decode() + '/' + folder

        header = []

        header.append(InlineKeyboardButton(emojis["back"], callback_data='/email/back' + common_sufix))
        print(int(page))

        if int(page) > 0:  # Need previous page button
            header.append(InlineKeyboardButton(emojis["previous_page"], callback_data='/email/label_l/' +
                                                                                      str(int(page)-1) + common_sufix))
        header.append(InlineKeyboardButton(emojis["archive"], callback_data='/email/archive' + common_sufix))
        header.append(InlineKeyboardButton(emojis["delete"], callback_data='/email/delete'+common_sufix))
        header.append(InlineKeyboardButton(emojis["link"], callback_data='/email/link' + common_sufix))

        if (len(folders) - (int(page) + 1) * folders_by_page) > 0:  # Need next page button
            header.append(InlineKeyboardButton(emojis["next_page"], callback_data='/email/label_l/' +
                                                                                  str(int(page)+1) + common_sufix))
        body = [header]
        for a in range(0, int(folders_by_page/2)):
            n = a * 2 + (int(page) * folders_by_page)
            body.append([
                InlineKeyboardButton(folders[n].name, callback_data='/email/label' + common_sufix),
                InlineKeyboardButton(folders[n+1].name, callback_data='/email/label' + common_sufix),
                         ])

        response, reply_markup = load_main_view(get_email_server(user_email).get_email_by_uid(folder, msg_uid))
        bot.edit_message_text(parse_mode="Markdown",
                              text=response + "+-",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(body))
        query.answer()
    except Exception as e:
        logging.error(e)
        logging.error("label_list_email error")
        query.answer(text="label_list_email error")


def delete_email(bot, update):
    query = update.callback_query
    try:
        data = filter_callback_data(update, "/email/delete", 3)
        user_email = data[0]
        msg_uid = bytes(data[1], 'utf-8')
        folder = data[2]

        get_email_server(user_email).add_to_folder(msg_uid, 'inbox', '[Gmail]/Trash')
        get_email_server(user_email).delete_from_folder(msg_uid, 'Inbox')

        previous_response = query.message.text_markdown

        bot.edit_message_text(parse_mode="Markdown",
                              text=previous_response+"\n\n"+emojis["delete"]+"Deleted! "+emojis["delete"],
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        query.answer()
    except Exception as e:
        logging.error(e)
        logging.error("delete_email error")
        query.answer(text="delete_email error")



def help_email(bot, update):
    text = emojis["back"] + " previous content\n"
    text += emojis["help"] + " show this menu\n"
    text += emojis["link"] + " link to web email\n"
    text += emojis["details"] + " show additionals details\n"
    text += emojis["archive"] + " archive the message\n"
    text += emojis["reply"] + " reply to the message\n"
    text += emojis["remember"] + " remember in the future\n"
    text += emojis["label"] + " manage labels\n"
    text += emojis["mark_as_unread"] + "/" + emojis["mark_as_read"] + " mark as unread/read\n"
    bot.send_message(chat_id=update.effective_chat.id, parse_mode="Markdown",
                                text=text)


# Prefix without last /
def filter_callback_data(update, prefix, fields=1, separator='/'):
    data = update.callback_query.data[len(prefix)+1:]

    return data.split(separator, fields-1)
