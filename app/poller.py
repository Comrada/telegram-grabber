import asyncio
import logging
import os
from typing import List

import aiocron
from telethon import TelegramClient

from db_connector import DbConnector
from db_worker import DbWorker
from message_parser import MessageParser

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
phone_number = os.environ.get('PHONE_NUMBER')
channel_name = os.environ.get('CHANNEL_NAME')
session_id = os.environ.get('SESSION_ID', 'local')
cache = dict()
message_parser = MessageParser()


async def get_last_messages(client) -> List[dict]:
    messages = []
    async for message in client.iter_messages(entity=channel_name):
        message_object = message_parser.parse(message)
        if message.id not in cache:
            cache[message.id] = message_object
            messages.append(message_object)
        else:
            break
    return messages


async def poll_messages(client: TelegramClient, db_worker: DbWorker) -> None:
    messages = await get_last_messages(client)
    for mess in messages:
        db_worker.write_message(mess)


def warm_cache(db_worker: DbWorker) -> None:
    messages = db_worker.load_messages(10)
    if len(messages) == 0:
        messages = db_worker.load_last_messages(10)
    for message in messages:
        cache[message['id']] = message


async def main():
    db_connector = DbConnector(
        os.environ.get('DB_NAME'),
        os.environ.get('DB_USER'),
        os.environ.get('DB_PASS'),
        os.environ.get('DB_HOST', 'localhost'),
        os.environ.get('DB_PORT', 5432)
    )
    db_worker = DbWorker(db_connector)
    warm_cache(db_worker)
    async with TelegramClient(session_id, api_id, api_hash) as client:
        aiocron.crontab('*/10 * * * *', func=poll_messages, args=(client, db_worker,), start=True)
        while True:
            await asyncio.sleep(1)


asyncio.run(main())
