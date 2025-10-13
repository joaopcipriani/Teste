from minidump.minidumpfile import MinidumpFile
import os

def analyze_dump(dmp_bytes):
    os.makedirs("uploads", exist_ok=True)
    path = "uploads/temp.dmp"

    with open(path, "wb") as f:
        f.write(dmp_bytes)

    dump = MinidumpFile.parse(path)
    stacks = []

    # Corrigido: dump.threads é um objeto, precisamos usar .threads
    for thread in dump.threads.threads:
        thread_info = {
            "thread_id": thread.thread_id,
            "stack_start": hex(thread.stack.start_virtual_address) if thread.stack else None,
            "stack_end": hex(thread.stack.end_virtual_address) if thread.stack else None,
            "stack_memory_size": len(thread.stack.memory) if thread.stack and thread.stack.memory else 0
        }
        stacks.append(thread_info)

    return {
        "thread_count": len(dump.threads.threads),
        "threads": stacks
    }
