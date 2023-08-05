# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/core/node/common/service/object_search_permission_update_message.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# syft absolute
from syft.proto.core.common import (
    common_object_pb2 as proto_dot_core_dot_common_dot_common__object__pb2,
)
from syft.proto.core.io import address_pb2 as proto_dot_core_dot_io_dot_address__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="proto/core/node/common/service/object_search_permission_update_message.proto",
    package="syft.core.node.common.service",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\nLproto/core/node/common/service/object_search_permission_update_message.proto\x12\x1dsyft.core.node.common.service\x1a%proto/core/common/common_object.proto\x1a\x1bproto/core/io/address.proto"\xdf\x01\n#ObjectSearchPermissionUpdateMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x19\n\x11target_verify_key\x18\x03 \x01(\x0c\x12/\n\x10target_object_id\x18\x04 \x01(\x0b\x32\x15.syft.core.common.UID\x12\x1d\n\x15\x61\x64\x64_instead_of_remove\x18\x05 \x01(\x08\x62\x06proto3',
    dependencies=[
        proto_dot_core_dot_common_dot_common__object__pb2.DESCRIPTOR,
        proto_dot_core_dot_io_dot_address__pb2.DESCRIPTOR,
    ],
)


_OBJECTSEARCHPERMISSIONUPDATEMESSAGE = _descriptor.Descriptor(
    name="ObjectSearchPermissionUpdateMessage",
    full_name="syft.core.node.common.service.ObjectSearchPermissionUpdateMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="msg_id",
            full_name="syft.core.node.common.service.ObjectSearchPermissionUpdateMessage.msg_id",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="address",
            full_name="syft.core.node.common.service.ObjectSearchPermissionUpdateMessage.address",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="target_verify_key",
            full_name="syft.core.node.common.service.ObjectSearchPermissionUpdateMessage.target_verify_key",
            index=2,
            number=3,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="target_object_id",
            full_name="syft.core.node.common.service.ObjectSearchPermissionUpdateMessage.target_object_id",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="add_instead_of_remove",
            full_name="syft.core.node.common.service.ObjectSearchPermissionUpdateMessage.add_instead_of_remove",
            index=4,
            number=5,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=180,
    serialized_end=403,
)

_OBJECTSEARCHPERMISSIONUPDATEMESSAGE.fields_by_name[
    "msg_id"
].message_type = proto_dot_core_dot_common_dot_common__object__pb2._UID
_OBJECTSEARCHPERMISSIONUPDATEMESSAGE.fields_by_name[
    "address"
].message_type = proto_dot_core_dot_io_dot_address__pb2._ADDRESS
_OBJECTSEARCHPERMISSIONUPDATEMESSAGE.fields_by_name[
    "target_object_id"
].message_type = proto_dot_core_dot_common_dot_common__object__pb2._UID
DESCRIPTOR.message_types_by_name[
    "ObjectSearchPermissionUpdateMessage"
] = _OBJECTSEARCHPERMISSIONUPDATEMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ObjectSearchPermissionUpdateMessage = _reflection.GeneratedProtocolMessageType(
    "ObjectSearchPermissionUpdateMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _OBJECTSEARCHPERMISSIONUPDATEMESSAGE,
        "__module__": "proto.core.node.common.service.object_search_permission_update_message_pb2"
        # @@protoc_insertion_point(class_scope:syft.core.node.common.service.ObjectSearchPermissionUpdateMessage)
    },
)
_sym_db.RegisterMessage(ObjectSearchPermissionUpdateMessage)


# @@protoc_insertion_point(module_scope)
