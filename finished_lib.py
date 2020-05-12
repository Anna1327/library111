# -*- coding: utf-8 -*-

from pathlib import Path

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.ttk as ttk
import json
import csv

from PIL import ImageTk, Image
from ttkthemes import ThemedTk
from dicttoxml import dicttoxml
import pandas as pd

from Baza_dannyh import *

# root
root = ThemedTk()
root.title("Добро пожаловать в приложение My library")
root.geometry('895x600')
root.set_theme('aquativo')
background_root = PhotoImage(file="pictures/kls.png")
Label(root, image=background_root).place(x=0, y=0)

output_on_display = Text(root, width=60, height=20, font="12", wrap=WORD)
output_on_display.place(x=230, y=200)

# windows
win_create_table = Text(root)
win_create_update_str = Text(root)
win_create_delete_str = Text(root)
win_update_concurrence = Text(root)
win_create_add_str = Text(root)
help_window = Text(root)

# widgets
list_of_table = Listbox(root, selectmode=SINGLE, height=7)
enter_table_name = Entry(win_create_table)
enter_column_values = Entry(win_create_table)
choice = ttk.Combobox()
confirmation = Label()
output1 = Text(root)
place_for_enter = Entry()
choose = Text(root)
search_delete_enter = ttk.Combobox()
canvas = Canvas()
forward_button = ttk.Button
image = ImageTk


# globals
new_data = []
data = []
column_names = []
record = []
enters_data = []
res = []
choice_row = []
my_lst = []
result = []
import_lst = []
my_iterator = []
picture_lst = []
zero = 0
number_str = 0
table = ""
data_base = ""
iterable = ""
image_base = "test/base.png"


# functions


def parse(database_path: str) -> str:
    """
    This function parses the database path that get from the load file function

    :param database_path: str
    :return: str

    Takes a database path, returns the database file name
    """
    new_path = database_path.split("/")
    database_file_name = './' + new_path[-1]
    return database_file_name


def create_table(enter_data_base: str, enter_table: str, enter_data: list):
    """
    This function creates a database table with columns Name, Author and Year of publication
    and writes the data in columns

    :param enter_data_base: str
    :param enter_table: str
    :param enter_data: list
    :return: nothing

    Takes a database name, table name and data, returns nothing
    """
    if type(enter_table) is not str:
        raise ValueError('имя таблицы должно быть строковым!')  # тут переделать, ошибка должна выводиться графически

    con = sqlite3.connect(enter_data_base)
    cur = con.cursor()
    q = """
        CREATE TABLE {table} ( 
          Name {txt}, 
          Author {txt}, 
          Published year {txt})
        """
    cur.execute(q.format(table=enter_table, txt='TEXT'))
    cur.execute('INSERT INTO ' + enter_table + ' VALUES(?, ?, ?)', enter_data)
    con.commit()
    cur.close()
    con.close()


def update_list_tables(special_data: str) -> list:
    """
    This function gets the list of tables from the database and displays them on the main screen

    :param special_data: : name of the database file
    :return: new list of tables in the database
    """
    global list_of_table
    data_for_list_of_table = get_inform_from_db(special_data)
    list_of_table = Listbox(root, selectmode=SINGLE, height=7)
    but_load = ttk.Button(text="  Загрузить  ", command=output)
    for i in data_for_list_of_table:
        for j in i:
            list_of_table.insert(END, i)
            new_data.append(j)
    list_of_table.place(x=25, y=270)
    but_load.place(x=50, y=420)
    return new_data


def get_create_data():
    """
    This function parses data received from the user: table name and column values, and create table

    :return: nothing
    """
    global enter_table_name, enter_column_values, table, win_create_table

    table = enter_table_name.get()
    column_values = enter_column_values.get()
    win_create_table.destroy()
    column_data = column_values
    column_data = column_data.split(',')
    create_table(data_base, table, column_data)
    update_list_tables(data_base)


