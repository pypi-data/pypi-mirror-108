# -*- coding: utf-8 -*-

import os
import sys
import json
import errno
import datetime

from loguru import logger
from dotenv import load_dotenv


class Rotator:
    def __init__(self, *, size: int, at: datetime.time):
        _now = datetime.datetime.now()
        self._size_limit = size
        self._time_limit = _now.replace(hour=at.hour, minute=at.minute, second=at.second)

        if self._time_limit <= _now:
            # The current time is already past the target time so it would rotate already.
            # Add one day to prevent an immediate rotation.
            self._time_limit += datetime.timedelta(days=1)

    def should_rotate(self, message, file):
        file.seek(0, 2)
        if self._size_limit < (file.tell() + len(message)):
            return True

        if self._time_limit.timestamp() < message.record["time"].timestamp():
            self._time_limit += datetime.timedelta(days=1)
            return True
        return False


## Filter for adding short level name:
def _add_lvlname(record: dict):
    record['lvlname'] = record['level'].name
    if record['level'].name == 'SUCCESS':
        record['lvlname'] = 'OK'
    elif record['level'].name == 'WARNING':
        record['lvlname'] = 'WARN'
    elif record['level'].name == 'CRITICAL':
        record['lvlname'] = 'CRIT'
    return record

## Printing message based on log level to stdout or stderr:
def _std_sink(message):
    if message.record["level"].no < 40:
        sys.stdout.write(message)
    else:
        sys.stderr.write(message)


