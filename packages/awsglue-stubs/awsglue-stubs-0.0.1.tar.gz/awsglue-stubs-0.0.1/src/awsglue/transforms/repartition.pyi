from awsglue.transforms import GlueTransform as GlueTransform
from typing import Any

class Repartition(GlueTransform):
    def __call__(
        self,
        frame: Any,
        num_partitions: Any,
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