def create_win_create_table():
    """
    This function displays a window for the enter data to the user when creating a table

    :return: nothing
    """
    global data_base, table, enter_table_name, win_create_table, enter_column_values
    if data_base == '':
        mistake_load_table()
    else:
        win_create_table = Toplevel(root)
        win_create_table.title("Ввод")
        win_create_table.geometry('320x150')
        enter_table_name = Entry(win_create_table)
        enter_table_name.place(x=15, y=40, width=210)
        lbl2 = Label(win_create_table, text="Введите название таблицы: ")
        lbl2.place(x=10, y=10)
        enter_data_button = ttk.Button(win_create_table, text="  Ввод  ", command=get_create_data)
        enter_data_button.place(x=250, y=70)
        lbl3 = Label(win_create_table, text="Введите через запятую: Название книги, \nИмя автора и Год публикации")
        lbl3.place(x=10, y=70)
        enter_column_values = Entry(win_create_table)
        enter_column_values.place(x=15, y=110, width=200)


def create_new_db():
    """
    This function create new database file with table

    :return: nothing
    """
    global data_base, table
    data_base = asksaveasfilename(title="Select file", filetypes=(("DATA BASE", "*.db"), ("all files", "*.*")),
                                  defaultextension='.db')

    if Path(data_base).suffix == '.db':
        create_win_create_table()
    else:
        mistake_db_file()


def mistake_db_file():
    """
    This function displays an error message when loading a database file
    if the user tries to download a file with a different extension

    :return: nothing
    """
    win_mistake_load_file = Toplevel(root)
    win_mistake_load_file.title("Ошибка")
    win_mistake_load_file.geometry('270x40')
    message = Label(win_mistake_load_file, text="Файл должен быть с расширением .db!", width=45, height=2)
    message.place(x=-30, y=0)


def load_file():
    """
    This function loads a file with the extension .db and displays a list of tables

    :return: nothing
    """
    global list_of_table, data_base, new_data
    open_name = askopenfilename()

    if Path(open_name).suffix == '.db':
        data_base = open_name
        data_base = str(data_base)
        new_data_base = parse(data_base)
        new_data = update_list_tables(new_data_base)
        new_data.clear()

    else:
        mistake_db_file()


def mistake_del_table():
    """
    This function displays an error message when deleting a system table from database

    :return: nothing
    """
    win_mistake_del_table = Toplevel(root)
    win_mistake_del_table.title("Ошибка")
    win_mistake_del_table.geometry('350x40')
    message = Label(win_mistake_del_table, text="Эта таблица является системной и не может быть удалена!", width=45,
                    height=2)
    message.place(x=10, y=0)


def del_table():
    """
    This function deletes a table from the database and displays an updated list of tables

    :return: nothing
    """
    global data_base, table, output_on_display
    try:
        sqlite3_simple_delete_table(data_base, table)
        list_tables = update_list_tables(data_base)
        list_tables.clear()
        output_on_display.delete(1.0, END)
        output_on_display.insert(END, '')
        return
    except sqlite3.OperationalError:
        mistake_del_table()


def clear_data_from_table():
    """
    This function delete all records from selected table

    :return: nothing
    """
    global data_base, table
    sqlite3_simple_clear_table(data_base, table)
    output_on_display.delete(1.0, END)
    output_on_display.insert(END, '')
    return


def output() -> tuple:
    """
    This function displays data from the table on the main screen

    :return: data from the table
    """
    global new_data, data, table, list_of_table, import_lst, win_create_add_str, win_create_delete_str, \
        win_create_update_str
    clear_table = ttk.Button(root, text="  Очистить таблицу  ", command=clear_data_from_table)
    delete_table = ttk.Button(root, text="  Удалить таблицу ", command=del_table)
    clear_table.place(x=30, y=460)
    delete_table.place(x=35, y=500)
    import_lst.clear()
    try:
        table = list_of_table.get(*list_of_table.curselection())
    except TypeError:
        pass

    if type(table) is tuple:
        table = str(table[0])
    data = sqlite3_simple_read_db(data_base, table)
    new_data = data[0]

    counter_row = 0
    for i in data:
        output_on_display.delete(1.0, END)
        try:
            for j in i:
                output_lst = list(j)
                import_lst.append(output_lst)
                output_on_display.insert(END, str(output_lst) + '\t')
                output_on_display.insert(END, '\n')
                counter_row += 1

        except UnboundLocalError:
            output_on_display.delete(1.0, END)
            output_on_display.insert(END, "В таблице нет данных")
    create_delete_entry(data[0], root, 10, 210)

    try:
        win_create_add_str.destroy()
        win_create_delete_str.destroy()
        win_create_update_str.destroy()
    except AttributeError:
        pass
    counter_row -= len(data[0])
    text_message = f'Найдено колонок: {counter_row}'
    sum_rows = Label(root, text=text_message, width=20, height=1)
    sum_rows.place(x=15, y=570)
    return data


