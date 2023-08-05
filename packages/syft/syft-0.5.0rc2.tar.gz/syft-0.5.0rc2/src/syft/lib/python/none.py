# stdlib
from typing import Any
from typing import Optional

# third party
from google.protobuf.reflection import GeneratedProtocolMessageType

# syft relative
from ... import deserialize
from ... import serialize
from ...core.common import UID
from ...core.common.serde.serializable import bind_protobuf
from ...proto.lib.python.none_pb2 import SyNone as None_PB
from .primitive_factory import PrimitiveFactory
from .primitive_interface import PyPrimitive
from .types import SyPrimitiveRet

NoneType = type(None)


@bind_protobuf
class _SyNone(PyPrimitive):
    def __init__(self, id: Optional[UID] = None):
        self._id: UID = id if id else UID()

    @property
    def id(self) -> UID:
        """We reveal PyPrimitive.id as a property to discourage users and
        developers of Syft from modifying .id attributes after an object
        has been initialized.

        :return: returns the unique id of the object
        :rtype: UID
        """
        return self._id

    def upcast(self) -> NoneType:
        return None

    def __eq__(self, other: Any) -> SyPrimitiveRet:
        if isinstance(other, _SyNone):
            return PrimitiveFactory.generate_primitive(value=True)

        if other is None:
            return PrimitiveFactory.generate_primitive(value=True)

        res = None.__eq__(other)
        return PrimitiveFactory.generate_primitive(value=res)

    def __hash__(self) -> SyPrimitiveRet:
        res = None.__hash__()
        return PrimitiveFactory.generate_primitive(value=res)

    def _object2proto(self) -> None_PB:
        none_pb = None_PB()
        none_pb.id.CopyFrom(serialize(obj=self.id))
        return none_pb

    @staticmethod
    def _proto2object(proto: None_PB) -> "_SyNone":
        none_id: UID = deserialize(blob=proto.id)

        de_none = _SyNone()
        de_none._id = none_id

        return de_none

    @staticmethod
    def get_protobuf_schema() -> GeneratedProtocolMessageType:
        return None_PB


SyNone = _SyNone()
