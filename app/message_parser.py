import re

from telethon.tl.types import MessageEntityTextUrl


class MessageParser:

    @classmethod
    def parse(cls, message) -> dict:
        if message.message:
            text = cls.__clean(message.message)
            asset, amount = cls.__get_assets(text)
        else:
            text = message.message
            asset = 'unknown'
            amount = 0
        link = cls.__get_links(message)
        return {'id': message.id, 'message': text, 'link': link, 'posted_at': message.date, 'asset': asset,
                'amount': amount}

    @staticmethod
    def __get_links(message) -> str:
        if message.entities is not None:
            links = []
            for entity in message.entities:
                if isinstance(entity, MessageEntityTextUrl):
                    links.append(entity.url)
            if len(links) > 0:
                return '|'.join(links)
            else:
                return 'none'
        else:
            return 'none'

    @staticmethod
    def __clean(message: str) -> str:
        return message \
            .removesuffix('Details') \
            .replace('ℹ', '') \
            .replace('🚨', '') \
            .replace('🎁', '') \
            .replace('💰', '') \
            .replace('💤', '') \
            .replace('🔥', '') \
            .replace('💵', '') \
            .replace('⚠', '') \
            .replace('🔒', '') \
            .replace('🔓', '') \
            .replace('🎉', '') \
            .replace('💸', '') \
            .replace('💸', '') \
            .replace('🖼️', '') \
            .strip()

    @staticmethod
    def __get_assets(message: str):
        """
        This regular expression finds a sequence like "27,205 #ETH" in the
        text and extracts from it, at the same time, the amount (group 3) and
        type of asset (group 2)

        Sometimes, when the transaction is a donation, the message has a
        slightly different form, namely "A donation of 0.861 BTC (41,
        406 USD)". Then the first regular expression cannot find the amount
        and type of the asset, and we try to find them using another
        expression.
        """
        regexp = re.search(r"(([\d,.]+)\s#)([A-Z]+)", message)
        if regexp is not None:
            return regexp.group(3), regexp.group(2).replace(',', '')
        else:
            regexp = re.search(r"(([\d.]+)\s)([A-Z]+)\s", message)
            if regexp is not None:
                return regexp.group(3), regexp.group(2)
            else:
                return 'unknown', 0
