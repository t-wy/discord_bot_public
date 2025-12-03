from common.exception import CustomException
from .byte_reader import LittleEndianReader
import struct, logging
from typing import *

# References:
# https://github.com/Perfare/Il2CppDumper/blob/master/Il2CppDumper/Il2Cpp/Metadata.cs
# https://github.com/Unity-Technologies/DesktopSamples/blob/master/UniversalWindowsPlatformSamples/CSharpProjectExample/bin/Il2CppOutputProject/IL2CPP/libil2cpp/vm/GlobalMetadataFileInternals.h
# Python version implemented by @t-wy: https://github.com/t-wy

"""
MIT License

Copyright (c) 2025 t-wy
Copyright (c) 2022 Unity Technologies
Copyright (c) 2016 Perfare

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

class InvalidGlobalMetadataException(CustomException):
    def __init__(self, message: str):
        super().__init__(message)

class ReprClass:
    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join("{}={}".format(k, v) for k, v in self.__dict__.items())
        )

class GlobalMetadata(ReprClass):
    class Il2CppGlobalMetadataHeader(ReprClass):
        __slots__ = (
            "sanity",
            "version",
            "stringLiteralOffset",
            "stringLiteralSize",
            "stringLiteralDataOffset",
            "stringLiteralDataSize",
            "stringOffset",
            "stringSize",
            "eventsOffset",
            "eventsSize",
            "propertiesOffset",
            "propertiesSize",
            "methodsOffset",
            "methodsSize",
            "parameterDefaultValuesOffset",
            "parameterDefaultValuesSize",
            "fieldDefaultValuesOffset",
            "fieldDefaultValuesSize",
            "fieldAndParameterDefaultValueDataOffset",
            "fieldAndParameterDefaultValueDataSize",
            "fieldMarshaledSizesOffset",
            "fieldMarshaledSizesSize",
            "parametersOffset",
            "parametersSize",
            "fieldsOffset",
            "fieldsSize",
            "genericParametersOffset",
            "genericParametersSize",
            "genericParameterConstraintsOffset",
            "genericParameterConstraintsSize",
            "genericContainersOffset",
            "genericContainersSize",
            "nestedTypesOffset",
            "nestedTypesSize",
            "interfacesOffset",
            "interfacesSize",
            "vtableMethodsOffset",
            "vtableMethodsSize",
            "interfaceOffsetsOffset",
            "interfaceOffsetsSize",
            "typeDefinitionsOffset",
            "typeDefinitionsSize",
            "rgctxEntriesOffset",
            "rgctxEntriesCount",
            "imagesOffset",
            "imagesSize",
            "assembliesOffset",
            "assembliesSize",
            "metadataUsageListsOffset",
            "metadataUsageListsCount",
            "metadataUsagePairsOffset",
            "metadataUsagePairsCount",
            "fieldRefsOffset",
            "fieldRefsSize",
            "referencedAssembliesOffset",
            "referencedAssembliesSize",
            "attributesInfoOffset",
            "attributesInfoCount",
            "attributeTypesOffset",
            "attributeTypesCount",
            "attributeDataOffset",
            "attributeDataSize",
            "attributeDataRangeOffset",
            "attributeDataRangeSize",
            "unresolvedVirtualCallParameterTypesOffset",
            "unresolvedVirtualCallParameterTypesSize",
            "unresolvedVirtualCallParameterRangesOffset",
            "unresolvedVirtualCallParameterRangesSize",
            "windowsRuntimeTypeNamesOffset",
            "windowsRuntimeTypeNamesSize",
            "windowsRuntimeStringsOffset",
            "windowsRuntimeStringsSize",
            "exportedTypeDefinitionsOffset",
            "exportedTypeDefinitionsSize",
        )
        def __init__(self, reader: LittleEndianReader, version: float = ...):
            (
                self.sanity,
                self.version,
                self.stringLiteralOffset, # string data for managed code
                self.stringLiteralSize,
                self.stringLiteralDataOffset,
                self.stringLiteralDataSize,
                self.stringOffset, # string data for metadata
                self.stringSize,
                self.eventsOffset, # Il2CppEventDefinition
                self.eventsSize,
                self.propertiesOffset, # Il2CppPropertyDefinition
                self.propertiesSize,
                self.methodsOffset, # Il2CppMethodDefinition
                self.methodsSize,
                self.parameterDefaultValuesOffset, # Il2CppParameterDefaultValue
                self.parameterDefaultValuesSize,
                self.fieldDefaultValuesOffset, # Il2CppFieldDefaultValue
                self.fieldDefaultValuesSize,
                self.fieldAndParameterDefaultValueDataOffset, # uint8_t
                self.fieldAndParameterDefaultValueDataSize,
                self.fieldMarshaledSizesOffset, # Il2CppFieldMarshaledSize
                self.fieldMarshaledSizesSize,
                self.parametersOffset, # Il2CppParameterDefinition
                self.parametersSize,
                self.fieldsOffset, # Il2CppFieldDefinition
                self.fieldsSize,
                self.genericParametersOffset, # Il2CppGenericParameter
                self.genericParametersSize,
                self.genericParameterConstraintsOffset, # TypeIndex
                self.genericParameterConstraintsSize,
                self.genericContainersOffset, # Il2CppGenericContainer
                self.genericContainersSize,
                self.nestedTypesOffset, # TypeDefinitionIndex
                self.nestedTypesSize,
                self.interfacesOffset, # TypeIndex
                self.interfacesSize,
                self.vtableMethodsOffset, # EncodedMethodIndex
                self.vtableMethodsSize,
                self.interfaceOffsetsOffset, # Il2CppInterfaceOffsetPair
                self.interfaceOffsetsSize,
                self.typeDefinitionsOffset, # Il2CppTypeDefinition
                self.typeDefinitionsSize,
            ) = struct.unpack("<" + "Ii" * 10 + "ii" + "Ii" * 8 + "ii" + "Ii", reader.read(168)) # I: uint32_t, i: int32_t
            if version is not ...:
                self.version = version
            if self.version <= 24.1:
                self.rgctxEntriesOffset = reader.readUInt() # Il2CppRGCTXDefinition
                self.rgctxEntriesCount = reader.readInt()
            self.imagesOffset = reader.readUInt() # Il2CppImageDefinition
            self.imagesSize = reader.readInt()
            self.assembliesOffset = reader.readUInt() # Il2CppAssemblyDefinition
            self.assembliesSize = reader.readInt()
            if 19 <= self.version <= 24.5:
                self.metadataUsageListsOffset = reader.readUInt() # Il2CppMetadataUsageList
                self.metadataUsageListsCount = reader.readInt()
                self.metadataUsagePairsOffset = reader.readUInt() # Il2CppMetadataUsagePair
                self.metadataUsagePairsCount = reader.readInt()
            if 19 <= self.version:
                self.fieldRefsOffset = reader.readUInt() # Il2CppFieldRef
                self.fieldRefsSize = reader.readInt()
            if 20 <= self.version:
                self.referencedAssembliesOffset = reader.readInt() # int32_t
                self.referencedAssembliesSize = reader.readInt()
            if 21 <= self.version <= 27.2:
                self.attributesInfoOffset = reader.readUInt() # Il2CppCustomAttributeTypeRange
                self.attributesInfoCount = reader.readInt()
                self.attributeTypesOffset = reader.readUInt() # TypeIndex
                self.attributeTypesCount = reader.readInt()
            if 29 <= self.version:
                self.attributeDataOffset = reader.readUInt()
                self.attributeDataSize = reader.readInt()
                self.attributeDataRangeOffset = reader.readUInt()
                self.attributeDataRangeSize = reader.readInt()
            if 22 <= self.version:
                self.unresolvedVirtualCallParameterTypesOffset = reader.readInt() # TypeIndex
                self.unresolvedVirtualCallParameterTypesSize = reader.readInt()
                self.unresolvedVirtualCallParameterRangesOffset = reader.readInt() # Il2CppRange
                self.unresolvedVirtualCallParameterRangesSize = reader.readInt()
            if 23 <= self.version:
                self.windowsRuntimeTypeNamesOffset = reader.readInt() # Il2CppWindowsRuntimeTypeNamePair
                self.windowsRuntimeTypeNamesSize = reader.readInt()
            if 27 <= self.version:
                self.windowsRuntimeStringsOffset = reader.readInt() # const char*
                self.windowsRuntimeStringsSize = reader.readInt()
            if 24 <= self.version:
                self.exportedTypeDefinitionsOffset = reader.readInt() # TypeDefinitionIndex
                self.exportedTypeDefinitionsSize = reader.readInt()

    class Il2CppAssemblyDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.imageIndex = reader.readInt()
            if 24.1 <= parent.header.version:
                self.token = reader.readUInt()
            if parent.header.version <= 24:
                self.customAttributeIndex = reader.readInt()
            else:
                self.customAttributeIndex = 0
            if 20 <= parent.header.version:
                self.referencedAssemblyStart = reader.readInt()
            if 20 <= parent.header.version:
                self.referencedAssemblyCount = reader.readInt()
            self.aname = GlobalMetadata.Il2CppAssemblyNameDefinition(reader, parent)

    class Il2CppAssemblyNameDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.name: str = ...
            self.nameIndex = reader.readUInt()
            self.cultureIndex = reader.readUInt()
            if parent.header.version <= 24.3:
                self.hashValueIndex = reader.readInt()
            self.publicKeyIndex = reader.readUInt()
            self.hash_alg = reader.readUInt()
            self.hash_len = reader.readInt()
            self.flags = reader.readUInt()
            self.major = reader.readInt()
            self.minor = reader.readInt()
            self.build = reader.readInt()
            self.revision = reader.readInt()
            self.public_key_token = reader.readBytes(8)

    class Il2CppImageDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.name: str = ...
            self.nameIndex = reader.readUInt()
            self.assemblyIndex = reader.readInt()

            self.typeStart = reader.readInt()
            self.typeCount = reader.readUInt()

            if 24 <= parent.header.version:
                self.exportedTypeStart = reader.readInt()
                self.exportedTypeCount = reader.readUInt()

            self.entryPointIndex = reader.readInt()
            if 19 <= parent.header.version:
                self.token = reader.readUInt()

            if 24.1 <= parent.header.version:
                self.customAttributeStart = reader.readInt()
                self.customAttributeCount = reader.readUInt()

    class Il2CppTypeDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.name: str = ...
            self.nameIndex = reader.readUInt()
            self.namespace: str = ...
            self.namespaceIndex = reader.readUInt()
            if parent.header.version <= 24:
                self.customAttributeIndex = reader.readInt()
            else:
                self.customAttributeIndex = 0
            self.byvalTypeIndex = reader.readInt()
            if parent.header.version <= 24.5:
                self.byrefTypeIndex = reader.readInt()

            self.declaringTypeIndex = reader.readInt()
            self.parentIndex = reader.readInt()
            self.elementTypeIndex = reader.readInt() # we can probably remove this one. Only used for enums

            if parent.header.version <= 24.1:
                self.rgctxStartIndex = reader.readInt()
            if parent.header.version <= 24.1:
                self.rgctxCount = reader.readInt()

            self.genericContainerIndex = reader.readInt()

            if parent.header.version <= 22:
                self.delegateWrapperFromManagedToNativeIndex = reader.readInt()
            if parent.header.version <= 22:
                self.marshalingFunctionsIndex = reader.readInt()
            if 21 <= parent.header.version <= 22:
                self.ccwFunctionIndex = reader.readInt()
            if 21 <= parent.header.version <= 22:
                self.guidIndex = reader.readInt()

            self.flags = reader.readUInt()

            self.fieldStart = reader.readInt()
            self.methodStart = reader.readInt()
            self.eventStart = reader.readInt()
            self.propertyStart = reader.readInt()
            self.nestedTypesStart = reader.readInt()
            self.interfacesStart = reader.readInt()
            self.vtableStart = reader.readInt()
            self.interfaceOffsetsStart = reader.readInt()

            self.method_count = reader.readUShort()
            self.property_count = reader.readUShort()
            self.field_count = reader.readUShort()
            self.event_count = reader.readUShort()
            self.nested_type_count = reader.readUShort()
            self.vtable_count = reader.readUShort()
            self.interfaces_count = reader.readUShort()
            self.interface_offsets_count = reader.readUShort()

            # bitfield to portably encode boolean values as single bits
            # 01 - valuetype
            # 02 - enumtype
            # 03 - has_finalize
            # 04 - has_cctor
            # 05 - is_blittable
            # 06 - is_import_or_windows_runtime
            # 07-10 - One of nine possible PackingSize values (0, 1, 2, 4, 8, 16, 32, 64, or 128)
            # 11 - PackingSize is default
            # 12 - ClassSize is default
            # 13-16 - One of nine possible PackingSize values (0, 1, 2, 4, 8, 16, 32, 64, or 128) - the specified packing size (even for explicit layouts)
            self.bitfield = reader.readUInt()
            if 19 <= parent.header.version:
                self.token = reader.readUInt()

        @property
        def IsValueType(self) -> bool:
            return (self.bitfield & 0x1) == 1
        
        @property
        def IsEnum(self) -> bool:
            return ((self.bitfield >> 1) & 0x1) == 1

    class Il2CppMethodDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.name: str = ...
            self.nameIndex = reader.readUInt()
            self.declaringType = reader.readInt()
            self.returnType = reader.readInt()
            if 31 <= parent.header.version:
                self.returnParameterToken = reader.readInt()
            self.parameterStart = reader.readInt()
            if parent.header.version <= 24:
                self.customAttributeIndex = reader.readInt()
            else:
                self.customAttributeIndex = 0
            self.genericContainerIndex = reader.readInt()
            if parent.header.version <= 24.1:
                self.methodIndex = reader.readInt()
            if parent.header.version <= 24.1:
                self.invokerIndex = reader.readInt()
            if parent.header.version <= 24.1:
                self.delegateWrapperIndex = reader.readInt()
            if parent.header.version <= 24.1:
                self.rgctxStartIndex = reader.readInt()
            if parent.header.version <= 24.1:
                self.rgctxCount = reader.readInt()
            self.token = reader.readUInt()
            self.flags = reader.readUShort()
            self.iflags = reader.readUShort()
            self.slot = reader.readUShort()
            self.parameterCount = reader.readUShort()

    class Il2CppParameterDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.name: str = ...
            self.nameIndex = reader.readUInt()
            self.token = reader.readUInt()
            if parent.header.version <= 24:
                self.customAttributeIndex = reader.readInt()
            else:
                self.customAttributeIndex = 0
            self.typeIndex = reader.readInt()

    class Il2CppFieldDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.name: str = ...
            self.nameIndex = reader.readUInt()
            self.typeIndex = reader.readInt()
            if parent.header.version <= 24:
                self.customAttributeIndex = reader.readInt()
            else:
                self.customAttributeIndex = 0
            if 19 <= parent.header.version:
                self.token = reader.readUInt()

    class Il2CppFieldDefaultValue(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.fieldIndex = reader.readInt()
            self.typeIndex = reader.readInt()
            self.dataIndex = reader.readInt()

    class Il2CppPropertyDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.name: str = ...
            self.nameIndex = reader.readUInt()
            self.get = reader.readInt()
            self.set = reader.readInt()
            self.attrs = reader.readUInt()
            if parent.header.version <= 24:
                self.customAttributeIndex = reader.readInt()
            else:
                self.customAttributeIndex = 0
            if 19 <= parent.header.version:
                self.token = reader.readUInt()

    class Il2CppCustomAttributeTypeRange(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            if 24.1 <= parent.header.version:
                self.token = reader.readUInt()
            self.start = reader.readInt()
            self.count = reader.readInt()

    class Il2CppMetadataUsageList(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.start = reader.readUInt()
            self.count = reader.readUInt()

    class Il2CppMetadataUsagePair(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.destinationIndex = reader.readUInt()
            self.encodedSourceIndex = reader.readUInt()

    class Il2CppStringLiteral(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.length = reader.readUInt()
            self.dataIndex = reader.readInt()
            self.value = ...

    class Il2CppParameterDefaultValue(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.parameterIndex = reader.readInt()
            self.typeIndex = reader.readInt()
            self.dataIndex = reader.readInt()

    class Il2CppEventDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.name: str = ...
            self.nameIndex = reader.readUInt()
            self.typeIndex = reader.readInt()
            self.add = reader.readInt()
            self.remove = reader.readInt()
            setattr(self, 'raise', reader.readInt())
            if parent.header.version <= 24:
                self.customAttributeIndex = reader.readInt()
            else:
                self.customAttributeIndex = 0
            if 19 <= parent.header.version:
                self.token = reader.readUInt()

    class Il2CppGenericContainer(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            # index of the generic type definition or the generic method definition corresponding to this container
            self.ownerIndex = reader.readInt() # either index into Il2CppClass metadata array or Il2CppMethodDefinition array
            self.type_argc = reader.readInt()
            # If true, we're a generic method, otherwise a generic type definition.
            self.is_method = reader.readInt()
            # Our type parameters.
            self.genericParameterStart = reader.readInt()

    class Il2CppFieldRef(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.typeIndex = reader.readInt()
            self.fieldIndex = reader.readInt() # local offset into type fields

    class Il2CppGenericParameter(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.ownerIndex = reader.readInt() # Type or method this parameter was defined in.
            self.name: str = ...
            self.nameIndex = reader.readUInt()
            self.constraintsStart = reader.readShort()
            self.constraintsCount = reader.readShort()
            self.num = reader.readUShort()
            self.flags = reader.readUShort()

    from enum import Enum
    class Il2CppRGCTXDataType(Enum):
        from enum import auto
        IL2CPP_RGCTX_DATA_INVALID = auto()
        IL2CPP_RGCTX_DATA_TYPE = auto()
        IL2CPP_RGCTX_DATA_CLASS = auto()
        IL2CPP_RGCTX_DATA_METHOD = auto()
        IL2CPP_RGCTX_DATA_ARRAY = auto()
        IL2CPP_RGCTX_DATA_CONSTRAINED = auto()

    class Il2CppRGCTXDefinitionData(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.rgctxDataDummy = reader.readInt()
            self.methodIndex = reader.readInt()
            self.typeIndex = reader.readInt()

    class Il2CppRGCTXDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            if parent.header.version <= 27.1:
                self.type = parent.Il2CppRGCTXDataType(reader.readInt())
            if 29 <= parent.header.version:
                self.type = parent.Il2CppRGCTXDataType(reader.readULong())
            if parent.header.version <= 27.1:
                self.data = parent.Il2CppRGCTXDefinitionData(reader, parent)
            if 27.2 <= parent.header.version:
                self._data = reader.readULong()

    class Il2CppMetadataUsage(Enum):
        from enum import auto
        kIl2CppMetadataUsageInvalid = auto()
        kIl2CppMetadataUsageTypeInfo = auto()
        kIl2CppMetadataUsageIl2CppType = auto()
        kIl2CppMetadataUsageMethodDef = auto()
        kIl2CppMetadataUsageFieldInfo = auto()
        kIl2CppMetadataUsageStringLiteral = auto()
        kIl2CppMetadataUsageMethodRef = auto()

    class Il2CppCustomAttributeDataRange(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.token = reader.readUInt()
            self.startOffset = reader.readUInt()

    @staticmethod
    def loads(data: bytes) -> 'GlobalMetadata':
        return GlobalMetadata(LittleEndianReader(data))

    def __init__(self, reader: LittleEndianReader):
        self.reader = reader
        def load_list(_type: type, offset: int, size: int) -> list: # _type
            result = []
            reader.seek(offset)
            while reader.tell() < offset + size:
                result.append(_type(reader, self))
            return result
        def load_type(_type: type, offset: int, size: int) -> list: # _type
            result = []
            reader.seek(offset)
            while reader.tell() < offset + size:
                result.append(_type())
            return result
        def load_str(offset: int, size: int) -> str:
            reader.seek(offset)
            return reader.read(size).decode()
        def resolve_name(cls: Any):
            # assert hasattr(cls, "nameIndex")
            reader.seek(self.header.stringOffset + cls.nameIndex)
            cls.name = reader.readNullString()
            if hasattr(cls, "namespaceIndex"):
                reader.seek(self.header.stringOffset + cls.namespaceIndex)
                cls.namespace = reader.readNullString()
        def resolve_raw(_from: int, _to: int):
            reader.seek(_from)
            return reader.read(_to - _from)
        # il2cpp::vm::GlobalMetadata::Initialize
        # GlobalMetadataFileInternals.h
        self.header = GlobalMetadata.Il2CppGlobalMetadataHeader(reader)
        if self.header.sanity != 0xFAB11BAF: # sanity
            raise InvalidGlobalMetadataException("Magic number not match.")
        if not (16 <= self.header.version <= 31):
            raise InvalidGlobalMetadataException("Metadata version not supported.")
        # Differentiate version 24
        if self.header.version == 24:
            if self.header.stringLiteralDataOffset == 264:
                # exclude rgctxEntries
                reader.seek(0)
                self.header = GlobalMetadata.Il2CppGlobalMetadataHeader(reader, 24.2)
            else:
                self.imageDefinitions: List[GlobalMetadata.Il2CppImageDefinition] = load_list(GlobalMetadata.Il2CppImageDefinition, self.header.imagesOffset, self.header.imagesSize)
                if any(entry.token != 1 for entry in self.imageDefinitions):
                    self.header.version = 24.1
        self.imageDefinitions: List[GlobalMetadata.Il2CppImageDefinition] = load_list(GlobalMetadata.Il2CppImageDefinition, self.header.imagesOffset, self.header.imagesSize)
        for temp in self.imageDefinitions:
            resolve_name(temp) # All those *.dll
        if self.header.version == 24.2 and self.header.assembliesSize < len(self.imageDefinitions) * 68:
            self.header.version = 24.4
        fake_24_4 = self.header.version == 24.1 and self.header.assembliesSize == len(self.imageDefinitions) * 64
        if fake_24_4:
            self.header.version = 24.4
        self.assemblyDefinitions: List[GlobalMetadata.Il2CppAssemblyDefinition] = load_list(GlobalMetadata.Il2CppAssemblyDefinition,self.header.assembliesOffset, self.header.assembliesSize)
        for temp in self.assemblyDefinitions:
            resolve_name(temp.aname)
            logging.debug(f"Il2CppAssemblyDefinition {temp.aname.name}")
        if fake_24_4:
            self.header.version = 24.1
        self.typeDefinitions: List[GlobalMetadata.Il2CppTypeDefinition] = load_list(GlobalMetadata.Il2CppTypeDefinition,self.header.typeDefinitionsOffset, self.header.typeDefinitionsSize)
        for temp in self.typeDefinitions:
            resolve_name(temp)
            logging.debug(f"Il2CppTypeDefinition {temp.name}")
        self.methodDefinitions: List[GlobalMetadata.Il2CppMethodDefinition] = load_list(GlobalMetadata.Il2CppMethodDefinition,self.header.methodsOffset, self.header.methodsSize)
        for temp in self.methodDefinitions:
            resolve_name(temp)
            logging.debug(f"Il2CppMethodDefinition {temp.name}")
        self.parameterDefinitions: List[GlobalMetadata.Il2CppParameterDefinition] = load_list(GlobalMetadata.Il2CppParameterDefinition,self.header.parametersOffset, self.header.parametersSize)
        for temp in self.parameterDefinitions:
            resolve_name(temp)
            logging.debug(f"Il2CppParameterDefinition {temp.name}")
        self.fieldDefinitions: List[GlobalMetadata.Il2CppFieldDefinition] = load_list(GlobalMetadata.Il2CppFieldDefinition,self.header.fieldsOffset, self.header.fieldsSize)
        for temp in self.fieldDefinitions:
            resolve_name(temp)
            logging.debug(f"Il2CppFieldDefinition {temp.name}")

        fieldDefaultValues: List[GlobalMetadata.Il2CppFieldDefaultValue] = load_list(GlobalMetadata.Il2CppFieldDefaultValue, self.header.fieldDefaultValuesOffset, self.header.fieldDefaultValuesSize)
        self.fieldDefaultValues = {entry.fieldIndex : entry for entry in fieldDefaultValues}

        parameterDefaultValues: List[GlobalMetadata.Il2CppParameterDefaultValue] = load_list(GlobalMetadata.Il2CppParameterDefaultValue, self.header.parameterDefaultValuesOffset, self.header.parameterDefaultValuesSize)
        self.parameterDefaultValues = {entry.parameterIndex : entry for entry in parameterDefaultValues}
    
        self.propertyDefinitions: List[GlobalMetadata.Il2CppPropertyDefinition] = load_list(GlobalMetadata.Il2CppPropertyDefinition, self.header.propertiesOffset, self.header.propertiesSize)
        for temp in self.propertyDefinitions:
            resolve_name(temp)
            logging.debug(f"Il2CppPropertyDefinition {temp.name}")
        self.interfaceIndices = load_type(reader.readInt, self.header.interfaceOffsetsOffset, self.header.interfaceOffsetsSize)
        self.nestedTypeIndices = load_type(reader.readInt, self.header.nestedTypesOffset, self.header.nestedTypesSize)
        self.eventDefinitions: List[GlobalMetadata.Il2CppEventDefinition] = load_list(GlobalMetadata.Il2CppEventDefinition, self.header.eventsOffset, self.header.eventsSize)
        for temp in self.eventDefinitions:
            resolve_name(temp)
            logging.debug(f"Il2CppEventDefinition {temp.name}")
        self.genericContainers: List[GlobalMetadata.Il2CppGenericContainer] = load_list(GlobalMetadata.Il2CppGenericContainer, self.header.genericContainersOffset, self.header.genericContainersSize)
        self.genericParameters: List[GlobalMetadata.Il2CppGenericParameter] = load_list(GlobalMetadata.Il2CppGenericParameter, self.header.genericParametersOffset, self.header.genericParametersSize)
        for temp in self.genericParameters:
            resolve_name(temp)
            logging.debug(f"Il2CppGenericParameter {temp.name}")
        self.constraintIndices = load_type(reader.readInt, self.header.genericParameterConstraintsOffset, self.header.genericParameterConstraintsSize)
        self.vtableMethods = load_type(reader.readUInt, self.header.vtableMethodsOffset, self.header.vtableMethodsSize)
        self.stringLiterals: List[GlobalMetadata.Il2CppStringLiteral] = load_list(GlobalMetadata.Il2CppStringLiteral, self.header.stringLiteralOffset, self.header.stringLiteralSize)
        for entry in self.stringLiterals:
            entry.value = load_str(self.header.stringLiteralDataOffset + entry.dataIndex, entry.length)
    
        if 16 <= self.header.version:
            self.fieldRefs: List[GlobalMetadata.Il2CppFieldRef] = load_list(GlobalMetadata.Il2CppFieldRef,self.header.fieldRefsOffset, self.header.fieldRefsSize)
            if self.header.version < 27:
                self.metadataUsageLists: List[GlobalMetadata.Il2CppMetadataUsageList] = load_list(GlobalMetadata.Il2CppMetadataUsageList, self.header.metadataUsageListsOffset, self.header.metadataUsageListsCount)
                self.metadataUsagePairs: List[GlobalMetadata.Il2CppMetadataUsagePair] = load_list(GlobalMetadata.Il2CppMetadataUsagePair, self.header.metadataUsagePairsOffset, self.header.metadataUsagePairsCount)
                # process_metadata_usage
                self.metadataUsageDict = {GlobalMetadata.Il2CppMetadataUsage(i): {} for i in range(6)}
                for entry in self.metadataUsageLists:
                    for i in range(entry.count):
                        offset = entry.start + i
                        if offset >= len(self.metadataUsagePairs):
                            continue
                        metadataUsagePair: GlobalMetadata.Il2CppMetadataUsagePair = self.metadataUsagePairs[offset]
                        usage = GlobalMetadata.Il2CppMetadataUsage(((metadataUsagePair.encodedSourceIndex) & 0xE0000000) >> 29)
                        decodedIndex = (metadataUsagePair.encodedSourceIndex & 0x1FFFFFFF) >> (self.header.version >= 27)
                        self.metadataUsageDict[usage][metadataUsagePair.destinationIndex] = decodedIndex
                self.metadataUsagesCount = max(key for key in self.metadataUsageDict.keys() if len(self.metadataUsageDict[key]) > 0) + 1
            else:
                self.metadataUsagesCount = 0
        if 20 < self.header.version < 29:
            self.attributeTypeRanges: List[GlobalMetadata.Il2CppCustomAttributeTypeRange] = load_list(GlobalMetadata.Il2CppCustomAttributeTypeRange, self.header.attributesInfoOffset, self.header.attributesInfoCount)
            self.attributeTypes = load_type(reader.readInt, self.header.attributeTypesOffset, self.header.attributeTypesCount)
        if self.header.version >= 29:
            self.attributeDataRanges: List[GlobalMetadata.Il2CppCustomAttributeDataRange] = load_list(GlobalMetadata.Il2CppCustomAttributeDataRange, self.header.attributeDataRangeOffset, self.header.attributeDataRangeSize)
            self.attributeDataSlice = []
            for i in range(len(self.attributeDataRanges) - 1):
                length = self.attributeDataRanges[i + 1].startOffset - self.attributeDataRanges[i].startOffset
                reader.seek(self.header.attributeDataOffset + self.attributeDataRanges[i].startOffset)
                self.attributeDataSlice.append(reader.readBytes(length))
        if self.header.version > 24:
            self.attributeTypeRangesDict = {}
            entry: GlobalMetadata.Il2CppImageDefinition
            for entry in self.imageDefinitions:
                temp_range = range(entry.customAttributeStart, entry.customAttributeStart + entry.customAttributeCount)
                if self.header.version >= 29:
                    self.attributeTypeRangesDict[entry.nameIndex] = {
                        self.attributeDataRanges[i].token: i
                    for i in temp_range}
                else:
                    self.attributeTypeRangesDict[entry.nameIndex] = {
                        self.attributeTypeRanges[i].token: i
                    for i in temp_range}
        if self.header.version <= 24.1:
            self.rgctxEntries: List[GlobalMetadata.Il2CppRGCTXDefinition] = load_list(GlobalMetadata.Il2CppRGCTXDefinition, self.header.rgctxEntriesOffset, self.header.rgctxEntriesCount)
        # resolve default values
        dataIndices = sorted(set([
            field.dataIndex for field in fieldDefaultValues
            if field.dataIndex != -1
        ] + [
            field.dataIndex for field in parameterDefaultValues
            if field.dataIndex != -1
        ])) + [ self.header.fieldAndParameterDefaultValueDataSize ]
        self.fieldDefaultValuesRaw = {
            dataIndices[i]:
            resolve_raw(
                self.header.fieldAndParameterDefaultValueDataOffset + dataIndices[i],
                self.header.fieldAndParameterDefaultValueDataOffset + dataIndices[i + 1],
            )
            for i in range(len(dataIndices) - 1)
        }