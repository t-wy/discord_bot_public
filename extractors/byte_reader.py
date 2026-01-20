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

from io import BytesIO

class Reader(BytesIO):
    def readByte(self) -> int:
        return self.read(1)[0]
    def readBytes(self, length: int) -> bytes:
        return self.read(length)
    def readVarint(self) -> int:
        result = 0
        shift = 0
        while True:
            b = self.readByte()
            result |= (b & 0x7F) << shift
            shift += 7
            if not b & 0x80:
                break
        return result
    def readNullBytes(self) -> bytes:
        pos = self.tell()
        temp = []
        while True:
            chunk = self.read(256)
            position = chunk.find(b'\0')
            if position == -1:
                temp.append(chunk)
            else:
                temp.append(chunk[:position])
                break
            if len(chunk) < 256: # End of file
                break
        result = b"".join(temp)
        self.seek(pos + len(result) + 1)
        return result
    def readNullString(self) -> str:
        return self.readNullBytes().decode("UTF-8", "surrogateescape")
    def peek(self, length: int) -> bytes:
        pos = self.tell()
        temp = self.read(length)
        self.seek(pos)
        return temp

class BigEndianReader(Reader):
    def readUShort(self) -> int:
        "16-bit Unsigned Integer"
        temp = self.read(2)
        return (temp[0] << 8) | temp[1]
    def readShort(self) -> int:
        "16-bit Signed Integer"
        temp = self.readUShort()
        return temp - ((temp & 0x8000) << 1)
    def readUInt(self) -> int:
        "32-bit Unsigned Integer"
        return (self.readUShort() << 16) | self.readUShort()
    def readInt(self) -> int:
        "32-bit Signed Integer"
        return (self.readShort() << 16) | self.readUShort()
    def readULong(self) -> int:
        "64-bit Unsigned Integer"
        return (self.readUInt() << 32) | self.readUInt()
    def readLong(self) -> int:
        "64-bit Signed Integer"
        return (self.readInt() << 32) | self.readUInt()

class LittleEndianReader(Reader):
    def readUShort(self) -> int:
        "16-bit Unsigned Integer"
        return (self.readByte()) | (self.readByte() << 8)
    def readShort(self) -> int:
        "16-bit Signed Integer"
        temp = self.readUShort()
        return temp - ((temp & 0x8000) << 1)
    def readUInt(self) -> int:
        "32-bit Unsigned Integer"
        return self.readUShort() | (self.readUShort() << 16)
    def readInt(self) -> int:
        "32-bit Signed Integer"
        return self.readUShort() | (self.readShort() << 16)
    def readULong(self) -> int:
        "64-bit Unsigned Integer"
        return self.readUInt() | (self.readUInt() << 32)
    def readLong(self) -> int:
        "64-bit Signed Integer"
        return self.readUInt() | (self.readInt() << 32)

class Writer(BytesIO):
    def writeByte(self, value: int) -> int:
        self.write(bytes([value & 0xff]))
    def writeVarint(self, value: int):
        while value >= 0x80:
            self.writeByte((value & 0x7f) | 0x80)
            value >>= 7
        self.writeByte(value)

class BigEndianWriter(Writer):
    def writeShort(self, value: int) -> None:
        self.write(bytes([value >> 8, value & 0xff]))
    def writeInt(self, value: int) -> None:
        self.writeShort(value >> 16)
        self.writeShort(value & 0xffff)
    def writeLong(self, value: int) -> None:
        self.writeInt(value >> 32)
        self.writeInt(value & 0xffffffff)

class LittleEndianWriter(Writer):
    def writeShort(self, value: int) -> None:
        self.write(bytes([value & 0xff, value >> 8]))
    def writeInt(self, value: int) -> None:
        self.writeShort(value & 0xffff)
        self.writeShort(value >> 16)
    def writeLong(self, value: int) -> None:
        self.writeInt(value & 0xffffffff)
        self.writeInt(value >> 32)