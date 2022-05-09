import pymysql, os, pandas as pd
from sqlalchemy import create_engine
from config import *
from termcolor import colored


class AWSConstruct:
    def __init__(self, sql_info=aws_information_list):
        """
        For this constructor to accomplish the first step, you need a config.py with
        a list named aws_information_list with the following information:
        HOST, PORT, USER, PASSWORD, DATABASE
        :param sql_info:
        """
        self.endpoint = sql_info[0]
        self.port = sql_info[1]
        self.user = sql_info[2]
        self.pwd = sql_info[3]
        self.db = sql_info[4]

    def aws_connection_sql(self):
        """
        This will use the config.py file to attempt a connection to
        the selected Amazon Web Services Relational Database Server.
        Make sure that if it is not in the same folder that you
        locate it, or use the variable outside the CLASS prior to running.
        :return:
        """
        try:
            db_test_connection = pymysql.connect(host=self.endpoint,
                                                 user=self.user,
                                                 password=self.pwd,
                                                 database=self.db,
                                                 charset='utf8mb4',
                                                 cursorclass=pymysql.cursors.DictCursor
                                                 )
        except:
            try:
                db_test_connection = pymysql.connect(host=self.endpoint,
                                                     user=self.user,
                                                     password=self.pwd,
                                                     #database=self.db,
                                                     charset='utf8mb4',
                                                     cursorclass=pymysql.cursors.DictCursor
                                                     )
            except:
                return print(colored(f"Connection to AWS RDS unsuccessful...", "red"))
            else:
                cursor = db_test_connection.cursor()
                cursor.execute("select version()")
                version = cursor.fetchone()

        else:
            cursor = db_test_connection.cursor()
            cursor.execute("select version()")
            version = cursor.fetchone()
            return db_test_connection
        finally:
            if db_test_connection:
                print(colored(f"Handshake Successful! MySQL version {version['version()']}", "green"))
                return db_test_connection
            else:
                return print(colored(f"Connection to AWS RDS unsuccessful...", "red"))

    def sql_check_for_database(self, db_connection):
        """
        Function is calling for the database to show the current tables.
        Once we have a few of the different binning processes completed they will each
        have a schema that you can pull from in order to run testing with.
        :param db_connection:
        :return:
        """
        cursor = db_connection.cursor()
        sql_show_table = """SHOW DATABASES"""
        try:
            cursor.execute(sql_show_table)
            return print(colored(f"{cursor.fetchall()}", "green"))

        except:
            return print(colored("There was an error", "red"))

    def sql_show_tables(self, db_connection, db_name):
        """
        Function will display all tables within Database.
        :param db_connection:
        :param db_name:
        :return:
        """
        try:
            cursor = db_connection.cursor()
            cursor.execute(f"USE {db_name}")
            sql_show_table = """SHOW TABLES"""
            cursor.execute(sql_show_table)
        except:
            return print(
                colored("Something happened. Please check your previous calls.\nReach out if problem persists", 'red'))
        else:
            return print(colored(cursor.fetchall(), 'green'))

    def sql_drop_database(self, db_connection, table_name):
        """
        Function is attempting to drop a table from the database connection.
        This should only be used during testing and will be disabled prior to
        full deployment.
        :param db_connection:
        :param table_name:
        :return:
        """
        cursor = db_connection.cursor()
        sql_drop = f"""DROP DATABASE {table_name}"""
        sure = input(f'(Y to confirm the deletion of database: {table_name}: ').capitalize()
        if sure == "T" or sure == 'Y':
            try:
                cursor.execute(sql_drop)
                return print(colored(f"Table {table_name} has been deleted.", "green"))

            except:
                return print(colored(f"Cannot drop Database {table_name}. It does not exist.", "red"))

        return print(colored(f"No action taken against Database: {table_name}", "blue"))

    def sql_create_database(self, db_connection, db_name):
        """
        This function is attempting to create a database within MySQL.
        :param db_connection:
        :param db_name:
        :return:
        """
        cursor = db_connection.cursor()
        sql_create_database = f"""CREATE DATABASE {db_name}"""
        try:
            cursor.execute(sql_create_database)
            return print(colored(f"Database {db_name} created successfully", "green"))

        except:
            try:
                select_table = f"""USE {db_name}"""
                cursor.execute(select_table)
                return print(colored(f"Database {db_name} exists.", 'blue'))
            except:
                return print(colored(f"Creation of Database {db_name} unsuccessful.", "red"))

    # def create_table_in_database(self, database, db_connection, table_name, dataframe):
    #     """
    #     This function will attempt to make a table within the database.
    #     :param database:
    #     :param db_connection:
    #     :param table_name:
    #     :param dataframe:
    #     :return:
    #     """
    #     cursor = db_connection.cursor()
    #     try:
    #         columns = [f"""{i.replace(' ', '_').replace('-', '')} {dataframe[i].dtypes}""" for i in dataframe.columns]
    #         columns = [s.replace('64', '').replace(' or more', '').replace(' or older', '').replace('/', '_') for s in columns]
    #
    #     except:
    #         print('failed')
    #
    #     finally:
    #         cursor.execute(f"""USE {database} * FROM {table_name}""")
    #         result = cursor.fetchone()
    #         if result:
    #             return print(colored(f"Table {table_name} failed because table already exists.", "blue"))
    #         else:
    #             create_table = f"""CREATE TABLE {table_name} (""" + ", ".join(columns) + ")"
    #             cursor.execute(create_table)
    #             print(colored(f"Schema/Table {table_name} created!", 'green'))

    def sql_truncate_table_from_database(self, db_connection, database, table_name):
        """
        Function attempts to truncate/delete the rows in a table without deleting the columns.
        :param db_connection:
        :param database:
        :param table_name:
        :return:
        """
        try:
            cursor = db_connection.cursor()
            cursor.execute(f"""USE {database}""")
            cursor.execute(f"""TRUNCATE TABLE {table_name}""")
            return print(colored(f'''Truncation of table {table_name} from {database} successfully executed'''), 'green')

        except:
            return print(colored(f"""Truncation of table {table_name} from {database} failed""", 'red'))

    def show_counts_from_table(self, db_connection, database, table_name):
        """
        This will show all current tables from the selected Database
        :param db_connection:
        :param database:
        :param table_name:
        :return:
        """
        cursor = db_connection.cursor()
        cursor.execute(f"""USE {database}""")
        cursor.execute(f"""SELECT COUNT(ID_ref) FROM {table_name}""")
        return print(colored(f"{cursor.fetchall()}", "green"))

    def upload_excel_to_database(self, db_connection, database, table_name, dataframe):
        """
        This will upload the excel document to the database.
        :param db_connection:
        :param database:
        :param table_name:
        :param dataframe:
        :return:
        """
        cursor = db_connection.cursor()
        try:
            cursor.execute(f"""DROP TABLE {table_name}""")
        finally:

            try:
                engine = create_engine(
                    f"""mysql+pymysql://{str(db_connection.user)[2:-1]}:{str(db_connection.password)[2:-1]}@{db_connection.host}:{str(db_connection.port)[2:-1]}/{database}""")
                dataframe.to_sql(name=table_name, con=engine)
                return print(colored(f"{len(dataframe)} rows and {len(dataframe.columns)} columns added.", 'green'))
            except:
                dataframe.to_sql(name=table_name * 2, con=engine)
                return print(
                    colored(f"{len(dataframe)} rows and {len(dataframe.columns)} columns added to {table_name * 2}.",
                            'green'))

    def show_columns_in_table(self, db_connection, database, table_name):
        """
        The intention of this is to show the columns that exist within a table
        :param db_connection:
        :param database:
        :param table_name:
        :return:
        """
        cursor = db_connection.cursor()

        try:
            cursor.execute(f"""USE {database}""")
            return cursor.execute(f"""SELECT COUNT(*) FROM {table_name};""")
        except:
            return print(f"task failed successfully!")

    def check_for_duplicates(self, dataframe):
        """
        This will run through the dataset to check for duplications
        :param dataframe:
        :return:
        """
        return print(dataframe.duplicated().value_counts())

    def drop_duplicates(self, dataframe):
        """
        This will drop duplicates, but keep the first occurence.
        :param dataframe:
        :return:
        """
        return dataframe.drop_duplicates(keep='first')



    def sql_disconnect(self, db_connection):
        """
        This function will close the connection to the host (AWS).
        :param db_connection:
        :return:
        """
        cursor = db_connection.cursor()
        try:
            cursor.close()
            return print(colored(f"Disconnection from {db_connection} successful.", "green"))

        except:
            return print(colored("Disconnect unsuccessful.", "red"))
