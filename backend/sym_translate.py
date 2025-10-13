import ctypes
from ctypes import wintypes

# DbgHelp functions
dbghelp = ctypes.windll.dbghelp

class SYMBOL_INFO(ctypes.Structure):
    _fields_ = [
        ("SizeOfStruct", wintypes.ULONG),
        ("TypeIndex", wintypes.ULONG),
        ("Reserved", wintypes.ULONG * 2),
        ("Index", wintypes.ULONG),
        ("Size", wintypes.ULONG),
        ("ModBase", wintypes.ULONG64),
        ("Flags", wintypes.ULONG),
        ("Value", wintypes.ULONG64),
        ("Address", wintypes.ULONG64),
        ("Register", wintypes.ULONG),
        ("Scope", wintypes.ULONG),
        ("Tag", wintypes.ULONG),
        ("NameLen", wintypes.ULONG),
        ("MaxNameLen", wintypes.ULONG),
        ("Name", ctypes.c_char * 256)
    ]

def translate_address(pid, address):
    process = ctypes.windll.kernel32.OpenProcess(0x001F0FFF, False, pid)
    if not dbghelp.SymInitialize(process, None, True):
        return f"Failed to initialize symbols"
    info = SYMBOL_INFO()
    info.SizeOfStruct = ctypes.sizeof(SYMBOL_INFO)
    info.MaxNameLen = 255
    addr = wintypes.ULONG64(int(address, 16))
    if dbghelp.SymFromAddr(process, addr, None, ctypes.byref(info)):
        name = info.Name.decode()
        return f"{name} + 0x{addr.value - info.Address:x}"
    return f"Symbol not found"
