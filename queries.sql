-- Создание таблицы

CREATE TABLE total_database (
    company_id int,
    company_name text,
    vacation_name text,
    salary_from int,
    salary_to int,
    salary_currency varchar(3),
    professional_roles varchar(64),
    experience varchar(32),
    employment varchar(32),
    snippet text,
    url text,
    address varchar(64)
)


-- Заполнение таблицы происходит непосредственно python.
-- Если описывать его исключительно языком SQL это займёт много места


-- Получает список всех компаний и количество вакансий у каждой компании."""

SELECT DISTINCT(company_name), COUNT(*), company_id
FROM total_database
GROUP BY (company_name, company_id)
ORDER BY company_name;


-- Получает список всех вакансий с указанием названия компании,
--названия вакансии и зарплаты и ссылки на вакансию.

SELECT company_name, vacation_name, salary_to, salary_currency, url
FROM total_database
WHERE salary_to <> 0;


-- Получает среднюю зарплату по вакансиям

SELECT AVG(salary_from + salary_to)
AS average
FROM total_database;


-- Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. """

SELECT company_name, vacation_name, salary_to, salary_currency, url
FROM total_database
WHERE salary_to > (
    SELECT AVG(salary_from + salary_to)
    FROM total_database);


-- Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”. """

SELECT company_name, vacation_name, salary_to, salary_currency, url
FROM total_database
WHERE vacation_name
LIKE '%python%'

-- Выше в кавычках, между знаками % пример слова для поиска.
-- В программе оно реализовано через input()


--Для получения списка вакансий по ID

SELECT company_id, company_name, vacation_name, salary_to, salary_currency, url
FROM total_database
WHERE company_id=5


--Получаем всю таблицу целиком

SELECT *
FROM total_database
