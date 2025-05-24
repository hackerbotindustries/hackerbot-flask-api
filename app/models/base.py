################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.05.16
#
# This script contains the base request models.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from pydantic import BaseModel
from typing import Literal, Optional
from typing import Union

class InitializeRequest(BaseModel):
    method: Literal["initialize"]

class ModeRequest(BaseModel):
    method: Literal["mode"]
    mode_id: int

class StartRequest(BaseModel):
    method: Literal["start"]

class QuickmapRequest(BaseModel):
    method: Literal["quickmap"]

class DockRequest(BaseModel):
    method: Literal["dock"]

class KillRequest(BaseModel):
    method: Literal["kill"]

class TriggerBumpRequest(BaseModel):
    method: Literal["trigger-bump"]
    left: bool
    right: bool

class SpeakRequest(BaseModel):
    method: Literal["speak"]
    model_src: str
    text: str
    speaker_id: Optional[int] = None

class DriveRequest(BaseModel):
    method: Literal["drive"]
    linear_velocity: float
    angle_velocity: float

BaseCommand = Union[
    InitializeRequest,
    ModeRequest,
    StartRequest,
    QuickmapRequest,
    DockRequest,
    KillRequest,
    TriggerBumpRequest,
    SpeakRequest,
    DriveRequest
]