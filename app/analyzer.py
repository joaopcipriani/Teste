from minidump.minidumpfile import MinidumpFile

def analyze_dump(dmp_bytes):
    with open("temp.dmp", "wb") as f:
        f.write(dmp_bytes)
    dump = MinidumpFile.parse("temp.dmp")
    stacks = []
    for thread in dump.threads:
        stacks.append({
            "thread_id": thread.thread_id,
            "stack": [hex(frame.instruction) for frame in thread.stack]
        })
    return stacks
