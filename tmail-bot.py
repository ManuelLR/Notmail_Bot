import logging
from telegram.ext import Updater
import click  # http://click.pocoo.org/6/
import services.email as email_service
import os

from commands import load_dispatcher

@click.command()
@click.option('--log_level', default="INFO", help='Level to log. [INFO, DEBUG]')
@click.option('--token', help='The bot token. Please talk with @BotFather')
@click.option('--refresh_inbox', help='The time between mail checks')
@click.option('--db_path', help='Path to db (could be empty)')
def init(log_level, token, refresh_inbox, db_path):

    # ============== LOGs ============
    log_formatter = logging.Formatter(fmt='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                                      datefmt='%d-%m-%y %H:%M:%S')

    logger = logging.getLogger()

    fileHandler = logging.FileHandler(os.path.join("config", "tmail-bot.log"))
    fileHandler.setFormatter(log_formatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(log_formatter)
    logger.addHandler(consoleHandler)

    if log_level != "INFO":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.setLevel(logging.DEBUG)

    logging.getLogger('telegram').setLevel(logging.INFO)

    # ================== BOT ==================

    # Create the Updater and pass it your bot's token.
    updater = Updater("token")
    load_dispatcher(updater.dispatcher)

    # Start the Bot
    updater.start_polling(read_latency=6)
    logging.error("Bot started")
    email_service.init_email_service(updater.bot)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    init()
