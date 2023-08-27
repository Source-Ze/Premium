import os
from os import getenv
from dotenv import load_dotenv
if os.path.exists("local.env"):
load_dotenv("local.env")
load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME","BACVlPpYz3HbyVGGbEuCTjImdjf_kOoWhvusBNgKWAMcfOBjttR6xC4Mts52kR6GOx_B32dIu4Ee8jdcZ5ZVnTWr412EtjLcAo0KcLSfpTC7B-X3S9KVtyEp1Qj-mxpUik6LFTP5XWjfNreQLhGK6UylTHnIDDXOeQGSibAHEWuebSG_2kZxX3zjBDAxKOC8TdTKYFi1GCHHv1fWP3W1Bqx6e9kptnI-ii7XZcB6BBTgRg_G2NM0FYZ03BWgqRytlYKrawgDqGSt5vuxdy0Q6Xywx9CzjWa6MB7qrPX6QWDeeIxpi0WPuh_8weW_C7jlVyWnoqQnAQtuC0SRtr_fR3RZAAAAAUK_EDAA")
BOT_TOKEN = getenv("BOT_TOKEN","5575043797:AAGVf55-dFr9DTDZb5EZBWCoZeObK5MJk6U")
API_ID = int(getenv("API_ID","21627756"))
MONGODB_URL = getenv("MONGODB_URL")
API_HASH = getenv("API_HASH","0460ce261e766e2fbe4c740518f91192")
OWNER_NAME = getenv("OWNER_NAME", "UP_UI")
MONGODB_URL = getenv("MONGODB_URL")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "UI_XB")
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/file/4c7636b9c50116387d9f6.jpg")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "240"))
UPSTREAM_REPO = getenv("UPSTREAM_REPO")
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/d6f92c979ad96b2031cba.png")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/6213d2673486beca02967.png")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/f02efde766160d3ff52d6.png")
FORCE_SUBSCRIBE_TEXT = getenv("SUBSCRIBE_TEXT", f"عليك الاشتراك في قناة البوت لتتمكن من استخدامة \n- @{UPDATES_CHANNEL}")
SUBSCRIBE = getenv("SUBSCRIBE", "no")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "5650717789").split()))
