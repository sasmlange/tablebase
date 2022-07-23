import re


class Table(object):
    """The Table class is the basic table in tablebase."""
    name = ""
    table_content = [[]]
    """
    The table_content holds the table data
    """

    def display(self, divider=", "):
        """
        Use display for pretty-printing to the console.

        :param divider: Used to customize the divider between the columns.
        :return: A string with a pretty-print of your table.
        """
        string = ""
        for row in self.table_content:
            for record in range(int(len(row))):
                string = string + str(row[record])
                if int(len(row)) != record + 1:
                    string = string + str(divider)
            string = string + "\n"
        return string

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
        :return: A list of all data in one column.
        """
        col_position = self.table_content[0].index(col_name)

        col = []

        for i in range(int(len(self.table_content))-1):
            col.append(self.table_content[i+1][col_position])

        return col

    def add_legacy_expand(self, new_col_name, old_col_name, action, value):
        """
        Used to add a column that is based on another column. If you want to use the non legacy way to add an expand, see the add_expand function

        :param new_col_name: The name for you new column.
        :param old_col_name: The name for the column you wish to expand from.
        :param action: What change you want from your old column to your new column. Can be "+" (or "add"), "-" (or subtract), "*" (or multiply), "/" (or divide), or "join" for combining two strings.
        :param value: What difference from the old column you wish to make. For example, if your action was "*", then and your value was "2", everything would get multiplied by two.
        :return:
        """
        result = []


        for i in self.get_col(old_col_name):
            if action == "+" or action == "add":
                result.append(float(i) + float(value))

            elif action == "-" or action == "subtract":
                result.append(float(i) - float(value))

            elif action == "*" or action == "multiply":
                result.append(float(i) * float(value))

            elif action == "/" or action == "divide":
                result.append(float(i) / float(value))

            elif action == "join":
                result.append(str(i) + str(value))

            else:
                raise Exception(f"Unknown action '{action}'")

        self.add_col(new_col_name, result)

    def _private_expand(self, formula):
        col_names_found = re.findall("@(.+?)@", formula)

        results = []

        for i in range(int(len(self.table_content)) - 1):
            current_formula = formula
            for j in col_names_found:
                current_formula = current_formula.replace(f"@{j}@", str(self.get_col(j)[i]))

            results.append(eval(current_formula))

        return results

    def add_expand(self, new_col_name, formula):
        """
         Used to add a column that is based on another column.

        :param new_col_name: The new name for your column.
        :param formula: The formula for your expand. More info coming soon!
        :return:
        """

        self.add_col(new_col_name, self._private_expand(formula))

    def expand(self, col_name, formula):
        """
         Used to override a column that is based on another column.

        :param col_name: The name of the column that you want to override.
        :param formula: The formula for your expand. More info coming soon!
        :return:
        """

        self.override_col(col_name, self._private_expand(formula))

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

    def edit_row(self, row_num, col_name, new_value):
        """
        Used to edit a record of your table.

        :param row_num: The row number of the record that you wish to edit.
        :param col_name: The column name of your record that you wish to edit.
        :param new_value: The new record value.
        :return:
        """
        self.table_content[row_num][self.table_content[0].index(col_name)] = new_value

    def filter(self, col_name, value, type="exact", search_start=1, search_end="END", add_headers_to_result=True, legacy=False):
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
        content = self.display(divider)
        with open(path, 'w') as csv:
            csv.write(content)


class CsvTable(Table):
    """
    Used to import a CSV file.

    :param csv_path: The path to your CSV
    :param divider: The divider between columns.
    """
    def __init__(self, csv_path, divider=","):
        self.csv_path = csv_path

        with open(csv_path) as csv_file:
            csv_content = csv_file.read()

        csv_content = csv_content.split("\n")

        csv_content_list = []
        for row in csv_content:
            csv_content_list.append(row.split(divider))

        self.table_content = csv_content_list
