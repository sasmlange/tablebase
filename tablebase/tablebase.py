import re
import csv


class Table(object):
    """The Table class is the basic table in tablebase."""
    name = ""
    table_content = [[]]
    """
    The table_content holds the table data
    
    .. note::

        :code:`.table_content` returns a list of lists
    
    """

    def display(self, divider=""):
        """
        Use display for pretty-printing to the console.

        :param divider: Used to customize the divider between the columns.
        :return:
        """
        longest_cols = [
            (max([len(str(row[i])) for row in self.table_content]) + 3)
            for i in range(len(self.table_content[0]))
        ]
        row_format = "".join(["{:>" + str(longest_col) + "}" + divider for longest_col in longest_cols])
        for row in self.table_content:
            print(row_format.format(*row))

    def override_col(self, col_name, value):
        """
        Used to override all content in the column

        :param col_name: The name of the column
        :param value: A list with your new column content.
        :return:
        """

        col_num = self.table_content[0].index(col_name)
        for i in range(int(len(self.table_content)) - 1):
            self.table_content[i + 1][col_num] = value[i]

    def rename_col(self, col_name, new_col_name):
        """
        Used to rename a column.

        :param col_name: The current name of the column
        :param new_col_name: The new name that you want to give your column
        :return:
        """
        self.table_content[0][self.table_content[0].index(col_name)] = new_col_name

    def del_col(self, col_name):
        """
        Used to delete a column

        :param col_name: The name of the column you wish to delete
        :return:
        """

        del_num = self.table_content[0].index(col_name)

        for i in range(int(len(self.table_content))):
            self.table_content[i].pop(del_num)

    def get_col(self, col_name):
        """
        Used to get all data in one column.

        :param col_name: The name of the column you wish to get.
        :return: A list of all data in one column (column name not included).
        """
        col_position = self.table_content[0].index(col_name)
        temp_table_content = self.table_content[:]
        temp_table_content.pop(0)

        col = []

        for i in temp_table_content:
            col.append(i[col_position])

        return col

    def __string_type(self, string):
        if type(string) is str:
            return f"'{string}'"
        else:
            return string

    def __private_expand(self, formula):
        col_names_found = re.findall("@(.+?)@", formula)

        results = []

        for i in range(int(len(self.table_content)) - 1):
            current_formula = formula
            for j in col_names_found:
                current_formula = current_formula.replace(f"@{j}@", str(self.__string_type(self.get_col(j)[i])))

            results.append(eval(current_formula))

        return results

    def add_expand(self, new_col_name, formula):
        """
         Used to add a column that is based on another column.

        :param new_col_name: The new name for your column.
        :param formula: The formula (string) for your expand. Use @ signs to name your column names. For example :code:`"@col_name@"`. The return result will be in your result. You can use built-in python functions. Example: :code:`str(int(@col_name@) + 10) + @another_col_name@`
        :return:
        """

        self.add_col(new_col_name, self.__private_expand(formula))

    def expand(self, col_name, formula):
        """
         Used to override a column that is based on another column.

        :param col_name: The name of the column that you want to override.
        :param formula: The formula (string) for your expand. Use @ signs to name your column names. For example :code:`"@col_name@"`. The return result will be in your result. You can use built-in python functions. Example: :code:`str(int(@col_name@) + 10) + @another_col_name@`
        :return:
        """

        self.override_col(col_name, self.__private_expand(formula))

    def add_row(self, new_content):
        """
        Used to add a row to your table.

        :param new_content: A list of the entries you wish to add.
        :return:
        """
        self.table_content.append(new_content)

    def add_col(self, col_name, default_value=""):
        """
        Used to add a column to your table.

        :param col_name: The name of your new column.
        :param default_value: The default value for new records in that column or a list of specific values for this column.
        :return:
        """
        self.table_content[0].append(col_name)

        for i in range(int(len(self.table_content)) - 1):
            if type(default_value) is str:
                self.table_content[i + 1].append(default_value)
            elif type(default_value) is list:

                self.table_content[i + 1].append(default_value[i])

    def edit_row(self, row_num, new_value):
        """
        Used to edit a row.

        :param row_num: The row number to edit.
        :param new_value: Use a list override a row. If you use a dictionary, the key will be the column name.
        :return:
        """
        if type(new_value) is not dict and type(new_value) is not list:
            raise TypeError("Only types 'dict' and 'list' are excepted")

        if type(new_value) is dict:
            for row_name, value in new_value.items():
                index = self.table_content[0].index(row_name)
                self.table_content[row_num][index] = value
        else:
            if len(new_value) != len(self.table_content[0]):
                raise ValueError("The new value is not the same length as the table header.")
            self.table_content[row_num] = new_value

    def edit_cell(self, row_num, col_name, new_value):
        """
        Used to edit a cell of your table.

        :param row_num: The row number of the record that you wish to edit.
        :param col_name: The column name of your record that you wish to edit.
        :param new_value: The new record value.
        :return:
        """
        self.table_content[row_num][self.table_content[0].index(col_name)] = new_value

    def filter(self, formula, search_start=1, search_end="END"):
        """
        Used to filter your table.

        :param formula: The formula (string) for your filter. Use @ signs to name your column names. For example :code:`@col_name@`. You can write your filter just like an if statement. Example: :code:`@col_name@ == 'hello'` You can use built-in python functions. Example: :code:`float(@col_name@) + float(@another_col_name@) > 10`
        :param search_start: The row to start filtering at.
        :param search_end: The row to stop filtering at. Type "END" to stop at the end.
        :return: A Table object with the filtered results.
        """
        if search_end == "END":
            search_end = int(len(self.table_content))

        result_list = []
        for i in enumerate(self.table_content[search_start:search_end]):
            col_names_found = re.findall("@(.+?)@", formula)
            current_formula = formula
            for j in col_names_found:
                current_formula = current_formula.replace(f"@{j}@", str(self.__string_type(self.get_col(j)[i[0]])))

            if eval(current_formula):
                result_list.append(i[1])

        result_list.insert(0, self.table_content[0])
        temp_table = Table()
        temp_table.table_content = result_list
        return temp_table

    def legacy_filter(self, col_name, value, type="exact", search_start=1, search_end="END", add_headers_to_result=True, legacy=False):
        """
        Used to filter your table.

        :param col_name: The column you wish to use to filter.
        :param value: The value you wish to use to filter with.
        :param type: The filter type. Can be "exact" (same), "iexact" (not case-sensitive), "greaterthan", or "lessthan".
        :param search_start: The row to start filtering at.
        :param search_end: The row to stop filtering at. Type "END" to stop at the end.
        :param add_headers_to_result: If True, your table headers will be included in the result.
        :param legacy: If True, will return a list instead of a Table object.
        :return: A Table object with the filtered results (unless specified otherwise).
        """
        if search_end == "END":
            search_end = int(len(self.table_content))

        result_list = []
        for i in self.table_content[search_start:search_end]:

            if type == "exact":
                if i[self.table_content[0].index(col_name)] == value:
                    result_list.append(i)
            elif type == "iexact":
                if i[self.table_content[0].index(col_name)].lower() == value.lower():
                    result_list.append(i)

            elif type == "greaterthan":
                if float(i[self.table_content[0].index(col_name)]) > float(value):
                    result_list.append(i)

            elif type == "lessthan":
                if float(i[self.table_content[0].index(col_name)]) < float(value):
                    result_list.append(i)

            else:
                raise Exception(f'Could not find filter method "{type}"')

        if add_headers_to_result:
            result_list.insert(0, self.table_content[0])

        if legacy:
            return result_list
        else:
            temp_table = Table()
            temp_table.table_content = result_list
            return temp_table

    def save(self, path, divider=","):
        """
        Used to save your table for that file.

        :param path: Path to that file.
        :param divider: The divider between columns.
        :return:
        """
        with open(path, 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=divider)
            csv_writer.writerows(self.table_content)


class CsvTable(Table):
    """
    Used to import a CSV file.

    :param csv_path: The path to your CSV
    :param divider: The divider between columns.
    """
    def __init__(self, csv_path, divider=","):
        self.csv_path = csv_path

        with open(csv_path) as csv_file:
            csv_content_list = list(csv.reader(csv_file, delimiter=divider))

        self.table_content = csv_content_list
