# Based on https://github.com/Cysharp/MemoryPack/blob/main/sandbox/SandboxWebApp/wwwroot/js/memorypack/MemoryPackReader.ts
# Python version implemented by @t-wy: https://github.com/t-wy

"""
MIT License

Copyright (c) 2025 t-wy
Copyright (c) 2022 Cysharp, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import *
from .byte_reader import LittleEndianReader
from dataclasses import is_dataclass
from datetime import datetime, timezone, timedelta

def deserialize(_type, content: bytes):
    reader = LittleEndianReader(content)
    return deserialize_buffer(_type, reader)

def deserialize_buffer(_type, reader: LittleEndianReader):
    # print(_type)
    typing_origin = get_origin(_type)
    if typing_origin is dict:
        return deserialize_map(*get_args(_type), reader)
    if typing_origin is tuple:
        return deserialize_tuple(get_args(_type), reader)
    if typing_origin is list:
        return deserialize_array(get_args(_type)[0], reader)
    if _type is str:
        return deserialize_string(reader)
    if _type is int:
        return reader.readInt()
    if _type is bool:
        return reader.readByte() != 0
    if _type is float:
        import struct
        return struct.unpack("<f", reader.read(4))[0]
    if _type is datetime:
        dateTimeMask = 0b00111111_11111111_11111111_11111111_11111111_11111111_11111111_11111111
        unixEpochTicks = 621355968000000000
        ticks = reader.readULong() & dateTimeMask
        unixMillisecond = (ticks - unixEpochTicks) / 10000
        return datetime.fromtimestamp(unixMillisecond / 1000, tz=timezone(offset=timedelta(hours=9)))
    if is_dataclass(_type):
        return deserialize_dataclass(_type, reader)
    from enum import Enum
    if issubclass(_type, Enum):
        return _type(reader.readInt())
    raise NotImplementedError("Type {} not supported".format(_type))

def deserialize_map(key_type, value_type, reader: LittleEndianReader) -> dict:
    length = reader.readInt()
    result = {}
    for _ in range(length):
        key = deserialize_buffer(key_type, reader)
        value = deserialize_buffer(value_type, reader)
        result[key] = value
    return result

def deserialize_tuple(data_types, reader: LittleEndianReader) -> tuple:
    result = []
    for _type in data_types:
        result.append(deserialize_buffer(_type, reader))
    return tuple(result)

def deserialize_array(data_type, reader: LittleEndianReader) -> list:
    length = reader.readInt()
    result = []
    for _ in range(length):
        result.append(deserialize_buffer(data_type, reader))
    return result

def deserialize_dataclass(dataclass, reader: LittleEndianReader):
    length = reader.readByte()
    assert len(dataclass.__annotations__) == length, (hex(reader.tell()), len(dataclass.__annotations__), length)
    arguments = []
    for key in dataclass.__annotations__:
        arguments.append(deserialize_buffer(dataclass.__annotations__[key], reader))
    temp = dataclass(*arguments)
    return temp

def deserialize_string(reader: LittleEndianReader) -> str:
    length = reader.readInt()
    if length == 0:
        return ""
    if length > 0: # UTF-16
        byte_length = length * 2
        return reader.read(byte_length).decode("UTF-16")
    else: # UTF-8
        utf8_length = ~length # e.g. ~(-1) -> 0, ~(-2) -> 1
        reader.read(4) # utf16-length, no use
        return reader.read(utf8_length).decode("UTF-8")
    