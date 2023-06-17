from database import DBManager, Database
import os


db = Database()
dbm = DBManager()


if __name__ == "__main__":
    # У меня Linux Ubuntu, поэтому я использую слово "clear".
    # Если у тебя Windows то пиши "cls"
    os.system("clear")

    db.create_the_table()
    db.fill_the_table()

    dbm.database_manager()
