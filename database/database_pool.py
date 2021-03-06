from psycopg2 import pool
import psycopg2.extras

class PostgreSql:
    def __init__(self):
        try:
            self.connectPool = pool.SimpleConnectionPool(2, 10, host="postgres", port="5432",
                                                         user="postgres", password="123456",
                                                         database="video_spider", keepalives=1,
                                                         keepalives_idle=30, keepalives_interval=10,
                                                         keepalives_count=5)
        except Exception as e:
            print(e)
    def get_connect(self):
        conn = self.connectPool.getconn()
        nt_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return conn, nt_cur

    def close_connect(self, conn, cursor):
        cursor.close()
        self.connectPool.putconn(conn)

    def close_all(self):
        self.connectPool.closeall()

    def execute(self, sql, value=None):
        conn, cursor = self.get_connect()
        try:
            res = cursor.execute(sql, value)
            conn.commit()
            self.close_connect(conn, cursor)
            return res
        except Exception as e:
            raise e

    def select_one(self, sql):
        conn, cursor = self.get_connect()
        cursor.execute(sql)
        result = cursor.fetchone()
        self.close_connect(conn, cursor)
        return result

    def select_all(self, sql):
        conn, cursor = self.get_connect()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.close_connect(conn, cursor)
        return result

    def select_by_ids(self, sql, param):
        conn, cursor = self.get_connect()
        cursor.execute(sql, param)
        result = cursor.fetchall()
        self.close_connect(conn, cursor)
        return result

    def count(self, sql, value=None):
        conn, cursor = self.get_connect()
        cursor.execute(sql, value)
        result = cursor.fetchone()
        self.close_connect(conn, cursor)
        return result[0]