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
import os, tempfile, errno, sys
import logging
from configparser import ConfigParser


# Solo cargará las variables del archivo de configuración si se especifica el archivo al lanzar el programa

global_config = None


class Config:
    def __init_empty_vars(self):
        self.telegram_token = None
        self.telegram_admin_user_id = None
        self.telegram_admin_username = None
        self.default_refresh_inbox = None
        self.log_path = None
        self.db_path = None
        self.log_level = None

    def __init__(self):
        self.__init_empty_vars()
        # ========  Telegram
        self.__set_telegram_token(os.getenv('TELEGRAM_TOKEN', ""))
        self.__set_telegram_admin_user_id(os.getenv('TELEGRAM_ADMIN_USER_ID', ""))
        self.__set_telegram_admin_username(os.getenv('TELEGRAM_ADMIN_USERNAME', ""))

        # ========  Database
        self.__set_db_path(os.getenv('TMAIL_DB_PATH', os.path.join("my-config", "notmail_bot-db.json")))

        # ========  Email
        self.__set_default_refresh_inbox(os.getenv('TMAIL_DEFAULT_REFRESH_TIME', 4 * 60))  # 4 minutos

        # ========  Log
        self.__set_log_level(os.getenv('TMAIL_LOG_LEVEL', "INFO"))
        self.__set_log_path(os.getenv('TMAIL_LOG_PATH', None))

    def load_config_file(self, path):
        if not is_path_exists_or_creatable_portable(path):
            raise AssertionError
        config = ConfigParser()
        config.read(path)

        self.__set_telegram_token(self.__lod(config, 'Telegram', 'TOKEN', self.telegram_token))
        self.__set_telegram_admin_username(self.__lod(config, 'Telegram', 'ADMIN_USERNAME', self.telegram_admin_username))
        self.__set_telegram_admin_user_id(self.__lod(config, 'Telegram', 'ADMIN_USER_ID', self.telegram_admin_user_id))

        self.__set_db_path(self.__lod(config, 'Database', 'PATH', self.db_path))

        self.__set_default_refresh_inbox(self.__lod(config, 'Email', 'DEFAULT_REFRESH_TIME', self.default_refresh_inbox))

        self.__set_log_level(self.__lod(config, 'Log', 'LOG_LEVEL', self.log_level))
        self.__set_log_path(self.__lod(config, 'Log', 'LOG_PATH', self.log_path))

    def load_config_variables(self, token, admin_user_id, admin_username, db_path, refresh_inbox, log_level, log_path):
        self.__set_telegram_token(self.__lov(token, self.telegram_token))
        self.__set_telegram_admin_username(self.__lov(admin_user_id, self.telegram_admin_username))
        self.__set_telegram_admin_user_id(self.__lov(admin_username, self.telegram_admin_user_id))

        self.__set_db_path(self.__lov(db_path, self.db_path))

        self.__set_default_refresh_inbox(self.__lov(refresh_inbox, self.default_refresh_inbox))

        self.__set_log_level(self.__lov(log_level, self.log_level))
        self.__set_log_path(self.__lov(log_path, self.log_path))

    @staticmethod
    def __lod(config, section, key, default_value=None):
        if config.has_option(section, key):
            return config[section][key]
        else:
            return default_value

    @staticmethod
    def __lov(var, default_value=None):
        if var:
            return var
        else:
            return default_value

    def __set_telegram_token(self, inp):
        if not isinstance(inp, str):
            raise AssertionError
        self.telegram_token = inp

    def __set_telegram_admin_user_id(self, inp):
        if not isinstance(inp, str):
            raise AssertionError
        self.telegram_admin_user_id = inp

    def __set_telegram_admin_username(self, inp):
        if not isinstance(inp, str):
            raise AssertionError
        self.telegram_admin_username = inp

    def __set_default_refresh_inbox(self, inp):
        if isinstance(inp, str):
            inp = int(inp)
        if not isinstance(inp, int):
            raise AssertionError
        self.default_refresh_inbox = inp

    def __set_log_level(self, inp):
        level = logging. _nameToLevel.get(inp)
        if level is None:
            if logging._levelToName.get(inp) is None:
                raise AssertionError
            else:
                self.log_level = inp
        else:
            self.log_level = level

    def __set_log_path(self, inp):
        if not is_path_exists_or_creatable_portable(inp):
            return
        self.log_path = inp

    def __set_db_path(self, inp):
        if not is_path_exists_or_creatable_portable(inp):
            raise AssertionError
        self.db_path = inp


