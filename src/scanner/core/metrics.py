"""Pico de memoria del proceso; interpretación depende del sistema operativo."""

from __future__ import annotations

import os
import sys


def pico_memoria_bytes() -> int:
    if os.name == "nt":
        import ctypes

        class MemoryCounters(ctypes.Structure):
            _fields_ = [
                ("cb", ctypes.c_ulong),
                ("PageFaultCount", ctypes.c_ulong),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]

        counters = MemoryCounters()
        counters.cb = ctypes.sizeof(counters)
        get_process = ctypes.windll.kernel32.GetCurrentProcess
        get_process.restype = ctypes.c_void_p
        get_memory = ctypes.windll.psapi.GetProcessMemoryInfo
        get_memory.argtypes = [ctypes.c_void_p, ctypes.POINTER(MemoryCounters), ctypes.c_ulong]
        get_memory.restype = ctypes.c_int
        process = get_process()
        success = get_memory(process, ctypes.byref(counters), counters.cb)
        if not success:
            raise OSError("No se pudo medir el pico de memoria del proceso")
        return int(counters.PeakWorkingSetSize)

    import resource

    max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(max_rss * (1 if sys.platform == "darwin" else 1024))
