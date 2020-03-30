class ColorPicker:
    COLORS = ["#4287f5","#04b30f","#ff8717","#b13de3","#f0438e"]
    DARKCOLORS = ["#3164b5","#03820b","#c76912","#8d31b5","#b5316a"]

    def colors(self, number):
        if number >= len(self.COLORS):
            return None
        else:
            return self.COLORS[number]

    def colors_dark(self, number):
        if number >= len(self.DARKCOLORS):
            return None
        else:
            return self.DARKCOLORS[number]