def get_config():
    return global_config


def set_config(conf):
    global global_config
    global_config = conf

# ------------ https://stackoverflow.com/a/34102855

# Sadly, Python fails to provide the following magic number for us.
ERROR_INVALID_NAME = 123

'''
Windows-specific error code indicating an invalid pathname.

See Also
----------
https://msdn.microsoft.com/en-us/library/windows/desktop/ms681382%28v=vs.85%29.aspx
    Official listing of all such codes.
'''
def is_pathname_valid(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    '''
    # If this pathname is either not a string or is but is empty, this pathname
    # is invalid.
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`)
        # if any. Since Windows prohibits path components from containing `:`
        # characters, failing to strip this `:`-suffixed prefix would
        # erroneously invalidate all valid absolute Windows pathnames.
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            # If an OS-specific exception is raised, its error code
            # indicates whether this pathname is valid or not. Unless this
            # is the case, this exception implies an ignorable kernel or
            # filesystem complaint (e.g., path not found or inaccessible).
            #
            # Only the following exceptions indicate invalid pathnames:
            #
            # * Instances of the Windows-specific "WindowsError" class
            #   defining the "winerror" attribute whose value is
            #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
            #   fine-grained and hence useful than the generic "errno"
            #   attribute. When a too-long pathname is passed, for example,
            #   "errno" is "ENOENT" (i.e., no such file or directory) rather
            #   than "ENAMETOOLONG" (i.e., file name too long).
            # * Instances of the cross-platform "OSError" class defining the
            #   generic "errno" attribute whose value is either:
            #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
            #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    # If a "TypeError" exception was raised, it almost certainly has the
    # error message "embedded NUL character" indicating an invalid pathname.
    except TypeError as exc:
        return False
    # If no exception was raised, all path components and hence this
    # pathname itself are valid. (Praise be to the curmudgeonly python.)
    else:
        return True
    # If any other exception was raised, this is an unrelated fatal issue
    # (e.g., a bug). Permit this exception to unwind the call stack.
    #
    # Did we mention this should be shipped with Python already?


def is_path_creatable(pathname: str) -> bool:
    '''
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    '''
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)


def is_path_exists_or_creatable(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS _and_
    either currently exists or is hypothetically creatable; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    '''
    try:
        # To prevent "os" module calls from raising undesirable exceptions on
        # invalid pathnames, is_pathname_valid() is explicitly called first.
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_creatable(pathname))
    # Report failure on non-fatal filesystem complaints (e.g., connection
    # timeouts, permissions issues) implying this path to be inaccessible. All
    # other exceptions are unrelated fatal issues and should not be caught here.
    except OSError:
        return False


def is_path_sibling_creatable(pathname: str) -> bool:
    '''
    `True` if the current user has sufficient permissions to create **siblings**
    (i.e., arbitrary files in the parent directory) of the passed pathname;
    `False` otherwise.
    '''
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()

    try:
        # For safety, explicitly close and hence delete this temporary file
        # immediately after creating it in the passed path's parent directory.
        with tempfile.TemporaryFile(dir=dirname): pass
        return True
    # While the exact type of exception raised by the above function depends on
    # the current version of the Python interpreter, all such types subclass the
    # following exception superclass.
    except EnvironmentError:
        return False


def is_path_exists_or_creatable_portable(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname on the current OS _and_
    either currently exists or is hypothetically creatable in a cross-platform
    manner optimized for POSIX-unfriendly filesystems; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    '''
    try:
        # To prevent "os" module calls from raising undesirable exceptions on
        # invalid pathnames, is_pathname_valid() is explicitly called first.
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_sibling_creatable(pathname))
    # Report failure on non-fatal filesystem complaints (e.g., connection
    # timeouts, permissions issues) implying this path to be inaccessible. All
    # other exceptions are unrelated fatal issues and should not be caught here.
    except OSError:
        return False
