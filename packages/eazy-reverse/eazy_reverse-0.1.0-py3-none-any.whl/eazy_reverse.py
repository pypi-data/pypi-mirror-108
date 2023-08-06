class Reverse():
    def __init__(self, number : float):
        self.original_number = number
        if number != 0:
            self.reverse_number = 0 - self.original_number
        if number == 0:
            self.reverse_number = 0
            print("ReverseNumber: Error in function Reverse\nError: Number = 0\n")
        global reverse_number
        reverse_number = self.reverse_number
        
    def print(self):
        print(self.reverse_number)