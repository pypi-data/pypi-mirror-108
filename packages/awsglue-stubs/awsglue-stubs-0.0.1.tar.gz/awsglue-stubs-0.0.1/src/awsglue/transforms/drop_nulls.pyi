from awsglue.gluetypes import (
    ArrayType as ArrayType,
    NullType as NullType,
    StructType as StructType,
)
from awsglue.transforms import DropFields as DropFields, GlueTransform as GlueTransform
from typing import Any

class DropNullFields(GlueTransform):
    def __call__(
        self,
        frame: Any,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    @classmethod
    def describeArgs(cls): ...
    @classmethod
    def describeTransform(cls): ...
    @classmethod
    def describeErrors(cls): ...
    @classmethod
    def describeReturn(cls): ...
