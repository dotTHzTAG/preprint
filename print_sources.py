import re
import base64
import zlib
import pickle

with open('runtests.py', 'r') as f:
    content = f.read()

match = re.search(r"sources = b'(.+)'", content, re.DOTALL)
if match:
    sources_b64 = match.group(1).replace('\\n', '')
    
    # Add padding if necessary
    padding = '=' * (4 - (len(sources_b64) % 4))
    sources_b64 += padding
    
    try:
        decoded_sources = base64.b64decode(sources_b64)
        decompressed_sources = zlib.decompress(decoded_sources)
        modules = pickle.loads(decompressed_sources, encoding='latin1')
        print(modules.keys())
    except Exception as e:
        print(e)