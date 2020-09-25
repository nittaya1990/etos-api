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
"""Generic ETOS tester module."""
import uuid
from etos_api.lib.base_tester import BaseTester


class GenericTester(BaseTester):
    """Tester for generic test suites."""

    def validate(self):
        """Validate data for this generic tester."""
        if self.artifact_id is None:
            raise Exception(
                "No EiffelArtifactCreatedEvent for product '{}'.".format(
                    self.params.artifact_identity
                )
            )

    def handle(self):  # pylint: disable=duplicate-code
        """Handle this tester endpoint.

        :return: Data generated from this tester.
        :rtype: dict
        """
        self.validate()
        selection_strategy = {"tracker": "Suite Builder", "id": str(uuid.uuid4())}
        tercc = self.etos.events.send_test_execution_recipe_collection_created(
            selection_strategy,
            links={"CAUSE": self.artifact_id},
            batchesUri=self.params.test_suite,
        )
        self.configure_environment_provider(tercc.meta.event_id)

        return {
            "EiffelTestExecutionRecipeCollectionCreatedEvent": tercc.json,
            "EiffelArtifactCreatedEvent": self.artifact_id,
        }
