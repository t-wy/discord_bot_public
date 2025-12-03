# Python version implemented by @t-wy: https://github.com/t-wy

"""
MIT License

Copyright (c) 2025 t-wy

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
if TYPE_CHECKING:
    from .byte_reader import LittleEndianReader

def loads(data: bytes) -> Dict[int, object]:
    # return a JSON dumpable object (i.e. bytes as surrogateescape str)
    from .byte_reader import LittleEndianReader
    reader = LittleEndianReader(data)
    def set_field(target, field, value):
        if field in target:
            if not isinstance(target[field], list):
                target[field] = [target[field]]
            target[field].append(value)
        else:
            target[field] = value
    def message():
        result = {}
        target = result
        stack = []
        while reader.tell() < len(data):
            tag = reader.readVarint() & 0xffffffff # uint32 varint
            field, wire_type = tag >> 3, tag & 0x7
            if wire_type == 0:  # varint
                set_field(target, field, reader.readVarint())
            elif wire_type == 1:  # i64
                set_field(target, field, reader.readULong())
            elif wire_type == 2:  # len
                size = reader.readVarint() & 0xffffffff
                size -= (size & 0x80000000) << 1
                assert reader.tell() + size <= len(data)
                raw_bytes = reader.readBytes(size)
                try:
                    target[field] = loads(raw_bytes)
                except:
                    target[field] = raw_bytes.decode("utf-8", "surrogateescape")
            elif wire_type == 3:  # sgroup
                stack.append((target, field))
                obj = {}
                set_field(target, field, obj)
                target = obj
            elif wire_type == 4:  # egroup
                target, field2 = stack.pop()
                assert field == field2
            elif wire_type == 5:  # i32
                set_field(target, field, reader.readUInt())
            else:
                assert False, "Wire type {} does not exist".format(wire_type)
        if len(stack) > 0:
            assert False, "Unclosed group"
        return result
    return message()

def dumps(obj: Dict[int, object]) -> bytes:
    from .byte_reader import Writer
    def write_value(field, value) -> Tuple[int, bytes]:
        if isinstance(value, int):
            writer.writeVarint((field << 3) | 0)
            writer.writeVarint(value)
        elif isinstance(value, bytes):
            writer.writeVarint((field << 3) | 2)
            writer.writeVarint(len(value))
            writer.write(value)
        elif isinstance(value, str):
            writer.writeVarint((field << 3) | 2)
            writer.writeVarint(len(value))
            writer.write(value.encode("utf-8", "surrogateescape"))
        elif isinstance(value, dict):
            return write_value(field, dumps(value))
        else:
            assert False, "Type \"{}\" not supported".format(type(value).__name__)
    writer = Writer()
    for field, value in obj.items():
        if isinstance(value, list):
            for v in value:
                write_value(field, v)
        else:
            write_value(field, value)
    writer.seek(0)
    return writer.read()

# real protobuf to class instance
# https://protobuf.dev/programming-guides/encoding/

# by default wire type 0, but can be used in other wire types as fallback
int32 = Annotated[int, "int32"] # signed but without zigzag
int64 = Annotated[int, "int64"] # signed but without zigzag
sint = Annotated[int, "sint"] # zigzag when encounting varint
sint32 = sint64 = sint
uint = Annotated[int, "uint"] # same as int
uint32 = uint64 = uint

fixed64 = Annotated[int, "fixed64"] # explicitly wire type 1, makes the distinction when parsed in wire type 2 as packed repeated fields
sfixed64 = Annotated[int, "sfixed64"] # explicitly wire type 1, makes the distinction when parsed in wire type 2 as packed repeated fields
fixed32 = Annotated[int, "fixed32"] # explicitly wire type 5, makes the distinction when parsed in wire type 2 as packed repeated fields
sfixed32 = Annotated[int, "sfixed32"] # explicitly wire type 5, makes the distinction when parsed in wire type 2 as packed repeated fields

double = Annotated[float, "double"] # explicitly wire type 1, makes the distinction from float (single) when parsed in wire type 2 as packed repeated fields

def deserialize(_type, content: bytes):
    from dataclasses import is_dataclass
    assert is_dataclass(_type)
    from .byte_reader import LittleEndianReader
    from enum import Enum
    import struct
    reader = LittleEndianReader(content)
    def get_default_value(_type):
        if _type is None: # deprecated fields
            return None
        # typing_origin = get_origin(_type)
        # if typing_origin is list:
        #     return []
        # if _type is sint or _type is uint or _type is int32 or _type is int64 or _type is fixed64 or _type is sfixed64 or _type is fixed32 or _type is sfixed32 or _type is int:
        #     return 0
        # if _type is str:
        #     return ""
        # if _type is bytes:
        #     return b""
        # if _type is bool:
        #     return False
        # if _type is float or _type is double:
        #     return 0
        if is_dataclass(_type):
            return None
        if isinstance(_type, type) and issubclass(_type, Enum):
            return _type(0)
        if getattr(_type, "__origin__", None) is list: # quick check to avoid get_origin, which is slow
            return []
        return _type()
        # raise NotImplementedError("Type {} not supported".format(_type))
    types = list(_type.__annotations__.values())
    values = [get_default_value(t) for t in types] # 1-based
    total_length = len(reader.getvalue())

    def cast_wire_type_0(value, _type): # varint
        if _type is int or _type is uint:
            return value
        elif _type is sint:
            sign = value & 1
            value = value >> 1
            if sign:
                value = ~value
            return value
        elif _type is int32:
            value &= 0xffffffff
            if value & (1 << 31):
                value -= (1 << 32)
            return value
        elif _type is int64:
            value &= 0xffffffffffffffff
            if value & (1 << 63):
                value -= (1 << 64)
            return value
        elif _type is bool:
            assert value <= 1
            return value == 1
        elif issubclass(_type, Enum):
            try:
                return _type(value)
            except:
                return value
        else:
            assert False, f"Cannot cast value {value} to type {_type}"

    def cast_wire_type_1(value, _type): # i64
        if _type is int or _type is uint or _type is fixed64:
            return value
        elif _type is sint or _type is int64 or _type is sfixed64:
            value &= 0xffffffffffffffff
            if value & (1 << 63):
                value -= (1 << 64)
            return value
        elif _type is float or _type is double:
            # double
            return struct.unpack("<d", struct.pack("<Q", value))[0]
        else:
            assert False, f"Cannot cast value {value} to type {_type}"

    def cast_wire_type_5(value, _type): # i64
        if _type is int or _type is uint or _type is fixed32:
            return value
        elif _type is sint or _type is int32 or _type is int64 or _type is sfixed32:
            value &= 0xffffffff
            if value & (1 << 31):
                value -= (1 << 32)
            return value
        elif _type is float or _type is double:
            # single float
            return struct.unpack('<f', struct.pack('<I', value))[0]
        else:
            assert False, f"Cannot cast value {value} to type {_type}"
    
    while reader.tell() < total_length:
        # current = reader.tell() # debug
        tag = reader.readVarint()
        field_number, wire_type = tag >> 3, tag & 0x7
        assert field_number >= 1, f"Invalid field number: {field_number}"
        field_number -= 1
        # print(current, field_number, wire_type)
        # print(types[field_number])
        field_type = types[field_number] if field_number < len(values) else ...
        typing_origin = get_origin(field_type)
        is_list = typing_origin is list
        if is_list:
            single_type = get_args(field_type)[0]
        else:
            single_type = field_type
        is_repeated = False # wire type 2 multiple entries
        if wire_type == 0:  # varint
            value = cast_wire_type_0(reader.readVarint(), single_type)
        elif wire_type == 1:  # i64
            value = cast_wire_type_1(reader.readULong(), single_type)
        elif wire_type == 2:  # len
            size = reader.readVarint() & 0xffffffff # int32 varint
            size -= (size & 0x80000000) << 1
            assert reader.tell() + size <= total_length
            value = reader.readBytes(size)
            if single_type is bytes:
                pass
            elif single_type is str:
                value = value.decode('utf-8', 'surrogateescape')
            elif is_dataclass(single_type):
                value = deserialize(single_type, value)
            elif is_list and not (
                single_type is bytes or
                single_type is str or
                is_dataclass(single_type)
            ):
                # packed repeated fields
                is_repeated = True
                if (
                    single_type is fixed64 or
                    single_type is sfixed64 or
                    single_type is double
                ):
                    # wire type 1
                    assert size & 7 == 0, "Wire type 1 size must be a multiple of 8"
                    value = struct.unpack(
                        '<' + (
                            'Q' if single_type is fixed64 else 'q' if single_type is sfixed64 else 'd'
                        ) * (size >> 3),
                        value
                    )
                elif (
                    single_type is fixed32 or
                    single_type is sfixed32 or
                    single_type is float
                ):
                    # wire type 5
                    assert size & 3 == 0, "Wire type 5 size must be a multiple of 4"
                    value = struct.unpack(
                        '<' + (
                            'I' if single_type is fixed64 else 'i' if single_type is sfixed32 else 'f'
                        ) * (size >> 2),
                        value
                    )
                else:
                    # wire type 0
                    assert len(value) == 0 or value[-1] < 0x80, "Last byte of Wire type 0 values must be less than 0x80"
                    sub_reader = LittleEndianReader(value)
                    temp = []
                    while sub_reader.tell() < len(value):
                        temp.append(cast_wire_type_0(sub_reader.readVarint(), single_type))
                    value = temp
            else:
                assert False, f"Cannot cast value {value} to type {single_type}"
        elif wire_type == 5:  # i32
            value = cast_wire_type_5(reader.readUInt(), single_type)
        else:
            assert False, f"Wire type {wire_type} is not supported"
        if field_number < len(values):
            if is_list:
                if is_repeated:
                    values[field_number].extend(value)
                else:
                    values[field_number].append(value)
            else:
                values[field_number] = value
        else:
            # Skip assigning value
            pass
    return _type(*values)