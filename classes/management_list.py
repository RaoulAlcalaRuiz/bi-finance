class ManagementList:
    def __init__(self,list):
        self._list = list

    def sum_data(self):
        sum_data = 0
        for r in self._list:
            if r != 'null':
                sum_data += r
        return sum_data