class ManagementList:
    def __init__(self,list):
        self._list = list

    def sum_data(self):
        sum_data = 0
        for r in self._list:
            if r != 'null':
                sum_data += r
        return sum_data

    def compute_difference(self, list_real):
        new_list = []
        i = 0
        while i < len(self._list):
            new_list.append(self._list[i]-list_real[i])
            i += 1
        return new_list
