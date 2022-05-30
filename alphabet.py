LENGTH = 33
ZERO = 1071

def get_char(i):
    if i < 7:
        return chr(ZERO + i)
    elif i == 7:
        return chr(1105)
    else:
        if ZERO + i - 1 >= 1105:
            return chr(ZERO + i)
        else:
            return chr(ZERO + i - 1)

def get_num(char):
    sym_num = ord(char)
    if sym_num < ZERO + 7:
        return sym_num - ZERO
    elif sym_num == 1105:
        return 7
    else:
        if sym_num < 1105:
            return sym_num - ZERO + 1
        else:
            return sym_num - ZERO

# if __name__ == '__main__':
#     print(chr(1106))
#     for i in range(100):
#         print('unicode',ZERO + i)
#         c = get_char(i)
#         print('char',c)
#         print('ord',get_num(c))
