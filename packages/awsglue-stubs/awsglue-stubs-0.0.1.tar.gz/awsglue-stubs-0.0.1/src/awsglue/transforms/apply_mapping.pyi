from awsglue.transforms import DropFields as DropFields, GlueTransform as GlueTransform
from typing import Any

class ApplyMapping(GlueTransform):
    def __call__(
        self,
        frame: Any,
        mappings: Any,
        case_sensitive: bool = ...,
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
