from awsglue.transforms import GlueTransform as GlueTransform
from typing import Any

class UnnestFrame(GlueTransform):
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
