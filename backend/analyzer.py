from minidump.minidumpfile import MinidumpFile
import os
from pdbparse.pe import PE
from pdbparse import pdb
import glob

SYMBOLS_PATH = "symbols"

def load_symbols():
    symbols = {}
    for pdb_file in glob.glob(os.path.join(SYMBOLS_PATH, "*.pdb")):
        try:
            pdb_data = pdb.PDB(open(pdb_file, "rb"))
            symbols[pdb_file] = pdb_data
        except Exception:
            pass
    return symbols

def analyze_dump(dmp_bytes):
    os.makedirs("uploads", exist_ok=True)
    with open("uploads/temp.dmp", "wb") as f:
        f.write(dmp_bytes)

    dump = MinidumpFile.parse("uploads/temp.dmp")
    results = []
    for thread in dump.threads:
        stack = [hex(frame.instruction) for frame in thread.stack]
        results.append({
            "thread_id": thread.thread_id,
            "stack": stack
        })
    return results
