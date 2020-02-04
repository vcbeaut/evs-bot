import ctypes
from ctypes import *

dllObj = None
functype = None
dllcallback = None

def set_c_callback(dll,function):
    global dllObj,functype,dllcallback
    dllObj = ctypes.cdll.LoadLibrary(dll)
    functype = ctypes.CFUNCTYPE(None,ctypes.c_char_p,ctypes.c_char_p)
    dllcallback = functype(function)
    dllObj.set_call(dllcallback)