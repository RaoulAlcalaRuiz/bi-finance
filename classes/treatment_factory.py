from .treatment import Classic, Cumulative


class TreatmentFactory:
    def __init__(self,type):
        self._type = type

    def get_treatment(self):
        if self._type == "normal":
            return Classic()
        elif self._type == "cumulative":
            return Cumulative()
        else:
            return Classic()
