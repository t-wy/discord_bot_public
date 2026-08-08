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
        if hasattr(self, "__slots__"):
            return "{}({})".format(
                self.__class__.__name__,
                ", ".join("{}={}".format(k, getattr(self, k)) for k in self.__slots__)
            )
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join("{}={}".format(k, v) for k, v in self.__dict__.items())
        )

def read_index(reader: LittleEndianReader, size: int) -> int:
    if size == 1:
        temp, value = 255, reader.readByte()
    elif size == 2:
        temp, value = 65535, reader.readUShort()
    elif size == 4:
        temp, value = 4294967295, reader.readUInt()
    else:
        assert False, f"Unsupported index size: {size}"
    if value == temp:
        return -1
    return value
        
class GlobalMetadata(ReprClass):
    class Il2CppSectionMetadata(ReprClass):
        __slots__ = (
            "offset",
            "size",
            "count",
        )
        def __init__(self, reader: LittleEndianReader, version: float, min_version: float = 0, max_version: float = 5e9):
            # introduced since 39.0 (should be 38.0+, not confirmed)
            if min_version <= version <= max_version:
                if version >= 38.0:
                    self.offset = reader.readInt()
                    self.size = reader.readInt()
                    self.count = reader.readInt()
                else:
                    self.offset = reader.readUInt()
                    self.size = reader.readInt()
                    self.count: int = ...
            else:
                self.offset: int = ...
                self.size: int = ...
                self.count: int = ...

    class Il2CppGlobalMetadataHeader(ReprClass):
        __slots__ = (
            "sanity",
            "version",
            "stringLiterals",
            "stringLiteralData",
            "strings",
            "events",
            "properties",
            "methods",
            "parameterDefaultValues",
            "fieldDefaultValues",
            "fieldAndParameterDefaultValueData",
            "fieldMarshaledSizes",
            "parameters",
            "fields",
            "genericParameters",
            "genericParameterConstraints",
            "genericContainers",
            "nestedTypes",
            "interfaces",
            "vtableMethods",
            "interfaceOffsets",
            "typeDefinitions",
            "rgctxEntries",
            "images",
            "assemblies",
            "metadataUsageLists",
            "metadataUsagePairs",
            "fieldRefs",
            "referencedAssemblies",
            "attributesInfo",
            "attributeTypes",
            "attributeData",
            "attributeDataRange",
            "unresolvedVirtualCallParameterTypes",
            "unresolvedVirtualCallParameterRanges",
            "windowsRuntimeTypeNames",
            "windowsRuntimeStrings",
            "exportedTypeDefinitions",
        )
        def __init__(self, reader: LittleEndianReader, version: float = ...):
            self.sanity = reader.readUInt()
            self.version = reader.readInt()
            # override version if specified
            if version is not ...:
                self.version = version
            (
                self.stringLiterals, # string data for managed code
                self.stringLiteralData,
                self.strings, # string data for metadat
                self.events, # Il2CppEventDefinition
                self.properties, # Il2CppPropertyDefinition
                self.methods, # Il2CppMethodDefinition
                self.parameterDefaultValues, # Il2CppParameterDefaultValue
                self.fieldDefaultValues, # Il2CppFieldDefaultValue
                self.fieldAndParameterDefaultValueData,
                self.fieldMarshaledSizes, # Il2CppFieldMarshaledSize, int, int actually
                self.parameters, # Il2CppParameterDefinition
                self.fields, # Il2CppFieldDefinition
                self.genericParameters, # Il2CppGenericParameter
                self.genericParameterConstraints, # TypeIndex
                self.genericContainers, # Il2CppGenericContainer
                self.nestedTypes, # Il2CppTypeDefinitionIndex
                self.interfaces, # TypeIndex
                self.vtableMethods, # EncodedMethodIndex
                self.interfaceOffsets, # Il2CppInterfaceOffsetPair, int, int actually
                self.typeDefinitions,
            ) = [
                GlobalMetadata.Il2CppSectionMetadata(reader, self.version)
                for _ in range(20)
            ]
            self.rgctxEntries = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, max_version = 24.1) # Il2CppRGCTXDefinition
            self.images = GlobalMetadata.Il2CppSectionMetadata(reader, self.version) # Il2CppImageDefinition
            self.assemblies = GlobalMetadata.Il2CppSectionMetadata(reader, self.version) # Il2CppAssemblyDefinition
            self.metadataUsageLists = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 19, max_version = 24.5) # Il2CppMetadataUsageList
            self.metadataUsagePairs = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 19, max_version = 24.5) # Il2CppMetadataUsagePair
            self.fieldRefs = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 19) # Il2CppFieldRef
            self.referencedAssemblies = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 20) # int32_t
            self.attributesInfo = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 21, max_version = 27.2) # Il2CppCustomAttributeTypeRange
            self.attributeTypes = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 21, max_version = 27.2) # TypeIndex
            self.attributeData = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 29)
            self.attributeDataRange = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 29)
            self.unresolvedVirtualCallParameterTypes = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 22) # TypeIndex
            self.unresolvedVirtualCallParameterRanges = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 22) # Il2CppRange
            self.windowsRuntimeTypeNames = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 23) # Il2CppWindowsRuntimeTypeNamePair
            self.windowsRuntimeStrings = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 27) # const char*
            self.exportedTypeDefinitions = GlobalMetadata.Il2CppSectionMetadata(reader, self.version, min_version = 24)
        
        # backward-compatible
        @property
        def stringLiteralOffset(self):
            return self.stringLiterals.offset
        @property
        def stringLiteralSize(self):
            return self.stringLiterals.size
        @property
        def stringLiteralDataOffset(self):
            return self.stringLiteralData.offset
        @property
        def stringLiteralDataSize(self):
            return self.stringLiteralData.size
        @property
        def stringOffset(self):
            return self.strings.offset
        @property
        def stringSize(self):
            return self.strings.size
        @property
        def eventsOffset(self):
            return self.events.offset
        @property
        def eventsSize(self):
            return self.events.size
        @property
        def propertiesOffset(self):
            return self.properties.offset
        @property
        def propertiesSize(self):
            return self.properties.size
        @property
        def methodsOffset(self):
            return self.methods.offset
        @property
        def methodsSize(self):
            return self.methods.size
        @property
        def parameterDefaultValuesOffset(self):
            return self.parameterDefaultValues.offset
        @property
        def parameterDefaultValuesSize(self):
            return self.parameterDefaultValues.size
        @property
        def fieldDefaultValuesOffset(self):
            return self.fieldDefaultValues.offset
        @property
        def fieldDefaultValuesSize(self):
            return self.fieldDefaultValues.size
        @property
        def fieldAndParameterDefaultValueDataOffset(self):
            return self.fieldAndParameterDefaultValueData.offset
        @property
        def fieldAndParameterDefaultValueDataSize(self):
            return self.fieldAndParameterDefaultValueData.size
        @property
        def fieldMarshaledSizesOffset(self):
            return self.fieldMarshaledSizes.offset
        @property
        def fieldMarshaledSizesSize(self):
            return self.fieldMarshaledSizes.size
        @property
        def parametersOffset(self):
            return self.parameters.offset
        @property
        def parametersSize(self):                        
            return self.parameters.size
        @property
        def fieldsOffset(self):
            return self.fields.offset
        @property
        def fieldsSize(self):
            return self.fields.size
        @property
        def genericParametersOffset(self):
            return self.genericParameters.offset
        @property
        def genericParametersSize(self):
            return self.genericParameters.size
        @property
        def genericParameterConstraintsOffset(self):
            return self.genericParameterConstraints.offset
        @property
        def genericParameterConstraintsSize(self):
            return self.genericParameterConstraints.size
        @property
        def genericContainersOffset(self):
            return self.genericContainers.offset
        @property
        def genericContainersSize(self):
            return self.genericContainers.size
        @property
        def nestedTypesOffset(self):
            return self.nestedTypes.offset
        @property
        def nestedTypesSize(self):
            return self.nestedTypes.size
        @property
        def interfacesOffset(self):
            return self.interfaces.offset
        @property
        def interfacesSize(self):
            return self.interfaces.size
        @property
        def vtableMethodsOffset(self):
            return self.vtableMethods.offset
        @property
        def vtableMethodsSize(self):
            return self.vtableMethods.size
        @property
        def interfaceOffsetsOffset(self):
            return self.interfaceOffsets.offset
        @property
        def interfaceOffsetsSize(self):
            return self.interfaceOffsets.size
        @property
        def typeDefinitionsOffset(self):
            return self.typeDefinitions.offset
        @property
        def typeDefinitionsSize(self):
            return self.typeDefinitions.size
        @property
        def rgctxEntriesOffset(self):
            return self.rgctxEntries.offset
        @property
        def rgctxEntriesCount(self):
            return self.rgctxEntries.size
        @property
        def imagesOffset(self):
            return self.images.offset
        @property
        def imagesSize(self):
            return self.images.size
        @property
        def assembliesOffset(self):
            return self.assemblies.offset
        @property
        def assembliesSize(self):
            return self.assemblies.size
        @property
        def metadataUsageListsOffset(self):
            return self.metadataUsageLists.offset
        @property
        def metadataUsageListsCount(self):
            return self.metadataUsageLists.size
        @property
        def metadataUsagePairsOffset(self):
            return self.metadataUsagePairs.offset
        @property
        def metadataUsagePairsCount(self):
            return self.metadataUsagePairs.size
        @property
        def fieldRefsOffset(self):
            return self.fieldRefs.offset
        @property
        def fieldRefsSize(self):
            return self.fieldRefs.size
        @property
        def referencedAssembliesOffset(self):
            return self.referencedAssemblies.offset
        @property
        def referencedAssembliesSize(self):
            return self.referencedAssemblies.size
        @property
        def attributesInfoOffset(self):
            return self.attributesInfo.offset
        @property
        def attributesInfoCount(self):
            return self.attributesInfo.size
        @property
        def attributeTypesOffset(self):
            return self.attributeTypes.offset
        @property
        def attributeTypesCount(self):
            return self.attributeTypes.size
        @property
        def attributeDataOffset(self):
            return self.attributeData.offset
        @property
        def attributeDataSize(self):
            return self.attributeData.size
        @property
        def attributeDataRangeOffset(self):
            return self.attributeDataRange.offset
        @property
        def attributeDataRangeSize(self):
            return self.attributeDataRange.size
        @property
        def unresolvedVirtualCallParameterTypesOffset(self):
            return self.unresolvedVirtualCallParameterTypes.offset
        @property
        def unresolvedVirtualCallParameterTypesSize(self):
            return self.unresolvedVirtualCallParameterTypes.size
        @property
        def unresolvedVirtualCallParameterRangesOffset(self):
            return self.unresolvedVirtualCallParameterRanges.offset
        @property
        def unresolvedVirtualCallParameterRangesSize(self):
            return self.unresolvedVirtualCallParameterRanges.size
        @property
        def windowsRuntimeTypeNamesOffset(self):
            return self.windowsRuntimeTypeNames.offset
        @property
        def windowsRuntimeTypeNamesSize(self):
            return self.windowsRuntimeTypeNames.size
        @property
        def windowsRuntimeStringsOffset(self):
            return self.windowsRuntimeStrings.offset
        @property
        def windowsRuntimeStringsSize(self):
            return self.windowsRuntimeStrings.size
        @property
        def exportedTypeDefinitionsOffset(self):
            return self.exportedTypeDefinitions.offset
        @property
        def exportedTypeDefinitionsSize(self):
            return self.exportedTypeDefinitions.size
        

    class Il2CppAssemblyDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.imageIndex = reader.readInt()
            if 24.1 <= parent.header.version:
                self.token = reader.readUInt()
            if parent.header.version <= 24:
                self.customAttributeIndex = reader.readInt()
            else:
                self.customAttributeIndex = 0
            if parent.header.version >= 38.0:
                self.moduleToken = reader.readUInt()
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
            
            if parent.header.version >= 38.0:
                self.typeStart = read_index(reader, parent.sizes["type_definition_index"])
            else:
                self.typeStart = reader.readInt()
            self.typeCount = reader.readUInt()

            if parent.header.version >= 38.0:
                self.exportedTypeStart = read_index(reader, parent.sizes["type_definition_index"])
                self.exportedTypeCount = reader.readUInt()
            elif parent.header.version >= 24.0:
                self.exportedTypeStart = reader.readInt()
                self.exportedTypeCount = reader.readUInt()

            self.entryPointIndex = reader.readInt()
            if parent.header.version >= 19.0:
                self.token = reader.readUInt()

            if parent.header.version >= 24.1:
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
            if parent.header.version >= 38.0:
                self.byvalTypeIndex = read_index(reader, parent.sizes["type_index"])
            else:
                self.byvalTypeIndex = reader.readInt()
            if parent.header.version <= 24.5:
                self.byrefTypeIndex = reader.readInt()
            else:
                self.byrefTypeIndex = None

            if parent.header.version >= 38.0:
                self.declaringTypeIndex = read_index(reader, parent.sizes["type_index"])
                self.parentIndex = read_index(reader, parent.sizes["type_index"])
            else:
                self.declaringTypeIndex = reader.readInt()
                self.parentIndex = reader.readInt()
            if parent.header.version < 38.0:
                self.elementTypeIndex = reader.readInt() # we can probably remove this one. Only used for enums
            else:
                self.elementTypeIndex = None

            if parent.header.version <= 24.1:
                self.rgctxStartIndex = reader.readInt()
            if parent.header.version <= 24.1:
                self.rgctxCount = reader.readInt()

            if parent.header.version >= 38.0:
                self.genericContainerIndex = read_index(reader, parent.sizes["generic_definition_index"])
            else:
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
            if parent.header.version >= 38.0:
                self.declaringType = read_index(reader, parent.sizes["type_definition_index"])
                self.returnType = read_index(reader, parent.sizes["type_index"])
            else:
                self.declaringType = reader.readInt()
                self.returnType = reader.readInt()
            if 31 <= parent.header.version:
                self.returnParameterToken = reader.readInt()
            if parent.header.version >= 38.0:
                self.parameterStart = read_index(reader, parent.sizes["parameter_index"])
            else:
                self.parameterStart = reader.readInt()
            if parent.header.version <= 24:
                self.customAttributeIndex = reader.readInt()
            else:
                self.customAttributeIndex = 0
            if parent.header.version >= 38.0:
                self.genericContainerIndex = read_index(reader, parent.sizes["generic_definition_index"])
            else:
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
            if parent.header.version >= 38.0:
                self.typeIndex = read_index(reader, parent.sizes["type_index"])
            else:
                self.typeIndex = reader.readInt()

    class Il2CppFieldDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.name: str = ...
            self.nameIndex = reader.readUInt()
            if parent.header.version >= 38.0:
                self.typeIndex = read_index(reader, parent.sizes["type_index"])
            else:
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
            if parent.header.version >= 38.0:
                self.typeIndex = read_index(reader, parent.sizes["type_index"])
            else:
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
            if parent.header.version < 38.0:
                self.length = reader.readUInt()
            self.dataIndex = reader.readInt()
            self.value = ...

    class Il2CppParameterDefaultValue(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.parameterIndex = reader.readInt()
            if parent.header.version >= 38.0:
                self.typeIndex = read_index(reader, parent.sizes["type_index"])
            else:
                self.typeIndex = reader.readInt()
            self.dataIndex = reader.readInt()

    class Il2CppEventDefinition(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            self.name: str = ...
            self.nameIndex = reader.readUInt()
            if parent.header.version >= 38.0:
                self.typeIndex = read_index(reader, parent.sizes["type_index"])
            else:
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
            if parent.header.version >= 38.0:
                self.typeIndex = read_index(reader, parent.sizes["type_index"])
            else:
                self.typeIndex = reader.readInt()
            self.fieldIndex = reader.readInt() # local offset into type fields

    class Il2CppGenericParameter(ReprClass):
        def __init__(self, reader: LittleEndianReader, parent: 'GlobalMetadata'):
            if parent.header.version >= 38.0:
                self.ownerIndex = read_index(reader, parent.sizes["generic_definition_index"])
            else:
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
        kIl2CppMetadataUsageInvalid = 0
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
        resolved_names: Dict[int, str] = {} # memorize
        def resolve_name_internal(offset: int):
            if offset in resolved_names:
                return resolved_names[offset]
            reader.seek(self.header.stringOffset + offset)
            name = reader.readNullString()
            resolved_names[offset] = name
            return name
        def resolve_name(cls: Any):
            cls.name = resolve_name_internal(cls.nameIndex)
            if hasattr(cls, "namespaceIndex"):
                cls.namespace = resolve_name_internal(cls.namespaceIndex)
        def resolve_raw(_from: int, _to: int):
            reader.seek(_from)
            return reader.read(_to - _from)
        # il2cpp::vm::GlobalMetadata::Initialize
        # GlobalMetadataFileInternals.h
        self.header = GlobalMetadata.Il2CppGlobalMetadataHeader(reader)
        if self.header.sanity != 0xFAB11BAF: # sanity
            raise InvalidGlobalMetadataException("Magic number not match.")
        if not (16 <= self.header.version <= 39) or self.header.version in [30, 32, 33, 34, 35 ,36 ,37, 38]:
            raise InvalidGlobalMetadataException("Metadata version not supported.")
        # Differentiate version 24
        if self.header.version == 24:
            if self.header.stringLiteralOffset == 264:
                # exclude rgctxEntries
                reader.seek(0)
                self.header = GlobalMetadata.Il2CppGlobalMetadataHeader(reader, 24.2)
            else:
                self.imageDefinitions: List[GlobalMetadata.Il2CppImageDefinition] = load_list(GlobalMetadata.Il2CppImageDefinition, self.header.imagesOffset, self.header.imagesSize)
                if any(entry.token != 1 for entry in self.imageDefinitions):
                    self.header.version = 24.1

        if self.header.version >= 38.0:
            def get_index_size(number_of_elements: int) -> int:
                if number_of_elements < 256:
                    return 1
                if number_of_elements < 65536:
                    return 2
                return 4
            
            self.sizes: Dict[str, int] = {
                "type_index": ..., # from MetadataRegistration->typesCount
                "type_definition_index": get_index_size(
                    self.header.typeDefinitions.count
                ), # from typeDefinitions.count
                "generic_definition_index": get_index_size(
                    self.header.genericContainers.count
                ), # from genericContainers.count
                "parameter_index": get_index_size(
                    self.header.parameters.count
                ), # from parameters.count
            }

            # try to determine typeIndexSize
            if self.header.interfaceOffsets.count > 0:
                # TypeIndex + int32_t
                entry_size = self.header.interfaceOffsets.size // self.header.interfaceOffsets.count
                self.sizes["type_index"] = entry_size - 4
            else:
                print("Cannot determine sizes.typeIndex")
        else:
            self.sizes: Dict[str, int] = {}

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
            # logging.debug(f"Il2CppAssemblyDefinition {temp.aname.name}")
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
        # resolve stringLiterals
        if self.header.version >= 38.0:
            for index in range(len(self.stringLiterals) - 1):
                string_literal = self.stringLiterals[index]
                string_literal_next = self.stringLiterals[index + 1]
                string_literal.value = load_str(
                    self.header.stringLiteralDataOffset + string_literal.dataIndex,
                    string_literal_next.dataIndex - string_literal.dataIndex
                )
            if len(self.stringLiterals):
                self.stringLiterals[-1].value = None
        else:
            for string_literal in self.stringLiterals:
                string_literal.value = load_str(
                    self.header.stringLiteralDataOffset + string_literal.dataIndex,
                    string_literal.length
                )
    
        if self.header.version > 16:
            self.fieldRefs: List[GlobalMetadata.Il2CppFieldRef] = load_list(GlobalMetadata.Il2CppFieldRef,self.header.fieldRefsOffset, self.header.fieldRefsSize)
            if self.header.version < 27:
                self.metadataUsageLists: List[GlobalMetadata.Il2CppMetadataUsageList] = load_list(GlobalMetadata.Il2CppMetadataUsageList, self.header.metadataUsageListsOffset, self.header.metadataUsageListsCount)
                self.metadataUsagePairs: List[GlobalMetadata.Il2CppMetadataUsagePair] = load_list(GlobalMetadata.Il2CppMetadataUsagePair, self.header.metadataUsagePairsOffset, self.header.metadataUsagePairsCount)
                # process_metadata_usage
                self.metadataUsageDict = {i: {} for i in GlobalMetadata.Il2CppMetadataUsage}
                for entry in self.metadataUsageLists:
                    for i in range(entry.count):
                        offset = entry.start + i
                        if offset >= len(self.metadataUsagePairs):
                            continue
                        metadataUsagePair: GlobalMetadata.Il2CppMetadataUsagePair = self.metadataUsagePairs[offset]
                        usage = GlobalMetadata.Il2CppMetadataUsage(((metadataUsagePair.encodedSourceIndex) & 0xE0000000) >> 29)
                        decodedIndex = (metadataUsagePair.encodedSourceIndex & 0x1FFFFFFF) >> (self.header.version >= 27)
                        self.metadataUsageDict[usage][metadataUsagePair.destinationIndex] = decodedIndex
                self.metadataUsagesCount = max(
                    (
                        max(
                            Dict.keys(),
                            default = 0
                        ) for Dict in self.metadataUsageDict.values()
                    ),
                    default = 0
                ) + 1
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