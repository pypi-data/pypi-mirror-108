from typing import Generic, Optional, TypeVar

from pydantic import validator
from pydantic.generics import GenericModel

DataType = TypeVar('DataType')
ErrorType = TypeVar('ErrorType')


class GraphQLResponse(GenericModel, Generic[DataType, ErrorType]):
    data: Optional[DataType] = None
    error: Optional[ErrorType] = None

    @validator('error', always=True)
    def check_consistency(cls, v, values):
        if v is not None and values['data'] is not None:
            raise ValueError('must not provide both data and error')

        if v is None and values.get('data') is None:
            raise ValueError('must provide data or error')

        return v
