#!/usr/bin/env python

import os
import errno


class Util(object):
    @staticmethod
    def create_dir(local_dir):
        try:
            os.makedirs(local_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
