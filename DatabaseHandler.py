
"""
Uses: 
    - Logger

Called From:
    - AuthenticationHandler
    - InventoryManagement
    - FinanceModule
    - ReportGenerator
    - EmployeeManagement
    - AssetManagement
"""

from Logger import Logger

import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost", # [CHANGE] Change this string to host of the database we are using 
    user = "username", # [CHANGE] Change this string to username database is using
    password = "password", # [CHANGE] Change this string to password database is using
    database = "database" # [CHANGE] Change this string to the name of the database we are using
)

mycursor = mydb.cursor()


class DatabaseHandler:
    def __init__(self):
        self.logger = Logger()
    
    # Inserts data into the database
    def insert(data, table: str) -> bool:

        initial_row_count = mycursor.rowcount() # Track initial row count of database

        # Insert row into database
        sql_statement = "INSERT INTO" + table + "(column1) VALUES (%s)" #  [CHANGE] Replace column 1 with name of columns that appear in database, (Can also add more attributes, not sure if data contains one or more columns)
        mycursor.execute(data)

        # Not sure if data is a single string that's formatted such as (%s)
        # Assuming data is a string in the format of "itemName" 

        mydb.commit(); # Commit / apply changes to database

        current_row_count = mycursor.rowcount()

        # Determine if database inserted an item
        if (current_row_count != initial_row_count):
            return True
        else:
            return False
        ...

    # Deletes specified data from the database
    def delete(data, table: str) -> bool:

        result = DatabaseHandler.contains(data, table) # Determine if data is in database

        if (result == False):
            return False
        else:

            sql_statement = "DELETE FROM " + table + " WHERE (column1) = '%s'" # [CHANGE] Replace column 1 with name of columns that appear in database
            mycursor.execute(data)

            mydb.commit() # Commit / apply changes to database

            return True
        ...

    # Checks if database contains specified data
    def contains(data, table: str) -> bool:

        mycursor.execute("SELECT columnName FROM " + table + " WHERE columnName=%s", data) # Execute query [CHANGE] columnName to name ot column that we will use in database

        selected_data = mycursor.fetchall() # Retrieves results of most recent query that has been executed (empty if no result)

        # Determine if database contains data
        if not selected_data:
            return False
        else:
            return True
        ...
    
    """
    These functions are a bit more complex because sometimes you might want to conditionally update or fetch something.
    Could be modified to use an SQL query if we use an SQL database.
    """
    def update(data, new_data, column, table: str) -> bool: 
        """
        Replaces instances of data with new_data
        """

        result = True

        # Fetch data currently in row
        query_statement = "SELECT " + column + " FROM " + table + " WHERE " + column + " = " + data
        mycursor.execute(query_statement)

        curr_data = mycursor.fetchall() # Fetch recently executed query
        curr_data = list(zip(*curr_data)) # Convert query of data into a list/array of items


        # Update data in row
        query_statement = "UPDATE " + table + " SET " + column + " = " + data + " WHERE" + column + " = " + new_data
        mycursor.execute(query_statement)

        updated_data = mycursor.fetchall() # Fetch recently executed query
        updated_data = list(zip(*curr_data)) # Convert query of data into a list/array of items


        # Determine if data was updated, if data was the same or unsuccessful return false
        length = len(curr_data)

        if (len(curr_data) == len(updated_data)):

            # Check contents of fetched rows
            for i in range(length):
                if (curr_data[i] != updated_data[i]):
                    result = False

        else:
            result = False
        
        return result


    def fetch_row(condition, table: str) -> list:
        
        # Fetch row
        query_statement = "SELECT * FROM " + table + " " + condition # Assuming "condition" contains WHERE statement for query
        mycursor.execute(query_statement)

        data = mycursor.fetchall() # Fetch recently executed query
        data = list(zip(*data)) # Convert query of data into a list/array of items

        return data
    
        
    def fetch_table(table: str) -> list:
        
        # Fill arrays with data from both columns in the database
        query_statement = "SELECT * FROM " + table
        mycursor.execute(query_statement)

        data = mycursor.fetchall() # Fetch recently executed query
        data = list(zip(*data)) # Convert query of data into a list/array of items

        return data