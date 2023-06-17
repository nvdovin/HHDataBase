import requests
import json
import utils as u


class HeadHunter:
    def __init__(self):
        self.companies = u.research_list

        self.employees = "https://api.hh.ru/employers"
        self.vacancies = "https://api.hh.ru/vacancies"

    def get_data_employees(self, company):
        """ Возвращает данные о работодателях со ссылкой на список вакансий """

        employers_list = []
        request = requests.get(
            self.employees,
            params={"text": company}
        )

        for item in request.json()["items"]:
            if item["open_vacancies"] > 5:
                employers_list.append(
                    {
                        "name": item["name"],
                        "id": item["id"]
                    }
                )

        return employers_list

    def get_vacations_list(self, company_id: str):
        request = requests.get(
            self.vacancies,
            params={"employer_id": company_id}
        )
        return request.json()

    def get_data_dict(self):
        """ Здесь создается список словарей, состоящий из ID работодателей,
         и его вакансий """

        all_the_vacancies = []

        for company in self.companies:
            data_dict = self.get_data_employees(company)
            for item in data_dict:
                name = item["name"]
                company_id = item["id"]

                vacancies_data = self.get_vacations_list(company_id)
                vacancies_list = []

                for vacation in vacancies_data["items"]:
                    vacation_name = f"{vacation['name']}"

                    try:
                        salary_from = vacation["salary"]["from"]
                    except TypeError:
                        salary_from = None

                    try:
                        salary_currency = vacation["salary"]["currency"]
                    except TypeError:
                        salary_currency = None

                    try:
                        salary_to = vacation['salary']['to']
                    except TypeError:
                        salary_to = None

                    try:
                        address = f'{vacation["address"]["city"]}, {vacation["address"]["street"]}'
                    except TypeError:
                        address = None

                    url = f'{vacation["alternate_url"]}'
                    snippet = f'{vacation["snippet"]["requirement"]}'
                    professional_roles = f'{vacation["professional_roles"][0]["name"]}'
                    experience = f'{vacation["experience"]["name"]}'
                    employment = f'{vacation["employment"]["name"]}'

                    vacancies_list.append(
                        {
                            "vacation_name": vacation_name,
                            "salary_from": salary_from,
                            "salary_to": salary_to,
                            "salary_currency": salary_currency,
                            "professional_roles": professional_roles,
                            "experience": experience,
                            "employment": employment,
                            "snippet": snippet,
                            "url": url,
                            "address": address
                        }
                    )
            dict_to_write = {"name": f"{name}", "vacancies": vacancies_list}
            if dict_to_write not in all_the_vacancies:
                all_the_vacancies.append(dict_to_write)

        return all_the_vacancies

    # Ниже некоторые тестовые функции, которые могут пригодиться в будущем.

    def get_info(self):
        for company in self.get_data_dict():
            print(company)

    def write_to_json(self):
        data = self.get_vacations_list("5122356")
        with open("data_test.txt", "w", encoding="utf-8") as test_file:
            to_write = json.dumps(data, indent=4, ensure_ascii=False)
            test_file.write(to_write)


hh = HeadHunter()
hh.write_to_json()
