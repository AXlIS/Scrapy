from pymongo import MongoClient
import click

client = MongoClient('localhost', 27017)
db = client['HH']
python = db.python


@click.command()
@click.option("--sum", prompt="Введите желаемую зарплату")
def filters(sum):
    result = python.find({'$or': [
        {'min_salary': {'$lte': int(sum)}, 'max_salary': None},
        {'min_salary': None, 'max_salary': {'$gte': int(sum)}},
        {'min_salary': {'$lte': int(sum)}, 'max_salary': {'$gte': int(sum)}},
    ]})
    for item in result:
        print(item, 1)


if __name__ == '__main__':
    filters()
a