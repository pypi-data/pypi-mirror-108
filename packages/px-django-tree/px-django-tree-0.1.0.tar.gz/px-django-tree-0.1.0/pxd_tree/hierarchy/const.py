from dataclasses import dataclass

from pxd_tree.adjacency_list import (
    FieldsConfig as Base,
    DEFAULT_FIELDS_CONFIG as BASE
)


__all__ = 'FieldsConfig', 'DEFAULT_FIELDS_CONFIG',


@dataclass
class FieldsConfig(Base):
    path: str


DEFAULT_FIELDS_CONFIG = FieldsConfig(
    id=BASE.id,
    parent_id=BASE.parent_id,
    path='path'
)