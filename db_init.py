from sqlalchemy import exc
from pathlib import Path
import argparse
import os
from db_functions import talk_db

parser = argparse.ArgumentParser(
    description="take schema from sql file and create the tables into PostgreSQL database")
parser.add_argument('-f', '--this-file', default='schema.sql',
                    help='optional,  provide the path to the sql file.\n default is schema.sql in current directory.\nUsage: db_init.py [-f path/to/file/schemq.sql]', required=False)
parser.add_argument('-r', '--reset-db', action="store_true", default=False,
                    help='optional,  reset db , delete all tables then recreate it.\n .\nUsage: db_init.py [-r]', required=False)
args = parser.parse_args()


def init_db():

    with open(schema_file, mode='rt') as f:
        r = talk_db(f.read())
    if r:
        print('schema.sql has been executed successfully')


def reset_db():
    q = ('DROP TABLE if exists users, books, reviews')

    uInput = input(
        'are you sure? all db tables will be deleted!(type DEL to continue or anything else to cancel.')
    if uInput == 'DEL':
        talk_db(q)
        print('databsae tables have been deleted successfully.')
    else:
        print('the operation was canceld')
        exit(0)


if __name__ == '__main__':
    schema_file = Path(args.this_file)
    if not schema_file.is_file():
        print("schema.sql not found. you can point the program where to look!")
        print("Usage: db_init.py -f [path/to/file/schema.sql]")
        exit(1)
    if args.reset_db:
        reset_db()
        init_db()
    else:
        init_db()
