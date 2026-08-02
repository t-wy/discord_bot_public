# Handle Asset Lists from api.octo-cloud.com or similar services
# Python version implemented by @t-wy: https://github.com/t-wy

from typing import *
from dataclasses import dataclass
from enum import Enum
from .protobuf import int32, int64, uint32

class State(Enum):
    NONE = 0
    ADD = 1
    UPDATE = 2
    LATEST = 3
    DELETE = 4

@dataclass
class Data:
    id: int32
    filepath: str
    name: str
    size: int32
    crc: int
    priority: int32
    tagid: List[int32]
    dependencies: List[int32]
    state: State
    md5: str
    objectName: str
    generation: int
    uploadVersionId: int32

@dataclass
class Database:
    revision: int32
    assetBundleList: List[Data]
    tagname: List[str]
    resourceList: List[Data]
    urlFormat: str

def loads(data: bytes) -> Database:
    from .protobuf import deserialize
    return deserialize(Database, data)

@dataclass
class DataV2:
    id: int32
    name: str
    size: int32
    crc: uint32
    md5: str
    dependencies: List[int32]
    objectName: str
    addresses: List[str]

@dataclass
class DatabaseV2:
    revision: int32
    assetBundleList: List[DataV2]
    resourceList: List[DataV2]
    urlFormat: str
    rollbackRevisionIds: List[int32]
    rollbackTimes: List[int32]
    serverTime: int64

def loads_v2(data: bytes) -> DatabaseV2:
    from .protobuf import deserialize, loads
    return deserialize(DatabaseV2, data)

def build_url(
    urlFormat: str,
    data: Union[Data, DataV2],
    _type: Union[Literal["assetbundle"], Literal["resources"]]
) -> bytes:
    return urlFormat.format(
        type = _type,
        o = data.objectName,
        v = data.uploadVersionId if isinstance(data, Data) else '',
        g = data.generation if isinstance(data, Data) else '',
    )

async def download(
    urlFormat: str,
    data: Data,
    _type: Union[Literal["assetbundle"], Literal["resources"]]
) -> bytes:
    import common.arequests as arequests
    response = await arequests.get(build_url(urlFormat, data, _type))
    if response.status != 200:
        from common.exception import AssetDownloadException
        raise AssetDownloadException
    return await response.read()

def decrypt(
    content: bytes,
    asset_name: str,
    key: int = 0x9B
) -> bytes:
    # StringToMaskBytes
    # maskString = asset_name.encode()
    maskString = bytes(ord(c) & 0xff for c in asset_name) # non-ascii characters should still be treated as a single character
    maskBytes = [0] * (len(maskString) << 1)
    maskBytes[::2] = maskString
    maskBytes[-1::-2] = [255 - c for c in maskString]
    for b in maskBytes:
        key = (((key & 1) << 7) | (key >> 1)) ^ b
    maskBytes = [c ^ key for c in maskBytes]
    # unobfuscate by keystream
    repeatTimes = 1 + 256 // len(maskBytes)
    return bytes(
        a ^ b for a, b in zip(content[:256], maskBytes * repeatTimes)
    ) + content[256:]