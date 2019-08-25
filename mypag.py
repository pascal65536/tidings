import math

class Mypag(object):

    def __init__(self, page, num, btn, tail=False):
        self.tail = tail
        self.btn = btn
        self.num = num
        self.page = page


    def listpage(self, page, num, btn, tail):

        if tail == True:
            c = math.ceil(len(self) / num)
            v = len(self) % num
        else:
            c = len(self) // num
            v = num + (len(self) % num)

        b = num * (page - 1)
        if v == 0 or page != c:
            e = num * page
        else:
            e = num * (page - 1) + v

        return self[b:e]


    def strpage(self, page, num, btn, tail):

        if tail == True:
            c = math.ceil(len(self)/num)
        else:
            c = len(self)//num

        l1 = []
        l2 = []
        for i in list(range(-btn+page, 1+btn+page)):
            if 1<=i and i<=c:
                l1.append(str(i))
                l2.append(i)

        p = dict(zip(l2, l1))
        p.update({1: 'First page', c: 'Last page', page: 'Selected page'})

        return p

    l = []
    for k in range(200):
        l.append(k+1)

    for k in sorted(strpage(l, 11, 5, 3, False)):
        print('p'+str(k), strpage(l, 11, 5, 3, False)[k])

    print(sorted(strpage(l, 11, 5, 3, False)))


    print(listpage(l, 11, 5, 3, False))