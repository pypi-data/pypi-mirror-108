#!/usr/bin/env python

import pandas
import os
from mlops.dataset import DataSet


class Local(DataSet):
    def __init__(self, file_name=os.environ.get("LOCAL_FILE_NAME", None)):
        self.file_name = file_name

    def print_data(self, sep):
        data = pandas.read_csv(self.file_name, sep=sep, encoding='utf-8')
        print('Printing the data frame:')
        print(data)

    def remove_unnamed_column(self, data):
        data.columns.str.match("Unnamed")
        data.loc[:, ~data.columns.str.match("Unnamed")]
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
        return data

    def data_collection(self, file_name1, file_name2, column_name_left, how, sep):
        data1 = pandas.read_csv(file_name1, sep=sep, encoding='utf-8')
        data2 = pandas.read_csv(file_name2, sep=sep, encoding='utf-8')
        output = pandas.merge(data1, data2, on=column_name_left, how=how)
        output = self.remove_unnamed_column(output)
        print(output)
        output.to_csv(self.file_name, sep=sep, index=False)

    def formatting_data(self, file_name, column_name, to_replace, value, sep):
        data = pandas.read_csv(file_name, sep=sep, encoding='utf-8')
        data[column_name] = data[column_name].replace(to_replace, value)
        data = self.remove_unnamed_column(data)
        data.to_csv(self.file_name, sep=sep, index=False)

    def agregation_data(self, file_name, new_column_name, column_name_a, column_name_b, sep):
        data = pandas.read_csv(file_name, sep=sep, encoding='utf-8')
        new_col = (data[column_name_a] + data[column_name_b]).tolist()
        data[new_column_name] = new_col
        data.to_csv(self.file_name, sep=sep, index=False)
