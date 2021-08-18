import os
from telegram.ext import (
    Updater, 
    CallbackContext, 
    Filters,
    MessageHandler,
    CommandHandler
)
from telegram import (
    Update,
    ParseMode,
    Bot
)

import logging
import re
# import yaml
import arrow
from random import randint, random
from difflib import SequenceMatcher
from api_utils import AnecdotRuApi, BaneksApi, PiroshkiApi, RedditMemeApi


# logging.basicConfig(
#     format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s",
#     level=logging.INFO,
#     handlers=[
#         logging.StreamHandler(),
#         # logging.FileHandler("chebanina_bot.log")
#     ]
# )
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
dev_ids = [40322523]


def reply_anecdote(update: Update, context: CallbackContext) -> None:
    txt = update.message.text.lower()
    target = "анекдот"
    match = SequenceMatcher(None, target, txt).find_longest_match(0, len(target), 0, len(txt))
    matched = match.size/len(target)
    if random()>(matched-0.2):
        return None
      
    anekdote = "Никаких тебе шуточек, дрочила!"
    try:
        anekdote = BaneksApi().get_random_anecdote()
    except:
        anekdote = AnecdotRuApi().get_random_anecdote(1)
    update.message.reply_text(
        anekdote,
        quote=True
    )
    logger.info(
        "Send joke in chat {0} from user {1} with text {2}...".format(
            update.effective_chat.title or update.effective_user.username,
            update.effective_user.username,
            anekdote[:30]
        )
    )


def reply_pirozhok(update: Update, context: CallbackContext) -> None:
    if random()<0.3:
        page_num = randint(1, 100)
        offset = randint(0, 29)
        try:
            anekdote = PiroshkiApi().get_random_anecdote(
                page_num=page_num,
                offset=offset
            )
        except:
            raise
        update.message.reply_text(
            anekdote,
            quote=True
        )
        logger.info(
            "Send joke in chat {0} from user {1} with text {2}...".format(
                update.effective_chat.title or update.effective_user.username,
                update.effective_user.username,
                anekdote[:30]
            )
        )


def reply_meme(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id in dev_ids:
        meme = RedditMemeApi().get_random_meme()
        update.message.reply_text(
            meme,
            quote=True
        )
        logger.info(
            "Send meme in chat {0} from user {1} with text {2}...".format(
                update.effective_chat.title or update.effective_user.username,
                update.effective_user.username,
                meme
            )
        )


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "hello yoba",
        quote=True
    )
    

def setup(token):
    bot = Bot(token=token)
    updater = Updater(bot=bot, use_context=True)
    dispatcher = updater.dispatcher  
    dispatcher.add_handler(CommandHandler("start", start))
    anekdote_pat = re.compile(r'ане', re.IGNORECASE)
    pirozhok_pat = re.compile(r'п+.*р+.*(ж|ш)+', re.IGNORECASE)
    meme_pat = re.compile(r'\s?мем.*', re.IGNORECASE)   
    dispatcher.add_handler(MessageHandler(Filters.regex(anekdote_pat), reply_anecdote))
    dispatcher.add_handler(MessageHandler(Filters.regex(pirozhok_pat), reply_pirozhok))
    dispatcher.add_handler(MessageHandler(Filters.regex(meme_pat), reply_meme))

    return dispatcher