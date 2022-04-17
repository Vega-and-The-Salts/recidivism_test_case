import pymysql, pandas as pd
from config import aws_information_dict, aws_information_list
from termcolor import colored


class AWSConstruct:
    def __init__(self, sql_info=aws_information_list):
        """
        For this constructor to accomplish the first step, you need a config.py with
        a list named aws_information_list with the following information:
        HOST, PORT, USER, PASSWORD, DATABASE
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
        """
        try:
            db_test_connection = pymysql.connect(host=self.endpoint,
                                                 user=self.user,
                                                 password=self.pwd,
                                                 database=self.db,
                                                 charset='utf8mb4',
                                                 cursorclass=pymysql.cursors.DictCursor
                                                 )

            try:
                cursor = db_test_connection.cursor()
                cursor.execute("select version()")
                version = cursor.fetchone()
                print(colored(f"Handshake Successful! MySQL version {version['version()']}", "green"))
                return db_test_connection
            except:
                print(colored(f"Connection to AWS RDS unsuccessful...", "red"))
                return db_test_connection
        except:
            print(colored(f"Connection to AWS RDS unsuccessful...", "red"))
            return db_test_connection

    def sql_check_for_database(self, db_connection):
        """
        Function is calling for the database to show the current tables.
        Once we have a few of the different binning processes completed they will each
        have a schema that you can pull from in order to run testing with.
        """
        cursor = db_connection.cursor()
        sql_show_table = """SHOW DATABASES"""
        try:
            cursor.execute(sql_show_table)
            return print(colored(f"{cursor.fetchall()}", "blue"))

        except:
            return print(colored("There was an error", "red"))

    def sql_drop_database(self, db_connection, table_name):
        """
        Function is attempting to drop a table from the database connection.
        This should only be used during testing and will be disabled prior to
        full deployment.
        """
        cursor = db_connection.cursor()
        sql_drop = f"""DROP DATABASE {table_name}"""
        sure = input(f'(Y/N) Are you sure you want to delete Database: {table_name}: ').capitalize()
        if sure == "T" or sure == 'Y':
            try:
                cursor.execute(sql_drop)
                return print(colored(f"Table {table_name} has been deleted.", "blue"))

            except:
                return print(colored(f"Cannot drop table {table_name}. It does not exist.", "red"))

        return print(colored(f"No action taken against table: {table_name}", "blue"))

    def sql_create_database(self, db_connection, db_name):
        """
        This function is attempting to create a table within the database.
        """
        cursor = db_connection.cursor()
        sql_create_database = f"""CREATE DATABASE {db_name}"""
        try:
            cursor.execute(sql_create_database)
            return print(colored(f"Database {db_name} created successfully", "green"))

        except:
            try:
                select_table = f"""SELECT * FROM {db_name}"""
                cursor.execute(select_table)
                return print(colored(f"Database {db_name} exists.", 'orange'))
            except:
                return print(colored(f"Creation of Database {db_name} unsuccessful.", "red"))

    def upload_excel_to_database(self, db_connection, dataframe):
        """

        :param db_connection:
        :param dataframe:
        :return:
        """
        pass

    def sql_disconnect(self, db_connection):
        """
        This function will close the connection to the host (AWS).
        """
        cursor = db_connection
        try:
            cursor.close()
            return print(colored(f"Disconnection from {db_connection} successful.", "green"))

        except:
            return print(colored("Disconnect unsuccessful.", "red"))
