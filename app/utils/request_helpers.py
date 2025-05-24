################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.05.19
#
# This script contains helper functions for handling HTTP requests.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from fastapi import HTTPException
from typing import Any, Dict

def get_required_param(data: Dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None:
        raise HTTPException(status_code=400, detail=f"Missing '{key}' parameter")
    return value
