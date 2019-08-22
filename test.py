# -*- coding: utf-8 -*-
import sys

a = b'\x02\x00\x18\x00\x00\x00\x00\x00\xb6\xbf\x00\x06\x20\xc88982\x00\x00\x00\x00\x00\x00\x03\x00\x00'

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

chars = list(a)
print(chars)

for char in chars:
    print(char)
