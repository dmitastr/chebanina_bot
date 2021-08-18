import os
import json
from telegram import Update, TelegramObject
from chebanina_bot import setup

dispatcher = setup(token=os.environ.get("BOT_TOKEN"))

def handler(event, context):
    dispatcher.process_update(
        Update.de_json(json.loads(event["body"]), dispatcher.bot)
    )
    
    return {
        'statusCode': 200,
        'body': 'Hello World!',
    }

