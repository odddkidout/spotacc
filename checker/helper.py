import binascii
import hashlib
# test_str = "9a8d2f0ce77a4e248bb71fefcb557637"
# print(ascii(test_str))
# res = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in test_str)
#
# # printing result
# print("The unicode converted String : " + str(res))


# import unicodedata
#
# uni_str = gf
#
# normal_str = unicodedata.normalize('NFKD', uni_str).encode('utf-16', 'ignore')
# print(normal_str)
import traceback


def log(n,text):
    with open('log.txt', 'a') as f:
        f.write(str(n)+": "+text+"\n")


def get_traceback(e):
    lines = traceback.format_exception(type(e), e, e.__traceback__)
    return ''.join(lines)


import struct


def sha1(string):
    return hashlib.sha1(string).hexdigest()


def substr(string, start, length=None):
    if len(string) >= start:
        if start > 0:
            return False
        else:
            return string[start:]
    if not length:
        return string[start:]
    elif length > 0:
        return string[start:start + length]
    else:
        return string[start:length]


def unpack(format_codes, data):
    try:
        return struct.unpack(format_codes, data)
    except Exception as e:
        print(get_traceback(e))
        raise


def array_splice(array, offset, length, replacement=None):
    if replacement is None:
        del array[offset: offset + length]
    else:
        array[offset: offset + length] = replacement
    return array


def array_merge(array1, array2):
    if isinstance(array1, list) and isinstance(array2, list):
        return array1 + array2
    elif isinstance(array1, dict) and isinstance(array2, dict):
        return dict(list(array1.items()) + list(array2.items()))
    elif isinstance(array1, set) and isinstance(array2, set):
        return array1.union(array2)
    return False


def array_map(callback, array):
    return map(callback, array)


def join(glue='', pieces=[]):
    return glue.join(pieces)


def hex2ByteArray(string):
    sstr = binascii.unhexlify(string)
    # unpacked = unpack('C*', sstr)
    unpacked = sstr[1:]
    # array = array_splice(unpacked, 0, len(unpacked))
    data = list(unpacked)
    return data


# def hex2ByteArray2(hexString):
#     byteArray = bytearray.fromhex(hexString)
#     unpacked = byteArray[1:]
#     return list(unpacked)


def byteArray2Hex(string):
    # chrr = map(chr, string)

    # string = ''.join([b for b in chrr])
    string = ''.join([chr(b) for b in string])
    # print(binascii.hexlify(string.encode()))
    return binascii.hexlify(string.encode())


def byteArray2Hex2(byteArray):
    hexString = ''
    for b in byteArray:
        hexByte = hex(b)[2:]  # Strip the leading '0x'
        if len(hexByte) < 2:
            hexByte = '0' + hexByte
        hexString += hexByte
    return hexString.encode()
    return binascii.hexlify(hexString.encode())


def incrementCtr(arrr, intt):
    arrr[intt] += 1
    if arrr[intt] > 0xFF and intt != 0:
        arrr[intt] = 0
        arrr = incrementCtr(arrr, intt - 1)
    return arrr


def checkTenTrailingBits(dd32):
    if dd32[len(dd32) - 1] != 0:
        return False

    return countTrailingZero(dd32[len(dd32) - 2]) >= 2


def countTrailingZero(dd32):
    if dd32 == 0:
        return 32
    count = 0
    while (dd32 & 1) == 0:
        dd32 = dd32 >> 1
        count += 1

    return count


def solver(df, pre):
    contex = sha1(df)
    seed = substr(contex, -18)
    arr = hex2ByteArray(seed)
    suffix = array_merge(arr, [0, 0, 0, 0, 0, 0, 0, 0])
    countmax = 0
    while True:
        sec = byteArray2Hex2(suffix)
        inp = (binascii.hexlify(pre) + sec)
        # print(inp)
        digest = sha1(binascii.unhexlify(inp))
        dd3 = hex2ByteArray(digest)
        if not checkTenTrailingBits(dd3):
            suffix = incrementCtr(suffix, len(suffix) - 1)
            suffix = incrementCtr(suffix, 7)
            countmax += 1
            if countmax > 5000:
                break
            continue
        tr = byteArray2Hex2(suffix)
        suff = binascii.unhexlify(tr)
        return suff, countmax

    return False, False



# import base64
# hash = "7qMyvOJAkbUzfr/QKLo/+g=="
# hash = base64.b64decode(hash)
# loginc = "AwD7NHHOABQedYaBGfKQnvnxIgMtT3KxTyav8yLQJFFji31XZYSxpORTxOBra8EaMtoLblLxDlLYUP0y/cFVC3GTgdBrlzUzkE2/FlHJ/cvI+7h4Gg87M2Y8Ogo6sF1zJhEkj5rL2N1I+FaIPCBIDQF8yfcKxjXWLE1cXIqj/PCM/59jxCo64wTHQv5kw8Ty2aJPqdlr/Xzcegol2KX/bpX6tCRDMIIJuZJ7czrKf5Aeop0pFSAKOvDiIZ6UulaNQsGX0aZqxMdLwcioptwUpfmKOPmCfztNrmMZyOWiA57zxsmsW00="
# loginc = base64.b64decode(loginc)
# solver(loginc, hash)
# print(base64.b64decode('9f5syTQwzogAAAAAAAABMw=='))
# solver(dfo, preo)
# byteArray2Hex2([100, 158, 162, 200, 233, 38, 243, 223, 0, 0, 0, 0, 0, 6, 223])