## Checking logger module already exists or not:
if os.getenv('__INIT_LOG_HANDLER_ID__') is None:
    ## Loading environment variables from .env file, if it's exits:
    _env_filename = '.env'
    _current_dir = os.getcwd()
    _env_file_path = os.path.join(_current_dir, _env_filename)
    if os.path.isfile(_env_file_path):
        load_dotenv(dotenv_path=_env_file_path, override=True)

    ## Options for loggers
    _USE_COLOR = True
    _USE_BACKTRACE = True
    _STD_FORMAT_STR = '[<c>{time:YYYY-MM-DD HH:mm:ss.SSS Z}</c> | <level>{lvlname:<5}</level> | <w>{file}</w>:<w>{line}</w>]: <level>{message}</level>'
    _FILE_FORMAT_STR = '[{time:YYYY-MM-DD HH:mm:ss.SSS Z} | {lvlname:<5} | {file}:{line}]: {message}'
    _ROTATE_WHEN = datetime.time(0, 0, 0) # At midnight every day
    _ROTATE_FILE_SIZE = 10 * 1000 * 1000 # Max size for each file: 10MB
    _BACKUP_FILE_COUNT = 50
    _FILE_ENCODING = 'utf8'
    _ALL_LOG_FILENAME = '{app_name}.std.all.log'
    _ERR_LOG_FILENAME = '{app_name}.std.err.log'
    _JSON_ALL_LOG_FILENAME = '{app_name}.json.all.log'
    _JSON_ERR_LOG_FILENAME = '{app_name}.json.err.log'

    ## Loading configs from file, if it's exits:
    _configs_file_path = os.path.join(_current_dir, 'configs', 'logger.json')
    if os.path.isfile(_configs_file_path):
        _json_configs = {}
        try:
            with open(_configs_file_path, 'r') as _json_configs_file:
                _json_configs = json.load(_json_configs_file)
                _USE_COLOR = _json_configs['use_color']
                _USE_BACKTRACE = _json_configs['use_backtrace']
                _STD_FORMAT_STR = _json_configs['std_format_str']
                _FILE_FORMAT_STR = _json_configs['file_format_str']
                _AT_HOUR = _json_configs['rotate_when']['at_hour']
                _AT_MINUTE = _json_configs['rotate_when']['at_minute']
                _AT_SECOND = _json_configs['rotate_when']['at_second']
                _ROTATE_WHEN = datetime.time(_AT_HOUR, _AT_MINUTE, _AT_SECOND)
                _ROTATE_FILE_SIZE = _json_configs['rotate_file_size']
                _BACKUP_FILE_COUNT = _json_configs['backup_file_count']
                _FILE_ENCODING = _json_configs['file_encoding']
                _ALL_LOG_FILENAME = _json_configs['all_log_filename']
                _ERR_LOG_FILENAME = _json_configs['err_log_filename']
                _JSON_ALL_LOG_FILENAME = _json_configs['json_all_log_filename']
                _JSON_ERR_LOG_FILENAME = _json_configs['json_err_log_filename']
        except Exception:
            logger.exception(f"Failed to load '{_configs_file_path}' configs file.")
            exit(2)

    ## Checking environment for DEBUG option:
    _ENV = str(os.getenv('ENV')).strip().lower()
    _DEBUG = str(os.getenv('DEBUG')).strip().lower()
    _is_debug = False
    if (_DEBUG == 'true') or ((_ENV == 'development') and ((_DEBUG == 'none') or (_DEBUG == ''))):
        _is_debug = True
        os.environ['DEBUG'] = 'true'

    _level = 'INFO'
    _use_diagnose = False
    if _is_debug:
        _level = 'DEBUG'
        _use_diagnose = True

    # if _USE_COLOR:
    #     ## Checking terminal could support xterm colors:
    #     _TERM = str(os.getenv('TERM'))
    #     if (_TERM != 'xterm') and (_TERM != 'xterm-16color') and (_TERM != 'xterm-88color') and (_TERM != 'xterm-256color'):
    #         _USE_COLOR = False

    ## Initializing std stream log handler:
    logger.remove()
    _log_handler_id = logger.add(_std_sink,
                                level=_level,
                                format=_STD_FORMAT_STR,
                                colorize=_USE_COLOR,
                                filter=_add_lvlname,
                                backtrace=_USE_BACKTRACE,
                                diagnose=_use_diagnose)

    ## Checking required environment variables for logger module:
    # _required_envs = ['APP_NAME', 'LOGS_DIR']
    # for _env in _required_envs:
    #     try:
    #         os.environ[_env]
    #     except Exception:
    #         logger.exception(f"Not found '{_env}' environment variable.")
    #         exit(2)

    _APP_NAME = str(os.getenv('APP_NAME')).strip().replace(' ', '_').lower()
    if _APP_NAME == 'none':
        _APP_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        logger.debug(f"Not found 'APP_NAME' environment variable, changed to '{_APP_NAME}'.")

    _ENABLE_LOG_FILE = (os.getenv('ENABLE_LOG_FILE', 'true').strip().lower() == 'true')
    _ENABLE_LOG_JSON = (os.getenv('ENABLE_LOG_JSON', 'false').strip().lower() == 'true')
    if _ENABLE_LOG_FILE or _ENABLE_LOG_JSON:

        _LOGS_DIR = str(os.getenv('LOGS_DIR')).strip()
        if _LOGS_DIR == 'None':
            _LOGS_DIR = os.path.join(_current_dir, 'logs')
            logger.debug(f"Not found 'LOGS_DIR' environment variable, changed to '{_LOGS_DIR}'.")

        if not os.path.isdir(_LOGS_DIR):
            logger.warning(f"'{_LOGS_DIR}' directory doesn't exist!")
            try:
                os.makedirs(_LOGS_DIR)
            except Exception as err:
                if err.errno == errno.EEXIST:
                    logger.info(f"'{_LOGS_DIR}' directory already exists.")
                else:
                    logger.exception(f"Failed to create '{_LOGS_DIR}' directory.")
                    exit(2)
            logger.success(f"Successfully created '{_LOGS_DIR}' directory!")

        if _ENABLE_LOG_FILE:
            ## Initializing log file handler:
            _out_rotator = Rotator(size=_ROTATE_FILE_SIZE, at=_ROTATE_WHEN)
            _log_file_path = os.path.join(_LOGS_DIR, _ALL_LOG_FILENAME.format(app_name=_APP_NAME))
            logger.add(_log_file_path,
                        level=_level,
                        format=_FILE_FORMAT_STR,
                        rotation=_out_rotator.should_rotate,
                        retention=_BACKUP_FILE_COUNT,
                        encoding=_FILE_ENCODING,
                        enqueue=True,
                        backtrace=_USE_BACKTRACE,
                        diagnose=_use_diagnose)

            ## Initializing error log file handler:
            _err_rotator = Rotator(size=_ROTATE_FILE_SIZE, at=_ROTATE_WHEN)
            _log_file_path = os.path.join(_LOGS_DIR, _ERR_LOG_FILENAME.format(app_name=_APP_NAME))
            logger.add(_log_file_path,
                        level='WARNING',
                        format=_FILE_FORMAT_STR,
                        rotation=_err_rotator.should_rotate,
                        retention=_BACKUP_FILE_COUNT,
                        encoding=_FILE_ENCODING,
                        enqueue=True,
                        backtrace=_USE_BACKTRACE,
                        diagnose=_use_diagnose)

        if _ENABLE_LOG_JSON:
            ## Initializing json log file handler:
            _json_out_rotator = Rotator(size=_ROTATE_FILE_SIZE, at=_ROTATE_WHEN)
            _log_file_path = os.path.join(_LOGS_DIR, _JSON_ALL_LOG_FILENAME.format(app_name=_APP_NAME))
            logger.add(_log_file_path,
                        level=_level,
                        format='',
                        serialize=True,
                        rotation=_json_out_rotator.should_rotate,
                        retention=_BACKUP_FILE_COUNT,
                        encoding=_FILE_ENCODING,
                        enqueue=True,
                        backtrace=_USE_BACKTRACE,
                        diagnose=_use_diagnose)

            ## Initializing json error log file handler:
            _json_err_rotator = Rotator(size=_ROTATE_FILE_SIZE, at=_ROTATE_WHEN)
            _log_file_path = os.path.join(_LOGS_DIR, _JSON_ERR_LOG_FILENAME.format(app_name=_APP_NAME))
            logger.add(_log_file_path,
                        level='WARNING',
                        format='',
                        serialize=True,
                        rotation=_json_err_rotator.should_rotate,
                        retention=_BACKUP_FILE_COUNT,
                        encoding=_FILE_ENCODING,
                        enqueue=True,
                        backtrace=_USE_BACKTRACE,
                        diagnose=_use_diagnose)

    ## Setting checkpoint environment variable for initializing logger.
    os.environ['__INIT_LOG_HANDLER_ID__'] = str(_log_handler_id)
