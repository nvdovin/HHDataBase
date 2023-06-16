import requests
import json


class HeadHunter:
    def __init__(self):
        self.companies = ["Самокат", "Газпром", "Магнит",
                          "Эльдорадо", "DNS", "development",
                          "Yandex", "Вкусно и точка", "Клининг",
                          "Больница", "Delivery", "AB Inbev", "Талина"]
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

    def get_vacations_list(self, id: str, response):
        request = requests.get(
            self.vacancies,
            params={
                "employer_id": id,
                "text": response
                    }
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
                id = item["id"]
                vacancies_data = self.get_vacations_list(id, name)
                vacancies_list = []

                for vacation in vacancies_data["items"]:
                    vacation_name = f"{vacation['name']}"

                    try:
                        if vacation["salary"]["from"] is not None and vacation["salary"]["to"] is not None:
                            salary = f"от {vacation['salary']['from']} до {vacation['salary']['to']} {vacation['salary']['currency']}"
                        elif vacation['salary']['to'] is None:
                            salary = f"от {vacation['salary']['from']} {vacation['salary']['currency']}"
                        elif vacation['salary']['from'] is None:
                            salary = f"до {vacation['salary']['to']} {vacation['salary']['currency']}"
                    except:
                        salary = "Нет данных"

                    try:
                        address = f'{vacation["address"]["city"]}, {vacation["address"]["street"]}'
                    except TypeError:
                        city = "Нет данных"

                    url = f'{vacation["url"]}'
                    snippet = f'{vacation["snippet"]["requirement"]}'
                    professional_roles = f'{vacation["professional_roles"][0]["name"]}'
                    experience = f'{vacation["experience"]["name"]}'
                    employment = f'{vacation["employment"]["name"]}'

                    vacancies_list.append(
                        {
                            "vacation_name": vacation_name,
                            "salary": salary,
                            "professional_roles": professional_roles,
                            "experience": experience,
                            "employment": employment,
                            "snippet": snippet,
                            "url": url,
                            "address": address
                        }
                    )
            if {f"{name}": vacancies_list} not in all_the_vacancies:
                all_the_vacancies.append({f"{name}": vacancies_list})

        return all_the_vacancies

    def get_info(self):
        for company in self.get_data_dict():
            print(company)

    def write_to_json(self):
        data = self.get_data_dict()
        with open("data_test.txt", "w", encoding="utf-8") as test_file:
            to_write = json.dumps(data, indent=4, ensure_ascii=False)
            test_file.write(to_write)

