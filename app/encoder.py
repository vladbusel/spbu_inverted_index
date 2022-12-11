import numpy as np

def unary(x):
    return b'0'*(len(x)-1)

def binary(x):
    return str.encode(f'{x:b}')

def elias_delta(x):
    a = binary(x+1)
    l = len(a)

    return elias_gamma(l-1) + a[1:]

def elias_gamma(x):
    a = x + 1
    a = binary(a)

    return unary(a) + a

def decoding_gamma_bytes(gamma_bytes):
    i = 0
    num_list = []
    while i < len(gamma_bytes):
      num_len = 1
      while gamma_bytes[i] != 49:
        i += 1
        num_len += 1
      num_list.append(int(gamma_bytes[i:i+num_len], 2) - 1)
      i += num_len
    for i in range(1, len(num_list)):
        num_list[i] += num_list[i-1]
    return num_list

def decoding_delta_bytes(delta_bytes):
    i = 0
    num_list = []
    while i < len(delta_bytes):
      zero_count = 0
      while delta_bytes[i] != 49:
        i += 1
        zero_count += 1
      l = int(delta_bytes[i:i+zero_count+1], 2)
      i += zero_count+1
      num_list.append(int(b'1'+delta_bytes[i:i+l-1], 2) - 1)
      i += l-1
    for i in range(1, len(num_list)):
        num_list[i] += num_list[i-1]
    return num_list

def list_compression(ids, compression_alg_method):
    copy = ids
    copy.sort()
    res = np.array(copy) - np.array([0] + copy[0:-1])
    res = b''.join(list(map(compression_alg_method, res)))
    return res
