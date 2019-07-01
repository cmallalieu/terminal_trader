from model.orm import Sqlite3ORM
import time

class Trade(Sqlite3ORM):

    fields = ["ticker", "price", "time", "volume", "user_info_pk"]
    dbpath = "trader.db"
    dbtable = "trades"

    create_sql = """
    CREATE TABLE trades (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker VARCHAR(6) NOT NULL,
        time FLOAT,
        price FLOAT,
        volume INTEGER,
        user_info_pk INTEGER,
        FOREIGN KEY(user_info_pk) REFERENCES user_info(pk)
    )"""

    def __init__(self, **kwargs):
        self.pk = kwargs.get('pk')
        self.ticker = kwargs.get('ticker')
        self.volume = kwargs.get('volume')
        self.price = kwargs.get('price')
        self.time = kwargs.get('time', time.time())
        self.user_info_pk = kwargs.get('user_info_pk')

    def json(self):
        return {
            "ticker": self.ticker,
            "volume": self.volume,
            "price": self.price,
            "time": self.time
        }
