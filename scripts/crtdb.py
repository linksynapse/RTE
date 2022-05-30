import argparse
import sqlite3
from sqlite3 import Error

def create_db_file(dbpath):
    """ create a database file in system"""
    conn = None
    try:
        conn = sqlite3.connect(dbpath)
        create_table_db(conn)
        print('Verified version is ' + sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_table_db(conn):
    SQL = """
        CREATE TABLE IF NOT EXISTS TagHistory(
            badge text NOT NULL,
            user_id text NOT NULL,
            user_name text NOT NULL,
            card_id text NOT NULL,
            card_name text NOT NULL,
            com_id text NOT NULL,
            com_name text NOT NULL,
            created_on text NOT NULL,
            send_to integer NOT NULL default 0
        )
    """
    cursor = conn.cursor()
    cursor.execute(SQL)
    conn.commit()
    cursor.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create new database tool')
    parser.add_argument('-o','--out', type=str ,help='out put file path', required=True)

    args = parser.parse_args()

    dbpath = args.out
    create_db_file(dbpath)
    print("done.")