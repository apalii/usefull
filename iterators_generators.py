#iterator

iterator.__iter__()   |   iter(iterator)
iterator.__next__()   |   next(iterator)


class Range(object):
    def __init__(self, start, stop):
        self._current = start
        self._stop = stop
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if self._current < self._stop:
            result = self._current
            self._current += 1
            return result
        else: 
            raise StopIteration
r = Range(1,4)

for i in r:
    print(i)
# OR
i = iter([1,2,3])    
while True:
    try:
        print(next(i))
    except StopIteration:
        break             

# Generators

generator.__iter__()
generator.__next__()
generator.send(arg)
generator.throw(typ, [val, [tb,]])
generator.close()

def range(start, stop):
    current = start
    while  current < stop:
        yield current
        current += 1

g = range(0,3)