def get_inform_from_db(database_file_name: str) -> list:
    """
    This function gets list of tables from database
    :param database_file_name: filename database
    :return: table name list
    """
    global data
    con = sqlite3.connect(database_file_name)
    cur = con.cursor()
    master = 'sqlite_master'
    query = "SELECT name FROM " + master + " WHERE type = 'table'"
    cur.execute(query)
    data = cur.fetchall()
    return data


def mistake_load_table():
    """
    This function displays an error message when user try to do operation with strings before loading table

    :return: nothing
    """
    text_message = "Сначала загрузите таблицу!"
    if data_base == '':
        text_message = 'Сначала загрузите базу данных или создайте новую!'
    win_mistake_load_table = Toplevel(root)
    win_mistake_load_table.title("Ошибка")
    win_mistake_load_table.geometry('330x40')
    message = Label(win_mistake_load_table, text=text_message, width=45, height=2)
    message.place(x=10, y=0)


def create_enter_window():
    """
    This function creates a window for entering data when adding a row to the table

    :return: nothing
    """
    global data, record, column_names, win_create_add_str
    try:
        column_names = data[0]
        win_create_add_str = Toplevel(root, relief=SUNKEN, bd=10, bg="light sky blue")
        win_create_add_str.title("Окно ввода")
        win_create_add_str.minsize(width=500, height=200)
        record = create_enter_entry(win_create_add_str)
        enter_data_button = ttk.Button(win_create_add_str, text="  Ввод  ", command=get_item)
        enter_data_button.place(x=400, y=33)
        update_button = ttk.Button(win_create_add_str, text="  Обновить  ", command=output)
        update_button.place(x=385, y=80)

    except IndexError:
        mistake_load_table()


def create_enter_entry(window) -> list:
    """
    This function creates input fields when adding a new string depending on the number of columns in the table

    :param window: data entry window
    :return: list of input fields
    """
    global record, column_names
    count = len(column_names)
    x = 0
    y = 0
    width = 100
    height = 15
    while count != 0:
        for i in column_names:
            sign = Label(window, text=str(i), width=10, height=2, bg="light sky blue", fg="black", bd=10)
            sign.place(x=x, y=y)
            entry = Entry(window)
            entry.place(x=width, y=height, width=250)
            record.append(entry)
            count -= 1
            y += 33
            height += 33
    return record


def add_record_table(lst: list):
    """
    This function adds a new string  to the table in the database

    :param lst: список чего-то там enters_data
    :return: nothing
    """
    global table
    con = sqlite3.connect(data_base)
    cur = con.cursor()
    cur.execute('INSERT INTO ' + table + ' VALUES (%s)' % ','.join('?' * len(lst)), lst)
    con.commit()
    cur.close()
    con.close()


def mistake_enter_fields():
    """
    This function displays an error message when the user has not completed all fields

    :return: nothing
    """
    win_mistake_enter_fields = Toplevel(root)
    win_mistake_enter_fields.title("Ошибка")
    win_mistake_enter_fields.geometry('200x40')
    message = Label(win_mistake_enter_fields, text="Сначала заполните все поля!", width=30, height=2)
    message.place(x=-5, y=0)


def get_item():
    """
    This function obtains values ​​from input fields and writes them to a table

    :return: nothing
    """
    global enters_data, record, table

    remember_table = table
    enters_data.clear()
    for i in range(len(record)):
        try:
            a = record[i]
            b = a.get()
            enters_data.append(b)
            a.delete(0, END)
        except TclError:
            pass

    if '' in enters_data:
        mistake_enter_fields()

    if len(enters_data) > 1:
        add_record_table(enters_data)

    if remember_table != table:
        record.clear()


