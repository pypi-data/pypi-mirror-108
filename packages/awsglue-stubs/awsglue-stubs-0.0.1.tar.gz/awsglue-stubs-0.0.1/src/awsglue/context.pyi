from awsglue.data_sink import DataSink as DataSink
from awsglue.data_source import DataSource as DataSource
from awsglue.dataframereader import DataFrameReader as DataFrameReader
from awsglue.dynamicframe import (
    DynamicFrame as DynamicFrame,
    DynamicFrameCollection as DynamicFrameCollection,
    DynamicFrameReader as DynamicFrameReader,
    DynamicFrameWriter as DynamicFrameWriter,
)
from awsglue.gluetypes import DataType as DataType
from awsglue.streaming_data_source import StreamingDataSource as StreamingDataSource
from awsglue.utils import callsite as callsite, makeOptions as makeOptions
from py4j.java_gateway import JavaClass as JavaClass
from pyspark.sql import SQLContext
from typing import Any, Optional

def register(sc: Any) -> None: ...

STREAMING_EXCEPTION_BACKOFF: int
STREAMING_EXCEPTION_INTERVAL: int
STREAMING_EXCEPTION_MAX_RETRIES_WITHIN_INTERVAL: int

class GlueContext(SQLContext):
    Spark_SQL_Formats: Any = ...
    create_dynamic_frame: Any = ...
    create_data_frame: Any = ...
    write_dynamic_frame: Any = ...
    spark_session: Any = ...
    def __init__(self, sparkContext: Any, **options: Any) -> None: ...
    def getSource(
        self,
        connection_type: Any,
        format: Optional[Any] = ...,
        transformation_ctx: str = ...,
        push_down_predicate: str = ...,
        **options: Any
    ): ...
    def get_catalog_schema_as_spark_schema(
        self,
        database: Optional[Any] = ...,
        table_name: Optional[Any] = ...,
        catalog_id: Optional[Any] = ...,
    ): ...
    def create_dynamic_frame_from_rdd(
        self,
        data: Any,
        name: Any,
        schema: Optional[Any] = ...,
        sample_ratio: Optional[Any] = ...,
        transformation_ctx: str = ...,
    ): ...
    def create_dynamic_frame_from_catalog(
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
    def create_data_frame_from_catalog(
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
    def create_dynamic_frame_from_options(
        self,
        connection_type: Any,
        connection_options: Any = ...,
        format: Optional[Any] = ...,
        format_options: Any = ...,
        transformation_ctx: str = ...,
        push_down_predicate: str = ...,
        **kwargs: Any
    ): ...
    def getSink(
        self,
        connection_type: Any,
        format: Optional[Any] = ...,
        transformation_ctx: str = ...,
        **options: Any
    ): ...
    def write_dynamic_frame_from_options(
        self,
        frame: Any,
        connection_type: Any,
        connection_options: Any = ...,
        format: Optional[Any] = ...,
        format_options: Any = ...,
        transformation_ctx: str = ...,
    ): ...
    def write_from_options(
        self,
        frame_or_dfc: Any,
        connection_type: Any,
        connection_options: Any = ...,
        format: Any = ...,
        format_options: Any = ...,
        transformation_ctx: str = ...,
        **kwargs: Any
    ): ...
    def write_dynamic_frame_from_catalog(
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
    def write_dynamic_frame_from_jdbc_conf(
        self,
        frame: Any,
        catalog_connection: Any,
        connection_options: Any = ...,
        redshift_tmp_dir: str = ...,
        transformation_ctx: str = ...,
        catalog_id: Optional[Any] = ...,
    ) -> None: ...
    def write_from_jdbc_conf(
        self,
        frame_or_dfc: Any,
        catalog_connection: Any,
        connection_options: Any = ...,
        redshift_tmp_dir: str = ...,
        transformation_ctx: str = ...,
        catalog_id: Optional[Any] = ...,
    ): ...
    def convert_resolve_option(self, path: Any, action: Any, target: Any): ...
    def extract_jdbc_conf(
        self, connection_name: Any, catalog_id: Optional[Any] = ...
    ): ...
    def purge_table(
        self,
        database: Any,
        table_name: Any,
        options: Any = ...,
        transformation_ctx: str = ...,
        catalog_id: Optional[Any] = ...,
    ) -> None: ...
    def purge_s3_path(
        self, s3_path: Any, options: Any = ..., transformation_ctx: str = ...
    ) -> None: ...
    def transition_table(
        self,
        database: Any,
        table_name: Any,
        transition_to: Any,
        options: Any = ...,
        transformation_ctx: str = ...,
        catalog_id: Optional[Any] = ...,
    ) -> None: ...
    def transition_s3_path(
        self,
        s3_path: Any,
        transition_to: Any,
        options: Any = ...,
        transformation_ctx: str = ...,
    ) -> None: ...
    def get_logger(self): ...
    def currentTimeMillis(self): ...
    def forEachBatch(
        self, frame: Any, batch_function: Any, options: Any = ...
    ) -> None: ...
    def add_ingestion_time_columns(self, frame: Any, time_granularity: Any): ...
    def begin_transaction(self, read_only: Any): ...
    def commit_transaction(self, transaction_id: Any): ...
    def abort_transaction(self, transaction_id: Any): ...
