
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
