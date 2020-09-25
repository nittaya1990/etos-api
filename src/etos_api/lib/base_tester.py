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
"""Base test starter module."""
import os
from etos_lib import ETOS

ARTIFACT_REQUEST = """
{
  artifactCreated(%s, last:1) {
    edges {
      node {
        data {
          identity
        }
        meta {
          id
        }
      }
    }
  }
}
"""


class BaseTester:
    """Base tester API."""

    __artifact_id = None
    __gql_response = None

    def __init__(self, params):
        """Initialize.

        :param params: Parameter data storage for Tester APIs.
        :type params: :obj:`lib.params.Params`
        """
        self.params = params
        self.etos = ETOS("ETOS API", os.getenv("HOSTNAME"), "ETOS API")
        self.etos.config.rabbitmq_publisher_from_environment()
        self.etos.start_publisher()

    def configure_environment_provider(self, suite_id):
        """Configure the ETOS environment provider for a suite ID.

        :param suite_id: Suite ID to configure the environment provider for.
        :type suite_id: str
        """
        params = {
            "suite_id": suite_id,
            "iut_provider": self.params.iut_provider,
            "execution_space_provider": self.params.execution_space_provider,
            "log_area_provider": self.params.log_area_provider,
            "dataset": self.params.dataset,
        }
        generator = self.etos.http.retry(
            "POST",
            "{}/configure".format(self.etos.debug.environment_provider),
            as_json=False,
            json=params,
        )
        for response in generator:
            print(response)
            break
        else:
            raise Exception(
                "Could not configure the Environment Provider with %r" % params
            )

    def handle(self):  # pylint: disable=duplicate-code
        """Handle this tester."""
        raise NotImplementedError

    @property
    def gql_response(self):
        """GQL response for artifact created and published events."""
        if self.__gql_response is None:
            request = "search: \"{{'data.identity': {{'$regex': '{}'}}}}\"".format(
                self.params.artifact_identity
            )
            wait_generator = self.etos.utils.wait(
                self.etos.graphql.execute, query=ARTIFACT_REQUEST % request
            )
            for response in wait_generator:
                self.__gql_response = response
                break
        return self.__gql_response

    @property
    def artifact_id(self):
        """Figure out Artifact event ID from event storage."""
        if self.__artifact_id is None:
            try:
                artifact_node = self.gql_response["artifactCreated"]["edges"][0]["node"]
                self.__artifact_id = artifact_node["meta"]["id"]
            except (KeyError, IndexError):
                pass
        return self.__artifact_id
