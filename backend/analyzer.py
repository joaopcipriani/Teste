from minidump.minidumpfile import MinidumpFile
import pefile

def analyze_dump(dmp_bytes):
    path = "uploads/temp.dmp"
    with open(path, "wb") as f:
        f.write(dmp_bytes)

    dump = MinidumpFile.parse(path)
    stacks = []

    for thread in dump.threads:
        stack_info = {
            "thread_id": thread.thread_id,
            "stack": [hex(frame.instruction) for frame in thread.stack or []]
        }
        stacks.append(stack_info)

    return stacks
