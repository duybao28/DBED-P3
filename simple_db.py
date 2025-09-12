import os

from b_tree import BTree


class SimpleDatabase:
    def __init__(self):
        # before an actual table is loaded, class members are set to None

        # a header is a list of column names
        # e.g., ['name', 'id', 'grade']
        self.header = None

        # map column name to column index in the header
        self.columns = None

        # None if table is not loaded
        # otherwise list b-tree indices corresponding to columns
        self.b_trees = None

        # rows contains actual data; this is a list of lists
        # specifically, this is a list of rows, where each row
        # is a list of values for each column
        # e.g., if a table with the above header has two rows
        # self.rows can be [['Alice', 'a1234', 'HD'], ['Bob', 'a7654', 'D']]
        self.rows = None

        # name of the loaded table
        self.table_name = None

    def get_table_name(self):
        return self.table_name

    def load_table(self, table_name, file_name):
        # note our DBMS only supports loading one table at a time
        # as we load new table, the old one will be lost
        print(f"loading {table_name} from {file_name} ...")

        if not os.path.isfile(file_name):
            print("File not found")
            return

        # note, you could use a CSV module here, also we don't check
        # correctness of file
        with open(file_name) as f:
            self.header = f.readline().rstrip().split(",")
            self.rows = [line.rstrip().split(",") for line in f]
        self.table_name = table_name

        self.columns = {}
        for i, column_name in enumerate(self.header):
            self.columns[column_name] = i

        self.b_trees = [None] * len(self.header)
        print("... done!")

    def create_index(self, column_name):
        if self.table_name is None:         #Check for existence of table
            print("no table loaded")
            return
        if column_name not in self.columns: #Check for existence of column
            print("no such column")
            return

        column_id = self.columns[column_name]
        if self.b_trees[column_id] is not None: #Check for existence of index
            print("index already exists")
            return

        b_tree = BTree()
        for row_id, row in enumerate(self.rows):
            key = row[column_id]
            b_tree.insert_key(key, row_id)
        self.b_trees[column_id] = b_tree    #Create index
        print("index created")

    def drop_index(self, column_name):
        if self.table_name is None:         #Check for existence of table
            print("no table loaded")
            return
        if column_name not in self.columns: #Check for existence of column
            print("no such column")
            return

        column_id = self.columns[column_name]
        if self.b_trees[column_id] is None: #Check for existence of index
            print("no index to drop")
            return

        self.b_trees[column_id] = None      #Drop index
        print("index dropped")

    def get_indexed_columns(self):
        if self.columns is None:
            return []
        return [name for name, index in self.columns.items() if self.b_trees[index] is not None]

    def select_rows(self, table_name, column_name, column_value):
        # modify this code such that row selection uses index if it exists
        # note that our DBMS only supports loading one table at a time
        if table_name != self.table_name:
            # no such table
            return [], []

        if column_name not in self.columns:
            # no such column
            return self.header, []

        col_id = self.columns[column_name]

        selected_rows = []
        b_tree = self.b_trees[col_id]
        if b_tree is not None:
            result = b_tree.search_key(column_value)
            if result is not None:
                node, key_index = result
                row_ids = node.key_vals[key_index][1]
                for row_id in row_ids:
                    selected_rows.append(self.rows[row_id])
        else:
            for row in self.rows:
                if row[col_id] == column_value:
                    selected_rows.append(row)

        return self.header, selected_rows
