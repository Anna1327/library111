# -*- coding: utf-8 -*-
import sqlite3


def sqlite3_simple_read_db(data_base, table, column_name=None):
    """
    This function loads data from the selected table

    :param data_base: database name
    :param table: table name
    :param column_name: list of columns

    :return: column_name: list of columns, data = list of tuples with data from table
    """
    con = sqlite3.connect(data_base)
    cur = con.cursor()
    query_columns = 'pragma table_info(' + table + ')'
    cur.execute(query_columns)
    columns_description = cur.fetchall()
    columns_names = []
    for column in columns_description:
        columns_names.append(column[1])
    if column_name is None:
        query = 'SELECT * FROM ' + table
        cur.execute(query)
        data = cur.fetchall()
    else:
        query = ' SELECT ' + column_name + ' FROM ' + table
        cur.execute(query)
        data = cur.fetchall()
        new_data = []
        for element in data:
            new_data.append(element[0])
        data = new_data

    cur.close()
    con.close()
    return columns_names, data


def simple_search_from_db(data_base: str, table: str, column_name: str, key: str) -> list:
    """
    This function searches the database based on the selected parameters

    :param data_base: database name
    :param table: table name
    :param column_name: str - selected parameter to search
    :param key: str - value from input field from user when searching string

    :return: list of tuples -> founded rows to delete from table
    """
    con = sqlite3.connect(data_base)
    cur = con.cursor()
    key = chr(0x22) + key + chr(0x22)

    query = 'SELECT * FROM ' + table + ' WHERE ' + column_name + ' = ' + key

    cur.execute(query)
    data = cur.fetchall()
    if not data:
        data = 'Значение не найдено в базе данных!'
    cur.close()
    con.close()
    return data


def sqlite3_simple_delete_table(data_base, table):
    """
    This function removes the selected table from database

    :param data_base: database name
    :param table: table name

    :return: nothing
    """
    con = sqlite3.connect(data_base)
    cur = con.cursor()
    query = 'DROP TABLE IF EXISTS ' + table
    cur.execute(query)
    cur.close()
    con.close()


def sqlite3_simple_delete_record(data_base, table, id_column, record_id):
    """
    This function removes a row from the database table

    :param data_base: database name
    :param table: table name
    :param id_column: column name
    :param record_id: record in this column

    :return: nothing
    """
    con = sqlite3.connect(data_base)
    cur = con.cursor()
    query = 'DELETE FROM ' + table + ' WHERE ' + id_column + " = '" + record_id + "'"
    cur.execute(query)
    con.commit()
    cur.close()
    con.close()


def sqlite3_update_record(data_base, table, param_column, param_value, id_column, record_id):
    """
    This function updates the entry in the database table

    :param data_base: database name
    :param table: table name
    :param param_column: column in which need to change the value
    :param param_value: value to be set
    :param id_column: column name
    :param record_id: record in this column

    :return: nothing
    """
    con = sqlite3.connect(data_base)
    cur = con.cursor()
    try:
        query = 'UPDATE ' + table + ' SET ' + param_column + ' = "' + param_value + '" WHERE ' + id_column + " = '" + \
                record_id + "'"
        cur.execute(query)
    except sqlite3.OperationalError:
        pass
    con.commit()
    cur.close()
    con.close()


def choose_table_from_db(data_base):
    """
    This function finds the selected table in the database and loads all the information from it

    :param data_base: database name
    :return: all data from selected table
    """
    con = sqlite3.connect(data_base)
    cur = con.cursor()
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    cur.execute(query)
    data = cur.fetchall()
    new_data = []
    for element in data:
        new_data.append(element[0])
    data = new_data
    cur.close()
    con.close()
    return data


def sqlite3_simple_clear_table(data_base, table):
    """
    This function delete all records from selected table

    :param data_base: database name
    :param table: table name

    :return: nothing
    """
    con = sqlite3.connect(data_base)
    cur = con.cursor()
    query = 'DELETE FROM ' + table
    cur.execute(query)
    con.commit()
    cur.close()
    con.close()


if __name__ == '__main__':
    pass
    # sqlite3_simple_example_create_db(data_base)
    # sqlite3_simple_delete_table(data_base, table)
    # sqlite3_simple_delete_record(data_base, table, id_column, record_id)
    # sqlite3_update_record(data_base, table, id_column, record_id, param_column, param_value)
    # sqlite3_simple_read_db(data_base, table)
    # choose_table_from_db(data_base)
