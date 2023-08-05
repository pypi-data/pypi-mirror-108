from awsglue.transforms import GlueTransform as GlueTransform
from typing import Any, Optional

class ResolveChoice(GlueTransform):
    def __call__(
        self,
        frame: Any,
        specs: Optional[Any] = ...,
        choice: str = ...,
        database: Optional[Any] = ...,
        table_name: Optional[Any] = ...,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
        catalog_id: Optional[Any] = ...,
    ): ...
    @classmethod
    def describeArgs(cls): ...
    @classmethod
    def describeTransform(cls): ...
    @classmethod
    def describeErrors(cls): ...
    @classmethod
    def describeReturn(cls): ...
