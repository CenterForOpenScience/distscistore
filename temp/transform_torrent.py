#!/usr/bin/env python
import bencode
import sys

if len(sys.argv) < 2 or len(sys.argv) % 2 == 1:
    print >>sys.stderr, "Usage:"
    print >>sys.stderr, "%s torrent new_key_1 new_value_1 new_key_2 new_value_2 ..." % sys.argv[0]
    print >>sys.stderr, "Separate hierarchical names with / (example: info/length)\n"
    print >>sys.stderr, "Example: ./transform_torrent.py some.torrent info/name new_name"
    exit(1)

d = bencode.bdecode(file(sys.argv[1]).read())
def set((d, k), v):
    d[k] = v
def locate(d, k):
    keys = k.split('/')
    for i in xrange(len(keys)-1):
        d = d[keys[i]]
    return (d, keys[-1])
for i in xrange(2, len(sys.argv), 2):
    k = sys.argv[i]
    v = sys.argv[i+1]
    set(locate(d, k), v)
    d[k] = v
sys.stdout.write(bencode.bencode(d))
