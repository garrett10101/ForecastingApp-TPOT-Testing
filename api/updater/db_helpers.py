import day_conds as dc
import pandas as pd
import sqlite3
import os

class DB():
    """ DB class to manage the database contains connection and cursor"""

    def __init__(self, db_file_path='api/updater/forecastDB.db'):
        """
        The function initializes a connection to a SQLite database using a specified
        file path.
        
        :param db_file_path: parameter is the file path to the SQLite database 
        file that will be used. By default, it is set `'api/updater/forecastDB.db'`
        This parameter allows you to specify a custom database file path 
        """
        try:
            self.con = sqlite3.connect(db_file_path)
            self.cur = self.con.cursor()
        except Exception as e:
            print(e.args[0])

    def db_exists(self):
        """
        The function checks if a database file exists and creates it if it doesn't.
        :return: always returns `True`.
        """
        if not os.path.exists('api/updater/forecastDB.db'):
            con = sqlite3.connect('api/updater/forecastDB.db')
            print('Created DB file')
            return True
        return True

    def make_new_table(self, name, columns):
        """
        The function `make_new_table` creates a new table in a SQLite database with the
        specified name and columns.
        
        :param name: name for the db table
        :param columns: columns in the table
        """
        cols = ",".join(str(element) for element in columns)
        query = f"CREATE TABLE IF NOT EXISTS {name} ({cols})"
        self.cur.execute(query)


    def update_curr_cond(self):
        """
        The function `update_curr_cond` gets the current conditions and stores them
        in the database in a table called "conditions"
        """
        df = dc.get_today_cond()
        df.to_sql('conditions', self.con, index=True, index_label='TS', \
                  if_exists='replace')
        
    def get_stored_curr_cond(self):
        """
        This function retrieves and returns all stored current conditions data from
        the `conditions` table in the database. 
        :return: a DataFrame containing the current conditions data
        """
        query = self.cur.execute("SELECT * FROM conditions")
        cols = [col[0] for col in query.description]
        data = query.fetchall()
        df = pd.DataFrame(data=data, columns=cols)

        return df