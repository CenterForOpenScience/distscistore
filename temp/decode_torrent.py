#!/usr/bin/env python
import bencode
import sys
try:
    f = file(sys.argv[1])
except:
    f = sys.stdin
print bencode.bdecode(f.read())
