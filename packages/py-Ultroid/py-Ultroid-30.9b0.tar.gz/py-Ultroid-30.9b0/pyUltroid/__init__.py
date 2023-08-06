# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import os
import time
from datetime import datetime
from distutils.util import strtobool as sb
from logging import DEBUG, INFO, FileHandler, StreamHandler, basicConfig, getLogger

from decouple import config
from redis import ConnectionError, ResponseError, StrictRedis
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError
from telethon.sessions import StringSession

from .dB.core import *
from .dB.database import Var
from .misc import *
from .utils import *
from .version import __version__

LOGS = getLogger(__name__)

# remove the old logs file.
if os.path.exists("ultroid.log"):
    os.remove("ultroid.log")

# start logging into a new file.
basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=INFO,
    handlers=[FileHandler("ultroid.log"), StreamHandler()],
)

LOGS.info(
    """
                -----------------------------------
                        Starting Deployment
                -----------------------------------
"""
)


def connect_redis():
    redis_info = Var.REDIS_URI.split(":")
    DB = StrictRedis(
        host=redis_info[0],
        port=redis_info[1],
        password=Var.REDIS_PASSWORD,
        charset="utf-8",
        decode_responses=True,
    )
    return DB


try:
    udB = connect_redis()
    LOGS.info("Getting Connection With Redis Database")
    time.sleep(6)
except ConnectionError as ce:
    LOGS.info(f"ERROR - {ce}")
    exit(1)
except ResponseError as res:
    LOGS.info(f"ERROR - {res}")
    exit(1)
except Exception as er:
    LOGS.info(f"ERROR - {er}")
    exit(1)

START_TIME = datetime.now()

try:
    udB.ping()
except BaseException:
    ok = []
    LOGS.info("Can't connect to Redis Database.... Restarting....")
    for x in range(1, 6):
        udB = connect_redis()
        time.sleep(5)
        try:
            if udB.ping():
                ok.append("ok")
                break
        except BaseException:
            LOGS.info(f"Connection Failed ...  Trying To Reconnect {x}/5 ..")
    if not ok:
        LOGS.info("Redis Connection Failed.....")
        exit(1)
    else:
        LOGS.info("Reconnected To Redis Server Succesfully")

LOGS.info("Succesfully Established Connection With Redis DataBase.")

if os.path.exists("client-session.session"):
    _session = "client-session"
elif Var.SESSION:
    _session = StringSession(Var.SESSION)
else:
    LOGS.info("No String Session found. Quitting...")
    exit(1)

try:
    ultroid_bot = TelegramClient(_session, Var.API_ID, Var.API_HASH)
except Exception as ap:
    LOGS.info(f"ERROR - {ap}")
    exit(1)

if udB.get("HNDLR"):
    HNDLR = udB.get("HNDLR")
else:
    udB.set("HNDLR", ".")
    HNDLR = udB.get("HNDLR")

if not udB.get("SUDO"):
    udB.set("SUDO", "False")

if not udB.get("SUDOS"):
    udB.set("SUDOS", "777000")

if not udB.get("BLACKLIST_CHATS"):
    udB.set("BLACKLIST_CHATS", "[]")

if udB.get("VC_SESSION"):
    try:
        vcbot = TelegramClient(
            StringSession(udB.get("VC_SESSION")),
            api_id=Var.API_ID,
            api_hash=Var.API_HASH,
        )
    except AuthKeyDuplicatedError:
        LOGS.info("ERROR - Please create a new VC string Session !")
        vcbot = None
    except Exception:
        vcbot = None
else:
    vcbot = None
