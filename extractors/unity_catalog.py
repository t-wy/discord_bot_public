# Official files: check https://download.packages.unity.com/com.unity.addressables
# e.g. https://download.packages.unity.com/com.unity.addressables/-/com.unity.addressables-2.7.4.tgz
# Path: package/Runtime/ResourceLocators/ContentCatalogData.cs
# Class: ContentCatalogData
# Python version implemented by @t-wy: https://github.com/t-wy

from typing import *
from common.asset_list import AssetList
from extractors.byte_reader import LittleEndianReader

def readObject(reader: LittleEndianReader):
    obj_type = reader.readByte()
    if obj_type == 0: # AsciiString
        return reader.readBytes(reader.readUInt()).decode()
    if obj_type == 1: # UnicodeString
        return reader.readBytes(reader.readUInt()).decode("UTF-16")
    if obj_type == 2: # UInt16
        return reader.readUShort()
    if obj_type == 3: # UInt32
        return reader.readUInt()
    if obj_type == 4: # Int32
        return reader.readInt()
    if obj_type == 5: # Hash128
        return reader.read(reader.readByte()) # 128 bit hash represented as 32 hex chars
    if obj_type == 6: # Type
        return reader.read(reader.readByte()) # Refer to GetTypeFromCLSID 
    if obj_type == 7: # JsonObject
        import json
        return JsonObject(
            reader.readBytes(reader.readByte()).decode(), # assembly name
            reader.readBytes(reader.readByte()).decode(), # class name
            json.loads(reader.readBytes(reader.readUInt()).decode("UTF-16")) # data
        )
    assert False, "Type {} not supported".format(obj_type)

def readObject2(reader: LittleEndianReader, offset: int, version: int = 2):
    if offset == 0xFFFFFFFF:
        return None
    reader.seek(offset)
    type_name_offset = reader.readUInt()
    object_offset = reader.readUInt()
    is_default_object = object_offset == 0xFFFFFFFF
    serialized_type = SerializedType.read_binary(reader, offset = type_name_offset, version=version)
    assert "," in serialized_type.assembly_name, "Assembly name must have commas"
    match_name = (serialized_type.assembly_name.split(",")[0], serialized_type.class_name)
    if match_name == ("mscorlib", "System.Int32"):
        if is_default_object:
            return 0 # default of int
        reader.seek(object_offset)
        return reader.readInt()
    elif match_name == ("mscorlib", "System.Int64"):
        if is_default_object:
            return 0 # default of long
        reader.seek(object_offset)
        return reader.readLong()
    elif match_name == ("mscorlib", "System.Boolean"):
        if is_default_object:
            return False # default of bool
        reader.seek(object_offset)
        return reader.readByte() != 0
    elif match_name == ("mscorlib", "System.String"):
        if is_default_object:
            return None # default of string
        reader.seek(object_offset)
        string_offset = reader.readUInt()
        separator = reader.read(1).decode()
        return readEncodedString(reader, string_offset, version=version, separator=separator)
    elif match_name == ("UnityEngine.CoreModule", "UnityEngine.Hash128"):
        if is_default_object:
            return None # default of Hash128
        reader.seek(object_offset)
        # v0 = reader.readUInt()
        # v1 = reader.readUInt()
        # v2 = reader.readUInt()
        # v3 = reader.readUInt()
        return reader.read(16).hex()
    elif match_name == ("Unity.ResourceManager", "UnityEngine.ResourceManagement.ResourceProviders.AssetBundleRequestOptions"):
        # SerializedData
        # public object Deserialize(BinaryStorageBuffer.Reader reader, Type type, uint offset, out uint size)
        if is_default_object:
            return None # default
        reader.seek(object_offset)
        hash_offset = reader.readUInt()
        bundle_name_offset = reader.readUInt()
        crc = reader.readUInt()
        bundle_size = reader.readUInt()
        common_info_offset = reader.readUInt()
        reader.seek(hash_offset)
        hash = reader.read(16).hex()
        bundle_name = readEncodedString(reader, bundle_name_offset, version=version, separator="_")
        reader.seek(common_info_offset)
        common_info = {
            "m_Timeout": reader.readShort(),
            "m_RedirectLimit": reader.readByte(),
            "m_RetryCount": reader.readByte(),
            "m_Flags": (flags := reader.readInt()),
            "m_AssetLoadMode": flags & 1, # RequestedAssetAndDependencies, AllPackedAssetsAndDependencies
            "m_ChunkedTransfer": bool(flags & 2),
            "m_UseCrcForCachedBundles": bool(flags & 4),
            # UseUnityWebRequestForLocalBundles
            "m_UseUWRForLocalBundles": bool(flags & 8),
            "m_ClearOtherCachedVersionsWhenLoaded": bool(flags & 16),
        }
        return JsonObject(
            serialized_type.assembly_name,
            serialized_type.class_name,
            {
                # "version": 3,
                "m_Hash": hash,
                "m_BundleName": bundle_name,
                "m_Crc": crc,
                "m_BundleSize": bundle_size,
                **common_info
            }
        )
    assert False, f"Unable to find serialization adapter for type {match_name}"