def create_delete_entry(columns: list, win, x: int, y: int):
    """
    This function creates a field for entering data and selecting a parameter for searching

    :param columns: list of columns
    :param win: window
    :param x: weight
    :param y: height
    :return: ttk.Combobox - widget in which we will save the row search parameter
    when deleting a row from the table
    """
    global choice, search_delete_enter
    window_for_search = Frame(win)
    window_for_search.place(x=x, y=y)
    search_delete_enter = ttk.Combobox(window_for_search, values=columns, height=3)
    search_delete_enter.set(u'Выбор параметра')
    search_delete_enter.grid(column=0, row=0)
    choice = search_delete_enter
    return choice


def mistake_select_value():
    """
    This function displays an error message when the user has not selected value from list

    :return: nothing
    """
    win5 = Toplevel(root)
    win5.title("Ошибка")
    win5.geometry('270x40')
    lbl12 = Label(win5, text="Сначала выберите значение из списка!", width=45, height=2)
    lbl12.place(x=-30, y=0)


def mistake_not_found():
    """
    This function displays an error message when value not found in database

    :return: nothing
    """
    win6 = Toplevel(root)
    win6.title("Ошибка")
    win6.geometry('270x40')
    lbl13 = Label(win6, text="Значение не найдено в базе данных!", width=45, height=2)
    lbl13.place(x=-30, y=0)


def get_result_from_db() -> list:
    """
    This function get list of results from table

    :return: list of results from table
    """
    global choice, confirmation, res, data, column_names, result, choice_row
    column_names = data[0]
    try:
        confirmation.after(1, confirmation.destroy)
    except AttributeError:
        pass
    choice_row = choice.get()
    res = place_for_enter.get()
    if choice_row in column_names:
        result = simple_search_from_db(data_base, table, choice_row, res)
        return result
    else:
        mistake_select_value()


def choice_of_param():
    """
    This function display list of results on the delete screen

    :return: list of results from table
    """
    global output1, confirmation, win_create_delete_str, result
    result = get_result_from_db()
    if result == 'Значение не найдено в базе данных!':
        output1.delete(1.0, END)
        mistake_not_found()

    output1.delete(1.0, END)
    if len(result) == 1:
        confirmation = Label(win_create_delete_str, text="Вы действительно хотите удалить эту строку?")
    elif len(result) > 1:
        confirmation = Label(win_create_delete_str, text="Вы действительно хотите удалить эти строки?")
    confirmation.place(x=15, y=40)
    for i in range(len(result)):
        output1.insert(END, result[i])
        output1.insert(END, '\n')

    return result


def cancel():
    """
    This function deletes the label, the display field and the input field in the delete window

    :return: nothing
    """
    global confirmation, output1, place_for_enter
    output1.delete(1.0, END)
    confirmation.after(1, confirmation.destroy)
    place_for_enter.delete(0, END)


def delete_record():
    """
    This function removes the selected row from the database table and clears the output window

    :return: nothing
    """
    global data_base, table, choice, res, confirmation, output1, place_for_enter, choice_row
    choice_row = choice.get()
    sqlite3_simple_delete_record(data_base, table, choice_row, res)
    output1.delete(1.0, END)
    confirmation.after(1, confirmation.destroy)
    place_for_enter.delete(0, END)


def update_record():
    """
    This function update value in table

    :return: nothing
    """
    global data_base, table, choice, res, output1, result, column_names, choice_row, number_str
    a = output1.get('1.0', END)
    a = a[0:-1]
    changed_string = a.split('\n')
    changed_string = changed_string[0:-2]

    number_str = int(number_str) - 1
    source_string = []
    for i in result:
        for j in i:
            source_string.append(j)

    for i in range(0, 4):
        try:
            if changed_string[i] == source_string[i]:
                pass
        except IndexError:
            pass
        else:
            param_value = changed_string[i]
            step = i
            param_column = column_names[step]
            sqlite3_update_record(data_base, table, param_column, param_value, choice_row, res)
    output1.delete(1.0, END)


