import csv
import os
import sys
from pathlib import Path
import argparse
import psycopg2
from db_helper import engine, session


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="take books from csv file and import them into PostgreSQL database")
    parser.add_argument('-f', '--this-file', default='books.csv',
                        help='optional,  provide the path to the csv file.\n default is books.csv in current directory.\nUsage: import.py [-f path/to/file/filename.csv]', required=False)
    parser.add_argument('-H', '--have-a-header', action="store_true", default=True,
                        help='optional, tell the program if the csv file have a header or no.\n default is yes.\nUsage: import.py [-H]', required=False)
    parser.add_argument('-d', '--disable-native-import', action="store_true",
                        help='optional, disable the use of super fast native backend command "copy".\nUsage: import.py [-d]', required=False)
    args = parser.parse_args()

    file_to_import = args.this_file
    if not Path(file_to_import).is_file():
        raise RuntimeError(
            "file not found. you can point the program where to look!\nUsage: import.py -f [path/to/file/filename.csv]")

    print('Checking Tables .....', end='')

    if 'books' not in engine.table_names():
        print('Database is not fully initialized yet!')
        print('You need to run "db_init.py" first to creates the schema.')
        exit(100)

    print('done')

    def slowImport():
        with open(file_to_import, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            if args.have_a_header:
                next(reader)  # escape header
            for i, (isbn, title, author, publication_year) in enumerate(reader):
                print(f'{i}: adding {title} in the database ......', end='')
                r = session.execute(
                    "SELECT id FROM books WHERE isbn = :isbn", {"isbn": isbn})
                if r.rowcount == 1:
                    print('already exists, skip.')
                    continue

                session.execute("INSERT INTO books (isbn, title, author, publication_year) VALUES (:isbn, :title, :author, :publication_year) ON CONFLICT (isbn) DO NOTHING", {
                                "isbn": isbn, "title": title, "author": author, "publication_year": publication_year})
                session.commit()
                print('done')

            session.close()

    def nativeImport():
        with open(file_to_import, 'rt', newline='') as f:
            q = "COPY books (isbn, title, author, publication_year) from STDIN with delimiter as ',' CSV"
            if args.have_a_header:
                q = q + " HEADER "
            cur = session.connection().connection.cursor()
            print('importing ......', end='')
            try:
                cur.copy_expert(q, f)
            except psycopg2.IntegrityError as e:
                print(e)
                print(
                    'something wrong , may be you imported this csv before?\nor try to run the program with [-d] argument\ntype import_.py [-h] for help.')
                exit(101)
            else:
                cur.close()
                session.commit()
                print('done')
            finally:
                print('cleaning ..', end='')
                session.close()
                print('done')

    if args.disable_native_import:
        slowImport()
    else:
        nativeImport()
