
import os
import pickle
import zlib
import base64

modules = {}
file_paths = [
    'preprint/pack.py',
    'preprint/config.py',
    'preprint/__init__.py',
    'preprint/init.py',
    'preprint/latexdiff.py',
    'preprint/main.py',
    'preprint/make.py',
    'preprint/vc.py',
    'preprint/watch.py',
]

for file_path in file_paths:
    module_name = file_path.replace('/', '.').replace('.py', '')
    with open(file_path, 'r') as f:
        content = f.read()
    
    modules[module_name] = {
        'source': content,
        'path': os.path.abspath(file_path),
        'is_package': module_name.endswith('__init__')
    }

# Recreate the sources data structure
source_bytes = pickle.dumps(modules)
compressed_bytes = zlib.compress(source_bytes)
encoded_bytes = base64.b64encode(compressed_bytes)

# The sources string is too long to be included directly in the script.
# I will write it to a file and read it in the new runtests.py
with open('sources.dat', 'wb') as f:
    f.write(encoded_bytes)

runtests_content = """
import sys
import os
import zlib
import base64
import pickle
import importlib.abc
import importlib.machinery

with open('sources.dat', 'rb') as f:
    sources = f.read()

class DictImporter(importlib.abc.MetaPathFinder):
    def __init__(self, sources):
        self._sources = sources

    def find_spec(self, fullname, path, target=None):
        if fullname in self._sources:
            return importlib.machinery.ModuleSpec(
                fullname,
                DictLoader(self._sources),
                is_package=self._sources[fullname].get('is_package', False)
            )
        return None

class DictLoader(importlib.abc.Loader):
    def __init__(self, sources):
        self._sources = sources

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        fullname = module.__name__
        if fullname in self._sources:
            code = self._sources[fullname]['source']
            module.__file__ = self._sources[fullname]['path']
            exec(code, module.__dict__)
        else:
            raise ImportError(f"Could not find module {fullname}")

if __name__ == '__main__':
    source_bytes = zlib.decompress(base64.b64decode(sources))
    modules = pickle.loads(source_bytes, encoding='latin1')
    
    importer = DictImporter(modules)
    sys.meta_path.insert(0, importer)
    
    _old_os_path_isfile = os.path.isfile
    def _isfile(path):
        for module in modules.values():
            if module['path'] == path:
                return True
        return _old_os_path_isfile(path)
    os.path.isfile = _isfile
    
    import pytest
    sys.exit(pytest.main())
"""

with open('runtests_new.py', 'w') as f:
    f.write(runtests_content)
