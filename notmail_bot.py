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
import logging
from telegram.ext import Updater
import click  # http://click.pocoo.org/6/
from services.email import init_email_service
from utils.scheduler import init_scheduler
from commands import load_dispatcher
from services import set_bot
from config.loadConfig import Config, get_config, set_config
from repository.repository import DBC, set_dbc

@click.command()
@click.option('--config_path', default=None, help='Path to config file. It overwrite all env variables')
@click.option('--token', help='The bot token. Please talk with @BotFather')
@click.option('--admin_user_id', help='The bot token. Please talk with @BotFather')
@click.option('--admin_username', help='The bot token. Please talk with @BotFather')
@click.option('--db_path', help='Path to db (could be empty)')
@click.option('--refresh_inbox', help='The time between mail checks')
@click.option('--log_level', help='Level to log. [INFO, DEBUG]')
@click.option('--log_path', help='The bot token. Please talk with @BotFather')
def init(config_path, token, admin_user_id, admin_username, db_path, refresh_inbox, log_level, log_path):

    set_config(Config())
    if config_path:
        get_config().load_config_file(config_path)
    get_config().load_config_variables(token, admin_user_id, admin_username, db_path, refresh_inbox, log_level, log_path)

    # ================== Initializer ==================
    set_dbc(DBC(path=get_config().db_path))
    init_scheduler()

    # ============== LOGs ============
    log_formatter = logging.Formatter(fmt='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                                      datefmt='%d-%m-%y %H:%M:%S')

    logger = logging.getLogger()

    if get_config().log_path is not None:
        fileHandler = logging.FileHandler(get_config().log_path)
        fileHandler.setFormatter(log_formatter)
        logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(log_formatter)
    logger.addHandler(consoleHandler)

    logger.setLevel(get_config().log_level)

    logging.getLogger('telegram').setLevel(logging.INFO)

    # ================== BOT ==================
    updater = Updater(get_config().telegram_token)
    load_dispatcher(updater.dispatcher)
    set_bot(updater.bot)

    # Start the Bot
    updater.start_polling(timeout=15, read_latency=6)
    logging.error("Bot started")
    init_email_service()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    init()
