import click
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint


@click.command()
@click.option("--text", default="python")
def parse(text):
    next = True
    page = 0
    vacancies_list = []
    while next:

        main_link = 'https://hh.ru'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            'Accept': '*/*'
        }
        params = {
            'area': '1',
            'fromSearchLine': 'true',
            'st': 'searchVacancy',
            'text': text,
            'page': page
        }

        response = requests.get(main_link + '/search/vacancy', params=params, headers=headers)

        if response.ok:
            soup = bs(response.content, 'html.parser')

            vacancies = soup.findAll('div', attrs={'class': 'vacancy-serp-item'})

            for vacancy in vacancies:

                vacancy_dict = {}

                vacancy_a = vacancy.find('a', attrs={'class': 'bloko-link'})
                link = vacancy_a['href']
                vacancy_name = vacancy_a.getText()
                salary_obj = vacancy.find('div', attrs={'class': 'vacancy-serp-item__sidebar'}).find('span')
                if salary_obj is not None:
                    salary = salary_obj.getText()
                    currency = salary[-4:].strip()
                    if 'от' in salary:
                        min_salary = salary[3:-4].strip().replace('\xa0', ' ')
                        max_salary = None
                    elif 'до' in salary:
                        min_salary = None
                        max_salary = salary[3:-4].strip().replace('\xa0', ' ')
                    else:
                        min_salary, max_salary = [s.replace('\xa0', ' ') for s in salary[:-4].strip().split('-')]
                else:
                    min_salary = None
                    max_salary = None
                    currency = None

                vacancy_dict['min_salary'] = min_salary
                vacancy_dict['max_salary'] = max_salary
                vacancy_dict['currency'] = currency
                vacancy_dict['link'] = link
                vacancy_dict['name'] = vacancy_name
                vacancy_dict['site_link'] = main_link

                vacancies_list.append(vacancy_dict)

                pprint(vacancy_dict)

            if soup.find('a', attrs={'class': 'HH-Pager-Controls-Next'}) is not None:
                page += 1
            else:
                next = False


if __name__ == '__main__':
    parse()
