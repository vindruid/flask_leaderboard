import sqlite3
from sqlite3 import Error
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        password text NOT NULL,
                                        registered_at timestamp
                                    ); """
 
if __name__ == '__main__':
    conn = create_connection('leaderboard.db')
    create_table(conn, sql_create_user_table)