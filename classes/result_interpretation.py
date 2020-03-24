#renvois zero quand il n'y a pas de valeur
class ResultInterpretationZero:

    def interpretation(self,value):
        if len(value) != 0:
            value = value[0][0]
            if value:
                return value
            else:
                return 0
        else:
            return 0
