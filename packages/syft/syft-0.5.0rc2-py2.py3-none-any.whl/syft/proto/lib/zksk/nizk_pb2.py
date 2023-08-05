# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/lib/zksk/nizk.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# syft absolute
from syft.proto.lib.petlib import bn_pb2 as proto_dot_lib_dot_petlib_dot_bn__pb2
from syft.proto.lib.python import tuple_pb2 as proto_dot_lib_dot_python_dot_tuple__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="proto/lib/zksk/nizk.proto",
    package="syft.lib.zksk",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x19proto/lib/zksk/nizk.proto\x12\rsyft.lib.zksk\x1a\x19proto/lib/petlib/bn.proto\x1a\x1cproto/lib/python/tuple.proto"l\n\x04NIZK\x12&\n\tchallenge\x18\x01 \x01(\x0b\x32\x13.syft.lib.petlib.Bn\x12)\n\tresponses\x18\x02 \x01(\x0b\x32\x16.syft.lib.python.Tuple\x12\x11\n\tstmt_hash\x18\x03 \x01(\x0c\x62\x06proto3',
    dependencies=[
        proto_dot_lib_dot_petlib_dot_bn__pb2.DESCRIPTOR,
        proto_dot_lib_dot_python_dot_tuple__pb2.DESCRIPTOR,
    ],
)


_NIZK = _descriptor.Descriptor(
    name="NIZK",
    full_name="syft.lib.zksk.NIZK",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="challenge",
            full_name="syft.lib.zksk.NIZK.challenge",
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
            name="responses",
            full_name="syft.lib.zksk.NIZK.responses",
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
            name="stmt_hash",
            full_name="syft.lib.zksk.NIZK.stmt_hash",
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=101,
    serialized_end=209,
)

_NIZK.fields_by_name[
    "challenge"
].message_type = proto_dot_lib_dot_petlib_dot_bn__pb2._BN
_NIZK.fields_by_name[
    "responses"
].message_type = proto_dot_lib_dot_python_dot_tuple__pb2._TUPLE
DESCRIPTOR.message_types_by_name["NIZK"] = _NIZK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NIZK = _reflection.GeneratedProtocolMessageType(
    "NIZK",
    (_message.Message,),
    {
        "DESCRIPTOR": _NIZK,
        "__module__": "proto.lib.zksk.nizk_pb2"
        # @@protoc_insertion_point(class_scope:syft.lib.zksk.NIZK)
    },
)
_sym_db.RegisterMessage(NIZK)


# @@protoc_insertion_point(module_scope)
