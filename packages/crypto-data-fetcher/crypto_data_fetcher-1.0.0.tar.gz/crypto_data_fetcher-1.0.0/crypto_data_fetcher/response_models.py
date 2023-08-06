from pydantic import BaseModel, Field
from typing import List, Union, Optional, Dict, Any
from datetime import datetime


class BaseDataResponse(BaseModel):
    coinId: int
    coinName: str
    coinSymbol: str
    colValues: List[Union[int, float, str, None]]
    rank: int


class BaseResponse(BaseModel):
    data: List[BaseDataResponse]
    draw: str
    length: int
    recordsFiltered: int
    recordsTotal: int
    start: str


class BaseRequestModel(BaseModel):
    search: Optional[str] = Field("", description="Search")
    draw: int = Field(1, description="Page Count")
    order_0_column: int = Field(0, description="Column Ordering")
    order_0_dir: str = Field("asc", description="Sorting")
    start: int = Field(0, description="Start Index")
    length: int = Field(50, description="Default items per page")
    search_value: Optional[str] = Field("", description="Search Value")
    search_regex: bool = Field(False, description="Is Regex Search")

    @property
    def _param_map_(self):
        return {
            "order_0_column": "order[0][column]",
            "order_0_dir": "order[0][dir]",
            "search_value": "search[value]",
            "search_regex": "search[regex]"
        }

    @property
    def params(self) -> Dict[str, Any]:
        data_ = self.dict()
        for i, v in self._param_map_.items():
            data_[v] = data_.pop(i)
        data_["_"] = int(datetime.utcnow().timestamp() * 1000)
        return data_

    @classmethod
    def from_params(cls,
                    default_count_per_page=50,
                    start_index=0,
                    search_value=None,
                    search_regex=False,
                    page_number=1,
                    ordering="asc"
                    ):
        return cls(
            draw=page_number,
            length=default_count_per_page,
            start=start_index,
            search_value=search_value,
            search_regex=search_regex,
            order_0_dir=ordering
        )
