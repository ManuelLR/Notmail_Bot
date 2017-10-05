import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import click  # http://click.pocoo.org/6/
import services.email as email_service

from commands import load_dispatcher


@click.command()
@click.option('--log_level', default="INFO", help='Level to log. [INFO, DEBUG]')
@click.option('--token', help='The bot token. Please talk with @BotFather')
@click.option('--refresh_inbox', help='The time between mail checks')
@click.option('--db_path', help='Path to db (could be empty)')
def init(log_level, token, refresh_inbox, db_path):
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                        datefmt='%d-%m-%y %H:%M:%S')

    logger = logging.getLogger()

    if log_level != "INFO":
        logger.setLevel(logging.DEBUG)

    logger.setLevel(logging.DEBUG)

    logging.getLogger('telegram').setLevel(logging.INFO)

    # Create the Updater and pass it your bot's token.
    updater = Updater("token")
    load_dispatcher(updater.dispatcher)

    # Start the Bot
    updater.start_polling()
    logging.error("Bot started")
    email_service.init_2(updater.bot)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    init()