# ResourceManager/Util/BinaryStorageBuffer.cs
# public string ReadString(uint id, out uint size, char sep = (char)0, bool cacheValue = true)
def readEncodedString(reader: LittleEndianReader, offset: int, separator: str = "\0", version: int = 2):
    assert len(separator) == 1
    if offset == 0xFFFFFFFF:
        return None
    kUnicodeStringFlag = 0x80000000
    kDynamicStringFlag = 0x40000000
    kClearFlagsMask = 0x3fffffff
    unicode = offset & kUnicodeStringFlag == kUnicodeStringFlag
    if separator == "\0" or offset & kDynamicStringFlag == 0:
        # string ReadAutoEncodedString(uint id, out uint size, bool cacheValue)
        reader.seek((offset & kClearFlagsMask) - 4) # sizeof(uint): 4
        length = reader.readUInt()
        data = reader.readBytes(length)
        if unicode:
            return data.decode("UTF-16")
        else:
            return data.decode()
    else: # dynamic
        # string ReadDynamicString(uint id, out uint size, char sep, bool cacheValue)
        assert offset & kDynamicStringFlag == kDynamicStringFlag # else ReadAutoEncodedString
        # omitted: int GetDynamicStringLength(uint id, char sep)
        parts: List[str] = []
        next_part_offset = offset
        while next_part_offset != 0xffffffff:
            reader.seek(next_part_offset & kClearFlagsMask)
            part_string_offset = reader.readUInt() # stringId
            next_part_offset = reader.readUInt() # nextID
            parts.append(readEncodedString(reader, part_string_offset, version = version))
        if version > 1:
            return separator.join(parts[::-1])
        else:
            return separator.join(parts)

