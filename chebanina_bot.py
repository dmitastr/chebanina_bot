import os
from telegram.ext import (
    Updater, 
    CallbackContext, 
    Filters,
    MessageHandler,
    CommandHandler,
    Defaults
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
from api_utils import AnecdotRuApi, BaneksApi, PiroshkiApi, RedditMemeApi, DemotivationMeApi


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
dev_ids = [40322523]
demand_pat = re.compile(r'chebaninabot', re.IGNORECASE)
anekdote_pat = re.compile(r'ане', re.IGNORECASE)
pirozhok_pat = re.compile(r'п+.*р+.*(ж|ш)+', re.IGNORECASE)
meme_pat = re.compile(r'\s?мем.*', re.IGNORECASE) 
demot_pat = re.compile(r'\s?дем.*', re.IGNORECASE) 

Defaults.timeout = 6000

def reply_on_demand(update: Update, context: CallbackContext) -> None:
    logger.info(
        "Demand joke in chat {0} from user {1}".format(
            update.effective_chat.title or update.effective_user.username,
            update.effective_user.username
        )
    )
    txt = update.message.text
    if "@ChebaninaBot" in txt:
        anekdote = "Никаких тебе шуточек, дрочила!"
        if anekdote_pat.search(txt):
            try:
                anekdote = BaneksApi().get_random_anecdote()
            except:
                anekdote = AnecdotRuApi().get_random_anecdote(1)
        elif meme_pat.search(txt):
            subreddit = "dankmemes"
            if (
                "ебан" in txt
                or "сме" in txt
                or "ёбн" in txt
                or "пид" in txt
            ):
                subreddit = "darkmemers"
            anekdote = RedditMemeApi().get_random_meme(subreddit=subreddit)
        elif demot_pat.search(txt):
            anekdote = DemotivationMeApi().get_random_demotivator()
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
    logger.info(
        "Demand pirozhok in chat {0} from user {1}".format(
            update.effective_chat.title or update.effective_user.username,
            update.effective_user.username
        )
    )
    if random()<0.05:
        page_num = randint(1, 100)
        offset = randint(0, 29)
        try:
            anekdote = PiroshkiApi().get_random_anecdote(
                page_num=page_num,
                offset=offset
            )
        except:
            raise ValueError
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
    dispatcher.add_handler(
        MessageHandler(
            Filters.regex(demand_pat), 
            reply_on_demand
        )
    )
    dispatcher.add_handler(
        MessageHandler(
            Filters.regex(pirozhok_pat), 
            reply_pirozhok
        )
    )

    return dispatcher