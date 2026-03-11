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
                    content = loads(raw_bytes)
                except:
                    content = raw_bytes.decode("utf-8", "surrogateescape")
                set_field(target, field, content)
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
    return writer.getvalue()

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

def deserialize(_type, content: bytes, _temp = None):
    from dataclasses import is_dataclass
    assert is_dataclass(_type)
    from .byte_reader import LittleEndianReader
    from enum import Enum
    import struct, pickle
    if _temp is None:
        _temp = {}
    class_temp = _temp
    reader = LittleEndianReader(content)
    def get_default_value(_type):
        if _type is None: # deprecated fields
            return None
        if isinstance(_type, type):
            if issubclass(_type, Enum):
                return _type(0)
            if hasattr(_type, '__dataclass_fields__'):
                return None
        if getattr(_type, "__origin__", None) is list: # quick check to avoid get_origin, which is slow
            return [] # use tuple to check we are not adding things to this placeholder list
        return _type()
    if _type in class_temp:
        types, values, is_list_single_type = class_temp[_type]
        values = values.copy() # values would be modified in place later
    else:
        types = tuple(_type.__annotations__.values())
        values = [get_default_value(t) for t in types] # 1-based
        is_list_single_type = [
            (
                (True, get_args(field_type)[0])
                if getattr(field_type, "__origin__", None) is list  # quick check to avoid get_origin, which is slow
                else (False, field_type)
            )
            for field_type in types
        ]
        class_temp[_type] = (types, values.copy(), is_list_single_type) # values would be modified in place later
    total_length = len(reader.getvalue())

    def cast_wire_type_0(value, _type): # varint
        if _type is int or _type is uint:
            return value
        if _type is sint:
            sign = value & 1
            value = value >> 1
            if sign:
                value = ~value
            return value
        if _type is int32:
            value &= 0xffffffff
            if value & (1 << 31):
                value -= (1 << 32)
            return value
        if _type is int64:
            value &= 0xffffffffffffffff
            if value & (1 << 63):
                value -= (1 << 64)
            return value
        if _type is bool:
            assert value <= 1
            return value == 1
        if issubclass(_type, Enum):
            try:
                return _type(value)
            except:
                return value
        assert False, f"Cannot cast value {value} to type {_type}"

    def cast_wire_type_1(value: int, _type): # i64
        if _type is int or _type is uint or _type is fixed64:
            return value
        if _type is sint or _type is int64 or _type is sfixed64:
            value &= 0xffffffffffffffff
            if value & (1 << 63):
                value -= (1 << 64)
            return value
        if _type is float or _type is double:
            # double
            return struct.unpack("<d", struct.pack("<Q", value))[0]
        assert False, f"Cannot cast value {value} to type {_type}"

    def cast_wire_type_2(value: bytes, _type, is_list: bool): # len
        if _type is bytes:
            return value, False
        if _type is str:
            return value.decode('utf-8', 'surrogateescape'), False
        if hasattr(_type, '__dataclass_fields__'): # is_dataclass(_type):
            return deserialize(_type, value, _temp = _temp), False
        if is_list:
            # packed repeated fields
            if (
                _type is fixed64 or
                _type is sfixed64 or
                _type is double
            ):
                # wire type 1
                assert size & 7 == 0, "Wire type 1 size must be a multiple of 8"
                return struct.unpack(
                    '<' + (
                        'Q' if _type is fixed64 else 'q' if _type is sfixed64 else 'd'
                    ) * (size >> 3),
                    value
                ), True
            if (
                _type is fixed32 or
                _type is sfixed32 or
                _type is float
            ):
                # wire type 5
                assert size & 3 == 0, "Wire type 5 size must be a multiple of 4"
                return struct.unpack(
                    '<' + (
                        'I' if _type is fixed64 else 'i' if _type is sfixed32 else 'f'
                    ) * (size >> 2),
                    value
                ), True
            # wire type 0
            assert len(value) == 0 or value[-1] < 0x80, "Last byte of Wire type 0 values must be less than 0x80"
            sub_reader = LittleEndianReader(value)
            temp = []
            while sub_reader.tell() < len(value):
                temp.append(cast_wire_type_0(sub_reader.readVarint(), _type))
            return temp, True
        assert False, f"Cannot cast value {value} to type {_type}"

    def cast_wire_type_5(value: int, _type): # i32
        if _type is int or _type is uint or _type is fixed32:
            return value
        if _type is sint or _type is int32 or _type is int64 or _type is sfixed32:
            value &= 0xffffffff
            if value & (1 << 31):
                value -= 1 << 32
            return value
        if _type is float or _type is double:
            # single float
            return struct.unpack('<f', struct.pack('<I', value))[0]
        assert False, f"Cannot cast value {value} to type {_type}"
    
    is_list, single_type = False, int
    while reader.tell() < total_length:
        # current = reader.tell() # debug
        tag = reader.readVarint()
        field_number, wire_type = tag >> 3, tag & 0x7
        assert field_number >= 1, f"Invalid field number: {field_number}"
        field_number -= 1
        skip = field_number >= len(values)
        if not skip:
            is_list, single_type = is_list_single_type[field_number]
        is_repeated = False # wire type 2 multiple entries
        if wire_type == 0:  # varint
            value = reader.readVarint()
            if skip:
                continue
            value = cast_wire_type_0(value, single_type)
        elif wire_type == 1:  # i64
            value = reader.readULong()
            if skip:
                continue
            value = cast_wire_type_1(value, single_type)
        elif wire_type == 2:  # len
            size = reader.readVarint() & 0xffffffff # int32 varint
            size -= (size & 0x80000000) << 1
            assert reader.tell() + size <= total_length
            value = reader.readBytes(size)
            if skip:
                continue
            value, is_repeated = cast_wire_type_2(value, single_type, is_list)
        elif wire_type == 5:  # i32
            value = reader.readUInt()
            if skip:
                continue
            value = cast_wire_type_5(value, single_type)
        else:
            assert False, f"Wire type {wire_type} is not supported"
        if is_list:
            if len(values[field_number]) == 0: # by this we don't need to deep copy the default list
                if is_repeated:
                    values[field_number] = value
                else:
                    values[field_number] = [value]
            else:
                if is_repeated:
                    values[field_number].extend(value)
                else:
                    values[field_number].append(value)
        else:
            values[field_number] = value
    return _type(*values)

