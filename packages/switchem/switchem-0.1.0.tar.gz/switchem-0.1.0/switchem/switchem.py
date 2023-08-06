import onetrick

@onetrick
class switch:
    __value:object
    __fall = False

    def __init__(self, value:object):
        self.__value = value

    def __iter__(self):
        yield self

    def __call__(self, value, *values) -> bool:
        if self.__fall:
            return True
        
        if (self.__value == value) or (self.__value in values):
            self.__fall = True
            return True
        
        return False

if __name__ == "__main__":
    MONKEY = 1
    ELEPHANT = 2
    GIRAFFE = 3
    HORSE = 4
    SQUIRREL = 5

    for case in switch(4):
        if case(MONKEY):
            print("It is a monkey")
            break
        
        if case(ELEPHANT, GIRAFFE, HORSE):
            print("It is not a monkey or a squirrel")
        
        if case(SQUIRREL):
            print("It is not a monkey for sure")

        