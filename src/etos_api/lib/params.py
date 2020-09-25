# Copyright 2020 Axis Communications AB.
#
# For a full list of individual contributors, please see the commit history.
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
"""ETOS API parameter module."""
import os
import json
import logging
from etos_api.lib.generic_tester import GenericTester


class Params:
    """Parameters used for ETOS API."""

    __iut = None
    logger = logging.getLogger("Params")

    def __init__(self, request):
        """Initialize.

        :param request: Falcon request data.
        :type request: :obj:`falcon.Request`
        """
        self.request = request

    @property
    def iut_provider(self):
        """IUT provider name for use when configuring the environment provider."""
        return self.request.media.get("iut_provider", os.getenv("DEFAULT_IUT_PROVIDER"))

    @property
    def execution_space_provider(self):
        """Name of execution space provider to use when configuring the environment provider."""
        return self.request.media.get(
            "execution_space_provider", os.getenv("DEFAULT_EXECUTION_SPACE_PROVIDER")
        )

    @property
    def log_area_provider(self):
        """Log area provider name for use when configuring the environment provider."""
        return self.request.media.get(
            "log_area_provider", os.getenv("DEFAULT_LOG_AREA_PROVIDER")
        )

    @property
    def dataset(self):
        """Dataset dictionary for use when configuring the environment provider."""
        dataset = {}
        if os.getenv("DEFAULT_DATASET"):
            dataset = json.loads(os.getenv("DEFAULT_DATASET"))
        dataset.update(**self.request.media.get("dataset", {}))
        return dataset

    @property
    def artifact_identity(self):
        """Artifact identity to start tests for."""
        return self.request.media.get("artifact_identity")

    @property
    def tester(self):
        """Which tester to use."""
        return GenericTester(self)

    @property
    def test_suite(self):
        """Test suite URL request parameter."""
        return self.request.media.get("test_suite_url")