def serialize(instance) -> bytes:
    _type = type(instance)
    from dataclasses import is_dataclass
    assert is_dataclass(_type)
    field_types = list(_type.__annotations__.values())
    fields = list(_type.__dataclass_fields__.values())
    from .byte_reader import LittleEndianWriter
    from enum import Enum
    import struct
    def write_value(field_number, field_type, value) -> Tuple[int, bytes]:
        # typing_origin = get_origin(field_type)
        is_list = getattr(field_type, "__origin__", None) is list # quick check to avoid get_origin, which is slow
        if is_list:
            single_type = get_args(field_type)[0]
            for v in value:
                write_value(field_number, single_type, v)
            return
        if field_type is fixed32 or field_type is sfixed32:
            # wire type 5
            writer.writeVarint((field_number << 3) | 5)
            writer.writeInt(value)
        elif field_type is float:
            # wire type 5
            writer.writeVarint((field_number << 3) | 5)
            writer.write(struct.pack('<f', value))
        elif field_type is fixed64 or field_type is sfixed64:
            # wire type 1
            writer.writeVarint((field_number << 3) | 1)
            writer.writeLong(value)
        elif field_type is double:
            # wire type 1
            writer.writeVarint((field_number << 3) | 1)
            writer.write(struct.pack('<d', value))
        elif field_type is bytes:
            # wire type 2
            writer.writeVarint((field_number << 3) | 2)
            writer.writeVarint(len(value))
            writer.write(value)
        elif field_type is str:
            # wire type 2
            writer.writeVarint((field_number << 3) | 2)
            serialized = value.encode("utf-8", "surrogateescape")
            writer.writeVarint(len(serialized))
            writer.write(serialized)
        elif is_dataclass(field_type):
            if value is not None:
                # wire type 2
                writer.writeVarint((field_number << 3) | 2)
                serialized = serialize(value)
                writer.writeVarint(len(serialized))
                writer.write(serialized)
        else:
            # wire type 0
            if field_type is int or field_type is uint:
                pass
            elif field_type is sint:
                sign = value < 0
                if sign:
                    value = ~value
                value = (value << 1) | (1 if sign else 0)
            elif field_type is int32:
                if value < 0:
                    value += 1 << 32
            elif field_type is int64:
                if value < 0:
                    value += 1 << 64
            elif field_type is bool:
                value = 1 if value else 0
            elif issubclass(field_type, Enum):
                assert isinstance(value, field_type)
                value = value.value
            else:
                assert False, "Type \"{}\" not supported".format(type(value).__name__)
            writer.writeVarint((field_number << 3) | 0)
            writer.writeVarint(value)
    writer = LittleEndianWriter()
    for index, (field_type, value) in enumerate(zip(field_types, fields)):
        write_value(index + 1, field_type, getattr(instance, value.name))
    return writer.getvalue()