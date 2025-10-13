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
        "thread_id": thread.ThreadId,  # <--- propriedade correta
        "stack_start": hex(thread.Stack.StartOfMemoryRange) if thread.Stack else None,
        "stack_end": hex(thread.Stack.StartOfMemoryRange + thread.Stack.Memory.DataSize) if thread.Stack else None,
        "stack_memory_size": thread.Stack.Memory.DataSize if thread.Stack and thread.Stack.Memory else 0
    }
    stacks.append(thread_info)
    return {
        "thread_count": len(dump.threads.threads),
        "threads": stacks
    }