def choice_param_of_search():
    """
    This function display list of results on the main screen

    :return: list of results from table
    """
    global result, output_on_display, choice, entry1, place_for_enter, search_delete_enter, import_lst
    import_lst.clear()
    choice = search_delete_enter
    place_for_enter = entry1
    result = get_result_from_db()
    if result == 'Значение не найдено в базе данных!':
        output_on_display.delete(1.0, END)
        mistake_not_found()

    output_on_display.delete(1.0, END)
    import_lst = []
    counter_row = 0
    try:
        for j in result:
            lst = list(j)
            import_lst.append(lst)
    except TypeError:
        pass
    try:
        for i in range(len(result)):
            output_on_display.insert(END, str(import_lst[i]) + '\t')
            counter_row += 1
            output_on_display.insert(END, '\n')
    except TypeError:
        pass
    text_message = f'Найдено колонок: {counter_row}'
    sum_rows = Label(root, text=text_message, width=20, height=1)
    sum_rows.place(x=15, y=570)
    return result


def create_delete_window():
    """
    This function create window for delete record in the table of database

    :return: nothing
    """
    global data, column_names, output1, win_create_delete_str, place_for_enter
    try:
        column_names = data[0]
        win_create_delete_str = Toplevel(root, relief=SUNKEN, bd=10, bg="light sky blue")
        win_create_delete_str.title("Окно выбора данных")
        win_create_delete_str.minsize(width=500, height=300)
        create_delete_entry(column_names, win_create_delete_str, 5, 10)
        enter_data_button = ttk.Button(win_create_delete_str, text="  Ввод  ", command=choice_of_param)
        enter_data_button.place(x=420, y=10)
        place_for_enter = Entry(win_create_delete_str)
        place_for_enter.place(x=150, y=10, width=250)
        output1 = Text(win_create_delete_str, width=40, height=10, font="12", wrap=WORD)
        output1.place(x=10, y=80)

        but_delete = ttk.Button(win_create_delete_str, text="  Удалить ", command=delete_record)
        but_delete.place(x=394, y=85)

        but_cancel = ttk.Button(win_create_delete_str, text="  Отмена  ", command=cancel)
        but_cancel.place(x=394, y=135)

        but_cancel = ttk.Button(win_create_delete_str, text="  Обновить  ", command=output)
        but_cancel.place(x=390, y=185)

    except IndexError:
        mistake_load_table()


def get_choose():
    """
    This function displays a string to update if more than one match has been found

    :return: nothing
    """
    global result, choose, win_update_concurrence, output1, confirmation, win_create_update_str, number_str
    number_str = choose.get()
    result = result[int(number_str) - 1]
    output1.delete(1.0, END)
    for i in result:
        output1.insert(END, str(i) + '\n')
    confirmation.destroy()
    confirmation = Label(win_create_update_str, text='Измените строку и нажмите "Редактировать"')
    confirmation.place(x=15, y=40)
    win_update_concurrence.destroy()


def find_more_one_str():
    """
    This function displays a data selection window if more than one row was found during the update

    :return: nothing
    """
    global win_update_concurrence, choose
    win_update_concurrence = Toplevel(win_create_update_str)
    win_update_concurrence.title("Выберите значение")
    win_update_concurrence.geometry('240x60')
    lbl12 = Label(win_update_concurrence, text="Какую строку вы хотите обновить?", width=45, height=2)
    lbl12.place(x=-50, y=0)
    choose = Entry(win_update_concurrence)
    choose.place(x=15, y=30, width=50)
    enter_button1 = ttk.Button(win_update_concurrence, text="  Ввод  ", command=get_choose)
    enter_button1.place(x=100, y=30)
    confirmation.place(x=15, y=40)


def choice_of_update_param() -> list:
    """
    This function searches the database and displays founded values found on the screen of updating string

    :return: List of results from table
    """
    global choice, output1, confirmation, res, data, column_names, win_create_update_str, result, \
        choice_row, my_lst, zero, place_for_enter
    column_names = data[0]
    try:
        confirmation.after(1, confirmation.destroy)
    except AttributeError:
        pass
    choice_row = choice.get()
    res = place_for_enter.get()
    if choice_row in column_names:
        result = simple_search_from_db(data_base, table, choice_row, res)

        if result == 'Значение не найдено в базе данных!':
            output_on_display.delete(1.0, END)
            mistake_not_found()
        output1.delete(1.0, END)

        if len(result) == 1:
            confirmation = Label(win_create_update_str, text="Вы действительно хотите обновить эту строку?")
            confirmation.place(x=15, y=40)

        elif len(result) > 1:
            cnt = 1
            j = 0
            count = 0
            for w in range(len(result) - 1):
                for i in range(len(result[0])):
                    if result[j][count] == result[cnt][count]:
                        count += 1
                    else:
                        my_lst.append(result[j][count])
                j += 1
                cnt += 1
                zero = count

            confirmation = Label(win_create_update_str, text="Найдено более чем одно совпадение")
            find_more_one_str()

        for i in result:
            for j in i:
                output1.insert(END, str(j) + '\n')
            output1.insert(END, '\n')
        return result
    else:
        mistake_select_value()


