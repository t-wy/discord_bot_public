# limelight is the name used in SFP.
# hailstorm is the name used in LLLL.
# Python version implemented by @t-wy: https://github.com/t-wy

from dataclasses import dataclass
from typing import *

@dataclass
class CatalogBinary:
    group_relations: Dict[int, List[int]]
    entries: List['CatalogBinaryEntry']

@dataclass
class CatalogBinaryEntry:
    priority: int
    resource_type: int
    num_deps: int
    num_contents: int
    num_groups: int
    size: int
    label: str
    type_idx: int
    type: str # not in original implementation
    group_checksum: int
    label_crc: int
    content_address_crcs: bytes
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

class CatalogBinaryParser:
    @staticmethod
    def parse(bin: bytes) -> CatalogBinary:
        from extractors.byte_reader import BigEndianReader, BigEndianWriter
        from crc import crc32, crc64
        reader = BigEndianReader(bin)
        magic = reader.readUShort()
        assert magic == 0xbc10
        entryCount = reader.readVarint()
        typeCount = reader.readVarint()
        groupCount = reader.readVarint()
        type_map = [reader.readNullString() for _ in range(typeCount)]
        group_map = {}
        for i in range(groupCount):
            temp = reader.readNullBytes()
            group_map[i] = crc32(temp)
        group_relations: Dict[int, List[int]] = {}
        rev_map: Dict[str, int] = {}
        # parseTransposedArray
        priorities = [reader.readVarint() for _ in range(entryCount)]
        resource_types = [reader.readVarint() for _ in range(entryCount)]
        num_deps = [reader.readVarint() for _ in range(entryCount)]
        num_contents = [reader.readVarint() for _ in range(entryCount)]
        num_groups = [reader.readVarint() for _ in range(entryCount)]
        sizes = [reader.readVarint() for _ in range(entryCount)]
        type_idxs = [reader.readVarint() for _ in range(entryCount)]
        types = [type_map[type_idxs[i]] for i in range(entryCount)]
        content_types = [[type_map[reader.readVarint()] for _ in range(num_contents[i])] for i in range(entryCount)]
        group_checksums = []
        for i in range(entryCount):
            writer = BigEndianWriter()
            for _ in range(num_groups[i]):
                group_id = group_map[reader.readVarint()]
                writer.writeInt(group_id)
                group_relations.setdefault(group_id, [])
                group_relations[group_id].append(i)
            group_checksums.append(crc32(writer.getvalue()))
        labels = []
        label_crcs = []
        for i in range(entryCount):
            label = reader.readNullBytes()
            crc = crc64(label + b"." + type_map[type_idxs[i]].encode())
            labels.append(label.decode())
            label_crcs.append(crc)
            rev_map[labels[i]] = i
        content_address_crcs = []
        for i in range(entryCount):
            writer = BigEndianWriter()
            for j in range(num_contents[i]):
                address = reader.readNullBytes() # seems to be the names of each asset in atlas
                crc = crc64(address + b"." + content_types[i][j].encode())
                writer.writeLong(crc)
            content_address_crcs.append(writer.getvalue())
        dep_crcs = []
        num_rec_dep_crcs = []
        rec_dep_crcs = []
        for i in range(entryCount):
            writer = BigEndianWriter()
            for _ in range(num_deps[i]):
                dep = reader.readNullBytes() # names of the dependencies of prefab assets
                crc = crc64(dep)
                writer.writeLong(crc)
            dep_crcs.append(writer.getvalue())
            num_rec_dep_crcs.append(num_deps[i])
            rec_dep_crcs.append(dep_crcs[i])
        checksums = [reader.readULong() for _ in range(entryCount)]
        seeds = [reader.readULong() if reader.peek(1)[0] & 0x80 else reader.readByte() for _ in range(entryCount)]
        assert len(bin) == reader.tell()
        return CatalogBinary(group_relations, [
            CatalogBinaryEntry(
                priorities[i],
                resource_types[i],
                num_deps[i],
                num_contents[i],
                num_groups[i],
                sizes[i],
                labels[i],
                type_idxs[i],
                types[i],
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
    @staticmethod
    def get_real_name(label_crc: int, checksum: int, size: int) -> str:
        from base64 import b32encode
        from hashlib import md5
        from extractors.byte_reader import BigEndianWriter
        writer = BigEndianWriter()
        writer.writeLong(checksum)
        writer.writeVarint(size)
        writer.writeLong(label_crc)
        return b32encode(md5(writer.getvalue()).digest()).decode().rstrip("=")

# LimeLight.CatelogBinaryParser.ParseEncoded
# Limelight.RawAssetCoder.PackUnpack
def decrypt(data: bytes, seed: int, label_crc: int, size: int, is_manifest: bool = False) -> bytes:
    from hashlib import sha1
    from extractors.byte_reader import BigEndianWriter
    writer = BigEndianWriter()
    if is_manifest:
        writer.write(bytes.fromhex("E040926FB42EBD50886A8849E5545924"))
    writer.writeLong(seed)
    writer.writeLong(label_crc)
    if is_manifest:
        writer.writeVarint(size)
    else:
        writer.writeLong(size)
    hash = sha1(writer.getvalue()).digest()
    key = hash[:16]
    iv = hash[4:20]
    from Crypto.Cipher import AES
    aes = AES.new(key, AES.MODE_CTR, initial_value=iv, nonce=b"")
    data = aes.decrypt(data)
    import lz4.frame
    return lz4.frame.decompress(data)


@dataclass
class CatalogManifest:
    checksum: int
    seed: int
    size: int
    name_crc: int
    
    def get_real_name(self) -> str:
        return CatalogDefinition.get_real_name(self.name_crc, self.checksum, self.size)

    @staticmethod
    def from_unique_version(unique_version: str, bundle_version: str) -> 'CatalogManifest':
        assert "@" in unique_version
        simple_version, catalog_info_encoded = unique_version.split("@")
        from extractors.byte_reader import BigEndianReader
        from crc import crc64
        from base64 import b64decode
        reader = BigEndianReader(b64decode(catalog_info_encoded))
        checksum = reader.readULong()
        size = reader.readVarint()
        seed = reader.readULong()
        label_crc = crc64(f"{bundle_version}:{simple_version}".encode())
        return CatalogManifest(checksum, seed, size, label_crc)

    @staticmethod
    def from_values(label_crc: str, size: int, checksum: int, seed: int) -> 'CatalogManifest':
        return CatalogManifest(checksum, seed, size, label_crc)