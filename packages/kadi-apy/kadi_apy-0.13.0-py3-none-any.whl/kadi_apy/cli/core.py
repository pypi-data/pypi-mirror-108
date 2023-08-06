# Copyright 2020 Karlsruhe Institute of Technology
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
from kadi_apy.cli.lib.collections import CLICollection
from kadi_apy.cli.lib.groups import CLIGroup
from kadi_apy.cli.lib.miscellaneous import CLIMiscellaneous
from kadi_apy.cli.lib.records import CLIRecord
from kadi_apy.cli.lib.templates import CLITemplate
from kadi_apy.cli.lib.users import CLIUser
from kadi_apy.cli.search import CLISearchResource
from kadi_apy.cli.search import CLISearchUser
from kadi_apy.globals import Verbose
from kadi_apy.lib.core import KadiManager


class CLIKadiManager(KadiManager):
    """Kadi Manager for the command line interface.

    :param instance: The name of the instance to use in combination with a config file.
    :type instance: str, optional
    :param host: Name of the host.
    :type host: str, optional
    :param token: Personal access token.
    :type token: str, optional
    :param verify: Whether to verify the SSL/TLS certificate of the host.
    :type verify: bool, optional
    :param timeout: Timeout in seconds for the requests.
    :type timeout: float, optional
    :param verbose: Global verbose level to define the amount of prints.
    :type verbose: optional
    """

    def __init__(self, verbose=Verbose.INFO, **kwargs):
        super().__init__(verbose=verbose, **kwargs)

        self._misc = None

    @property
    def misc(self):
        if self._misc is None:
            self._misc = CLIMiscellaneous(self)

        return self._misc

    def record(self, **kwargs):
        """Init a record to be used in a cli.

        :return: The record.
        :rtype: CLIRecord
        """

        return CLIRecord(manager=self, **kwargs)

    def collection(self, **kwargs):
        """Init a collection to be used in a cli.

        :return: The collection.
        :rtype: CLICollection
        """

        return CLICollection(manager=self, **kwargs)

    def group(self, **kwargs):
        """Init a group to be used in a cli.

        :return: The group.
        :rtype: CLIGroup
        """

        return CLIGroup(manager=self, **kwargs)

    def user(self, **kwargs):
        """Init a user to be used in a cli.

        :return: The user.
        :rtype: CLIUser
        """

        return CLIUser(manager=self, **kwargs)

    def template(self, **kwargs):
        """Init a template to be used in a cli.

        :return: The template.
        :rtype: CLITemplate
        """

        return CLITemplate(manager=self, **kwargs)

    def search_resource(self, **kwargs):
        """Init a search to be used for resources in a cli.

        :return: The group.
        :rtype: CLISearchResource
        """

        return CLISearchResource(manager=self, **kwargs)

    def search_user(self, **kwargs):
        """Init a search to be used for users in a cli.

        :return: The group.
        :rtype: CLISearchUser
        """

        return CLISearchUser(manager=self, **kwargs)
