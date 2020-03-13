from .management_list import ManagementList

class Classic:

    def treatment(self, list, typelist):
        return list

    def sum(self,list):
        return ManagementList(list).sum_data()

class Cumulative:

    def treatment(self, list, typelist):
        if typelist == "goal":
            return self.cumulative_data(list, False)
        else:
            return self.cumulative_data(list, True)

    def cumulative_data(self, list, stop):
        new_list = []
        cumulative_data = 0
        for r in list:
            if r != 0:
                cumulative_data += r
                new_list.append(cumulative_data)
            else:
                if stop:
                    if self.data_continue(list, len(new_list)):
                        new_list.append(cumulative_data)
                    else:
                        if len(new_list) == 0:
                            new_list.append(0)
                        else:
                            new_list.append('null')
                else:
                    new_list.append(cumulative_data)
        return new_list

    def data_continue(self, list, i):
        index_null = 0
        index = i
        while i < len(list):
            if list[i] == 0:
                index_null += 1
            i += 1
        return not (index_null + index == len(list))

    def sum(self,list):
        return ManagementList(list).sum_data()
