import pefile

def translate_address_dummy(stack_lines):
    """
    Tradução de símbolos simulada para Linux.
    Como não podemos usar DbgHelp, vamos gerar algo legível.
    """
    result = []
    for line in stack_lines:
        addr = line.strip()
        if addr.startswith("0x"):
            # Simula a função e offset
            result.append(f"Function_{addr[-4:]} + offset 0x10")
        else:
            result.append(f"Unknown symbol: {addr}")
    return result
