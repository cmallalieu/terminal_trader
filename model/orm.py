import sqlite3

class Sqlite3ORM:
    fields = []
    dbpath = ""
    dbtable = ""
    create = ""

    def __init__(self):
        raise NotImplementedError
    
    def save(self):
        if self.pk is None:
            self._insert()
        else:
            self._update()

    @classmethod
    def _create_insert(cls):
        columnlist = ", ".join(cls.fields)
        qmarks = ", ".join("?" for val in cls.fields)
        SQL = """ INSERT INTO {tablename} ({columnlist})
        VALUES ({qmarks}) """
        return SQL.format(tablename=cls.dbtable, columnlist=columnlist, qmarks=qmarks)

    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            SQL = self._create_insert()
            propvals = [getattr(self, propname) for propname in self.fields]

            cur.execute(SQL, propvals)
            self.pk = cur.lastrowid
    
    @classmethod
    def _create_update(cls):
        """ TODO: IMPLEMENT THIS. Return a generic UPDATE SQL command like 
        _create_insert did. You will want to be updating WHERE pk = ? """
        # field=?
        update_column_list = ", ".join(field+"=?" for field in cls.fields)
        SQL = """
UPDATE {tablename} SET {update_column_list} WHERE pk = ?; """
        return SQL.format(tablename=cls.dbtable, update_column_list=update_column_list)
    
    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            SQL = self._create_update()
            propvals = [getattr(self, field) for field in self.fields + ["pk"]]
            cur.execute(SQL, propvals)
    
    @classmethod
    def one_where(cls, whereclause="TRUE", values=tuple()):
        SQL = "SELECT * FROM {tablename} WHERE " + whereclause
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute(SQL.format(tablename=cls.dbtable), values)
            row = cur.fetchone()
            if row is None:
                return None
            return cls(**row)
    
    @classmethod
    def many_where(cls, whereclause="TRUE", values=tuple()):
        """ equivalent of one_where but with fetchall, returns a list of objects or an
        empty list """
        SQL = "SELECT * FROM {tablename} WHERE " + whereclause
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute(SQL.format(tablename=cls.dbtable), values)
            rows = cur.fetchall()
            return [cls(**row) for row in rows]
    
    @classmethod
    def from_pk(cls, pk):
        return cls.one_where("pk=?", (pk,))
    
    @classmethod
    def all(cls):
        """ return a list of every row in the table as instances of the class """
        return cls.many_where()
    
    def delete(self):
        SQL = "DELETE FROM {tablename} WHERE pk=?"
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            cur.execute(SQL.format(tablename=self.dbtable), (self.pk,))
            self.pk = None

    def __repr__(self):
        reprstring = "<{cname} {fieldvals}>"
        # read over this:
        fieldvals = " ".join("{key}:{value}".format(key=key, value=getattr(self, key))
                             for key in ["pk", *self.fields])
        cname = type(self).__name__
        return reprstring.format(cname=cname, fieldvals=fieldvals)