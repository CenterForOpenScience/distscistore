#!/usr/bin/env python
import sys
import hashlib
import time
import base64
import os.path

from bencode import bencode

# FIXME rewrite below

def printv(*args,**kwargs): pass

def sha1_20(data):
    """Return the first 20 bytes of the given data's SHA-1 hash."""
    m = hashlib.sha1()
    m.update(data)
    return m.digest()[:20]

def create_single_file_info(file, piece_length, include_md5=True):
    """
    Return dictionary with the following keys:
      - pieces: concatenated 20-byte-sha1-hashes
      - name:   basename of the file
      - length: size of the file in bytes
      - md5sum: md5sum of the file (unless disabled via include_md5)

    @see:   BitTorrent Metainfo Specification.
    @note:  md5 hashes in torrents are actually optional
    """
    assert os.path.isfile(file), "not a file"

    # Total byte count.
    length = 0

    # Concatenated 20byte sha1-hashes of all the file's pieces.
    pieces = bytearray()

    md5 = hashlib.md5() if include_md5 else None

    printv("Hashing file... ", end="")

    with open(file, "rb") as fh:
        while True:
            piece_data = fh.read(piece_length)

            _len = len(piece_data)
            if _len == 0:
                break

            if include_md5:
                md5.update(piece_data)

            length += _len

            pieces += sha1_20(piece_data)

    printv("done")

    assert length > 0, "empty file"

    info =  {
            'pieces': pieces,
            'name':   os.path.basename(file),
            'length': length,
            
            }

    if include_md5:
        info['md5sum'] = md5.hexdigest()

    return info

def make_torrent(piece_length, announce, f):
    d = {}
    d["announce"] = announce
    d["created by"] = "DistSciStore"
    d["creation date"] = int(time.time())
    d["encoding"] = 'UTF-8'
    internal_info = create_single_file_info(f, piece_length)
    hash_hasher = hashlib.sha1()
    hash_hasher.update(internal_info["pieces"])
    info = {}
    d["info"] = info
    info["piece length"] = piece_length
    info["length"] = internal_info["length"]
    info["name"] = base64.b16encode(hash_hasher.digest())
    info["pieces"] = str(internal_info["pieces"])
    return bencode(d)

if __name__ == '__main__':
    piece_length = 256 * 1024
    announce = sys.argv[1]
    f = sys.argv[2]
    sys.stdout.write(make_torrent(piece_length, announce, f))
