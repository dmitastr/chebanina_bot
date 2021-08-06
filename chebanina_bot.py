from telegram.ext import (
    Updater, 
    CallbackContext, 
    Filters,
    MessageHandler,
    CommandHandler
)
from telegram import (
    Update,
    ParseMode
)

import logging
import re
import yaml
import arrow
from random import randint, random
from difflib import SequenceMatcher
from api_utils import AnecdotRuApi, BaneksApi, PiroshkiApi


logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("chebanina_bot.log")
    ]
)
logger = logging.getLogger(__name__)
with open("config.yml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

BOT_TOKEN = config["bot_token"]
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


def set_config(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id in dev_ids:
        context.bot_data["probalility"] = float("".join(context.args))
        prob = context.bot_data["probalility"]
        update.message.reply_text("Probability of getting a joke is {0}".format(prob))


def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher  
    anekdote_pat = re.compile(r'ане', re.IGNORECASE)
    pirozhok_pat = re.compile(r'п+.*р+.*(ж|ш)+', re.IGNORECASE)
    dispatcher.add_handler(MessageHandler(Filters.regex(anekdote_pat), reply_anecdote))
    dispatcher.add_handler(MessageHandler(Filters.regex(pirozhok_pat), reply_pirozhok))
    dispatcher.add_handler(CommandHandler("upd", set_config, pass_args=True))

    job_queue = updater.job_queue

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

