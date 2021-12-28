import logging
from datetime import timedelta, datetime
from typing import List, Optional, Any

from psycopg2.extras import RealDictRow

from db_connector import DbConnector


class DbWorker:

    def __init__(self, connector: DbConnector):
        self.connector = connector

    def load_messages(self, days: int = 1) -> Optional[List[Any]]:
        from_date = datetime.now() - timedelta(days=days)
        sql = '''
        SELECT wa.id, wa.message, wa.link, wa.posted_at, wa.asset, wa.amount from whale_alerts wa
        WHERE wa.posted_at >= '{from_date}'
        '''.format(from_date=from_date.strftime('%Y-%m-%d %H:%M:%S'))
        return self.__map_rows_to_objects(self.connector.select(sql))

    def load_last_messages(self, count: int) -> Optional[List[Any]]:
        sql = '''
        SELECT wa.id, wa.message, wa.link, wa.posted_at, wa.asset, wa.amount from whale_alerts wa
        ORDER BY wa.id DESC
        LIMIT {limit}
        '''.format(limit=count)
        return self.__map_rows_to_objects(self.connector.select(sql))

    def write_message(self, mess: dict):
        sql = '''
    INSERT INTO
      whale_alerts(id, message, link, posted_at, asset, amount)
    VALUES
      ({id}, '{message}', '{link}', '{posted_at}', '{asset}', '{amount}')
      ON CONFLICT DO NOTHING;
    '''.format(id=mess['id'], message=mess['message'], link=mess['link'], posted_at=mess['posted_at'],
               asset=mess['asset'], amount=mess['amount'])
        logging.info('New record: ' + mess['message'])
        self.connector.execute(sql)

    @staticmethod
    def __map_rows_to_objects(rows: Optional[List[RealDictRow]]) -> Optional[List[Any]]:
        """
        Simple dictionary mapping of type RealDictRow to regular array
        """
        messages = []
        for record in rows:
            messages.append({
                'id': record['id'],
                'text': record['message'],
                'link': record['link'],
                'posted_at': record['posted_at'],
                'asset': record['asset'],
                'amount': record['amount']
            })
        return messages