def readOffsetArray(reader: LittleEndianReader, offset: int):
    if offset == 0xffffffff:
        return []
    reader.seek(offset - 4)
    byte_size = reader.readInt()
    assert byte_size % 4 == 0, "Array size must be a multiple of 4"
    return [reader.readUInt() for _ in range(byte_size // 4)]


def expand_internal_id(internal_id_prefixes: List[str], v: str):
    # ContentCatalogData.cs, internal static string ExpandInternalId(string[] internalIdPrefixes, string v)
    if len(internal_id_prefixes) == 0 or "#" not in v:
        return v
    next_hash = v.rfind("#")
    prefix_index, remaining = v[:next_hash], v[next_hash + 1:]
    if not all(c in "0123456789" for c in prefix_index):
        return v
    return internal_id_prefixes[int(prefix_index)] + remaining

class exportable_object(dict):
    def __setattr__(self, __name: str, __value) -> None:
        super().__setitem__(__name, __value)
        super().__setattr__(__name, __value)

class JsonObject(exportable_object):
    def __init__(self, assembly_name, class_name, data):
        self.assembly_name = assembly_name
        self.class_name = class_name
        self.data = data

class SerializedType(exportable_object):
    def __init__(self, assembly_name, class_name):
        self.assembly_name = assembly_name
        self.class_name = class_name
    
    @staticmethod
    def read_binary(reader: LittleEndianReader, offset: int, version: int = 2):
        reader.seek(offset)
        assembly_name_offset = reader.readUInt()
        class_name_offset = reader.readUInt()
        assembly_name = readEncodedString(reader, offset = assembly_name_offset, version = version, separator=".")
        class_name = readEncodedString(reader, offset = class_name_offset, version = version, separator=".")
        return SerializedType(assembly_name, class_name)

class CompactLocation(exportable_object): # ResourceLocation
    def __init__(self, m_InternalId: str, m_ProviderId: str, m_Dependency: List['CompactLocation'], m_Data: object, m_DependencyHashCode: int, m_PrimaryKey: str, m_Type: str): # m_Type: type
        # m_Locator
        self.internal_id = m_InternalId
        self.provider_id = m_ProviderId
        self.dependency = m_Dependency
        self.dependency_hash_code = m_DependencyHashCode
        self.data = m_Data
        # m_HashCode = internalId.GetHashCode() * 31 + providerId.GetHashCode()
        self.primary_key = m_PrimaryKey
        self.resource_type = m_Type
        self.keys = []
    
    @staticmethod
    def create_uninitialized():
        return CompactLocation(None, None, None, None, None, None, None)
    
    # public ResourceLocation(BinaryStorageBuffer.Reader r, uint id, out uint size, bool resolveInternalId)
    @staticmethod
    def read_binary(reader: LittleEndianReader, offset: int, cache: dict, version: int = 2):
        if offset in cache:
            return cache[offset]
        # prevent infinite recursion, set the value here
        result = CompactLocation.create_uninitialized()
        cache[offset] = result
        reader.seek(offset)
        primary_key_offset = reader.readUInt()
        internal_id_offset = reader.readUInt()
        provider_id_offset = reader.readUInt()
        dependenies_offset = reader.readUInt()
        dependency_hash_code = reader.readInt()
        data_offset = reader.readUInt()
        type_offset = reader.readUInt()
        primary_key = readEncodedString(
            reader,
            offset = primary_key_offset,
            separator = "/",
            version = version
        )
        internal_id = readEncodedString(
            reader,
            offset = internal_id_offset,
            separator = "/",
            version = version
        )
        provider_id = readEncodedString(
            reader,
            offset = provider_id_offset,
            separator = ".",
            version = version
        )
        dependency_offsets = readOffsetArray(reader, offset = dependenies_offset)
        dependencies = []
        for object_offset in dependency_offsets:
            dependencies.append(CompactLocation.read_binary(reader, offset = object_offset, cache = cache, version = version))
        data = readObject2(reader, offset = data_offset, version=version)
        serialized_type = SerializedType.read_binary(reader, offset=type_offset, version=version)
        result.__init__(
            internal_id,
            provider_id,
            dependencies,
            data,
            dependency_hash_code,
            primary_key,
            {
                "m_AssemblyName": serialized_type.assembly_name,
                "m_ClassName": serialized_type.class_name
            }
        )
        return result

def resolve(catalog: dict, providerSuffix: Optional[str] = None) -> List[CompactLocation]:
    from base64 import b64decode
    from collections import namedtuple as T
    assert catalog["m_LocatorId"] == "AddressablesMainContentCatalog"

    # m_InstanceProviderData
    # m_SceneProviderData
    # m_ResourceProviderData

    bucket_reader = LittleEndianReader(b64decode(catalog['m_BucketDataString']))
    bucket_item = T("bucket_item", ["dataOffset", "entries"])
    buckets = [bucket_item(
        bucket_reader.readInt(), # offset
        [bucket_reader.readInt() for _ in range(bucket_reader.readInt())] # entry, entry count
    ) for _ in range(bucket_reader.readUInt())] # bucket count
    assert len(bucket_reader.read()) == 0

    m_ProviderIds: List[str] = catalog["m_ProviderIds"]
    if providerSuffix is not None:
        provider_ids = [
            provider_id if provider_id.endswith(providerSuffix) else (provider_id + providerSuffix)
            for provider_id in m_ProviderIds
        ]
    else:
        provider_ids = m_ProviderIds
    
    # m_Keys
    if "m_Keys" in catalog:
        keys = catalog["m_Keys"]
    else:
        assert "m_KeyDataString" in catalog
        key_data_reader = LittleEndianReader(b64decode(catalog['m_KeyDataString']))
        keys = [
            key_data_reader.seek(buckets[i].dataOffset) & 0 or readObject(key_data_reader)
            for i in range(key_data_reader.readUInt()) # key count
        ]

    # public ResourceLocationMap CreateLocator(string providerSuffix = null)
    entry_data_reader = LittleEndianReader(b64decode(catalog['m_EntryDataString']))
    extra_data_reader = LittleEndianReader(b64decode(catalog['m_ExtraDataString']))
    locations = []
    for i in range(entry_data_reader.readUInt()): # entry count
        internal_id_index, provider_index, dependency_key_index, dep_hash, data_index, primary_key_index, resource_type_index = [entry_data_reader.readInt() for _ in range(7)]
        data = None
        if data_index >= 0:
            extra_data_reader.seek(data_index)
            data = readObject(extra_data_reader)
        # AddressablesImpl.cs, public string ResolveInternalId(string id)
        # AddressablesRuntimeProperties.cs, public static string EvaluateString(string inputString)
        internal_id = expand_internal_id(
            catalog["m_InternalIdPrefixes"],
            catalog["m_InternalIds"][internal_id_index]
        )
        locations.append(CompactLocation(
            internal_id,
            provider_ids[provider_index],
            keys[dependency_key_index] if dependency_key_index >= 0 else None,
            data,
            dep_hash,
            keys[primary_key_index],
            catalog['m_resourceTypes'][resource_type_index]
        ))

    for bucket, key in zip(buckets, keys):
        for entry in bucket.entries:
            locations[entry].keys.append(key)

    return locations

def resolve_fast(catalog: dict) -> List[CompactLocation]:
    from base64 import b64decode
    assert catalog["m_LocatorId"] == "AddressablesMainContentCatalog"

    entry_data_reader = LittleEndianReader(b64decode(catalog['m_EntryDataString']))
    extra_data_reader = LittleEndianReader(b64decode(catalog['m_ExtraDataString']))
    locations = []
    for i in range(entry_data_reader.readUInt()):
        internal_id_index, provider_index, dependency_key_index, dep_hash, data_index, primary_key_index, resource_type_index = [entry_data_reader.readInt() for _ in range(7)]
        data = None
        if data_index >= 0:
            extra_data_reader.seek(data_index)
            data = readObject(extra_data_reader)
        internal_id = catalog["m_InternalIds"][internal_id_index]
        parts = internal_id.split("#")
        if len(parts) == 2 and all(c in "0123456789" for c in parts[0]):
            internal_id = catalog["m_InternalIdPrefixes"][int(parts[0])] + parts[1]
        locations.append(CompactLocation(
            internal_id,
            None,
            None,
            data,
            None,
            None,
            None
        ))

    return locations

def resolve_binary(catalog: bytes) -> List[CompactLocation]:
    reader = LittleEndianReader(catalog)
    # public object Deserialize(BinaryStorageBuffer.Reader reader, Type t, uint offset, out uint size)
    assert reader.readUInt() == 0x0de38942, "Invalid header data!!!" # magic: nameof(ContentCatalogData).GetHashCode() = 233015618
    version = reader.readUInt()
    assert version in (1, 2), f"Unsupported catalog version {version}"
    keys_offset, id_offset, instance_provider_offset, scene_provider_offset, init_objects_array_offset = [reader.readUInt() for _ in range(5)]
    if version == 1 and keys_offset == 0x20:
        build_result_hash_offset = 0xFFFFFFFF
    else:
        build_result_hash_offset = reader.readUInt()
    # m_LocatorId
    locator_id = readEncodedString(reader, id_offset, version = version)
    assert locator_id == "AddressablesMainContentCatalog"
    # m_BuildResultHash
    if build_result_hash_offset == 0xFFFFFFFF:
        build_result_hash = readEncodedString(reader, build_result_hash_offset, version = version)
    else:
        build_result_hash = ""
    # m_InstanceProviderData instance_provider_data
    # m_SceneProviderData scene_provider_data
    # m_ResourceProviderData resource_provider_data
    resource_location_cache = {}
    resources = {}
    locations = []

    key_location_offsets = readOffsetArray(reader, offset = keys_offset)
    assert len(key_location_offsets) % 2 == 0
    for key_offset, location_list_offset in zip(
        key_location_offsets[::2],
        key_location_offsets[1::2]
    ):
        key = readObject2(reader, offset = key_offset, version=version)
        location_offsets = readOffsetArray(reader, location_list_offset)
        local_locations = []
        for location_offset in location_offsets:
            # location_offset
            location = CompactLocation.read_binary(reader, offset = location_offset, cache = resource_location_cache, version = version)
            local_locations.append(location)
            locations.append(location)

        resources[key] = local_locations

    return locations


def match_path(path: Optional[str], prefix: str = "", suffix: str = "") -> Optional[str]:
    if path is None or not path.startswith(prefix) or not path.endswith(suffix):
        return None
    return path[len(prefix):]

def compute_size(location: CompactLocation):
    if location.data is None:
        return 0
    if not isinstance(location.data, JsonObject):
        return 0
    return location.data.data.get("m_BundleSize", 0)

def compute_hash(location: CompactLocation):
    if location.data is None:
        return ""
    if not isinstance(location.data, JsonObject):
        return ""
    return location.data.data.get("m_Hash", "")

def handle_catalog(resolved_catalog: List[CompactLocation], prefix: str = "", suffix: str = "", version: Union[int, str] = None) -> AssetList:
    from common.asset_list import Asset, AssetList
    assets = []
    for location in resolved_catalog:
        # print(location)
        path = match_path(location.internal_id, prefix = prefix, suffix = suffix)
        if path is None:
            continue
        assets.append(Asset(name = path, size = compute_size(location), hash = compute_hash(location)))
    return AssetList(assets, version)

def parse_json(catalog: dict, version: Union[int, str] = None, full: bool = False, prefix: str = "", suffix: str = "") -> AssetList:
    from common.asset_list import Asset, AssetList
    resolved_catalog = (resolve if full else resolve_fast)(catalog)
    return handle_catalog(resolved_catalog, prefix = prefix, suffix = suffix, version = version)

def parse_binary(catalog: bytes, version: Union[int, str] = None, prefix: str = "", suffix: str = "") -> AssetList:
    resolved_catalog = resolve_binary(catalog)
    return handle_catalog(resolved_catalog, prefix = prefix, suffix = suffix, version = version)