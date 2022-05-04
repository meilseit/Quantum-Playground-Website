

class Pot():
    def __init__(self, intervals):
        self.intervals = intervals #is list of pot_int that are parsed to return the appropriate value
    
    def parse(self,x):
        potential = 0
        for V in self.intervals: #iterate through the collection of objects 
            if V.left * 1e-10 < x and V.right * 1e-10 >= x:    
                potential = V.value
                
            else:
                continue  #skip to next object if the x is not in the interval 
        return potential

    def get_extrema(self):
        minimum = 0
        maximum = 0
        for V in self.intervals:
            if(V.value < minimum):
                minimum = V.value
            if(V.value > maximum):
                maximum = V.value
        return minimum, maximum