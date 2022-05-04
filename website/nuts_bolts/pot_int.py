
class Potint():
    def __init__(self, left, right, value):
        self.left = left #the right bound of the potential 
        self.right = right #the left bound of the potential
        self.value = value  # the magnitude of the potenial in that interval type int
    def __repr__(self):
        return str(self.left) +" " + str(self.right) + " " + str(self.value)
        