from awsglue.utils import (
    callsite as callsite,
    iteritems as iteritems,
    itervalues as itervalues,
    makeOptions as makeOptions,
)
from typing import Any, Optional

long = int
basestring = str
unicode = str
imap = map
ifilter = filter

class ResolveOption:
    path: Any = ...
    action: Any = ...
    target: Any = ...
    def __init__(self, path: Any, action: Any, target: Optional[Any] = ...) -> None: ...

class DynamicFrame:
    glue_ctx: Any = ...
    name: Any = ...
    def __init__(self, jdf: Any, glue_ctx: Any, name: str = ...) -> None: ...
    def with_frame_schema(self, schema: Any): ...
    def schema(self): ...
    def show(self, num_rows: int = ...) -> None: ...
    def filter(
        self,
        f: Any,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def mapPartitions(
        self,
        f: Any,
        preservesPartitioning: bool = ...,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def map(
        self,
        f: Any,
        preservesPartitioning: bool = ...,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def mapPartitionsWithIndex(
        self,
        f: Any,
        preservesPartitioning: bool = ...,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def printSchema(self) -> None: ...
    def toDF(self, options: Optional[Any] = ...): ...
    @classmethod
    def fromDF(cls, dataframe: Any, glue_ctx: Any, name: Any): ...
    def unbox(
        self,
        path: Any,
        format: Any,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
        **options: Any
    ): ...
    def drop_fields(
        self,
        paths: Any,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def select_fields(
        self,
        paths: Any,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def split_fields(
        self,
        paths: Any,
        name1: Any,
        name2: Any,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def split_rows(
        self,
        comparison_dict: Any,
        name1: Any,
        name2: Any,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def rename_field(
        self,
        oldName: Any,
        newName: Any,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def write(
        self,
        connection_type: Any,
        connection_options: Any = ...,
        format: Optional[Any] = ...,
        format_options: Any = ...,
        accumulator_size: int = ...,
    ): ...
    def count(self): ...
    def spigot(
        self,
        path: Any,
        options: Any = ...,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def join(
        self,
        paths1: Any,
        paths2: Any,
        frame2: Any,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def unnest(
        self,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def relationalize(
        self,
        root_table_name: Any,
        staging_path: Any,
        options: Any = ...,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def applyMapping(self, *args: Any, **kwargs: Any): ...
    def apply_mapping(
        self,
        mappings: Any,
        case_sensitive: bool = ...,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def resolveChoice(
        self,
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
    def mergeDynamicFrame(
        self,
        stage_dynamic_frame: Any,
        primary_keys: Any,
        transformation_ctx: str = ...,
        options: Any = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def union(
        self,
        other_frame: Any,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def getNumPartitions(self): ...
    def repartition(
        self,
        num_partitions: Any,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def coalesce(
        self,
        num_partitions: Any,
        shuffle: bool = ...,
        transformation_ctx: str = ...,
        info: str = ...,
        stageThreshold: int = ...,
        totalThreshold: int = ...,
    ): ...
    def errorsAsDynamicFrame(self): ...
    def errorsCount(self): ...
    def stageErrorsCount(self): ...
    def assertErrorThreshold(self): ...

class DynamicFrameCollection:
    def __init__(self, dynamic_frames: Any, glue_ctx: Any) -> None: ...
    def __getitem__(self, key: Any): ...
    def __len__(self): ...
    def keys(self): ...
    def values(self): ...
    def select(self, key: Any, transformation_ctx: str = ...): ...
    def map(self, callable: Any, transformation_ctx: str = ...): ...
    def flatmap(self, f: Any, transformation_ctx: str = ...): ...

class DynamicFrameReader:
    def __init__(self, glue_context: Any) -> None: ...
    def from_rdd(
        self,
        data: Any,
        name: Any,
        schema: Optional[Any] = ...,
        sampleRatio: Optional[Any] = ...,
    ): ...
    def from_options(
        self,
        connection_type: Any,
        connection_options: Any = ...,
        format: Optional[Any] = ...,
        format_options: Any = ...,
        transformation_ctx: str = ...,
        push_down_predicate: str = ...,
        **kwargs: Any
    ): ...
    def from_catalog(
        self,
        database: Optional[Any] = ...,
        table_name: Optional[Any] = ...,
        redshift_tmp_dir: str = ...,
        transformation_ctx: str = ...,
        push_down_predicate: str = ...,
        additional_options: Any = ...,
        catalog_id: Optional[Any] = ...,
        **kwargs: Any
    ): ...

class DynamicFrameWriter:
    def __init__(self, glue_context: Any) -> None: ...
    def from_options(
        self,
        frame: Any,
        connection_type: Any,
        connection_options: Any = ...,
        format: Optional[Any] = ...,
        format_options: Any = ...,
        transformation_ctx: str = ...,
    ): ...
    def from_catalog(
        self,
        frame: Any,
        database: Optional[Any] = ...,
        table_name: Optional[Any] = ...,
        redshift_tmp_dir: str = ...,
        transformation_ctx: str = ...,
        additional_options: Any = ...,
        catalog_id: Optional[Any] = ...,
        **kwargs: Any
    ): ...
    def from_jdbc_conf(
        self,
        frame: Any,
        catalog_connection: Any,
        connection_options: Any = ...,
        redshift_tmp_dir: str = ...,
        transformation_ctx: str = ...,
    ): ...
