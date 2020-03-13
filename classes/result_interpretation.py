#renvois zero quand il n'y a pas de valeur
class ResultInterpretationZero:

    def interpretation(self,value):
        if len(value) != 0:
            return value[0][0]
        else:
            return 0
