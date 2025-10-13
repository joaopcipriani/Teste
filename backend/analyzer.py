from minidump.minidumpfile import MinidumpFile
import os

def analyze_dump(dmp_bytes):
    os.makedirs("uploads", exist_ok=True)
    dump_path = "uploads/temp.dmp"

    with open(dump_path, "wb") as f:
        f.write(dmp_bytes)

    dump = MinidumpFile.parse(dump_path)
    results = []
    for thread in dump.threads:
        stack = [hex(frame.instruction) for frame in thread.stack]
        results.append({
            "thread_id": thread.thread_id,
            "stack": stack
        })
    return results
