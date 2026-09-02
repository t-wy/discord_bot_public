import io
from typing import Optional
def hca_decode(data: bytes, cipher: int = 0xCF222F1FE0748978, subkey: Optional[int] = None) -> io.BytesIO:
    try:
        from .hca import hca_decode
        return hca_decode(data, cipher, subkey=subkey)
    except:
        import traceback
        traceback.print_exc()
        # use https://github.com/Youjose/PyCriCodecs
        from PyCriCodecs import HCA
        hcaObj = HCA(data, key=cipher, subkey=0 if subkey is None else subkey)
        return io.BytesIO(hcaObj.decode())

def hca_duration(data: bytes) -> float:
    sampling_rate = int.from_bytes(data[13:16], byteorder='big')
    block_count = int.from_bytes(data[16:20], byteorder='big')
    # each block contains 1024 (8 * 0x80) samples for each channel
    return block_count * 8 * 0x80 / sampling_rate

def add_key_and_subkey(key: Optional[int], subkey: Optional[int]) -> Optional[int]:
    """
    Some hca files have an extra subkey to prevent key reuse
    """
    if key is None:
        return None
    if subkey is None or subkey == 0:
        return key
    return (key * ((subkey << 16) | (((subkey & 0xFFFF) ^ 0xFFFF) + 2))) & 0xFFFFFFFFFFFFFFFF

def decrypt_hca(data: bytes, cipher: int = 0xCF222F1FE0748978, subkey: Optional[int] = None) -> bytes:
    from .hca import hca_parse, checkSum
    hca_file = hca_parse(data, cipher, subkey)
    if hca_file.ciph.type == 0:
        # not encrypted
        return data
    assert hca_file.ciph_loc is not None
    sbox = hca_file.ciphertable
    parts = [
        data[:hca_file.ciph_loc + 4] + b"\0\0", # 0, overwrite the cipher type
        data[hca_file.ciph_loc + 6: hca_file.header.dataOffset], # unaffected
    ]
    for idx in range(hca_file.format.block_count):
        offset = hca_file.header.dataOffset + hca_file.comp.block_size * idx
        block = data[offset: offset + hca_file.comp.block_size]
        assert len(block) == hca_file.comp.block_size
        datablock = bytes([sbox[x] for x in block[:-2]])
        crc = checkSum(datablock)
        # Notice that CRC16Table[0] = 0x0000
        # calculate the last 2 bytes such that crc = 0, which is the same as the crc actually
        parts.append(datablock + bytes([crc >> 8, crc & 0xff]))
    return b"".join(parts)