from __future__ import annotations
import re
import csv
import warnings
from typing import Union, Any


def formula_setup(added_objects):
    """
    Add packages, modules, variables, functions, and other objects to be used in expand and filter formulas.

    :param added_objects: A list containing the objects you want to include
    :return:
    """

    if type(added_objects) is not list:
        added_objects = [added_objects]

    for added_object in added_objects:
        globals()[added_object.__name__] = added_object


class Table(object):
    """The Table class is the basic table in tablebase."""
    name = ""
    table_content = [[]]
    """
    The table_content holds the table data
    
    .. note::

        :code:`.table_content` returns a list of lists
    
    """

    def display(self, divider: str = "") -> None:
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

    def override_col(self, col_name: str, value: list) -> None:
        """
        Used to override all content in the column

        :param col_name: The name of the column
        :param value: A list with your new column content.
        :return:
        """

        col_num = self.table_content[0].index(col_name)
        for i in range(int(len(self.table_content)) - 1):
            self.table_content[i + 1][col_num] = value[i]

    def rename_col(self, col_name: str, new_col_name: str) -> None:
        """
        Used to rename a column.

        :param col_name: The current name of the column
        :param new_col_name: The new name that you want to give your column
        :return:
        """
        self.table_content[0][self.table_content[0].index(col_name)] = new_col_name

    def del_col(self, col_name: str) -> None:
        """
        Used to delete a column

        :param col_name: The name of the column you wish to delete
        :return:
        """

        del_num = self.table_content[0].index(col_name)

        for i in range(int(len(self.table_content))):
            self.table_content[i].pop(del_num)

    def get_col(self, col_name: str) -> list:
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

    def __string_type(self, string: str) -> str:
        if type(string) is str:
            return f"'{string}'"
        else:
            return string

    def __private_expand(self, formula: str) -> list:
        col_names_found = re.findall("@(.+?)@", formula)

        results = []

        for i in range(int(len(self.table_content)) - 1):
            current_formula = formula
            for j in col_names_found:
                current_formula = current_formula.replace(f"@{j}@", str(self.__string_type(self.get_col(j)[i])))

            results.append(eval(current_formula))

        return results

    def add_expand(self, new_col_name: str, formula: str) -> None:
        """
         Used to add a column that is based on another column.

        :param new_col_name: The new name for your column.
        :param formula: The formula (string) for your expand. Use @ signs to name your column names. For example :code:`"@col_name@"`. The return result will be in your result. You can use built-in python functions. Example: :code:`str(int(@col_name@) + 10) + @another_col_name@`
        :return:
        """

        self.add_col(new_col_name, self.__private_expand(formula))

    def expand(self, col_name: str, formula: str) -> None:
        """
         Used to override a column that is based on another column.

        :param col_name: The name of the column that you want to override.
        :param formula: The formula (string) for your expand. Use @ signs to name your column names. For example :code:`"@col_name@"`. The return result will be in your result. You can use built-in python functions. Example: :code:`str(int(@col_name@) + 10) + @another_col_name@`
        :return:
        """

        self.override_col(col_name, self.__private_expand(formula))

    def add_row(self, new_content: Union[list, dict]) -> None:
        """
        Used to add a row to your table.

        :param new_content: A list of the entries you wish to add. It can also be a dictionary with the key being the column name and the value being the content.
        :return:
        """
        if type(new_content) is list:
            if len(new_content) < len(self.table_content[0]):
                warnings.warn(f"Row adding list is only {len(new_content)} items while there are {len(self.table_content[0])} columns")
            new_record = new_content
        elif type(new_content) is dict:
            new_record = []
            for col, col_num in enumerate(self.table_content[0]):
                if col in new_content:
                    new_record.append(new_content[col])
                else:
                    new_record.append("")
        else:
            raise Exception(f"Type {type(new_content)} is not allowed.")
        self.table_content.append(new_record)

    def add_col(self, col_name: str, default_value: Any = "", trim: bool = True) -> None:
        """
        Used to add a column to your table.

        :param col_name: The name of your new column.
        :param default_value: The default value for new records in that column or a list of specific values for this column.
        :param trim: Boolean value to know whether to trim the default list value if longer than other columns
        :return:
        """
        self.table_content[0].append(col_name)

        if type(default_value) is list:
            for i, value in enumerate(default_value):
                if int(len(self.table_content)) <= i + 1:
                    if trim:
                        break
                    else:
                        self.table_content.append([""] * (len(self.table_content[0]) - 1) + [value])
                else:
                    self.table_content[i + 1].append(value)
        else:
            for i in range(int(len(self.table_content)) - 1):
                self.table_content[i + 1].append(default_value)

    def edit_row(self, row_num: int, new_value: Union[list, dict]) -> None:
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

    def edit_cell(self, row_num: int, col_name: str, new_value: Any) -> None:
        """
        Used to edit a cell of your table.

        :param row_num: The row number of the record that you wish to edit.
        :param col_name: The column name of your record that you wish to edit.
        :param new_value: The new record value.
        :return:
        """
        self.table_content[row_num][self.table_content[0].index(col_name)] = new_value

    def filter(self, formula: str, search_start: int = 1, search_end: Union[str, int] = "END") -> Table:
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

    def legacy_filter(self, col_name: str, value: Any, filter_type: str = "exact", search_start: int = 1, search_end: Union[str, int] = "END", add_headers_to_result: bool = True, legacy: bool = False) -> Union[Table, list]:
        """
        Used to filter your table.

        :param col_name: The column you wish to use to filter.
        :param value: The value you wish to use to filter with.
        :param filter_type: The filter type. Can be "exact" (same), "iexact" (not case-sensitive), "greaterthan", or "lessthan".
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

            if filter_type == "exact":
                if i[self.table_content[0].index(col_name)] == value:
                    result_list.append(i)
            elif filter_type == "iexact":
                if i[self.table_content[0].index(col_name)].lower() == value.lower():
                    result_list.append(i)

            elif filter_type == "greaterthan":
                if float(i[self.table_content[0].index(col_name)]) > float(value):
                    result_list.append(i)

            elif filter_type == "lessthan":
                if float(i[self.table_content[0].index(col_name)]) < float(value):
                    result_list.append(i)

            else:
                raise Exception(f'Could not find filter method "{filter_type}"')

        if add_headers_to_result:
            result_list.insert(0, self.table_content[0])

        if legacy:
            return result_list
        else:
            temp_table = Table()
            temp_table.table_content = result_list
            return temp_table

    def count(self) -> int:
        """
        Used to find how many rows in the Table.

        :return: An integer value of the amount of rows.
        """
        return int(len(self.table_content))

    def incorporate(self, new_table: Table) -> None:
        """
        Used to merge data from another table into the object applying the methood.

        :param new_table: The Table object to merge
        :return:
        """

        if new_table.table_content[0] != self.table_content[0]:
            temp_table = Table()
            for col_name in self.table_content[0]:
                if col_name not in new_table.table_content[0]:
                    raise ValueError(f"'{col_name}' is not found in the provided table to be incorporated")
                temp_table.add_col(col_name, new_table.get_col(col_name), False)

            new_table = temp_table

        new_table.table_content.pop(0)

        self.table_content = self.table_content + new_table.table_content

    def save(self, path: str, divider: str = ",") -> None:
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
    def __init__(self, csv_path: str, divider: str = ","):
        with open(csv_path) as csv_file:
            csv_content_list = list(csv.reader(csv_file, delimiter=divider))

        self.table_content = csv_content_list
