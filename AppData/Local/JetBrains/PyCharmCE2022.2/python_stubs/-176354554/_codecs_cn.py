# encoding: utf-8
# module _codecs_cn
# from (built-in)
# by generator 1.147
# no doc
# no imports

# functions

def getcodec(*args, **kwargs): # real signature unknown
    pass

# classes

class __loader__(object):
    """
    Meta path import for built-in modules.
    
        All methods are either class or static methods to avoid the need to
        instantiate the class.
    """
    def create_module(spec): # reliably restored by inspect
        """ Create a built-in module """
        pass

    def exec_module(module): # reliably restored by inspect
        """ Exec a built-in module """
        pass

    @classmethod
    def find_module(cls, *args, **kwargs): # real signature unknown
        """
        Find the built-in module.
        
                If 'path' is ever specified then the search is considered a failure.
        
                This method is deprecated.  Use find_spec() instead.
        """
        pass

    @classmethod
    def find_spec(cls, *args, **kwargs): # real signature unknown
        pass

    @classmethod
    def get_code(cls, *args, **kwargs): # real signature unknown
        """ Return None as built-in modules do not have code objects. """
        pass

    @classmethod
    def get_source(cls, *args, **kwargs): # real signature unknown
        """ Return None as built-in modules do not have source code. """
        pass

    @classmethod
    def is_package(cls, *args, **kwargs): # real signature unknown
        """ Return False as built-in modules are never packages. """
        pass

    @classmethod
    def load_module(cls, *args, **kwargs): # real signature unknown
        """
        Load the specified module into sys.modules and return it.
        
            This method is deprecated.  Use loader.exec_module() instead.
        """
        pass

    def module_repr(module): # reliably restored by inspect
        """
        Return repr for the module.
        
                The method is deprecated.  The import machinery does the job itself.
        """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    __weakref__ = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """list of weak references to the object (if defined)"""


    _ORIGIN = 'built-in'
    __dict__ = None # (!) real value is "mappingproxy({'__module__': '_frozen_importlib', '__doc__': 'Meta path import for built-in modules.\\n\\n    All methods are either class or static methods to avoid the need to\\n    instantiate the class.\\n\\n    ', '_ORIGIN': 'built-in', 'module_repr': <staticmethod(<function BuiltinImporter.module_repr at 0x00000223428F2320>)>, 'find_spec': <classmethod(<function BuiltinImporter.find_spec at 0x00000223428F23B0>)>, 'find_module': <classmethod(<function BuiltinImporter.find_module at 0x00000223428F2440>)>, 'create_module': <staticmethod(<function BuiltinImporter.create_module at 0x00000223428F24D0>)>, 'exec_module': <staticmethod(<function BuiltinImporter.exec_module at 0x00000223428F2560>)>, 'get_code': <classmethod(<function BuiltinImporter.get_code at 0x00000223428F2680>)>, 'get_source': <classmethod(<function BuiltinImporter.get_source at 0x00000223428F27A0>)>, 'is_package': <classmethod(<function BuiltinImporter.is_package at 0x00000223428F28C0>)>, 'load_module': <classmethod(<function _load_module_shim at 0x00000223428F17E0>)>, '__dict__': <attribute '__dict__' of 'BuiltinImporter' objects>, '__weakref__': <attribute '__weakref__' of 'BuiltinImporter' objects>})"


# variables with complex values

__map_gb18030ext = None # (!) real value is '<capsule object "multibytecodec.__map_*" at 0x0000022343296790>'

__map_gb2312 = None # (!) real value is '<capsule object "multibytecodec.__map_*" at 0x0000022343296910>'

__map_gbcommon = None # (!) real value is '<capsule object "multibytecodec.__map_*" at 0x00000223432967C0>'

__map_gbkext = None # (!) real value is '<capsule object "multibytecodec.__map_*" at 0x00000223432968E0>'

__spec__ = None # (!) real value is "ModuleSpec(name='_codecs_cn', loader=<class '_frozen_importlib.BuiltinImporter'>, origin='built-in')"

