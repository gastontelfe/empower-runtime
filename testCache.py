from sets import Set

class LVAPCache(object):
    def __init__(self, lvap_bssid_addr, label):
        self.lvap_bssid = lvap_bssid_addr
        self.label = label
        r = 0
        for c in self.lvap_bssid:
            r += ord(c)

        for c in self.label:
            r += ord(c)

        self._hash = r

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


a = LVAPCache('123', 'label1')
b = LVAPCache('1233', 'label1')
c =  LVAPCache('123', 'label1')

s = Set([a, b, c])
print(s)
