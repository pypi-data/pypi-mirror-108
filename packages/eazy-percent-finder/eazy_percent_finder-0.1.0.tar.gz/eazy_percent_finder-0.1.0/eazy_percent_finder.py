class Percent():

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.one_percent = self.a/100
        percent = self.one_percent*self.b
        self.percent = percent
    
    def print_result(self):
        print(self.percent)
    
    def print(self):
        print(self.percent)
    
    def print_formula(self):
        print(f"{self.a}/100*{self.b} = {self.percent}")