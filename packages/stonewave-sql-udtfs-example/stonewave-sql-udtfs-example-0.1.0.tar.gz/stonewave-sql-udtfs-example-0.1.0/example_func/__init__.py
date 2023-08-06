from stonewave.sql.udtfs.base_function import BaseFunction, udtf
from stonewave.sql.udtfs.logger import logger
from stonewave.sql.udtfs.utility import get_arrow_data_type_from_value


@udtf(is_parser=False)
class GenerateTableFunction(BaseFunction):
    def get_name(self):
        """
        :return: the name of the table function
        """
        return "generate_table_func"

    def initialize(self, table_row_writer):
        """
        This method will be called once for every batch in the input table with function applied
        :param table_row_writer: the row writer for writing produced results
        :return: None
        """
        pass

    def __init__(self):
        pass

    def process(self, table_row_writer, row_idx, row):
        """
        This method is used to process the current row of input, and it will be called once for every row in an input table.
        :param table_row_writer: Use the `table_row_writer` to write the produced rows into the result table.
        See the table_row_writer API for details.
        :param row_idx: the row index for the current row and current batch
        :param row: a list containing all of the parameters from the current row
        :return: None
        """

        """
        # method 1:
        # using kvpairs to append row, kv pairs means column_name and column value
        # all column are in string datatype
        row_num = row[0]
        for i in range(row_num):
            kv_pairs = {}
            for j in range(1, len(row)):
                cell = str(row[j])
                kv_pairs["col_{}".format(j)] = cell
            table_row_writer.record_batch_builder.append_row(kv_pairs)
        """

        # method 2:
        # using add_column to add a column using pyarrow datatype
        # using extend to append multiple value for column
        row_nums = row[0]
        logger.info("generate result batch", row_nums=row_nums)
        for i in range(1, len(row)):
            cell = row[i]
            column_name = "col_{}".format(i)
            table_row_writer.record_batch_builder.add_column(column_name, get_arrow_data_type_from_value(cell))
            table_row_writer.record_batch_builder.extend(column_name, [cell for j in range(row_nums)])
        table_row_writer.record_batch_builder.increase_row_count(row_nums)
