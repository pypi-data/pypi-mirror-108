from typing import Dict, Union, Protocol


__all__ = 'DataclassType', 'SettingsType',


class DataclassType(Protocol):
    __dataclass_fields__: Dict


SettingsType = Union[dict, tuple, DataclassType]
