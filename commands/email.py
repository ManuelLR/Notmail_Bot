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
    "archive": "🗄",  # 🗃
    "reply": "↩",
    "label": "🗂",  # 🏷
    "previous_page": "⏪",
    "next_page": "⏩",
}

folders_by_page = 8


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
    try:
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
    except:
        logging.error("mark_read_email error")


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


def archive_email(bot, update):
    query = update.callback_query

    try:
        data = filter_callback_data(update, "/email/archive", 3)
        user_email = data[0]
        msg_uid = bytes(data[1], 'utf-8')
        folder = data[2]
        email_repo.get_emails_servers()[user_email].delete_from_folder(msg_uid, folder)

        previous_response = query.message.text_markdown
        bot.edit_message_text(parse_mode="Markdown",
                              text=previous_response+"\n\n"+emojis["archive"]+"Archived! "+emojis["archive"],
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
    except Exception as e:
        logging.error(e)
        logging.error("archive_email error")


def label_list_email(bot, update):
    query = update.callback_query

    try:
        data = filter_callback_data(update, "/email/label_l", 4)
        user_email = data[1]
        msg_uid = bytes(data[2], 'utf-8')
        page = data[0]
        folder = data[3]
        folders = email_repo.get_emails_servers()[user_email].get_folders()

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

        response, reply_markup = __load_main_view(user_email, msg_uid, folder)
        bot.edit_message_text(parse_mode="Markdown",
                              text=response + "+-",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=InlineKeyboardMarkup(body))
    except Exception as e:
        logging.error(e)
        logging.error("label_list_email error")


def delete_email(bot, update):
    query = update.callback_query

    try:
        data = filter_callback_data(update, "/email/delete", 3)
        user_email = data[0]
        msg_uid = bytes(data[1], 'utf-8')
        folder = data[2]

        email_repo.get_emails_servers()[user_email].add_to_folder(msg_uid, '[Gmail]/Trash')
        email_repo.get_emails_servers()[user_email].delete_from_folder(msg_uid, 'Inbox')

        previous_response = query.message.text_markdown

        bot.edit_message_text(parse_mode="Markdown",
                              text=previous_response+"\n\n"+emojis["delete"]+"Deleted! "+emojis["delete"],
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
    except Exception as e:
        logging.error(e)
        logging.error("delete_email error")


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

