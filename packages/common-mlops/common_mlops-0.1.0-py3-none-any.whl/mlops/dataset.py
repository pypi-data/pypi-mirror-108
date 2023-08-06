#!/usr/bin/env python

from abc import ABC
from abc import abstractmethod


class DataSet(ABC):
    @abstractmethod
    def print_data(self):
        pass
