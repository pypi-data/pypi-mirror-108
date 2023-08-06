from dataclasses import dataclass


__all__ = 'FieldsConfig', 'DEFAULT_FIELDS_CONFIG',


@dataclass
class FieldsConfig:
    id: str
    parent_id: str


DEFAULT_FIELDS_CONFIG = FieldsConfig(id='id', parent_id='parent_id')
