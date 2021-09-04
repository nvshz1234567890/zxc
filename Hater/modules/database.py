from sqlite3 import connect


class Database:

    def __init__(self, database: str):

        self.database = database

        print("[DATABASE]: инициализирован")

    def init_database(self):

        with connect(self.database) as connection:

            cursor = connection.cursor()
            cursor.execute("SELECT path FROM base")

            result = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return result

    def check_hate(self, id):

        with connect(self.database) as connection:

            cursor = connection.cursor()
            cursor.execute("SELECT count(id) FROM conversations WHERE id = %d" % id)

            result = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if result == 0:
            return False

        if result == 1:
            return True

    def get_all_users(self):

        with connect(self.database) as connection:

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM conversations")

            result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result

    def add_hate(self, id):

        with connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT  INTO conversations(id) VALUES (%d)" % id)

            connection.commit()

        cursor.close()
        connection.close()

    def del_hate(self, id):

        with connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM conversations WHERE id = %d" % id)

            connection.commit()

        cursor.close()
        connection.close()
