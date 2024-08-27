from typing import Dict

def unpack(data: bytes) -> list:
    """
    Redistribution Notice:
    Properly attribute all entities listed below and request others to follow the same.
    Otherwise, DO NOT remove or modify this comment.
    Specification (MessagePack for C#):
    https://github.com/MessagePack-CSharp/MessagePack-CSharp
    Dependencies:
    msgpack: https://github.com/msgpack/msgpack-python
    lz4: https://github.com/python-lz4/python-lz4
    Implementation:
    @t-wy: https://github.com/t-wy
    """
    from msgpack import unpackb, Unpacker

    def LZ4_decompress(size: int, src: bytes) -> bytes:
        from lz4.block import decompress
        return decompress(src, uncompressed_size=size)

    def ext_hook(code, data):
        if code == 99:
            unpacker = Unpacker(None, max_buffer_size=0, strict_map_key=False) # integer may be used as key
            unpacker.feed(data)
            return unpackb(LZ4_decompress(unpacker.unpack(), data[unpacker.tell():]), strict_map_key=False) # make sure to call unpack before tell
        elif code == 98: # list of integers specifying lengths of each part
            unpacker = Unpacker(None, max_buffer_size=0)
            unpacker.feed(data)
            return tuple(unpacker)
        raise ValueError
    
    def check_98(lst):
        if len(lst) > 0 and type(lst[0]) is tuple:
            return unpackb(b"".join(LZ4_decompress(size, part) for size, part in zip(lst[0], lst[1:])), strict_map_key=False)
        return lst

    unpacker = Unpacker(None, ext_hook=ext_hook, list_hook=check_98, max_buffer_size=0, strict_map_key=False)
    unpacker.feed(data)
    return list(unpacker)


def master_memory_raw(data: bytes) -> Dict[str, list]:
    content = unpack(data)
    return {key: content[index + 1] for index, (key, (offset, length)) in enumerate(content[0].items())}
