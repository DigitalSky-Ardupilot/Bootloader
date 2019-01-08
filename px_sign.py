#!/usr/local/bin/python3
import zlib
import sys
import base64
import json
import ecdsa
import hashlib

compressed = open(sys.argv[1], 'r')
expanded = open(sys.argv[3], 'w')
desc = json.load(compressed)
compressed.close()
data = zlib.decompress(base64.b64decode(desc['image']))
key = open(sys.argv[2], "r")
sk = ecdsa.SigningKey.from_pem(key.read())
key.close()
data = bytearray(data)
while len(data) % 4 != 0:
    data.append(0)
digest = hashlib.sha256(data).digest()
sign = bytearray(sk.sign_digest(digest))
outRaw = data + sign
outCompressed = zlib.compress(outRaw)
outBase64 = base64.b64encode(outCompressed).decode("utf-8") 
desc['image'] = outBase64
desc['image_size'] = len(outRaw)
json.dump(desc, expanded)
expanded.close()
