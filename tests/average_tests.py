import unittest

from classes.average import AverageList, Average


class AverageListTest(unittest.TestCase):

    # =============  Sum Data  =============
    def test_sum_data_normal(self):
        list = [[(1, 1)], [(4, 2)], [(2, 3)]]
        sum_data = AverageList(list).sum_data()
        self.assertEqual(sum_data, 7)

    def test_sum_data_null_data(self):
        list = [[], [], [], [], [], [], [(50000, '2016', '7')], [], [], [], [], []]
        sum_data = AverageList(list).sum_data()
        self.assertEqual(sum_data, 50000)

    def test_sum_data_all_null_data(self):
        list = [[], [], [], [], [], [], [], [], [], [], [], []]
        sum_data = AverageList(list).sum_data()
        self.assertEqual(sum_data, 0)

    # =============  Cumulative Data  =============
    # Continue
    def test_cumulative_data_normal(self):
        list = [[(1, 1)], [(4, 2)], [(2, 3)]]
        new_list = [1, 5, 7]
        cumulative_data = AverageList(list).cumulative_data(False)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative_data_null_data_continue(self):
        list = [[], [(4, 2)], []]
        new_list = [0, 4, 4]
        cumulative_data = AverageList(list).cumulative_data(False)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative_data_all_null_data_continue(self):
        list = [[], [], []]
        new_list = [0, 0, 0]
        cumulative_data = AverageList(list).cumulative_data(False)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative_data_null_data_continue_2(self):
        list = [[(4, 1)], [], []]
        new_list = [4, 4, 4]
        cumulative_data = AverageList(list).cumulative_data(False)
        self.assertEqual(cumulative_data, new_list)

    # Stop
    def test_cumulative_data_stop(self):
        list = [[(1, 1)], [(4, 2)], [(2, 3)]]
        new_list = [1, 5, 7]
        cumulative_data = AverageList(list).cumulative_data(True)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative_data_null_data_stop(self):
        list = [[(4, 1)], [], []]
        new_list = [4, 'null', 'null']
        cumulative_data = AverageList(list).cumulative_data(True)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative_data_null_data_stop_1(self):
        list = [[], [(4, 2)], [(5, 3)], []]
        new_list = [0, 4, 9, 'null']
        cumulative_data = AverageList(list).cumulative_data(True)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative_data_null_data_stop_2(self):
        list = [[], [(4, 2)], [(5, 3)], [], [(2,4)], []]
        new_list = [0, 4, 9, 9,11,'null']
        cumulative_data = AverageList(list).cumulative_data(True)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative_data_all_null_data_stop(self):
        list = [[], [], []]
        new_list = [0, 'null', 'null']
        cumulative_data = AverageList(list).cumulative_data(True)
        self.assertEqual(cumulative_data, new_list)

    # =============  Cumulative1d Data  =============
    # Continue
    def test_cumulative1d_data_normal(self):
        list = [1,4,2]
        new_list = [1, 5, 7]
        cumulative_data = AverageList(list).cumulative_data_1d(False)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative1d_data_null_data_continue(self):
        list = [0, 4, 0]
        new_list = [0, 4, 4]
        cumulative_data = AverageList(list).cumulative_data_1d(False)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative1d_data_all_null_data_continue(self):
        list = [0, 0, 0]
        new_list = [0, 0, 0]
        cumulative_data = AverageList(list).cumulative_data_1d(False)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative1d_data_null_data_continue_2(self):
        list = [4, 0, 0]
        new_list = [4, 4, 4]
        cumulative_data = AverageList(list).cumulative_data_1d(False)
        self.assertEqual(cumulative_data, new_list)

    # Stop
    def test_cumulative1d_data_stop(self):
        list = [1, 4, 2]
        new_list = [1, 5, 7]
        cumulative_data = AverageList(list).cumulative_data_1d(True)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative1d_data_null_data_stop(self):
        list = [4, 0, 0]
        new_list = [4, 'null', 'null']
        cumulative_data = AverageList(list).cumulative_data_1d(True)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative1d_data_null_data_stop_1(self):
        list = [0, 4, 5, 0]
        new_list = [0, 4, 9, 'null']
        cumulative_data = AverageList(list).cumulative_data_1d(True)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative1d_data_null_data_stop_2(self):
        list = [0, 4, 5, 0, 2, 0]
        new_list = [0, 4, 9, 9, 11, 'null']
        cumulative_data = AverageList(list).cumulative_data_1d(True)
        self.assertEqual(cumulative_data, new_list)

    def test_cumulative1d_data_all_null_data_stop(self):
        list = [0, 0, 0]
        new_list = [0, 'null', 'null']
        cumulative_data = AverageList(list).cumulative_data_1d(True)
        self.assertEqual(cumulative_data, new_list)

    # =============  Compute Average  =============
    def test_compute_average_past_null(self):
        list = [0, 0, 0]
        second_list = [0, 0, 0]
        new_list = [[' 0.0 %', False], [' 0.0 %', False], [' 0.0 %', False]]

        compute_average = AverageList(list).compute_average(2018, second_list)
        self.assertEqual(compute_average, new_list)

    def test_compute_average_past_normal(self):
        list = [5, 2, 20]
        second_list = [10, 10, 10]
        new_list = [['50.0 %', False], ['20.0 %', False], ['200.0 %', True]]

        compute_average = AverageList(list).compute_average(2018, second_list)
        self.assertEqual(compute_average, new_list)

    def test_compute_average_past_null_2(self):
        list = [5, 'null', 'null']
        second_list = [10, 10, 10]
        new_list = [['50.0 %', False], [' 0.0 %', False], [' 0.0 %', False]]

        compute_average = AverageList(list).compute_average(2018, second_list)
        self.assertEqual(compute_average, new_list)

    def test_compute_average_past_null_3(self):
        list = [5, 'null', 'null']
        second_list = ['null', 'null', 10]
        new_list = [['100.0 %', True], [' 0.0 %', True], [' 0.0 %', False]]

        compute_average = AverageList(list).compute_average(2018, second_list)
        self.assertEqual(compute_average, new_list)

    def test_compute_average_futur_normal(self):
        list = [5, 2, 20]
        second_list = [10, 10, 10]
        new_list = [['50.0 %', True], ['20.0 %', True], ['200.0 %', True]]

        compute_average = AverageList(list).compute_average(2025, second_list)
        self.assertEqual(compute_average, new_list)

    def test_compute_average_futur_null(self):
        list = ['null', 'null', 20]
        second_list = [10, 'null', 'null']
        new_list = [[' 0.0 %', False], [' 0.0 %', True], ['100.0 %', True]]

        compute_average = AverageList(list).compute_average(2025, second_list)
        self.assertEqual(compute_average, new_list)


    def test_compute_average_futur_null_4(self):
        list = [5,5]
        second_list = [0,0]
        new_list = [['100.0 %', True],['100.0 %', True]]

        compute_average = AverageList(list).compute_average(2020, second_list)
        self.assertEqual(compute_average, new_list)

    def test_compute_average_present_normal(self):
        list = ['null', 'null', 20, 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null']
        second_list = ['null', 20, 'null', 50, 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null']
        new_list = [[' 0.0 %', True], [' 0.0 %', False], ['100.0 %', True], [' 0.0 %', False], [' 0.0 %', True],
                    [' 0.0 %', True], [' 0.0 %', True]
            , [' 0.0 %', True], [' 0.0 %', True], [' 0.0 %', True], [' 0.0 %', True], [' 0.0 %', True]]

        compute_average = AverageList(list).compute_average(2025, second_list)
        self.assertEqual(compute_average, new_list)

    # =============  Compute in time average  =============
    def test_compute_in_time_average_all_day_false(self):
        first = 2
        second = 10
        expected = False
        compute_in_time_average = Average(first, second).compute_in_time_average(30, 30)

        self.assertEqual(compute_in_time_average, expected)

    def test_compute_in_time_average_all_day_False_2(self):
        first = 9
        second = 10
        expected = False
        compute_in_time_average = Average(first, second).compute_in_time_average(30, 30)
        self.assertEqual(compute_in_time_average, expected)

    def test_compute_in_time_average_all_day_True(self):
        first = 10
        second = 10
        expected = True
        compute_in_time_average = Average(first, second).compute_in_time_average(30, 30)
        self.assertEqual(compute_in_time_average, expected)

    def test_compute_in_time_average_all_day_True_2(self):
        first = 12
        second = 10
        expected = True
        compute_in_time_average = Average(first, second).compute_in_time_average(30, 30)
        self.assertEqual(compute_in_time_average, expected)

    def test_compute_in_time_average_0day_1(self):
        first = 2
        second = 10
        expected = True
        compute_in_time_average = Average(first, second).compute_in_time_average(0, 30)
        self.assertEqual(compute_in_time_average, expected)

    def test_compute_in_time_average_0day_2(self):
        first = 0
        second = 10
        expected = True
        compute_in_time_average = Average(first, second).compute_in_time_average(0, 30)
        self.assertEqual(compute_in_time_average, expected)

    def test_compute_in_time_average_20days(self):
        first = 2
        second = 10
        expected = True
        compute_in_time_average = Average(first, second).compute_in_time_average(20, 100)
        self.assertEqual(compute_in_time_average, expected)

    def test_compute_in_time_average__20days_2(self):
        first = 1
        second = 10
        expected = False
        compute_in_time_average = Average(first, second).compute_in_time_average(20, 100)
        self.assertEqual(compute_in_time_average, expected)

    def test_compute_in_time_average__20days_3(self):
        first = 3
        second = 10
        expected = True
        compute_in_time_average = Average(first, second).compute_in_time_average(20, 100)
        self.assertEqual(compute_in_time_average, expected)

    # Extract First Value
    def test_extract_first_value_normal(self):
        list = [[], [(20,5,6)], [(6,5,6)]]
        new_list = [0, 20, 6]

        compute_average = AverageList(list).extract_first_value()
        self.assertEqual(compute_average, new_list)

if __name__ == '__main__':
    unittest.main()
