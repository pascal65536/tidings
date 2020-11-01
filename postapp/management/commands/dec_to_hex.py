from django.core.management import BaseCommand

# CHARSET_LST = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
CHARSET_LST = '_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-'
SALT = 65536


def get_short(idx):
    res_lst = list()
    n = idx * SALT
    m = len(CHARSET_LST)
    while n > 0:
        res_lst.append(CHARSET_LST[n % m])
        n = n // m
    return "".join(res_lst)


def get_num(short):
    summa = 0
    m = len(CHARSET_LST)
    for si, nn in enumerate(short):
        summa += CHARSET_LST.rfind(nn) * (m ** si)
    return int(summa / SALT)


class Command(BaseCommand):
    def handle(self, *args, **options):

        idx = 89138322788
        short = get_short(idx)
        short = 'QC9L2FebsYA'
        ret = get_num(short)
        m = len(CHARSET_LST)

        print(f'{idx} = {short}({m}) = {ret}(10)')
        print('*' * 80)
