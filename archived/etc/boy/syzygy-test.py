#!/usr/bin/env python3
#
# Copyright (c) 2021, F5 Networks, Inc.  All rights reserved.
#
# TODO: Add module docstring
"""

HOW TO RUN IT
-------------

# TODO: Add the path to the test
$ testtool.py run \
    -t src/tests_vanquish/common/PATH_TO_TEST \
    -e <EQUIPMENT_SERIAL_NUMBER>
"""
from syzygy.runtime import actions, conditions, results, testcase
from syzygy_equipment.specification import Equipment, EquipmentList


class (testcase.TestCase):
    """
    # TODO: docstring
    """
    __equipment__ = EquipmentList([Equipment("dut").service("network")])

    def __init__(self, dut):
        super().__init__()
        self.dut = dut

    def setup(self):
        pass

    def run(self):
        pass

    def teardown(self):
        pass


