from model.orm import Sqlite3ORM

class Position(Sqlite3ORM):

    fields = ["ticker", "amount", "user_info_pk"]
    dbpath = "trader.db"
    dbtable = "positions"

    create_sql = """
    CREATE TABLE positions (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker VARCHAR(6) NOT NULL,
        amount INTEGER,
        user_info_pk INTEGER,
        FOREIGN KEY(user_info_pk) REFERENCES user_info(pk)
    )"""

    def __init__(self, **kwargs):
        self.pk = kwargs.get('pk')
        self.ticker = kwargs.get('ticker')
        self.amount = kwargs.get('amount', 0)
        self.user_info_pk = kwargs.get('user_info_pk')
    
    def json(self):
        return {
            "ticker": self.ticker,
            "amount": self.amount
        }