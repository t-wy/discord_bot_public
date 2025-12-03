# Handle Asset Lists from api.octo-cloud.com or similar services
# Python version implemented by @t-wy: https://github.com/t-wy

from typing import *
from dataclasses import dataclass
from enum import Enum
from .protobuf import int32

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

def build_url(
    urlFormat: str,
    data: Data,
    _type: Union[Literal["assetbundle"], Literal["resources"]]
) -> bytes:
    return urlFormat.format(
        v = data.uploadVersionId,
        type = _type,
        o = data.objectName,
        g = data.generation,
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