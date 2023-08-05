from typing import Any, Optional

class DataFrameReader:
    def __init__(self, glue_context: Any) -> None: ...
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
