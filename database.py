from get_data import HeadHunter
import psycopg2
import utils as u


hh = HeadHunter()


class Database:
    def __init__(self):
        self.data = hh.get_data_dict()
        self.con = psycopg2.connect(
            host="localhost",
            database="hh_database",
            user="postgres",
            password=u.password
        )
        self.cur = self.con.cursor()

    def create_the_table(self):
        """ В этом блоке мы создаём таблицу, перед этим очищая её """
        with self.con as con:
            with con.cursor() as cur:
                cur.execute(f"DROP TABLE IF EXISTS total_database;")
                cur.execute(
                    f"""CREATE TABLE total_database (
                        company_id int,
                        company_name text,
                        vacation_name text,
                        salary_from int,
                        salary_to int,
                        salary_currency varchar(4),
                        professional_roles varchar(64),
                        experience varchar(32),
                        employment varchar(32),
                        snippet text,
                        url text,
                        address varchar(64) );"""
                )
                print("База данных создана")

    def fill_the_table(self):
        """ Функция для заполнения БД данными из API """

        company_id = 1
        for company in self.data:
            with self.con as con:
                with con.cursor() as cur:
                    for item in company["vacancies"]:

                        if item["salary_from"] is None:
                            salary_from = "NULL"
                        else:
                            salary_from = item["salary_from"]

                        if item["salary_to"] is None:
                            salary_to = "NULL"
                        else:
                            salary_to = item["salary_to"]

                        if item["salary_currency"] is None:
                            salary_currency = "NULL"
                        else:

                            salary_currency = item["salary_currency"]

                        if item["address"] is not None:
                            address = f"'{item['address']}'"
                        else:
                            address = "NULL"

                        cur.execute(
                            f"""INSERT INTO total_database
                            VALUES(
                                {company_id},
                                '{company["name"]}',
                                '{item["vacation_name"]}',
                                {salary_from},
                                {salary_to},
                                '{salary_currency}',
                                '{item["professional_roles"]}',
                                '{item["experience"]}',
                                '{item["employment"]}',
                                '{item["snippet"]}',
                                '{item["url"]}',
                                {address}
                            )"""
                                )
            company_id += 1
        print("База данных заполнена")


class DBManager(Database):
    def __init__(self):
        super().__init__()

    def database_manager(self):
        """ Здесь происходит обработка запросов от пользователя. """

        print(f"""
Приветствую тебя!
""")
        research_again = ""
        print("""    [+] cv - получает список всех компаний и количество вакансий у каждой компании.
    [+] vac - получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
    [+] avg - получает среднюю зарплату по вакансиям.
    [+] gr_avg - получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
    [+] word - получает список всех вакансий, в названии которых содержатся переданные в метод слова
    [+] all - показать всю таблицу
    [+] id - показать вакансии выбранной компании
        """)
        while research_again == "":
            chose = input("Выберите действие: ")
            while chose not in ("cv", "vac", "avg", "gr_avg", "word", "id", "all"):
                print("Нет такого варианта выбора")
                print()
                chose = input("Выберите действие: ")

            if chose == "cv":
                self.get_companies_and_vacancies_count()
                print()
            elif chose == "vac":
                self.get_all_vacancies()
                print()
            elif chose == "avg":
                self.get_avg_salary()
                print()
            elif chose == "gr_avg":
                self.get_vacancies_with_higher_salary()
                print()
            elif chose == "word":
                word = input("Введите запрос: ")
                self.get_vacancies_with_keyword(word)
                print()
            elif chose == "all":
                self.get_all_table()
                print()
            elif chose == "id":
                company_id = int(input("Введите ID компании: "))
                self.get_vacancies_by_id(company_id)
                print()

            research_again = input('Исследовать БД ещё раз? Если да, то введите "Enter" ')
            print()



    @staticmethod
    def printer(data):
        """ Функция для распечатки в консоли вывода программы"""

        for row in data:
            new_row = []
            for item in row:
                new_row.append(str(item))
            print(", ".join(new_row))

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании."""

        with self.con.cursor() as cur:
            cur.execute(f"""
                SELECT DISTINCT(company_name), COUNT(*), company_id
                FROM total_database
                GROUP BY (company_name, company_id)
                ORDER BY company_name; """)
            data = cur.fetchall()

        self.printer(data)

    def get_all_vacancies(self):
        """ Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию."""

        with self.con.cursor() as cur:
            cur.execute(f"""
                SELECT company_name, vacation_name, salary_to, salary_currency, url
                FROM total_database
                WHERE salary_to <> 0; """)
            data = cur.fetchall()
        self.printer(data)

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям."""

        with self.con.cursor() as cur:
            cur.execute(f"""
                SELECT AVG(salary_from + salary_to)
                AS average
                FROM total_database; """)
            data = cur.fetchall()
        self.printer(data)

    def get_vacancies_with_higher_salary(self):
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. """

        with self.con.cursor() as cur:
            cur.execute(f"""
                SELECT company_name, vacation_name, salary_to, salary_currency, url 
                FROM total_database
                WHERE salary_to > (
                    SELECT AVG(salary_from + salary_to)
                    FROM total_database); """)
            data = cur.fetchall()
        self.printer(data)

    def get_vacancies_with_keyword(self, word: str):
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”. """

        with self.con.cursor() as cur:
            cur.execute(f"""
                SELECT company_name, vacation_name, salary_to, salary_currency, url 
                FROM total_database
                WHERE vacation_name 
                LIKE '%{word.title()}%' """)
            data = cur.fetchall()
        if len(data) != 0:
            self.printer(data)
        else:
            print(f'По запросу "{word}" ничего не найдено.')

    def get_vacancies_by_id(self, company_id: int):
        """ Для получения списка вакансий по ID """

        with self.con.cursor() as cur:
            cur.execute(f"""
        SELECT company_id, company_name, vacation_name, salary_to, salary_currency, url
        FROM total_database
        WHERE company_id={company_id} """)
            data = cur.fetchall()
        self.printer(data)

    def get_all_table(self):
        """ Получаем всю таблицу целиком """

        with self.con.cursor() as cur:
            cur.execute(f"""
            SELECT *
            FROM total_database """)
            data = cur.fetchall()
        self.printer(data)
