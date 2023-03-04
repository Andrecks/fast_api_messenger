import psycopg2
from decouple import config


class db_control:
    def __init__(self):
        print(f'database name = {config("db_name")}')
        self.conn = psycopg2.connect(database=config("db_name"), user=config("db_user"), password=config("db_password"), host=config("db_host"), port=config("db_port"))
        self.cur = self.conn.cursor()

    def check_user_exists(self, phone):
        self.cur.execute(f"SELECT * FROM users WHERE phone = '{phone}'")
        self.conn.commit()
        if self.cur.fetchone() is None:
            return False
        return True


# db_class = db_control()
# print(db_class.check_user_exists('123'))