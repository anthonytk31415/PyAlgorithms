from collections import Counter 



a = "anthony"
b = "janice"

counterA, counterB = Counter(a), Counter(b)

print(counterA, counterB)

counterC = counterA & counterB
print(counterC)





class Logger():
    count = 0

    def __init__(cls):
        cls.count += 1
        print(cls.count)

    


a = Logger()
b = Logger()
c = Logger()