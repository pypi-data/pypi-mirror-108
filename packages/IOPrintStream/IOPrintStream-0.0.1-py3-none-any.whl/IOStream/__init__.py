from typing import Optional

class PrintModule:
    @staticmethod
    def Print(*values: object, pos: Optional[int] = 0):
        try:
            print(values[pos])
        except TypeError:
            print("Error Variable pos Type Is Int Type Not This Type")
        except IndexError:
            print(" ")
    @staticmethod
    def PrintLine(*values: object, pos: Optional[int] = 0):
        try:
            print(f'{values[pos]} \n')
        except TypeError:
            print("Error Variable pos Type Is Int Type Not This Type")
        except IndexError:
            print(" ")

class InputModule:
    @staticmethod
    def Scanner(values):
        return input(values)
        
