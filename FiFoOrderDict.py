#coding: utf-8
from collections import OrderedDict


class FIFOOrderdDict(OrderedDict):
    """FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key"""

    def __init__(self, capacity):
        super(FIFOOrderdDict, self).__init__()
        self._capacity = capacity


    def __setitem__(self, key, value):
        contains_key = 1 if key in self else 0
        if len(self) - contains_key >= self._capacity:
            last = self.popitem(last=False)
            #last = self.popitem()
            print 'remove:', last
        if contains_key:
            del self[key]
            print 'set:', (key, value)
        else:
            print 'add:', (key, value)
        OrderedDict.__setitem__(self, key, value)


def main():
    TestInts = FIFOOrderdDict(3)
    TestInts.__setitem__('z', 90)
    TestInts.__setitem__('x', 80)
    TestInts.__setitem__('y', 70)
    TestInts.__setitem__('a', 60)
    TestInts.__setitem__('z', 60)

if __name__ == '__main__':
    main()    
