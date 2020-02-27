import unittest

from classes.date_delivery import DateDelivery, compute_achievement


class DateDeliveryTest(unittest.TestCase):

    # =============  Null list  =============
    def test_null_data_1(self):
        list= [5,6,54,8,6,4,6,8,9,4,5,6]
        expected= [5,6,'null','null','null','null','null','null','null','null','null','null']
        new_list =DateDelivery(list,'2020').new_list
        self.assertEqual(new_list, expected)

    def test_null_data_2(self):
        list= [5,6,54,8,6,4,6,8,9,4,5,6]
        expected= ['null','null','null','null','null','null','null','null','null','null','null','null']
        new_list =DateDelivery(list,'2021').new_list
        self.assertEqual(new_list, expected)

    def test_null_data_3(self):
        list= [5,6,54,8,6,4,6,8,9,4,5,6]
        new_list =DateDelivery(list,'2019').new_list
        self.assertEqual(new_list, list)

    def test_compute_achievement_1(self):
        list= [20,20,30,20,'null']
        list1= [20,21,29,'null','null']
        expected= [True,False,True,True,True]
        new_list = compute_achievement(list,list1)
        self.assertEqual(new_list, expected)
