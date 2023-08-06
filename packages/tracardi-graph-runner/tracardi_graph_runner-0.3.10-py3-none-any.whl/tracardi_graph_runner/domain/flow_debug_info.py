from typing import List

from pydantic import BaseModel

from tracardi_graph_runner.domain.error_debug_info import ErrorDebugInfo


class FlowDebugInfo(BaseModel):
    error: List[ErrorDebugInfo] = []