def create_update_window():
    """
    This function create window for update record in the table of database

    :return: nothing
    """
    global data, column_names, output1, place_for_enter, win_create_update_str
    try:
        column_names = data[0]
        win_create_update_str = Toplevel(root, relief=SUNKEN, bd=10, bg="light sky blue")
        win_create_update_str.title("Окно выбора данных")
        win_create_update_str.minsize(width=500, height=300)
        create_delete_entry(column_names, win_create_update_str, 5, 10)
        enter_data_button = ttk.Button(win_create_update_str, text="  Ввод  ", command=choice_of_update_param)
        enter_data_button.place(x=420, y=10)
        place_for_enter = Entry(win_create_update_str)
        place_for_enter.place(x=150, y=10, width=250)

        output1 = Text(win_create_update_str, width=40, height=10, font="12", wrap=WORD)
        output1.place(x=10, y=80)

        but_update = ttk.Button(win_create_update_str, text="  Редактировать ", command=update_record)
        but_update.place(x=383, y=85)

        but_cancel = ttk.Button(win_create_update_str, text="  Отмена  ", command=cancel)
        but_cancel.place(x=398, y=135)

        but_cancel = ttk.Button(win_create_update_str, text="  Обновить  ", command=output)
        but_cancel.place(x=394, y=185)

    except IndexError:
        mistake_load_table()


def cancel_main():
    """
    This function clears the main screen after the search and displays information from the table again

    :return: nothing
    """
    entry1.delete(0, END)
    output_on_display.delete(1.0, END)
    output()


def save_txt_file():
    """
    This function receives information from the main screen and writes it to a file with the extension txt

    :return: nothing
    """
    global output_on_display
    if data_base == '':
        mistake_load_table()
    else:
        save_name = asksaveasfilename(title="Select file", filetypes=(("TXT", "*.txt"), ("all files", "*.*")),
                                      defaultextension='.txt')
        if Path(save_name).suffix == '.txt':
            data_txt = output_on_display.get('1.0', 'end')
            f = open(save_name, 'w')
            f.write(data_txt)
            f.close()


def save_csv_file():
    """
    This function receives information from the main screen and writes it to a file with the extension csv

    :return: nothing
    """
    global output_on_display, import_lst, column_names, data
    if data_base == '':
        mistake_load_table()
    else:
        column_names = data[0]
        save_name = asksaveasfilename(title="Select file", filetypes=(("CSV", "*.csv"), ("all files", "*.*")),
                                      confirmoverwrite=True, defaultextension='.csv')
        step = len(column_names)
        data_csv = import_lst
        if len(data_csv[0]) == step:
            pass
        else:
            data_csv = import_lst[step::]

        with open(save_name, 'w+') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(column_names)
            csv_writer.writerows(data_csv)


def save_xml_file():
    """
    This function receives information from the main screen and writes it to a file with the extension xml

    :return: nothing
    """
    global output_on_display, import_lst, column_names, data
    if data_base == '':
        mistake_load_table()
    else:
        column_names = data[0]
        step = len(column_names)

        save_name = asksaveasfilename(title="Select file", filetypes=(("XML", "*.xml"), ("all files", "*.*")),
                                      confirmoverwrite=True, defaultextension='.xml')
        data = import_lst

        if len(data[0]) == step:
            pass
        else:
            data = import_lst[step::]

        data2 = list(map(list, zip(*data)))

        data3 = {key: value for key, value in zip(column_names, data2)}

        column = list(data3.keys())

        df = pd.DataFrame(data3, columns=column)

        data_dict = df.to_dict(orient="records")
        with open('output.json', "w+") as f:
            json.dump(data_dict, f, indent=4)

        xml_data = dicttoxml(data_dict).decode()
        with open(save_name, "w+") as f:
            f.write(xml_data)

        data.clear()
        data2.clear()
        data3.clear()


