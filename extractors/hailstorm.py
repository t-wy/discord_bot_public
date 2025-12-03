# limelight is the name used in SFP.
# hailstorm is the name used in LLLL.
# Python version implemented by @t-wy: https://github.com/t-wy

from dataclasses import dataclass
from typing import *

@dataclass
class CatalogBinary:
    entries: List['CatalogBinaryEntry']

# Catalog.Entry
@dataclass
class CatalogBinaryEntry:
    priority: int
    resource_type: int
    num_deps: int
    num_contents: int
    num_groups: int # NumCategories
    size: int
    label: str
    type: str # not in original implementation
    group_checksum: int # CategoryCrcs
    label_crc: int # ContentNameCrcs
    content_address_crcs: bytes # ContentTypeCrcs
    dep_crcs: bytes
    rec_dep_crcs: bytes
    num_rec_dep_crcs: int
    checksum: int
    seed: int
    content_types: List[str]
    
    def get_real_name(self) -> str:
        return CatalogDefinition.get_real_name(self.label_crc, self.checksum, self.size)

    def to_catalog_manifest(self) -> 'CatalogManifest':
        return CatalogManifest(self.checksum, self.seed, self.size, self.label_crc)

# Hailstorm.Catalog
class CatalogBinaryParser:
    # Init, ParseTransposedArray
    @staticmethod
    def parse(bin: bytes) -> CatalogBinary:
        from extractors.byte_reader import BigEndianReader, BigEndianWriter
        from crc import crc32, crc64
        reader = BigEndianReader(bin)
        magic = reader.readUShort()
        assert magic == 0xca01
        reader.readUShort() # unused
        entryCount = reader.readVarint() # Size
        # Hailstorm:Catalog::ParseTransposedArray
        priorities = [reader.readVarint() for _ in range(entryCount)]
        resource_types = [reader.readVarint() for _ in range(entryCount)]
        num_deps = [reader.readVarint() for _ in range(entryCount)]
        num_contents = [reader.readVarint() for _ in range(entryCount)]
        num_groups = [reader.readVarint() for _ in range(entryCount)] # NumCategories
        sizes = [reader.readVarint() for _ in range(entryCount)]
        types = [reader.readNullString() for _ in range(entryCount)] # TypeCrc
        type_crcs = [crc32(types[i].encode()) for i in range(entryCount)]
        content_types = [[reader.readNullString() for _ in range(num_contents[i])] for i in range(entryCount)]
        # content_type_crcs = [[crc32(content_types[i][j].encode()) for j in range(num_contents[i])] for i in range(entryCount)]
        groups = [[reader.readNullString() for _ in range(num_groups[i])] for i in range(entryCount)]
        group_checksums = [[crc32(groups[i][j].encode()) for j in range(num_groups[i])] for i in range(entryCount)] # CategoryCrcs
        labels = [reader.readNullString() for i in range(entryCount)]
        label_crcs = [crc64(labels[i].encode()) for i in range(entryCount)]
        content_addresses = [[reader.readNullString() for _ in range(num_contents[i])] for i in range(entryCount)] # ContentNameCrcs
        content_address_crcs = [[crc32(content_addresses[i][j].encode()) for j in range(num_contents[i])] for i in range(entryCount)]
        dep = [[reader.readNullString() for _ in range(num_deps[i])] for i in range(entryCount)]
        dep_crcs = [[crc32(dep[i][j].encode()) for j in range(num_deps[i])] for i in range(entryCount)]
        checksums = [reader.readULong() for _ in range(entryCount)]
        seeds = [reader.readULong() if reader.peek(1)[0] & 0x80 else reader.readByte() for _ in range(entryCount)]
        num_rec_dep_crcs = num_deps
        rec_dep_crcs = dep_crcs
        assert len(bin) == reader.tell()
        return CatalogBinary([
            CatalogBinaryEntry(
                priorities[i],
                resource_types[i],
                num_deps[i],
                num_contents[i],
                num_groups[i],
                sizes[i],
                labels[i],
                types[i],
                # type_crcs[i],
                group_checksums[i],
                label_crcs[i],
                content_address_crcs[i],
                dep_crcs[i],
                rec_dep_crcs[i],
                num_rec_dep_crcs[i],
                checksums[i],
                seeds[i],
                content_types[i]
            )
        for i in range(entryCount)])

    @staticmethod
    def parse_compressed(bin: bytes) -> CatalogBinary:
        import lz4.frame
        return CatalogBinaryParser.parse(lz4.frame.decompress(bin))
    
    @staticmethod
    def parse_encoded(manifest: 'CatalogManifest', input: bytes) -> CatalogBinary:
        return CatalogBinaryParser.parse(decrypt(input, manifest.seed, manifest.name_crc, manifest.size, is_manifest=True))

class CatalogDefinition:
    # Catalog.Entry.GetRealName
    @staticmethod
    def get_real_name(label_crc: int, checksum: int, size: int) -> str:
        from base64 import b32encode
        from hashlib import md5
        from extractors.byte_reader import BigEndianWriter
        writer = BigEndianWriter()
        writer.writeLong(checksum)
        writer.writeLong(label_crc)
        writer.writeVarint(size)
        return b32encode(md5(writer.getvalue()).digest()).decode().rstrip("=").lower()

def decrypt(data: bytes, seed: int, crc64: int, resource_type: bytes, size: int) -> bytes:
    from hashlib import sha256
    from crc import crc32
    from extractors.byte_reader import BigEndianWriter
    writer = BigEndianWriter()
    # Hailstorm.Catalog::Parse
    writer.write(bytes.fromhex("c34ea77df4976cd8907096fa47bb97e61852305892494e3692ba0c7eb434f022c549c96cf7ca0ee1b6ba7f203b6c76e8679699ce9c44af7b1cb000173a515938"))
    writer.writeLong(seed)
    writer.writeLong(crc64)
    writer.writeInt(crc32(resource_type))
    writer.writeVarint(size)
    hash = sha256(writer.getvalue()).digest()
    key = hash[:16]
    iv = hash[16:]
    from Crypto.Cipher import AES
    aes = AES.new(key, AES.MODE_CBC, iv = iv)
    data = aes.decrypt(data)
    # Hailstorm.Catalog::Decompress
    import lz4.frame
    return lz4.frame.decompress(data)


# Catalog.Manifest
@dataclass
class CatalogManifest:
    checksum: int
    seed: int
    size: int
    label_crc: int # for decrypt
    name_crc: int # for remote path
    
    def get_real_name(self) -> str:
        return CatalogDefinition.get_real_name(self.name_crc, self.checksum, self.size)

    # FromSignature
    # DecomposeSignature
    @staticmethod
    def from_unique_version(unique_version: str, bundle_version: str) -> 'CatalogManifest':
        assert "@" in unique_version
        # SimpleResver
        simple_version, catalog_info_encoded = unique_version.split("@")
        from extractors.byte_reader import BigEndianReader
        from crc import crc64
        from base64 import b64decode
        reader = BigEndianReader(b64decode(catalog_info_encoded))
        checksum = reader.readULong()
        seed = reader.readULong()
        size = reader.readVarint()
        label_crc = crc64(f"{bundle_version}:{simple_version}".encode())
        name_crc = crc64(simple_version.encode())
        return CatalogManifest(checksum, seed, size, label_crc, name_crc)

    @staticmethod
    def from_values(label_crc: str, name_crc: str, size: int, checksum: int, seed: int) -> 'CatalogManifest':
        return CatalogManifest(checksum, seed, size, label_crc, name_crc)