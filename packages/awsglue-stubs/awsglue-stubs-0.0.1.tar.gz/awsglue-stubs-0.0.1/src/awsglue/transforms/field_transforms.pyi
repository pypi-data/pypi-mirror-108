from awsglue.transforms import GlueTransform as GlueTransform
from typing import Any, Optional

class RenameField(GlueTransform):
    def __call__(
        self,
        frame: Any,
        old_name: Any,
        new_name: Any,
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

class DropFields(GlueTransform):
    def __call__(
        self,
        frame: Any,
        paths: Any,
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

class SelectFields(GlueTransform):
    def __call__(
        self,
        frame: Any,
        paths: Any,
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

class SplitFields(GlueTransform):
    def __call__(
        self,
        frame: Any,
        paths: Any,
        name1: Optional[Any] = ...,
        name2: Optional[Any] = ...,
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

class SplitRows(GlueTransform):
    def __call__(
        self,
        frame: Any,
        comparison_dict: Any,
        name1: str = ...,
        name2: str = ...,
        transformation_ctx: str = ...,
        info: Optional[Any] = ...,
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

class Join(GlueTransform):
    def __call__(
        self,
        frame1: Any,
        frame2: Any,
        keys1: Any,
        keys2: Any,
        transformation_ctx: str = ...,
    ): ...
    @classmethod
    def describeArgs(cls): ...
    @classmethod
    def describeTransform(cls): ...
    @classmethod
    def describeErrors(cls): ...
    @classmethod
    def describeReturn(cls): ...

class Spigot(GlueTransform):
    def __call__(
        self, frame: Any, path: Any, options: Any, transformation_ctx: str = ...
    ): ...
    @classmethod
    def describeArgs(cls): ...
    @classmethod
    def describeTransform(cls): ...
    @classmethod
    def describeErrors(cls): ...
    @classmethod
    def describeReturn(cls): ...
