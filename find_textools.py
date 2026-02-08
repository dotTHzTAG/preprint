import base64
import zlib
import re

with open('runtests.py', 'r') as f:
    content = f.read()

match = re.search(r"sources = b'(.+)'", content, re.DOTALL)
if match:
    sources_b64 = match.group(1).replace('\\n', '')
    decoded_sources = base64.b64decode(sources_b64)
    decompressed_sources = zlib.decompress(decoded_sources)
    print(decompressed_sources.decode('latin1'))