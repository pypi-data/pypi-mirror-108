# -*- coding: utf-8 -*-
# Copyright 2020 TensorFlowTTS Team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Base Config for all config."""

import abc
import yaml
import os

from tensorflow_tts.utils.utils import CONFIG_FILE_NAME


class BaseConfig(abc.ABC):
    def set_config_params(self, config_params):
        self.config_params = config_params

    def save_pretrained(self, saved_path):
        """Save config to file"""
        os.makedirs(saved_path, exist_ok=True)
        with open(os.path.join(saved_path, CONFIG_FILE_NAME), "w") as file:
            yaml.dump(self.config_params, file, Dumper=yaml.Dumper)