def save_json_file():
    """
    This function receives information from the main screen and writes it to a file with the extension json

    :return: nothing
    """
    global output_on_display, import_lst, column_names, data, new_data
    if data_base == '':
        mistake_load_table()
    else:
        column_names = new_data
        step = len(column_names)
        save_name = asksaveasfilename(title="Select file", filetypes=(("JSON", "*.json"), ("all files", "*.*")),
                                      confirmoverwrite=True, defaultextension='.json')
        data = import_lst

        if len(data[0]) == step:
            pass
        else:
            data = import_lst[step::]

        data2 = list(map(list, zip(*data)))

        data3 = {key: value for key, value in zip(column_names, data2)}

        column = list(data3.keys())

        df = pd.DataFrame(data3, columns=column)

        data_dict = df.to_dict(orient="records")
        with open(save_name, "w+") as f:
            json.dump(data_dict, f, indent=4)

        data.clear()
        data2.clear()
        data3.clear()


def create_help_window():
    """
    This function create the help window and displays buttons

    :return: nothing
    """
    global help_window
    help_window = Toplevel(root, relief=SUNKEN, bd=10, bg="light sky blue")
    help_window.title("Справка")
    help_window.minsize(width=1000, height=550)
    main_win_button = ttk.Button(help_window, text="   Главное окно    ", command=help_main_but)
    main_win_button.place(x=20, y=50)
    add_db_table = ttk.Button(help_window, text="Добавить базу данных", command=help_add_db)
    add_db_table.place(x=10, y=120)
    add_string_button = ttk.Button(help_window, text=" Добавить строку ", command=help_add_str)
    add_string_button.place(x=15, y=190)
    load_file_button = ttk.Button(help_window, text="  Загрузить файл  ", command=help_load_file)
    load_file_button.place(x=20, y=260)
    del_string_button = ttk.Button(help_window, text="  Удалить строку   ", command=help_del_str)
    del_string_button.place(x=20, y=330)
    download_file_button = ttk.Button(help_window, text=" Выгрузить файл  ", command=help_download_file)
    download_file_button.place(x=20, y=400)
    update_string_button = ttk.Button(help_window, text=" Обновить строку ", command=help_update_str)
    update_string_button.place(x=20, y=470)


def help_add_db():
    """
    This function changes list of pictures and call help_main function, which create display for pictures
    :return: nothing
    """
    global picture_lst
    picture_lst = ["test/db1.jpg", "test/db2.jpg", "test/db3.jpg", "test/db4.jpg", "test/db5.jpg",
                   "test/db6.jpg", "test/db7.jpg", "test/db8.jpg", "test/db9.jpg", "test/db10.jpg"]
    help_main()


def help_main_but():
    """
    This function changes list of pictures and call help_main function, which create display for pictures
    :return: nothing
    """
    global picture_lst
    picture_lst = ["test/main.png", "test/main2.jpg", "test/main3.jpg", "test/main4.jpg", "test/main5.jpg",
                   "test/main6.jpg"]
    help_main()


def help_add_str():
    """
    This function changes list of pictures and call help_main function, which create display for pictures
    :return: nothing
    """
    global picture_lst
    picture_lst = ["test/add1.jpg", "test/add2.jpg", "test/add3.jpg", "test/add4.jpg"]
    help_main()


def help_load_file():
    """
    This function changes list of pictures and call help_main function, which create display for pictures
    :return: nothing
    """
    global picture_lst
    picture_lst = ["test/load1.png", "test/load2.png", "test/load3.png", "test/load4.png"]
    help_main()


def help_del_str():
    """
    This function changes list of pictures and call help_main function, which create display for pictures
    :return: nothing
    """
    global picture_lst
    picture_lst = ["test/del1.jpg", "test/del2.jpg", "test/del3.jpg", "test/del4.jpg", "test/del5.jpg"]
    help_main()


def help_download_file():
    """
    This function changes list of pictures and call help_main function, which create display for pictures
    :return: nothing
    """
    global picture_lst
    picture_lst = ["test/download1.png", "test/download2.png", "test/download3.png", "test/download4.png",
                   "test/download5.png", "test/download6.png", "test/download7.png", "test/download8.png",
                   "test/download9.png", "test/download10.png", "test/download11.png", "test/download12.png",
                   "test/download13.png"]
    help_main()


