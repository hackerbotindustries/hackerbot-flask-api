################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.01
#
# This script contains the configuration for the Flask application.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkey"

    class Config:
        env_file = ".env"

settings = Settings()