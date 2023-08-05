from awsglue.transforms import GlueTransform as GlueTransform
from typing import Any

class Unbox(GlueTransform):
    def __call__(
        self,
        frame: Any,
        path: Any,
        format: Any,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
        **options: Any
    ): ...
    @classmethod
    def describeArgs(cls): ...
    @classmethod
    def describeTransform(cls): ...
    @classmethod
    def describeErrors(cls): ...
    @classmethod
    def describeReturn(cls): ...