def help_update_str():
    """
    This function changes list of pictures and call help_main function, which create display for pictures
    :return: nothing
    """
    global picture_lst
    picture_lst = ["test/update1.jpg", "test/update2.jpg", "test/update3.jpg", "test/update4.jpg", "test/update5.jpg",
                   "test/update6.jpg"]
    help_main()


def forward():
    """
    This function displays the help window and sets the base picture

    :return: nothing
    """
    global my_iterator, iterable, canvas, help_window, forward_button, image
    try:
        iterable = next(my_iterator)
        pill_image = Image.open(iterable)
        image = ImageTk.PhotoImage(pill_image)
        canvas.create_image(10, 10, anchor=NW, image=image)
        help_window.mainloop()
    except StopIteration:
        forward_button.destroy()


def help_main():
    """
    This function allows you to process the list of pictures and display them on the screen

    :return: nothing
    """
    global help_window, my_iterator, iterable, canvas, forward_button, picture_lst, image
    my_iterator = iter(picture_lst)
    pill_image = Image.open(image_base)
    image = ImageTk.PhotoImage(pill_image)

    canvas = Canvas(help_window, width=700 + 15, height=490 + 15)
    canvas.create_image(10, 10, anchor=NW, image=image)

    canvas.place(x=170, y=10)

    forward_button = ttk.Button(help_window, text=" Вперед ", command=forward)
    forward_button.place(x=910, y=250)
    help_window.mainloop()

# buttons


menu1 = Menu(root, tearoff=False)
menu1.add_cascade(label="Создать новый файл .db", command=create_new_db)
menu1.add_cascade(label="Создать новую таблицу", command=lambda: create_win_create_table())

image1 = ImageTk.PhotoImage(file="pictures/ph.jpg")
but1 = ttk.Menubutton(root, text="test", menu=menu1, image=image1)
but1.place(x=0, y=0)

image3 = ImageTk.PhotoImage(file="pictures/add.jpg")
but3 = ttk.Button(image=image3, command=create_enter_window)
but3.place(x=150, y=0)

image4 = ImageTk.PhotoImage(file="pictures/file_upload.jpg")
but4 = ttk.Button(image=image4, command=load_file)
but4.place(x=304, y=0)

image5 = ImageTk.PhotoImage(file="pictures/del.jpg")
but5 = ttk.Button(image=image5, command=create_delete_window)
but5.place(x=398, y=0)

menu2 = Menu(root, tearoff=False)
menu2.add_cascade(label="Выгрузить в .txt", command=save_txt_file)
menu2.add_cascade(label="Выгрузить в .csv", command=save_csv_file)
menu2.add_cascade(label="Выгрузить в .xml", command=save_xml_file)
menu2.add_cascade(label="Выгрузить в .json", command=save_json_file)

image6 = ImageTk.PhotoImage(file="pictures/file_download.jpg")
but6 = ttk.Menubutton(root, menu=menu2, image=image6)
but6.place(x=552, y=0)

image7 = ImageTk.PhotoImage(file="pictures/images1.png")
but7 = ttk.Button(image=image7, command=create_update_window)
but7.place(x=645, y=0)

image8 = ImageTk.PhotoImage(file="pictures/help.png")
but8 = ttk.Button(image=image8, command=create_help_window)
but8.place(x=798, y=0)

ram_for_list_of_table = Frame(width=155, height=310, bg="light sky blue", relief=SUNKEN, bd=10)
ram_for_list_of_table.place(x=10, y=250)

lbl1 = Label(root, text="Загрузите таблицу и \nвыберите параметры поиска", width=30, height=2)
lbl1.place(x=-20, y=160)

entry1 = Entry(root)
entry1.place(x=230, y=160, width=540)

enter_button = ttk.Button(text="  Ввод  ", command=choice_param_of_search)
enter_button.place(x=800, y=155)

enter_button = ttk.Button(text="  Отмена ", command=cancel_main)
enter_button.place(x=795, y=200)

my_frame = Frame(root)
my_frame.grid()

create_delete_entry(column_names, root, 10, 210)

root.mainloop()

if __name__ == '__main__':
    pass
