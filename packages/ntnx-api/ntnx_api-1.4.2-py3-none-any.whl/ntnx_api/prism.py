#!/usr/bin/python
# Copyright: (c) 2020, Ross Davies <davies.ross@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
ntnx_api.prism
--------------

Config
^^^^^^
.. autoclass:: ntnx_api.prism.Config
    :members:

Cluster
^^^^^^^
.. autoclass:: ntnx_api.prism.Cluster
    :members:

Hosts
^^^^^
.. autoclass:: ntnx_api.prism.Hosts
    :members:

Vms
^^^
.. autoclass:: ntnx_api.prism.Vms
   :members:

Images
^^^^^^
.. autoclass:: ntnx_api.prism.Images
    :members:

Network
^^^^^^^
.. autoclass:: ntnx_api.prism.Network
    :members:

NetworkSwitch
^^^^^^^^^^^^^
.. autoclass:: ntnx_api.prism.NetworkSwitch
    :members:

StoragePool
^^^^^^^^^^^^^^^^
.. autoclass:: ntnx_api.prism.StoragePool
    :members:

StorageContainer
^^^^^^^^^^^^^^^^
.. autoclass:: ntnx_api.prism.StorageContainer
    :members:

StorageVolume
^^^^^^^^^^^^^
.. autoclass:: ntnx_api.prism.StorageVolume
    :members:
"""

from __future__ import (absolute_import, division, print_function)
import collections
from deprecated.sphinx import deprecated, versionadded, versionchanged
import logging
import logging.config
import time
from random import random
import threading
import paramiko
import os
import bitmath
import base64

__metaclass__ = type

DOCUMENTATION = r'''
    name: nutanix_api.prism
    author:
        - Ross Davies <davies.ross@gmail.com>

    short_description: Get & update data from Prism Element & Prism Central

    description:
        - Retrieve data from the API for the following API components
            - Prism UI
            - Prism Central Categories
            - Prism Central Tags
            - Clusters
            - Hosts
            - Images
            - Virtual Machines
            - Storage
                - Containers
                - Volume Groups

    requirements:
        - "python >= 3.5"
'''

EXAMPLES = r'''
'''


# Setup logging
logger = logging.getLogger('ntnx_api.client')
logging_level = os.environ.get('NTNX_API_LOG_LEVEL', 'WARNING').upper()
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,  # this fixes the problem
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'ntnx_api.prism': {
            'level': logging_level,
            'class': 'logging.StreamHandler',
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
    },
    'loggers': {
        '': {
            'handlers': ['ntnx_api.prism'],
            'level': 'INFO',
            'propagate': True
        }
    }
})


class Config(object):
    """A class to represent the configuration of the Nutanix Prism Instance

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        logger = logging.getLogger('ntnx_api.prism.Config.__init__')
        self.api_client = api_client
        self.categories = []
        self.category_keys = []
        self.projects = []
        self.ui_config = {}
        self.pulse = {}
        self.smtp = {}
        self.auth_types = {}
        self.auth_directories = {}
        self.auth_dir_role_mappings = {}
        self.local_users = {}
        self.alert_config = {}
        self.auth_config = {}
        self.ntp_servers = {}
        self.dns_servers = {}
        self.proxy = {}
        self.protection_rules = {}

    def get_ui_config(self, clusteruuid=None):
        """Get the configuration data for a clusters Prism Element user interface

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_ui_config')
        params = {}
        payload = None
        uri = '/application/system_data'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.ui_config = self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params)
        return self.ui_config[clusteruuid]

    def get_categories(self):
        """Retrieve data for all categories.

        .. note:: Will only return data when `connection_type=='pc'`
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_categories')
        params = {}

        if self.api_client.connection_type == "pc":
            uri = '/categories/list'
            payload = {
                "kind": "category",
                "offset": 0,
                "length": 2147483647
            }
            self.categories = self.api_client.request(uri=uri, payload=payload, params=params).get(
                'entities')

        else:
            # pe does not have category data
            self.categories = {}

        return self.categories

    def get_category_keys(self, category):
        """Retrieve data for all keys belonging to a specific category.

        :param category: Category name
        :type category: str

        .. note:: Will only return data when `connection_type=='pc'`
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_category_keys')
        params = {}

        if self.api_client.connection_type == "pc":
            uri = '/categories/{0}/list'.format(category)
            payload = {
                "kind": "category",
                "offset": 0,
                "length": 2147483647
            }
            self.category_keys = self.api_client.request(uri=uri, payload=payload, params=params).get(
                'entities')

        else:
            # pe does not expose category data
            self.category_keys = {}

        return self.category_keys

    def get_category_key_usage(self, category, key):
        """Retrieve data for all vms or hosts belonging to a specific category & key.

        :parameter category: Category name
        :type category: str
        :parameter key: Key name
        :type key: str

        .. note::
            Will only return data when `connection_type=='pc'`
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_category_key_usage')
        params = {}
        result = []

        if self.api_client.connection_type == "pc":
            uri = '/category/query'
            payload = {
                "group_member_count": 2147483647,
                "group_member_offset": 0,
                "usage_type": "APPLIED_TO",
                "category_filter": {
                    "type": "CATEGORIES_MATCH_ANY",
                    "kind_list": ["vm", "host"],
                    "params": {
                        category: key
                    }
                }
            }
            matches = self.api_client.request(uri=uri, payload=payload, params=params).get(
                'results')

            for match in matches:
                for kind_reference in match.get('kind_reference_list'):
                    item = {
                        "name": kind_reference.get('name'),
                        "uuid": kind_reference.get('uuid'),
                        "type": match.get('kind')
                    }
                    result.append(item)

        else:
            # pe does not expose category data
            pass

        return result

    def get_projects(self):
        """Retrieve data for all projects.

        .. note:: Will only return data when `connection_type=='pc'`
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_projects')
        params = {}
        self.projects = {}

        if self.api_client.connection_type == "pc":
            uri = '/projects/list'
            payload = {
                "kind": "project",
                "offset": 0,
                "length": 2147483647
            }
            self.projects = self.api_client.request(uri=uri, payload=payload, params=params).get('entities')

        return self.projects

    def get_project_usage(self, project_name):
        """Retrieve vms that belong to a specific project.

        :param project_name: Project name
        :type project_name: str

        .. note:: Will only return data when `connection_type=='pc'`
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_project_usage')
        params = {}
        result = []

        if self.api_client.connection_type == "pc":
            uri = '/vms/list'
            payload = {
                "kind": "vm",
                "offset": 0,
                "length": 2147483647
            }
            vms = self.api_client.request(uri=uri, payload=payload, params=params)

            for vm in vms:
                if vm.get('metadata'):
                    project_kind = vm.get('metadata').get('project_reference').get('kind')
                    vm_project_name = vm.get('metadata').get('project_reference').get('name')
                    if 'project_reference' in vm.get('metadata') and project_kind == 'project' and \
                            vm_project_name == project_name:
                        item = {
                            'name': vm.get('status').get('name'),
                            'uuid': vm.get('metadata').get('uuid')
                        }
                        result.append(item)

        return result

    def _add_ui_setting(self, setting_type, setting_key, setting_value, clusteruuid=None):
        """Add UI setting for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type setting_type: UI setting type
        :type setting_type: str
        :type setting_key: UI setting key
        :type setting_key: str
        :type setting_value: UI setting value
        :type setting_value: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config._add_ui_setting')
        params = {}
        uri = '/application/system_data'
        method = 'POST'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        payload = {
            'type': setting_type,
            'key': setting_key,
            'value': setting_value,
        }
        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def _update_ui_setting(self, setting_type, setting_key, setting_value, clusteruuid=None):
        """Update UI setting for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type setting_type: UI setting type
        :type setting_type: str
        :type setting_key: UI setting key
        :type setting_key: str
        :type setting_value: UI setting value
        :type setting_value: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config._update_ui_setting')
        params = {}
        uri = '/application/system_data'
        method = 'PUT'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        payload = {
            'type': setting_type,
            'key': setting_key,
            'value': setting_value,
        }
        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    # UI color
    def get_ui_color(self, clusteruuid=None):
        """Get UI color 1 and color 2 for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dict with the defined UI colors `{'color1': '#CC6164', 'color2':'#FFD055'}` or None
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_ui_color')
        result = None

        if self.ui_config.get(clusteruuid):
            self.get_ui_config(clusteruuid=clusteruuid)

        color1 = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "CUSTOM_LOGIN_SCREEN" and item["key"] == 'color_in').get('value')
        color2 = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "CUSTOM_LOGIN_SCREEN" and item["key"] == 'color_out').get('value')

        if color1 or color2:
            result = {
                'color1': color1,
                'color2': color2,
            }

        return result

    def set_ui_color(self, color1, color2, clusteruuid=None):
        """Set UI color 1 and color 2 for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type color1: First color value to set
        :type color1: str
        :type color2: Second color value to set
        :type color2: str

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_ui_color')
        result = None

        ui_colors = self.get_ui_color(clusteruuid=clusteruuid)
        if ui_colors.get('color1') and ui_colors.get('color1') != color2:
            self._update_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='color_in', setting_value=color1, clusteruuid=clusteruuid)
            result = 'updated'

        elif ui_colors.get('color2') and ui_colors.get('color2') != color2:
            self._update_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='color_out', setting_value=color2, clusteruuid=clusteruuid)
            result = 'updated'

        else:
            self._add_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='color_in', setting_value=color1, clusteruuid=clusteruuid)
            self._add_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='color_out', setting_value=color2, clusteruuid=clusteruuid)
            result = 'added'

        if result:
            self.get_ui_config(clusteruuid=clusteruuid)

        return result

    # UI title & blurb
    def get_ui_text(self, clusteruuid=None):
        """Get UI text (title/blurb) for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dict with the defined UI text `{'title': 'blah', 'blurb':'blah blah'}` or None
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_ui_text')
        result = None

        if self.ui_config.get(clusteruuid):
            self.get_ui_config(clusteruuid=clusteruuid)

        title = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "CUSTOM_LOGIN_SCREEN" and item["key"] == 'product_title').get('value')
        blurb = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "CUSTOM_LOGIN_SCREEN" and item["key"] == 'title').get('value')

        if title or blurb:
            result = {
                'title': title,
                'blurb': blurb,
            }

        return result

    def set_ui_text(self, title, blurb, clusteruuid=None):
        """Set UI text (title/blurb) for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type title: Logon UI title text (Above the username/password field)
        :type title: str
        :type blurb: Logon UI blurb text (Below the username/password field)
        :type blurb: str

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_ui_text')
        result = None
        ui_text = self.get_ui_text(clusteruuid=clusteruuid)

        if ui_text.get('title') and ui_text.get('title') != title:
            self._update_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='product_title', setting_value=title, clusteruuid=clusteruuid)
            result = 'updated'
        else:
            self._add_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='product_title', setting_value=blurb, clusteruuid=clusteruuid)
            result = 'added'

        if ui_text.get('blurb') and ui_text.get('blurb') != blurb:
            self._update_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='title', setting_value=blurb, clusteruuid=clusteruuid)
            result = 'updated'
        else:
            self._add_ui_setting(setting_type='CUSTOM_LOGIN_SCREEN', setting_key='title', setting_value=blurb, clusteruuid=clusteruuid)
            result = 'added'

        if result:
            self.get_ui_config(clusteruuid=clusteruuid)

        return result

    # UI logon banner
    def get_ui_banner(self, clusteruuid=None):
        """Get UI text (title/blurb) for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dict with the defined UI banner `{'status': 'true', 'content':'blah blah'}` or None
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_ui_banner')
        result = None

        if self.ui_config.get(clusteruuid):
            self.get_ui_config(clusteruuid=clusteruuid)

        status = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "WELCOME_BANNER" and
                      item["key"] == 'welcome_banner_status').get('value')
        content = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "WELCOME_BANNER" and
                       item["key"] == 'welcome_banner_content').get('value')

        if status or content:
            result = {
                'status': status,
                'content': content,
            }

        return result

    def set_ui_banner(self, status, content, clusteruuid=None):
        """Set UI welcome banner (title/blurb) for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type status: Logon UI banner status
        :type status: bool
        :type content: Logon UI banner content
        :type content: str

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_ui_banner')
        result = None

        ui_banner = self.get_ui_banner(clusteruuid=clusteruuid)
        if ui_banner.get('status') and ui_banner.get('status') != status:
            self._update_ui_setting(setting_type='WELCOME_BANNER', setting_key='welcome_banner_status', setting_value=str(status), clusteruuid=clusteruuid)
            result = 'updated'
        else:
            self._add_ui_setting(setting_type='WELCOME_BANNER', setting_key='welcome_banner_status', setting_value=str(status), clusteruuid=clusteruuid)
            result = 'added'

        if ui_banner.get('content') and ui_banner.get('content') != content:
            self._update_ui_setting(setting_type='WELCOME_BANNER', setting_key='welcome_banner_content', setting_value=content, clusteruuid=clusteruuid)
            result = 'updated'
        else:
            self._add_ui_setting(setting_type='WELCOME_BANNER', setting_key='welcome_banner_content', setting_value=content, clusteruuid=clusteruuid)
            result = 'added'

        if result:
            self.get_ui_config(clusteruuid=clusteruuid)

        return result

    # UI 2048 game
    def get_ui_2048_game(self, clusteruuid=None):
        """Get UI 2048 game status for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dict with the defined UI 2048 game setting `{'status': 'true'}` or None
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_ui_2048_game')
        result = None

        if self.ui_config.get(clusteruuid):
            self.get_ui_config(clusteruuid=clusteruuid)

        status = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "UI_CONFIG" and item["key"] == 'disable_2048').get('value')

        if status:
            result = {
                'status': True,
            }
        else:
            result = {
                'status': False,
            }

        return result

    def set_ui_2048_game(self, status, clusteruuid=None):
        """Set UI 2048 game status for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type status: 2048 game status
        :type status: bool

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_ui_2048_game')
        result = None

        ui_2048_status = self.get_ui_2048_game(clusteruuid=clusteruuid)
        if ui_2048_status.get('status') and ui_2048_status.get('status') != status:
            self._update_ui_setting(setting_type='UI_CONFIG', setting_key='disable_2048', setting_value=str(status).lower(), clusteruuid=clusteruuid)
            result = 'updated'
        else:
            self._add_ui_setting(setting_type='UI_CONFIG', setting_key='disable_2048', setting_value=str(status).lower(), clusteruuid=clusteruuid)
            result = 'added'

        if result:
            self.get_ui_config(clusteruuid=clusteruuid)

        return result

    # UI animation
    def get_ui_animation(self, clusteruuid=None):
        """Get UI animated background particles status for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dict with the defined UI particle animation setting `{'status': 'true'}` or None
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_ui_animation')
        result = None

        if self.ui_config.get(clusteruuid):
            self.get_ui_config(clusteruuid=clusteruuid)

        status = next(item for item in self.ui_config.get(clusteruuid) if item["type"] == "WELCOME_BANNER" and item["key"] == 'disable_video').get('value')

        if status:
            result = {
                'status': True,
            }
        else:
            result = {
                'status': False,
            }

        return result

    def set_ui_animation(self, status, clusteruuid=None):
        """Set UI animated background particles status for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type status: animated background particle status
        :type status: bool

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_ui_animation')
        result = None

        ui_animation_status = self.get_ui_animation(clusteruuid=clusteruuid)
        if ui_animation_status.get('status') and ui_animation_status.get('status') != status:
            self._update_ui_setting(setting_type='welcome_banner', setting_key='disable_video', setting_value=str(status).lower(), clusteruuid=clusteruuid)
            result = 'updated'
        else:
            self._add_ui_setting(setting_type='welcome_banner', setting_key='disable_video', setting_value=str(status).lower(), clusteruuid=clusteruuid)
            result = 'added'

        if result:
            self.get_ui_config(clusteruuid=clusteruuid)

        return result

    def get_pulse(self, clusteruuid=None):
        """Get pulse config for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dictionary describing pulse configuration from the specified cluster.
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_pulse')
        params = {}
        payload = None
        uri = '/pulse'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.pulse[clusteruuid] = self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params)
        return self.pulse[clusteruuid]

    def update_pulse(self, enable, email_address_list=None, email_nutanix=False, clusteruuid=None):
        """Get pulse config for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        """
        logger = logging.getLogger('ntnx_api.prism.Config.update_pulse')
        params = {}
        uri = '/pulse'
        method = 'PUT'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        payload = {
            'enable': enable,
            'enableDefaultNutanixEmail': email_nutanix,
            'emailContactList': email_address_list,
        }
        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def set_pulse(self, enable, email_address_list=None, email_nutanix=False, clusteruuid=None):
        """Set UI animated background particles status for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type enable: Pulse enabled
        :type enable: bool
        :type email_address_list: animated background particle status
        :type email_address_list: list, optional
        :type email_nutanix: Send pulse data to nutnaix via email
        :type email_nutanix: bool, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_pulse')
        result = None

        if self.pulse.get(clusteruuid):
            self.get_pulse(clusteruuid=clusteruuid)

        if bool(self.pulse.get(clusteruuid).get('enable')) != enable or \
                bool(self.pulse.get(clusteruuid).get('enableDefaultNutanixEmail')) != email_nutanix or \
                self.pulse.get(clusteruuid).get('emailContactList') != email_address_list:
            self.update_pulse(enable=enable, email_nutanix=email_nutanix, email_address_list=email_address_list, clusteruuid=clusteruuid)
            result = 'updated'

        if result:
            self.get_pulse(clusteruuid=clusteruuid)

        return result

    def get_smtp(self, clusteruuid=None):
        """Get smtp config for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dictionary describing smtp configuration from the specified cluster.
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_smtp')
        params = {}
        payload = None
        uri = '/cluster/smtp'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.smtp[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.smtp[clusteruuid]

    @staticmethod
    def _get_smtp_mode(mode):
        """Return smtp mode string based on boolean value

        :param mode: SMTP mode
        :type mode: str('tls', 'ssl', None)

        :returns: Text for API smtp mode type variable defined by supplied boolean variable.
        :rtype: Str
        """
        logger = logging.getLogger('ntnx_api.prism.Config._get_smtp_mode')

        modes = {
            'tls': 'STARTTLS',
            'ssl': 'SSL',
            None: 'NONE',
        }

        return modes[mode]

    def update_smtp(self, address, from_email_address, port, secure_mode=None, username=None, password=None, clusteruuid=None):
        """Update smtp config for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param address:
        :type address: str
        :param from_email_address:
        :type from_email_address: str
        :param port:
        :type port: int
        :param secure_mode:
        :type secure_mode: str, optional
        :param username:
        :type username: str, optional
        :param password:
        :type password: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.update_smtp')
        params = {}
        uri = '/cluster/smtp'
        method = 'PUT'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        payload = {
            'address': address,
            'from_email_address': from_email_address,
            'port': port,
            'secure_mode': self._get_smtp_mode(secure_mode),
        }

        if secure_mode and ((username and not password) or (password and not username)):
            raise ValueError('Secure mode defined but both username and password not provided.')
        else:
            payload['username'] = username
            payload['password'] = password

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def remove_smtp(self, clusteruuid=None):
        """Remove smtp config for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.remove_smtp')
        params = {}
        uri = '/cluster/smtp'
        method = 'DELETE'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def set_smtp(self, address, port, mode=None, from_email_address='do-not-reply@nutanix.cluster', username=None, password=None, force=False,
                 clusteruuid=None):
        """Set smtp config for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param address: SMTP server IP address or FQDN
        :type address: str
        :param port: SMTP server port
        :type port: int
        :param mode: SMTP connection mode
        :type mode: str('tls', 'ssl', None), optional
        :param from_email_address: Email address to send alerts from `(default: do-not-reply@nutanix.cluster)`
        :type from_email_address: str, optional
        :param username: Username to authenticate to the SMTP server
        :type username: str, optional
        :param password: Password for user to authenticate to the SMTP server
        :type password: str, optional
        :param force: Force update regardless of differences `(default=False)`
        :type force: bool, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_smtp')
        result = None

        if not self.smtp.get(clusteruuid):
            self.get_smtp(clusteruuid=clusteruuid)

        if mode and mode not in ('tls', 'ssl'):
            raise ValueError('smtp mode needs to be "tls", "ssl" or None.')

        if mode in ('tls', 'ssl') and not username and not password:
            raise ValueError('smtp modes "tls" and "ssl" require authentication. Provide a username & password.')

        # If SNMP not defined
        if not mode:
            if (self.smtp.get(clusteruuid).get('address') and self.smtp.get(clusteruuid).get('from_email_address') and self.smtp.get(clusteruuid).get(
                    'port')) or \
                    self.smtp.get(clusteruuid).get('address') != address or \
                    self.smtp.get(clusteruuid).get('from_email_address') != from_email_address or \
                    self.smtp.get(clusteruuid).get('port') != port:
                self.update_smtp(address, from_email_address, port, secure_mode=mode, username=username, password=password, clusteruuid=clusteruuid)
                result = 'updated'

        else:
            if (self.smtp.get(clusteruuid).get('address') and self.smtp.get(clusteruuid).get('from_email_address') and self.smtp.get(clusteruuid).get(
                    'port')) or \
                    self.smtp.get(clusteruuid).get('address') != address or \
                    self.smtp.get(clusteruuid).get('from_email_address') != from_email_address or \
                    self.smtp.get(clusteruuid).get('port') != port or \
                    self.smtp.get(clusteruuid).get('secure_mode') != self._get_smtp_mode(mode) or \
                    self.smtp.get(clusteruuid).get('username') != username:
                self.update_smtp(address, from_email_address, port, secure_mode=mode, username=username, password=password, clusteruuid=clusteruuid)
                result = 'added'

        if result:
            self.get_smtp(clusteruuid=clusteruuid)

        return result

    def get_auth_types(self, clusteruuid=None):
        """Get authentication types for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_auth_types')
        params = {}
        uri = '/authconfig/auth_types'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.auth_types[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.auth_types[clusteruuid]

    def get_auth_dirs(self, clusteruuid=None):
        """Get authentication directories for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_auth_dirs')
        params = {}
        uri = '/authconfig/directories'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.auth_directories[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.auth_directories[clusteruuid]

    @staticmethod
    def _get_group_search_type(recursive):
        """Return group search string based on boolean value

        :param recursive: Recursive search
        :type recursive: bool

        :returns: Text for API group search type variable defined by supplied boolean variable.
        :rtype: Str
        """
        logger = logging.getLogger('ntnx_api.prism.Config._get_group_search_type')
        group_search_type = {
            True: 'RECURSIVE',
            False: 'NON_RECURSIVE',
        }

        return group_search_type[recursive]

    def add_auth_dir(self, name, directory_url, domain, username, password, recursive=False, directory_type='LDAP', connection_type='LDAP',
                     clusteruuid=None):
        """Add authentication directory for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: Directory name
        :type name: str, optional
        :param directory_url: ldap/ldaps URL to connect to the domain including the port your LDAP target is listening on. eg ldap://192.168.1.10:384
        :type directory_url: str
        :param domain: Fully qualified name of the domain. eg nutanix.local
        :type domain: str
        :param username: Username to authenticate to the domain
        :type username: str
        :param password: Password for user to authenticate to the domain
        :type password: str
        :param recursive: Whether to search for nested groups
        :type recursive: bool, optional
        :param directory_type: Type of directory
        :type directory_type: str('ACTIVE_DIRECTORY', 'OPEN_LDAP'), optional
        :param connection_type: Type of connection
        :type connection_type: str('LDAP'), optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.add_auth_dir')
        params = {}
        uri = '/authconfig/directories'
        method = 'POST'

        if connection_type not in ['LDAP']:
            raise ValueError('Only "LDAP" connection types allowed.')

        if directory_type not in ['ACTIVE_DIRECTORY', 'OPEN_LDAP']:
            raise ValueError('Only "ACTIVE_DIRECTORY" and "OPEN_LDAP" directory types allowed.')

        payload = {
            'connection_type': connection_type,
            'directory_type': directory_type,
            'directory_url': directory_url,
            'domain': domain,
            'group_search_type': self._get_group_search_type(recursive=recursive),
            'name': name,
            'service_account_username': username,
            'service_account_password': password,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def update_auth_dir(self, name, directory_type, directory_url, domain, username, password, recursive=False, connection_type='LDAP', clusteruuid=None):
        """Update authentication directory for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: Directory name
        :type name: str, optional
        :param directory_url: ldap/ldaps URL to connect to the domain including the port your LDAP target is listening on. eg ldap://192.168.1.10:384
        :type directory_url: str
        :param domain: Fully qualified name of the domain. eg nutanix.local
        :type domain: str
        :param username: Username to authenticate to the domain
        :type username: str
        :param password: Password for user to authenticate to the domain
        :type password: str
        :param recursive: Whether to search for nested groups
        :type recursive: bool, optional
        :param directory_type: Type of directory
        :type directory_type: str('ACTIVE_DIRECTORY', 'OPEN_LDAP'), optional
        :param connection_type: Type of connection
        :type connection_type: str('LDAP'), optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.update_auth_dir')
        params = {}
        uri = '/authconfig/directories'
        method = 'PUT'

        if not any(name or directory_url or domain or username or password):
            raise ValueError('Please provide all non-optional variables.')

        if connection_type not in ['LDAP']:
            raise ValueError('Only "LDAP" connection types allowed.')

        if directory_type not in ['ACTIVE_DIRECTORY', 'OPEN_LDAP']:
            raise ValueError('Only "ACTIVE_DIRECTORY" and "OPEN_LDAP" directory types allowed.')

        payload = {
            'connection_type': connection_type,
            'directory_type': directory_type,
            'directory_url': directory_url,
            'domain': domain,
            'group_search_type': self._get_group_search_type(recursive=recursive),
            'name': name,
            'service_account_username': username,
            'service_account_password': password,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def remove_auth_dir(self, name, clusteruuid=None):
        """Remove authentication directory for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: Directory name
        :type name: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.remove_auth_dir')
        params = {}
        uri = '/authconfig/directories/{0}'.format(name)
        method = 'DELETE'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid
        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def set_auth_dir(self, name, directory_type, directory_url, domain, username, password, recursive=False, connection_type='LDAP', force=False,
                     clusteruuid=None):
        """Set authentication directory for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: Directory name
        :type name: str, optional
        :param directory_url: ldap/ldaps URL to connect to the domain including the port your LDAP target is listening on. eg ldap://192.168.1.10:384
        :type directory_url: str
        :param domain: Fully qualified name of the domain. eg nutanix.local
        :type domain: str
        :param username: Username to authenticate to the domain
        :type username: str
        :param password: Password for user to authenticate to the domain
        :type password: str
        :param recursive: Whether to search for nested groups  `(default: False)`
        :type recursive: bool, optional
        :param directory_type: Type of directory
        :type directory_type: str('ACTIVE_DIRECTORY', 'OPEN_LDAP'), optional
        :param connection_type: Type of connection `(default: 'LDAP')`
        :type connection_type: str('LDAP'), optional
        :param force: Force directory update. Use this to update the password of the auth domain user.
        :type force: bool, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_auth_dir')
        result = None

        if not self.auth_directories.get(clusteruuid):
            self.get_auth_dirs(clusteruuid=clusteruuid)

        group_search_type = {
            True: 'RECURSIVE',
            False: 'NON_RECURSIVE',
        }

        # If no directories defined
        if len(self.auth_directories.get(clusteruuid)) == 0:
            self.add_auth_dir(name=name, directory_url=directory_url, domain=domain, username=username, password=password,
                              recursive=recursive, directory_type=directory_type, connection_type=connection_type)

            self.get_auth_dirs(clusteruuid=clusteruuid)
            result = 'added'

        # Update defined directory
        elif len(self.auth_directories.get(clusteruuid)) == 1 and \
                any(item for item in self.auth_directories.get(clusteruuid) if item['name'] == name and
                                                                               (item.get('directory_type') != directory_type or
                                                                                item.get('directory_url') != directory_url or
                                                                                item.get('domain') != domain or
                                                                                item.get('service_account_username') != username or
                                                                                item.get('group_search_type') == group_search_type[recursive] or
                                                                                item.get('connection_type') == connection_type
                                                                               ) or force
                    ):
            self.update_auth_dir(name=name, directory_url=directory_url, domain=domain, username=username, password=password,
                                 recursive=recursive, directory_type=directory_type, connection_type=connection_type)
            self.get_auth_dirs(clusteruuid=clusteruuid)
            result = 'updated'

        # More than 1 directory defined
        elif not len(self.auth_directories.get(clusteruuid)) > 1:
            pass

        if result:
            self.get_auth_dirs(clusteruuid=clusteruuid)

        return result

    def get_auth_dir_role_mappings(self, clusteruuid=None):
        """Get all authentication role mappings for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_auth_dir_role_mappings')
        role_mappings = []
        params = {}
        payload = None

        if not self.auth_directories.get(clusteruuid):
            self.get_auth_dirs(clusteruuid=clusteruuid)

        for directory in self.auth_directories.get(clusteruuid):
            uri = '/authconfig/directories/{0}/role_mappings'.format(directory.get('name'))

            if clusteruuid:
                params['proxyClusterUuid'] = clusteruuid

            role_mapping = self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params)
            if role_mapping:
                role_mappings.extend(role_mapping)

        self.auth_dir_role_mappings[clusteruuid] = role_mappings
        return self.auth_dir_role_mappings[clusteruuid]

    @staticmethod
    def _check_auth_dir_role_mapping_directory_entity_type(directory_entity_type):
        """Check directory_entity_type string is correct

        :param directory_entity_type: Type of directory entity being added.
        :type directory_entity_type: str('USER', 'GROUP')
        """
        logger = logging.getLogger('ntnx_api.prism.Config._check_auth_dir_role_mapping_directory_entity_type')
        if directory_entity_type.upper() not in ['GROUP', 'USER']:
            raise ValueError('directory_entity_type has to be set to one of "GROUP", "USER".')

    @staticmethod
    def _get_auth_dir_role_mapping_role(cluster_admin, user_admin):
        """Return the role string based on `cluster_admin` and `user_admin` boolean inputs. `ROLE_CLUSTER_VIEWER` is always added to a user
        while `ROLE_CLUSTER_ADMIN` and `ROLE_USER_ADMIN` are optional based on inputs.

        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional

        :returns: Role based on boolean inputs.
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config._get_auth_dir_role_mapping_role')
        if user_admin:
            role = 'ROLE_USER_ADMIN'
        elif cluster_admin:
            role = 'ROLE_CLUSTER_ADMIN'
        else:
            role = 'ROLE_CLUSTER_VIEWER'

        return role

    @staticmethod
    def _check_auth_dir_role_mapping_role(mapping_role):
        """Check mapping_role string is correct

        :param mapping_role: Type of directory entity being added.
        :type mapping_role: str('ROLE_USER_ADMIN', 'ROLE_CLUSTER_ADMIN', 'ROLE_CLUSTER_VIEWER')
        """
        logger = logging.getLogger('ntnx_api.prism.Config._check_auth_dir_role_mapping_role')
        if mapping_role.upper() not in ['ROLE_USER_ADMIN', 'ROLE_CLUSTER_ADMIN', 'ROLE_CLUSTER_VIEWER']:
            raise ValueError('directory_entity_type has to be set to one of "ROLE_USER_ADMIN", "ROLE_CLUSTER_ADMIN", "ROLE_CLUSTER_VIEWER".')

    def add_auth_dir_role_mapping(self, directory, directory_entities, directory_entity_type, cluster_admin=False, user_admin=False, clusteruuid=None):
        """Add authentication role mapping for a named authentication directory on a specific cluster. If either `cluster_admin` or `user_admin` is not set the role granted to
        this user is `ROLE_CLUSTER_VIEWER`.

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param directory: Name of directory.
        :type directory: str
        :param directory_entities: List of users/groups to add.
        :type directory_entities: list of str
        :param directory_entity_type: Type of directory entity being added.
        :type directory_entity_type: str('USER', 'GROUP')
        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.add_auth_dir_role_mapping')
        params = {}
        uri = '/authconfig/directories/{0}/role_mappings'.format(directory)
        method = 'POST'

        self._check_auth_dir_role_mapping_directory_entity_type(directory_entity_type.upper())
        role = self._get_auth_dir_role_mapping_role(user_admin=user_admin, cluster_admin=cluster_admin)

        payload = {
            'directoryName': directory,
            'entityType': directory_entity_type.upper(),
            'entityValues': directory_entities,
            'role': role,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def update_auth_dir_role_mapping(self, directory, directory_entities, directory_entity_type, cluster_admin=False, user_admin=False, clusteruuid=None):
        """Update authentication role mapping for a named authentication directory on a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param directory: Name of directory.
        :type directory: str
        :param directory_entities: List of users/groups to add.
        :type directory_entities: list of str
        :param directory_entity_type: Type of directory entity being added.
        :type directory_entity_type: str('USER', 'GROUP')
        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.update_auth_dir_role_mapping')
        params = {}
        uri = '/authconfig/directories/{0}/role_mappings'.format(directory)
        method = 'PUT'

        self._check_auth_dir_role_mapping_directory_entity_type(directory_entity_type.upper())
        role = self._get_auth_dir_role_mapping_role(user_admin=user_admin, cluster_admin=cluster_admin)

        payload = {
            'directoryName': directory,
            'entityType': directory_entity_type.upper(),
            'entityValues': directory_entities,
            'role': role,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def remove_auth_dir_role_mapping(self, directory, directory_entities, directory_entity_type, cluster_admin=False, user_admin=False, clusteruuid=None):
        """Delete authentication role mapping for a named authentication directory on a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type clusteruuid: str, optional
        :param directory: Name of directory.
        :type directory: str
        :param directory_entities: List of users/groups to add.
        :type directory_entities: list of str
        :param directory_entity_type: Type of directory entity being added.
        :type directory_entity_type: str('USER', 'GROUP')
        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.remove_auth_dir_role_mapping')
        params = {}
        uri = '/authconfig/directories/{0}/role_mappings'.format(directory)
        method = 'DELETE'

        self._check_auth_dir_role_mapping_directory_entity_type(directory_entity_type.upper())
        # self._check_auth_dir_role_mapping_role(mapping_role.upper())
        role = self._get_auth_dir_role_mapping_role(user_admin=user_admin, cluster_admin=cluster_admin)

        payload = {
            'directoryName': directory,
            'entityType': directory_entity_type.upper(),
            'entityValues': directory_entities,
            'role': role,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def set_auth_dir_role_mapping(self, directory, directory_entities, directory_entity_type, cluster_admin=False, user_admin=False, clusteruuid=None):
        """Create or update authentication role mapping for a named authentication directory on a specific cluster.

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param directory: Name of directory.
        :type directory: str
        :param directory_entities: List of users/groups to add.
        :type directory_entities: list of str
        :param directory_entity_type: Type of directory entity being added.
        :type directory_entity_type: str('USER', 'GROUP')
        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_auth_dir_role_mapping')
        result = None

        role = self._get_auth_dir_role_mapping_role(user_admin=user_admin, cluster_admin=cluster_admin)

        # Check whether directory exists
        self.get_auth_dirs(clusteruuid=clusteruuid)
        if not self.auth_directories.get(clusteruuid) or \
                self.auth_directories.get(clusteruuid)[0].get('name') != directory:
            raise ValueError('Directory does not exist. Please create the directory prior to adding mappings.')

        # Check whether directory mapping exists
        if not self.auth_dir_role_mappings.get(clusteruuid):
            self.get_auth_dir_role_mappings(clusteruuid=clusteruuid)

        # Check whether directory name & role exists
        role_mapping = next((item for item in self.auth_dir_role_mappings.get(clusteruuid) if item["directoryName"] == directory and
                             item["entityType"] == directory_entity_type and item["role"] == role), None)

        # Create new role_mapping
        if not role_mapping:
            self.add_auth_dir_role_mapping(directory=directory, directory_entities=directory_entities, directory_entity_type=directory_entity_type,
                                           cluster_admin=cluster_admin, user_admin=user_admin, clusteruuid=clusteruuid)
            result = 'added'
            self.get_auth_dir_role_mappings(clusteruuid=clusteruuid)

        # Update existing role mapping
        elif role_mapping.get('entityType') == directory_entity_type or not all(elem in role_mapping.get('entityValues') for elem in directory_entities):
            self.update_auth_dir_role_mapping(directory=directory, directory_entities=directory_entities, directory_entity_type=directory_entity_type,
                                              cluster_admin=cluster_admin, user_admin=user_admin, clusteruuid=clusteruuid)
            result = 'updated'
            self.get_auth_dir_role_mappings(clusteruuid=clusteruuid)

        if result:
            self.get_auth_dir_role_mappings(clusteruuid=clusteruuid)

        return result

    def get_local_users(self, clusteruuid=None):
        """Get local users on a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_local_users')
        params = {}
        uri = '/users'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.local_users[clusteruuid] = self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params)
        return self.local_users[clusteruuid]

    @staticmethod
    def _check_user_language(language):
        """Check language string is correct

        :param language: Localization region for user account `(default='en-US')`
        :type language: str('en-US','zh-CN','ja-JP'), optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config._check_user_language')

        if language not in ['en-US', 'zh-CN', 'ja-JP']:
            raise ValueError('Region has to be set to one of "en-US", "zh-CN", "ja-JP".')

    @staticmethod
    def _build_role_list(cluster_admin=False, user_admin=False):
        """Build list of roles for user based on boolean inputs. `ROLE_CLUSTER_VIEWER` is always added to a user
        while `ROLE_CLUSTER_ADMIN` and `ROLE_USER_ADMIN` are optional based on inputs.

        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional

        :returns: A list of roles.
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.Config._build_role_list')

        roles = ['ROLE_CLUSTER_VIEWER']
        roles = []
        if cluster_admin or user_admin:
            roles.append('ROLE_CLUSTER_ADMIN')

        if user_admin:
            roles.append('ROLE_USER_ADMIN')

        return roles

    def add_local_user(self, username, password, firstname, lastname, email, enabled=True, cluster_admin=False,
                       user_admin=False, language='en-US', clusteruuid=None):
        """Add local user on a specific cluster. User is added with cluster viewer rights. Additional rights have to be added after the user is created

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param username: Username
        :type username: str
        :param password: Password
        :type password: str
        :param firstname: First name of user
        :type firstname: str, optional
        :param lastname: Last name of user
        :type lastname: str, optional
        :param email: Email address for user
        :type email: str, optional
        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional
        :param language: Localization region for user account `(default='en-US')`
        :type language: str('en-US','zh-CN','ja-JP'), optional
        :param enabled: Enable user account `(default=True)`
        :type enabled: bool, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.add_local_user')
        params = {}
        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        uri = '/users'
        method = 'POST'

        # Add User.
        self._check_user_language(language)
        roles = self._build_role_list(cluster_admin=cluster_admin, user_admin=user_admin)

        payload = {
            'profile': {
                'username': username,
                'firstName': firstname,
                'lastName': lastname,
                'emailId': email,
                'password': password,
                "locale": language,
                "region": language,
            },
            'enabled': enabled,
        }

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

        # Set user roles if not 'ROLE_CLUSTER_VIEWER'
        uri = '/users/{0}/roles'.format(username)
        method = 'PUT'
        payload = roles
        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def update_local_user(self, username, password, firstname, lastname, email, enabled=True, cluster_admin=False,
                          user_admin=False, language='en-US', clusteruuid=None):
        """Update local user on a specific cluster. User is added with cluster viewer rights. Additional rights have to be added after the user is created

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param username: Username
        :type username: str
        :param password: Password
        :type password: str
        :param firstname: First name of user
        :type firstname: str, optional
        :param lastname: Last name of user
        :type lastname: str, optional
        :param email: Email address for user
        :type email: str, optional
        :param cluster_admin: Whether to grant user `Cluster Admin` privilege
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` privilege
        :type user_admin: bool, optional
        :param language: Localization region for user account `(default='en-US')`
        :type language: str('en-US','zh-CN','ja-JP'), optional
        :param enabled: Enable user account `(default=True)`
        :type enabled: bool, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.update_local_user')
        params = {}
        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        uri = '/users'
        method = 'PUT'

        # Update user
        self._check_user_language(language)
        roles = self._build_role_list(cluster_admin=cluster_admin, user_admin=user_admin)
        payload = {
            'profile': {
                'username': username,
                'firstName': firstname,
                'lastName': lastname,
                'emailId': email,
                'password': password,
                "locale": language,
                "region": language,
            },
            'enabled': enabled,
        }

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

        # Update user roles if not 'ROLE_CLUSTER_VIEWER'
        uri = '/users/{0}/roles'.format(username)
        method = 'PUT'
        payload = roles
        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def remove_local_user(self, username, clusteruuid=None):
        """Remove local user on a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param username: Username
        :type username: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.remove_local_user')
        params = {}
        uri = '/users/{0}'.format(username)
        method = 'DELETE'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def set_local_user(self, username, password, firstname, lastname, email, enabled=True, cluster_admin=False,
                       user_admin=False, language='en-US', clusteruuid=None):
        """Create or update local user on a specific cluster. User is added with cluster viewer rights. Additional rights have to be added after the user is created

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param username: Username
        :type username: str
        :param password: Password
        :type password: str
        :param firstname: First name of user
        :type firstname: str, optional
        :param lastname: Last name of user
        :type lastname: str, optional
        :param email: Email address for user
        :type email: str, optional
        :param cluster_admin: Email address for user
        :type cluster_admin: bool, optional
        :param user_admin: Whether to grant user `User Admin` priviliges
        :type user_admin: bool, optional
        :param language: Localization region for user account `(default='en-US')`
        :type language: str('en-US','zh-CN','ja-JP'), optional
        :param enabled: Enable user account `(default=True)`
        :type enabled: bool, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_local_user')
        result = None

        if not self.local_users.get(clusteruuid):
            self.get_local_users(clusteruuid=clusteruuid)

        # find local user in list of local users or None
        local_user = next((item for item in self.local_users.get(clusteruuid) if item.get('profile').get('username') == username), None)

        roles = self._build_role_list(cluster_admin=cluster_admin, user_admin=user_admin)

        # user not found, add user
        if not local_user:
            self.add_local_user(username=username, password=password, firstname=firstname, lastname=lastname, email=email, enabled=enabled,
                                cluster_admin=cluster_admin, user_admin=user_admin, language=language, clusteruuid=None)
            self.get_local_users(clusteruuid=clusteruuid)
            result = 'added'

        # user config does not match, update user
        elif local_user and \
                local_user.get('profile').get('lastName') != lastname or \
                local_user.get('profile').get('emailId') != email or \
                local_user.get('profile').get('locale') != language or \
                local_user.get('profile').get('region') != language or \
                local_user.get('enabled') != enabled or \
                not all(elem in local_user.get('roles') for elem in roles):

            self.update_local_user(username=username, password=password, firstname=firstname, lastname=lastname, email=email, enabled=enabled,
                                   cluster_admin=cluster_admin, user_admin=user_admin, language=language, clusteruuid=None)
            self.get_local_users(clusteruuid=clusteruuid)
            result = 'updated'

        if result:
            self.get_local_users(clusteruuid=clusteruuid)

        return result

    def get_alert_config(self, clusteruuid=None):
        """Get alert configuration for specified cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_alert_config')
        params = {}
        uri = '/alerts/configuration'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.alert_config[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.alert_config[clusteruuid]

    def update_alert_config(self, email_list, enable=True, enable_default=True, enable_digest=True, nutanix_default_email='nos-alerts@nutanix.com',
                            clusteruuid=None):
        """Update alert configuration for specified cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param email_list:
        :type email_list: list of str
        :param enable:
        :type enable: bool, optional
        :param enable_default:
        :type enable_default: bool, optional
        :param enable_digest:
        :type enable_digest: bool, optional
        :param nutanix_default_email:
        :type nutanix_default_email: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.update_alert_config')
        params = {}
        uri = '/alerts/configuration'
        method = 'PUT'

        payload = {
            'default_nutanix_email': nutanix_default_email,
            'enable': enable,
            'enable_default_nutanix_email': enable_default,
            'enable_email_digest': enable_digest,
            'email_contact_list': email_list,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def remove_alert_config(self, clusteruuid=None):
        """Reset alert configuration for specified cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.remove_alert_config')
        email_list = []
        enable = False
        enable_default = False
        enable_digest = False
        self.update_alert_config(email_list, enable, enable_default, enable_digest, clusteruuid)

    def get_auth_config(self, clusteruuid=None):
        """Retrieve authentication data for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional :returns: A list of dictionaries describing the authentication configuration of the cluster.

        :returns: A list of authentication config.
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_auth_config')
        params = {}
        payload = None
        uri = '/authconfig'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.auth_config[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.auth_config[clusteruuid]

    def get_ntp(self, clusteruuid=None):
        """Retrieve ntp servers configured for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of the clusters ntp servers
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_ntp')
        params = {}
        payload = None
        uri = '/cluster/ntp_servers'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        if self.ntp_servers.get(clusteruuid):
            logger.info("cleaning up existing class ntp records")
            self.ntp_servers.pop(clusteruuid)

        self.ntp_servers[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.ntp_servers[clusteruuid]

    def add_ntp(self, ntp_server, clusteruuid=None):
        """Add ntp server to a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type ntp_server: IP address or hostname for a ntp server
        :type ntp_server: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.add_ntp')
        params = {}
        uri = '/cluster/ntp_servers'
        method = 'POST'
        payload = {
            "value": ntp_server
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def remove_ntp(self, ntp_server, clusteruuid=None):
        """Remove ntp server from a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type ntp_server: IP address or hostname for a ntp server
        :type ntp_server: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.remove_ntp')
        params = {}
        payload = None
        uri = '/cluster/ntp_servers/{0}'.format(ntp_server)
        method = 'DELETE'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def set_ntp(self, clusteruuid=None, ntp_servers=None):
        """Set ntp servers for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type ntp_servers: An ordered list of ntp servers
        :type ntp_servers: list, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_ntp')
        result = None

        if not ntp_servers:
            raise ValueError('no ntp server list provided.')

        if not self.ntp_servers.get(clusteruuid):
            self.get_ntp(clusteruuid=clusteruuid)

        # If no NTP servers are defined
        if len(self.ntp_servers.get(clusteruuid)) == 0:
            for ntp_server in ntp_servers:
                self.add_ntp(ntp_server)
            result = 'added'

        # If the NTP servers are not in the right order
        elif not collections.Counter(ntp_servers) == collections.Counter(self.ntp_servers.get(clusteruuid)):
            for ntp_server in self.get_ntp(clusteruuid=clusteruuid):
                self.remove_ntp(ntp_server=ntp_server, clusteruuid=clusteruuid)
            for ntp_server in ntp_servers:
                self.add_ntp(ntp_server=ntp_server, clusteruuid=clusteruuid)
            result = 'updated'

        if result:
            self.get_ntp(clusteruuid=clusteruuid)

        return result

    def get_dns(self, clusteruuid=None):
        """Retrieve dns servers configured for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of the clusters dns servers
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_dns')
        params = {}
        payload = None
        uri = '/cluster/name_servers'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        if self.dns_servers.get(clusteruuid):
            logger.info("cleaning up existing class dns records")
            self.dns_servers.pop(clusteruuid)

        self.dns_servers[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.dns_servers[clusteruuid]

    def add_dns(self, dns_server, clusteruuid=None):
        """Add dns server to a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type dns_server: IP address or hostname for a dns server
        :type dns_server: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.add_dns')
        params = {}
        uri = '/cluster/name_servers'
        method = 'POST'
        payload = {
            "value": dns_server
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        logger.info("adding dns server '{0}'".format(dns_server))
        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def remove_dns(self, dns_server, clusteruuid=None):
        """Remove dns server from a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type dns_server: IP address or hostname for a dns server
        :type dns_server: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.remove_dns')
        params = {}
        payload = None
        uri = '/cluster/name_servers/{0}'.format(dns_server)
        method = 'DELETE'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        logger.info("removing dns server '{0}'".format(dns_server))
        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def set_dns(self, clusteruuid=None, dns_servers=None):
        """Set dns servers for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type dns_servers: An ordered list of dns servers
        :type dns_servers: list, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_dns')
        result = None

        if not dns_servers:
            raise ValueError('no dns server list provided.')

        if not self.dns_servers.get(clusteruuid):
            self.get_dns(clusteruuid=clusteruuid)

        if len(dns_servers) > 3:
            raise ValueError('a maximum of 3 dns servers can be set.')

        if len(self.dns_servers.get(clusteruuid)) == 0:
            for dns_server in dns_servers:
                self.add_dns(dns_server, clusteruuid=clusteruuid)
            result = 'added'

        elif not collections.Counter(dns_servers) == collections.Counter(self.get_dns(clusteruuid=clusteruuid)):
            for dns_server in self.get_dns(clusteruuid=clusteruuid):
                self.remove_dns(dns_server=dns_server, clusteruuid=clusteruuid)

            for dns_server in dns_servers:
                self.add_dns(dns_server, clusteruuid=clusteruuid)
            result = 'updated'

        if result:
            self.get_dns(clusteruuid=clusteruuid)

        return result

    def get_proxy(self, clusteruuid=None):
        """Retrieve proxy configured for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of the clusters dns servers
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_proxy')
        params = {}
        payload = None
        uri = '/http_proxies'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.proxy[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.proxy[clusteruuid]

    def add_proxy(self, name, address, port, proxy_types, username=None, password=None, clusteruuid=None):
        """Add proxy configuration for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type name: Descriptive name for proxy server
        :type name: str
        :type address: IP address or FQDN of proxy server
        :type address: str
        :type port: Port that proxy server listens on
        :type port: int
        :type proxy_types: List of proxy types
        :type proxy_types: list('http', 'https', 'socks')
        :type username: Username to authenticate to the proxy
        :type username: str
        :type password: Password to authenticate to the proxy
        :type password: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.add_proxy')
        params = {}
        payload = {
            "address": address,
            "name": name,
            "port": port,
            "proxy_types": proxy_types,
        }

        if username and password:
            payload['username'] = username
            payload['password'] = password

        uri = '/http_proxies'
        method = 'POST'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method, response_code=201)

    def update_proxy(self, name, address, port, proxy_types, username=None, password=None, clusteruuid=None):
        """Add proxy configuration for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type name: Descriptive name for proxy server
        :type name: str
        :type address: IP address or FQDN of proxy server
        :type address: str
        :type port: Port that proxy server listens on
        :type port: int
        :type proxy_types: List of proxy types
        :type proxy_types: list('http', 'https', 'socks')
        :type username: Username to authenticate to the proxy
        :type username: str
        :type password: Password to authenticate to the proxy
        :type password: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.update_proxy')
        params = {}
        payload = {
            "address": address,
            "name": name,
            "port": port,
            "proxy_types": proxy_types,
        }

        if username and password:
            payload["username"] = username
            payload["password"] = password

        uri = '/http_proxies'
        method = 'PUT'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def remove_proxy(self, name, clusteruuid=None):
        """Remove proxy configuration from a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type name: Name of proxy server
        :type name: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.remove_proxy')
        params = {}
        payload = None
        uri = '/http_proxies/{0}'.format(name)
        method = 'DELETE'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    # flake8: noqa: C901
    def set_proxy(self, address, port, clusteruuid=None, name='proxy', username='', password='', http=True, https=False, socks=False):
        """Set proxy configuration for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :type address: IP address or FQDN of proxy server
        :type address: str
        :type port: Port that proxy server listens on
        :type port: int
        :type name: Descriptive name for proxy server
        :type name: str, optional
        :type username: Username to authenticate to the proxy
        :type username: str, optional
        :type password: Password to authenticate to the proxy
        :type password: str, optional
        :type http: Enable http for the proxy
        :type http: bool, optional
        :type https: Enable https for the proxy
        :type https: bool, optional
        :type socks: Enable socks for the proxy
        :type socks: bool, optional

        :returns: `updated` if changed, `added` if created or None otherwise
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Config.set_proxy')
        result = None

        if not address:
            raise ValueError('no proxy address provided.')

        if not port:
            raise ValueError('no proxy port provided.')

        if not self.proxy.get(clusteruuid):
            self.get_proxy(clusteruuid=clusteruuid)

        proxy_types = []

        if http:
            proxy_types.append('HTTP')
        if https:
            proxy_types.append('HTTPS')
        if socks:
            proxy_types.append('SOCKS')

        # If no proxy defined
        if not self.proxy.get(clusteruuid) or len(self.proxy.get(clusteruuid)) == 0:
            self.add_proxy(name=name, address=address, port=port, proxy_types=proxy_types, username=username, password=password, clusteruuid=clusteruuid)
            result = 'added'

        # If more than 1 proxy , remove all proxies and add new config
        elif len(self.proxy.get(clusteruuid)) > 1:
            for configured_proxy in self.proxy.get(clusteruuid):
                self.remove_proxy(configured_proxy.get('name'))
            self.add_proxy(name=name, address=address, port=port, proxy_types=proxy_types, username=username, password=password, clusteruuid=clusteruuid)
            result = 'updated'

        # If 1 proxy defined, update if name matches
        elif len(self.proxy.get(clusteruuid)) == 1 and self.proxy.get(clusteruuid)[0].get('name') == name:
            self.update_proxy(name=name, address=address, port=port, proxy_types=proxy_types, username=username, password=password, clusteruuid=clusteruuid)
            result = 'updated'

        # If 1 proxy defined, if name does not match remove and add new config
        elif len(self.proxy.get(clusteruuid)) == 1 and self.proxy.get(clusteruuid)[0].get('name') != name:
            self.remove_proxy(name=self.proxy.get(clusteruuid)[0].get('name'), clusteruuid=clusteruuid)
            self.add_proxy(name=name, address=address, port=port, proxy_types=proxy_types, username=username, password=password, clusteruuid=clusteruuid)
            result = 'updated'

        if result:
            self.get_proxy(clusteruuid=clusteruuid)

        return result

    def accept_elua(self, name, title, company, clusteruuid=None):
        """Accept the Nutanix ELUA

        :param name: Your name
        :type name: str
        :param title: Your job title
        :type title: str
        :param company: Name of your company
        :type company: str
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.accept_elua')
        params = {}
        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        uri = '/eulas/accept'
        method = 'POST'
        payload = {
            "username": name,
            "companyName": company,
            "jobTitle": title
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method)

    def change_ui_admin_password(self, admin_password, ssh_user='nutanix', ssh_password='nutanix/4u', clusteruuid=None):
        """Change the password for the 'admin' UI user account. This is not exposed via the API so paramiko is used to establish an ssh session to the CVM.
        If ssh is blocked or key-based authentication is enabled (cluster-lockdown) then this will not work.

        :param admin_password: The new admin password to be set for the prism admin user account. See https://portal.nutanix.com for password complexity requirements.
        :type admin_password: str
        :param ssh_user: The user with ssh access to the nutanix cluster (default='nutanix')
        :type ssh_password: str, optional
        :param ssh_password: The password for the user with ssh access to the nutanix cluster (default='nutanix/4u')
        :type ssh_password: str, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Config.change_admin_password')

        command = 'ncli user reset-password user-name="admin" password="{0}"'.format(admin_password)
        port = 22
        host_list = []

        if clusteruuid:
            cluster_obj = Cluster(api_client=self.api_client)
            host_list.append(cluster_obj.get(clusteruuid=clusteruuid).get('cluster_external_address').get('ipv4'))
        else:
            host_list.append(self.api_client.ip_address)

        for host in host_list:
            logger.info('changing UI admin password for cluster "{0}"'.format(host))
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, ssh_user, ssh_password)
            stdin, stdout, stderr = ssh.exec_command(command)
            logger.debug(stdout.readlines())

    def get_protection_rules(self):
        """Retrieve data for all protection rules.

        .. note:: Will only return data when `connection_type=='pc'`
        """
        logger = logging.getLogger('ntnx_api.prism.Config.get_protection_rules')
        params = {}

        if self.api_client.connection_type == "pc":
            self.protection_rules = {}
            uri = '/protection_rules/list'
            payload = {
                "kind": "protection_rule",
                "offset": 0,
                "length": 2147483647
            }
            self.protection_rules = self.api_client.request(uri=uri, payload=payload, params=params).get('entities')

        return self.protection_rules


class Cluster(object):
    """A class to represent a Nutanix Cluster

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        logger = logging.getLogger('ntnx_api.prism.Cluster.__init__')
        self.api_client = api_client
        self.clusters = []
        self.cluster = {}
        self.cluster_ha = {}

    def get_all_uuids(self):
        """Retrieve a list of all clusters.

        :returns: A list of dictionaries describing the configuration of each cluster.
        :rtype: ResponseList

        .. note:: Will return all registered clusters when `connection_type=='pc'`
        .. note:: Will only return one cluster when `connection_type=='pe'`
        """
        logger = logging.getLogger('ntnx_api.prism.Cluster.get_all_uuids')
        self.clusters = []
        params = {}
        payload = None

        if self.api_client.connection_type == "pc":
            uri = '/clusters/list'
            payload = {
                "kind": "cluster",
                "offset": 0,
                "length": 2147483647,
            }

        else:
            uri = '/clusters'

        clusters = self.api_client.request(uri=uri, payload=payload, params=params).get('entities')
        # Only return PE clusters ie. exclude any clusters defined as MULTICLUSTER or where the cluster name is not set
        cluster_list = []
        if self.api_client.connection_type == "pc":
            for cluster in clusters:
                logger.info('returned cluster: {0}'.format(cluster))
                if "PRISM_CENTRAL" not in cluster.get('status').get('resources').get('config').get('service_list'):
                    cluster_list.append(cluster)
        else:
            cluster_list = clusters

        for cluster in cluster_list:
            if self.api_client.connection_type == "pc":
                self.clusters.append(cluster.get('metadata').get('uuid'))
            else:
                self.clusters.append(cluster.get('uuid'))
        logger.info('found cluster uuids: {0}'.format(self.clusters))
        return self.clusters

    def get(self, clusteruuid=None, refresh=False):
        """Retrieve data for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param refresh: Refresh data for this cluster if it already exists.
        :type refresh: bool, optional

        :returns: A dictionary describing the configuration of the cluster.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Cluster.get')
        params = {}
        payload = None
        uri = '/cluster'
        result = {}

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        # Remove existing data for this cluster if it exists
        if refresh:
            logger.info('refresh selected')
            if self.cluster.get(clusteruuid):
                self.cluster.pop(clusteruuid)
                logger.info('removing existing data from class dict cluster for cluster {0}'.format(clusteruuid))
            result = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
            self.cluster[clusteruuid] = result

        elif not self.cluster.get(clusteruuid):
            logger.info('no existing data. getting cluster data from api.')
            result = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
            self.cluster[clusteruuid] = result

        else:
            logger.info('using existing data')
            result = self.cluster.get(clusteruuid)

        return result

    def get_ha(self, clusteruuid=None):
        """Retrieve HA data for a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dictionary describing the HA configuration of the cluster.
        :rtype: ResponseDict

        .. note:: Cluster HA configuration will only present for cluster running the AHV hypervisor.
        """
        logger = logging.getLogger('ntnx_api.prism.Cluster.get_ha')
        params = {}
        payload = None
        uri = '/ha'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.cluster_ha[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params)
        return self.cluster_ha[clusteruuid]

    def search_uuid(self, uuid, clusteruuid=None):
        """Retrieve data for a specific cluster, in a specific cluster by host uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A cluster uuid to search for.
        :type uuid: str, optional

        :returns: A dictionary describing the found cluster.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Cluster.search_uuid')
        found = {}
        if not self.clusters:
            self.get(clusteruuid)

        for entity in self.clusters:
            if entity.get('cluster_uuid') == uuid:
                found = entity
                break

        return found

    def search_name(self, name, clusteruuid=None):
        """Retrieve data for a specific cluster, in a specific cluster by host cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A host name to search for.
        :type name: str, optional

        :returns: A dictionary describing the found cluster.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Cluster.search_name')
        found = {}
        if not self.clusters:
            self.get(clusteruuid)

        for entity in self.clusters:
            if entity.get('name') == name:
                found = entity
                break

        return found


class Hosts(object):
    """A class to represent a Nutanix Clusters Hosts

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        logger = logging.getLogger('ntnx_api.prism.Hosts.__init__')
        self.api_client = api_client
        self.hosts = {}
        self.metadata = {}

    def get(self, clusteruuid=None):
        """Retrieve data for each host in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each host from the specified cluster.
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.Hosts.get')
        params = {}
        payload = None
        uri = '/hosts'

        # Remove existing data for this cluster if it exists
        if self.hosts.get(clusteruuid):
            self.hosts.pop(clusteruuid)
            logger.info('removing existing data from class dict hosts for cluster {0}'.format(clusteruuid))

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.hosts[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.hosts[clusteruuid]

    def get_metadata(self, refresh=False):
        """Retrieve metadata for each host from the connected PC instance

        :returns: A list of dictionaries describing each vm from the specified cluster.
        :rtype: ResponseList
        """
        params = {}
        payload = {
            "kind": "host",
            "offset": 0,
            "length": 2147483647
        }
        uri = '/hosts/list'

        if self.api_client.connection_type == "pc":
            # Remove existing data for this cluster if it exists
            if not self.metadata or refresh:
                self.metadata = {}
                logger.info('removing existing data from class dict metadata')

                hosts = self.api_client.request(uri=uri, api_version='v3', payload=payload, params=params).get('entities')
                for host in hosts:
                    self.metadata[host.get('metadata').get('uuid')] = host.get('metadata')

        return self.metadata

    def search_uuid(self, uuid, clusteruuid=None, refresh=False):
        """Retrieve data for a specific host, in a specific cluster by host uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A host uuid to search for.
        :type uuid: str, optional

        :returns: A dictionary describing the found host.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Hosts.search_uuid')
        found = {}
        if not self.hosts.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        for entity in self.hosts.get(clusteruuid):
            if entity.get('uuid') == uuid:
                found = entity
                break

        return found

    def search_name(self, name, clusteruuid=None, refresh=False):
        """Retrieve data for a specific host, in a specific cluster by host name

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A host name to search for.
        :type name: str, optional
        :param refresh: Whether to refresh the class dataset (default=False).
        :type refresh: bool, optional

        :returns: A dictionary describing the found host.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Hosts.search_name')
        found = {}
        if not self.hosts.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        for entity in self.hosts.get(clusteruuid):
            if entity.get('name') == name:
                found = entity
                break

        return found

    def search_ip(self, ip_address, clusteruuid=None, refresh=False):
        """Retrieve data for a specific host, in a specific cluster by ip_address. The CVM, Hypervisor and IPMI IP addresses will be tested

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param ip_address: A host name to search for.
        :type ip_address: str, optional
        :param refresh: Whether to refresh the class dataset (default=False).
        :type refresh: bool, optional

        :returns: A dictionary describing the found host.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Hosts.search_ip')
        found = {}
        if not self.hosts.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        for entity in self.hosts.get(clusteruuid):
            if entity.get('service_vmexternal_ip') == ip_address or entity.get('hypervisor_address') == ip_address or entity.get('ipmi_address') == ip_address:
                found = entity
                break

        return found

    def get_project(self, uuid, refresh=False):
        """Retrieve the project assigned to the specified host if connected to a prism central

        :param uuid: The UUID of a host.
        :type uuid: str
        :param refresh: Whether to refresh the class dataset (default=False).
        :type refresh: bool, optional

        :returns: A string containing the project name.
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Hosts.get_project')
        project = ''
        if self.api_client.connection_type == "pc":
            self.get_metadata(refresh=refresh)
            metadata = self.metadata.get(uuid)
            if metadata:
                logger.info('host "{0}" metadata "{1}"'.format(uuid, metadata))
                if metadata.get('project_reference'):
                    if metadata.get('project_reference').get('kind') == 'project':
                        project = metadata.get('project_reference').get('name')
                        logger.info('host "{0}" project "{1}"'.format(uuid, project))
        return project

    def get_categories(self, uuid, refresh=False):
        """Retrieve the categories assigned to the specified host if connected to a prism central

        :param uuid: The UUID of a host.
        :type uuid: str
        :param refresh: Whether to refresh the class dataset (default=False).
        :type refresh: bool, optional

        :returns: A dictionary with all categories for the specified host.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Hosts.get_categories')
        categories = {}
        if self.api_client.connection_type == "pc":
            self.get_metadata(refresh=refresh)
            metadata = self.metadata.get(uuid)
            if metadata:
                if 'categories' in metadata:
                    for key, value in metadata.get('categories').items():
                        # Skip keys that do not relate to categories
                        items_to_exclude = [
                            'ProtectionRule',
                        ]
                        if not any(value in key for value in items_to_exclude):
                            logger.info('host "{0}" category "{1}:{2}"'.format(uuid, key, value))
                            categories[key] = value
        return categories


class Vms(object):
    """A class to represent a Nutanix Clusters Virtual Machines

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        logger = logging.getLogger('ntnx_api.prism.Vms.__init__')
        self.api_client = api_client
        self.vms = {}
        self.metadata = {}

    def get(self, clusteruuid=None, include_disks=True, include_nics=True):
        """Retrieve host data for each virtual machine in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param include_disks: Include VM disk info in returned data (Default=False)
        :type include_disks: bool, optional
        :param include_nics: Include VM nic info in returned data (Default=False)
        :type include_nics: bool, optional

        :returns: A list of dictionaries describing each vm from the specified cluster.
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.get')
        params = {'length': '2147483647'}

        if include_disks:
            params['include_vm_disk_config'] = 'true'
        else:
            params['include_vm_disk_config'] = 'false'

        if include_nics:
            params['include_vm_nic_config'] = 'true'
        else:
            params['include_vm_nic_config'] = 'false'

        payload = None
        uri = '/vms'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        # Remove existing data for this cluster if it exists
        if self.vms.get(clusteruuid):
            self.vms.pop(clusteruuid)
            logger.info('removing existing data from class dict vms for cluster {0}'.format(clusteruuid))

        self.vms[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.vms[clusteruuid]

    def get_metadata(self, refresh=False):
        """Retrieve metadata for each virtual machine from the connected PC instance

        :returns: A list of dictionaries describing each vm from the specified cluster.
        :rtype: ResponseList
        """
        params = {}
        payload = {
            "kind": "vm",
            "offset": 0,
            "length": 2147483647
        }
        uri = '/vms/list'

        if self.api_client.connection_type == "pc":
            # Remove existing data for this cluster if it exists
            if not self.metadata or refresh:
                self.metadata = {}
                logger.info('removing existing data from class dict metadata')

                vms = self.api_client.request(uri=uri, api_version='v3', payload=payload, params=params).get('entities')
                logger.info('returned data: {0}'.format(vms))
                for vm in vms:
                    self.metadata[vm.get('metadata').get('uuid')] = vm.get('metadata')

        return self.metadata

    def search_uuid(self, uuid, clusteruuid=None, refresh=False):
        """Retrieve data for a specific vm, in a specific cluster by vm uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A vm uuid to search for.
        :type uuid: str, optional
        :param refresh: Whether to refresh the class VM dataset (default=False).
        :type refresh: bool, optional

        :returns: A dictionary describing the found vm.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.search_uuid')
        found = {}
        if not self.vms.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        for entity in self.vms.get(clusteruuid):
            if entity.get('uuid') == uuid:
                found = entity
                break

        return found

    def search_name(self, name, clusteruuid=None, refresh=False):
        """Retrieve data for a specific vm, in a specific cluster by vm name

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A vm name to search for.
        :type name: str, optional
        :param refresh: Whether to refresh the class VM dataset (default=False).
        :type refresh: bool, optional

        :returns: A dictionary describing the found vm.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.search_name')
        found = {}
        if not self.vms.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        for entity in self.vms.get(clusteruuid):
            if entity.get('name') == name:
                found = entity
                break

        return found

    def get_project(self, uuid, refresh=False):
        """Retrieve the project assigned to the specified VM if connected to a prism central

        :param uuid: The UUID of a VM.
        :type uuid: str
        :param refresh: Whether to refresh the class VM Metadata dataset (default=False).
        :type refresh: bool, optional

        :returns: A string containing the project name.
        :rtype: str
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.get_project')
        project = ''
        if self.api_client.connection_type == "pc":
            self.get_metadata(refresh=refresh)
            metadata = self.metadata.get(uuid)
            if metadata:
                logger.info('vm "{0}" metadata "{1}"'.format(uuid, metadata))
                if metadata.get('project_reference'):
                    if metadata.get('project_reference').get('kind') == 'project':
                        project = metadata.get('project_reference').get('name')
        return project

    def get_categories(self, uuid, refresh=False):
        """Retrieve the categories assigned to the specified VM if connected to a prism central

        :param uuid: The UUID of a VM.
        :type uuid: str
        :param refresh: Whether to refresh the class VM Metadata dataset (default=False).
        :type refresh: bool, optional

        :returns: A dictionary with all .
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.get_categories')
        categories = {}
        if self.api_client.connection_type == "pc":
            self.get_metadata(refresh=refresh)
            metadata = self.metadata.get(uuid)
            if metadata:
                if 'categories' in metadata:
                    for key, value in metadata.get('categories').items():

                        # Skip keys that do not relate to categories
                        items_to_exclude = [
                            'ProtectionRule',
                        ]
                        if not any(value in key for value in items_to_exclude):
                            logger.info('vm "{0}" category "{1}:{2}"'.format(uuid, key, value))
                            categories[key] = value
        return categories

    def get_protection_rules(self, uuid, refresh=False):
        """Retrieve the protection rules assigned to the specified VM if connected to a prism central

        :param uuid: The UUID of a VM.
        :type uuid: str
        :param refresh: Whether to refresh the class VM Metadata dataset (default=False).
        :type refresh: bool, optional

        :returns: A dictionary with all .
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.get_protection_rules')
        protection_rules = {}
        if self.api_client.connection_type == "pc":
            self.get_metadata(refresh=refresh)
            metadata = self.metadata.get(uuid)
            if metadata:
                if 'categories' in metadata:
                    for key, value in metadata.get('categories').items():

                        # Skip keys that do not relate to categories
                        items_to_include = [
                            'ProtectionRule',
                        ]
                        if any(value in key for value in items_to_include):
                            logger.info('vm "{0}" protection rule "{1}:{2}"'.format(uuid, key, value))
                            protection_rules[key] = value
        return protection_rules

    @staticmethod
    def _vm_disk_spec(bus:str='scsi', label:str=None, index:int=0, flash_mode:bool=False, size_gb:int=0, image_uuid:str=None, storage_container_uuid:str=None,
                      volume_group_uuid:str=None, **kwargs):
        """Generate the disk configuration when creating a VM for the v2 API.
        :param bus: The bus type to be used to attached the vdisk to the vm (default=scsi)
        :type bus: str('scsi', 'ide', 'pci', 'sata', 'spapr', 'nvme')
        :param label: (default=None)
        :type label: str, optional
        :param index: The SCSI bus index where the vdisk will be attached to the vm (default=0)
        :type index: int, optional
        :param flash_mode: Whether flash mode will be enabled on this vdisk. For more detail on flash mode refer to
                            https://portal.nutanix.com/page/documents/details?targetId=Web-Console-Guide-Prism-v5_19:wc-vm-flash-mode-c.html (default=False)
        :type flash_mode: bool, optional
        :param size_gb: The size of the vdisk in GB (default=0)
        :type size_gb: int, optional
        :param image_uuid: The uuid of an existing image that this vdisk will be built from. (default=None)
        :type image_uuid: str, optional
        :param storage_container_uuid: The uuid of an existing storage container that a new vdisk will be built on. (default=None)
        :type storage_container_uuid: str, optional
        :param volume_group_uuid: The uuid of an existing volume group that will be attached to at the specified SCSI bus index. (default=None)
        :type volume_group_uuid: str, optional
        :return: A dictionary containing the specification to be used to create a vm disk
        :rtype: dict
        ... warning:: Only one of image_uuid, storage_container_uuid or volume_group_uuid must be provided.
        """

        if bus.lower() not in ['scsi', 'ide', 'pci', 'sata', 'spapr', 'nvme', ]:
            raise ValueError()

        bm_size_gb = bitmath.GiB(size_gb)
        bm_size = bm_size_gb.to_Byte()

        disk = {
            'disk_address': {
                'device_bus': bus.upper(),
                'device_index': index,
                'is_cdrom': False,
            },
            'flash_mode_enabled': flash_mode,
            'is_cdrom': False,
        }

        if label:
            disk['disk_address']['disk_label'] = label

        if image_uuid:
            disk['is_empty'] = False
            disk['vm_disk_clone'] = {
                'disk_address': {
                    'vmdisk_uuid': image_uuid,
                },
                # 'storage_container_uuid': '',
            }

            if size_gb:
                disk['vm_disk_clone']['minimum_size'] = int(bm_size)

        elif volume_group_uuid:
            disk['is_empty'] = False
            disk['disk_address']['volume_group_uuid'] = volume_group_uuid

        else:
            if size_gb:
                disk['is_empty'] = False
                disk['vm_disk_create'] = {
                    'size': int(bm_size),
                    'storage_container_uuid': storage_container_uuid,
                }

            else:
                disk['is_empty'] = True

        return disk

    @staticmethod
    def _vm_nic_spec(network_uuid=None, adaptor_type:str='E1000', connect:bool=True, mac_address:str=None, model:str=None, ipam:bool=False,
                     requested_ip_address:str=None, **kwargs):
        """Generate the network interface configuration when creating a VM for the v2 API.
        :param network_uuid: The uuid of an existing network that a new vdisk will be built on. (default=None)
        :type network_uuid: str, optional
        :param adaptor_type: The type of network interface that is being created (default='e1000')
        :type adaptor_type: str('e1000', 'e1000e', 'pcnet32', 'vmxnet', 'vmxnet2', 'vmxnet3', 'unsupported'), optional
        :param connect: Whether to connect the network interface (equivalent of whether the network cable is plugged in or not). (default=True)
        :type connect: bool, optional
        :param mac_address: Whether to use a custom mac address. By default a new MAC address will be generated for this network interface (default=None)
        :type mac_address: str, optional
        :param model: TDB (default=None)
        :type model: str, optional
        :param ipam: Whether to enable AHV IPAM on this network interface. (default=False)
        :type ipam: bool, optional
        :param requested_ip_address: If AHV IPAM is enabled specify the IP address that will be assigned to this network interface. (default=None)
        :type requested_ip_address: str, optional
        :return: A dictionary containing the specification to be used to create a vm network interface
        :rtype: dict
        .. todo:: Determine the acceptable values for the model parameter & update documentation and add validation for the variable.
        """
        if not network_uuid:
            raise ValueError()

        if adaptor_type.lower() not in ['e1000', 'e1000e', 'pcnet32', 'vmxnet', 'vmxnet2', 'vmxnet3', 'unsupported', ]:
            raise ValueError()

        nic = {
            'adaptor_type': adaptor_type.upper(),
            'is_connected': connect,
            'network_uuid': network_uuid,
        }

        if mac_address:
            nic['mac_address'] = mac_address

        if model:
            nic['model'] = model

        if ipam:
            nic['request_ip'] = True

        if requested_ip_address:
            nic['request_ip'] = True
            nic['requested_ip_address'] = requested_ip_address

        return nic

    @staticmethod
    def _vm_gpu_spec(device_id:int=None, gpu_type:str='pass_through_graphics', gpu_vendor:str='nvidia', **kwargs):
        """Generate the gpu configuration when creating a VM for the v2 API.
        :param device_id: The GPU device ID. (default=None)
        :type device_id: str, optional
        :param gpu_type: The type of GPU that is to be added to the VM (default='pass_through_graphics')
        :type gpu_type: str('pass_through_graphics'), optional
        :param gpu_vendor: The GPU vendor that is to be added to the VM. (default='nvidia')
        :type gpu_vendor: str('nvidia'), optional
        :return: A dictionary containing the specification to be used to create a vm gpu
        :rtype: dict
        """
        if not device_id:
            raise ValueError()

        if gpu_type.lower() not in ['pass_through_graphics', ]:
            raise ValueError()

        if gpu_vendor.lower() not in ['nvidia', ]:
            raise ValueError()

        gpu = {
            'device_id': device_id,
            'gpu_type': gpu_type.upper(),
            'gpu_vendor': gpu_vendor.upper(),
        }

        return gpu

    @staticmethod
    def _vm_serial_port_spec(port_index:int=None, port_type:str='null', **kwargs):
        """Generate the serial port configuration when creating a VM for the v2 API.
        :param port_index: The serial port device index. (default=None)
        :type port_index: str, optional
        :param port_type: The type of serial port that is to be added to the VM (default='null')
        :type port_type: str('null', 'server'), optional
        :return: A dictionary containing the specification to be used to create a vm serial port
        :rtype: dict
        """
        if not port_index >= 0:
            raise ValueError()

        if port_type.lower() not in ['null', 'server', ]:
            raise ValueError()

        serial_port = {
            'index': port_index,
            'type': port_type.upper(),
        }

        return serial_port

    def create(self, name:str, vcpus:int, memory_gb:int, sockets:int=1, vcpu_reservation_hz:int=0, memory_reservation_gb:int=0, description:str='',
                  power_state:str='on', disks:list=[], storage_container_uuid:str=None, nics:list=[], gpus:list=[], serial_ports:list=[], timezone:str='UTC',
                  sysprep:str=None, cloudinit:str=None, add_cdrom:bool=True, ha_priority:int=0, machine_type:str='pc', wait:bool=True, clusteruuid:str=None):
        """ Create a new virtual machine.

        :param name: The name for the VM to be created. VM names do not have to be unique.
        :type name: str
        :param description: A description for the VM (default='')
        :type description: str, optional
        :param vcpus: The number of vCPUs to be assigned to this VM
        :type vcpus: int
        :param memory_gb: The amount of memory in GB to be assigne to this VM
        :type memory_gb: int
        :param sockets: The number of virtual CPU sockets to distribute the defined vCPUs over (default=1)
        :type sockets: int, optional
        :param vcpu_reservation_hz: A CPU reservation in hz for this VM. Only applicable on the ESXi hypervisor. (default=0)
        :type vcpu_reservation_hz: int, optional
        :param memory_reservation_gb: An amount of memory to lock to this VM. Only applicable on the ESXi hypervisor. (default=0)
        :type memory_reservation_gb: int, optional
        :param power_state: The desired power state for this VM after creation. (default='on')
        :type power_state: str('on', 'off'), optional
        :param storage_container_uuid: The UUID of the storage contain on which to create this VM. Only applicable on the ESXi hypervisor. (default='null')
        :type storage_container_uuid: str, optional
        :param add_cdrom: Whether to add a cdrom drive to this VM (default=True)
        :type add_cdrom: bool, optional
        :param disks: A list of vdisks dicts to be added to this VM (default='null').

            The dictionary format per-vDisk is as follows::
                - bus (str, optional, default='scsi'). The bus to use for the vDisk. Choice of 'scsi', 'ide', 'pci', 'sata', 'spapr', 'nvme'
                - size_gb (int, optional). Size of vDisk in GB. Use this when creating a new disk or cloning from an image. Can be used to increase the size of vDisk created from an image
                - storage_container_name (str, optional). Name of Storage Container. Only used when creating a new vDisk. Mutually exclusive with "storage_container_uuid"
                - storage_container_uuid (str, optional). UUID of Storage Container. Only used when creating a new vDisk. Mutually exclusive with "storage_container_name"
                - image_name (str, optional). Name of Image to clone from. Only used when creating a new vDisk from an existing image. Mutually exclusive with "image_uuid"
                - image_uuid (str, optional). UUID of Image to clone from. Only used when creating a new vDisk from an existing image. Mutually exclusive with "image_name"
                - volume_group_name (str, optional). Name of Volume Group to attach. Only used when attaching an existing volume group. Mutually exclusive with "volume_group_uuid"
                - volume_group_uuid (str, optional). UUID of Volume Group to attach. Only used when attaching an existing volume group. Mutually exclusive with "volume_group_name"
                - flash_mode (bool, optional, default=False). True or False
                - label (str, optional). Unknown

            Examples;
                1. Add a single virtual disk - [{'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 50, }, ]
                2. Add multiple virtual disk - [{'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 50, }, {'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 200, }, ]
                3. Add a single virtual disk with flash mode enabled - [{'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 15, 'flash_mode': True}, ]
                4. Add a single virtual disk from an image - [{'bus': 'scsi', 'image_name': 'centos8', }, ]
                5. Add a single virtual disk from an image with a new minimum size - [{'bus': 'scsi', 'image_name': 'centos8', 'size_gb': 500, }, ]
                6. Add a volume group - [{'bus': 'scsi', 'volume_group_name': 'volume_group_database1', }, ]
        :type disks: list, optional
        :param nics: A list of NIC dicts to be added to this VM (default='null').

            The dictionary format per-NIC is as follows::
                - network_name (str, optional). The name of the network or port group to attach the NIC onto. Mutually exclusive with "network_uuid".
                - network_uuid (str, optional). The uuid of the network or port group to attach the NIC onto. Mutually exclusive with "network_name".
                - adaptor_type (str, optional, default='e1000'). The network adaptor type to use for the NIC. Choice of 'e1000', 'e1000e', 'pcnet32', 'vmxnet', 'vmxnet2', 'vmxnet3',
                - connect (bool, optional, default=True). Whether to connect the NIC to the network.
                - mac_address (str, optional, default=None). A user-defined MAC address to use for this NIC.
                - ipam (bool, optional, default=False). Whether to use AHV IPAM to automatically provide an IP address.
                - requested_ip_address (str, optional). A user-defined IP address to use in conjunction with AHV IPAM. Requires 'ipam' to also be set to True.

            Examples;
                1. Create a simple NIC - [{'network_name': 'vm network',}, ]
                2. Create a NIC with AHV IPAM - [{'network_name': 'vm network', 'ipam': True, }, ]
                3. Create multiple NICs with mixed configuration - [{'network_name': 'vm network 1', }, {'network_name': 'vm network 2', 'ipam': True, }, ]
                4. Create a NIC with AHV IPAM and a defined IP address - [{'network_name': 'vm network', 'ipam': True, 'requested_ip_address': '172.16.100.51', }, ]
        :type nics: list, optional
        :param gpus: A list of GPU dicts to be added to the VM (default='null')

            The dictionary format per-GPU is as follows::
                - device_id (int).
                - gpu_type (str, optional, default='null'). The type of GPU to add. Choice of 'pass_through_graphics'
                - gpu_vendor (str, optional, default='null'). The GPU vendor to add. Choice of 'nvidia',
        :type gpus: list, optional
        :param serial_ports: A list of serial port dicts to be added to the VM (default='null')

            The dictionary format per-serial port is as follows::
                - port_index (int).
                - port_type (str, optional, default='null'). The type of serial port to add. Choice of 'null', 'server'
        :type serial_ports: list, optional
        :param timezone: The timezone for the virtual machine (default='UTC').
        :type timezone: str, optional
        :param sysprep: The sysprep XML string to use to customize this VM upon first power on. Only applicable for AHV and a Windows OS. (default='null')
        :type sysprep: str, optional
        :param cloudinit: The cloudinit text string to use to customize this VM upon first power on. Only applicable for AHV and a Linux OS. (default='null')
        :type cloudinit: str, optional
        :param ha_priority: VM HA priority. Only applicable to ESXi hypervisor (default=0)
        :type ha_priority: int, optional
        :param machine_type: The type of VM being deployed. This donates the target cpu architecture of the cluster. (default='pc')
        :type machine_type: str('pc', 'pseries', 'q35'), optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the VM was successfully created.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.create')

        params = {}
        version = 'v2.0'
        uri = '/vms'
        method = 'POST'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        bm_memory_gb = bitmath.GB(memory_gb)
        bm_memory_mb = bm_memory_gb.to_MB()
        bm_memory_reservation_mb = bitmath.GB(memory_reservation_gb)
        bm_memory_reservation_mb = bm_memory_reservation_mb.to_MB()
        vg_attach = []

        if power_state not in ["off", "on", ]:
            raise ValueError()

        if machine_type not in ["pc", "pseries", "q35",]:
            raise ValueError()

        payload = {
            'name': name,
            'description': description,
            'memory_mb': int(bm_memory_mb),
            'sockets': sockets,
            'num_vcpus': (vcpus/sockets),
            'power_state': 'OFF',
            'timezone': timezone,
            'ha_priority': ha_priority,
            'machine_type': machine_type,
            'vm_disks': [],
            'vm_nics': [],
        }

        if vcpu_reservation_hz:
            payload['vcpu_reservation_hz'] = vcpu_reservation_hz

        if memory_reservation_gb:
            payload['memory_reservation_mb'] = int(bm_memory_reservation_mb)

        if storage_container_uuid:
            containers_obj = StorageContainer(api_client=self.api_client)
            container = containers_obj.search_uuid(uuid=storage_container_uuid, clusteruuid=clusteruuid)
            if container:
                logger.info('found container with uuid "{0}"'.format(storage_container_uuid))
                payload['storage_container_uuid'] = container.get('storage_container_uuid')
            else:
                logger.warning('cannot find container with uuid "{0}"'.format(storage_container_uuid))
                raise ValueError()

        device_indexes = {
            'ide': 0,
            'scsi': 0,
            'pci': 0,
            'sata': 0,
            'spapr': 0,
            'nvme': 0,
        }
        if add_cdrom:
            cdrom_config = {
                'is_cdrom': True,
                'is_empty': True,
                'disk_address': {
                    'device_bus': 'IDE',
                    'device_index': device_indexes['ide'],
                    'is_cdrom': True,
                }
            }
            device_indexes['ide'] += 1
            payload['vm_disks'].append(cdrom_config)

        for disk in disks:
            disk['index'] = device_indexes[disk.get('bus', 'scsi')]
            device_indexes[disk.get('bus', 'scsi')] += 1

            if any([disk.get('storage_container_name'), disk.get('storage_container_uuid')]) and any([disk.get('image_name'), disk.get('image_uuid')]) and \
                    any([disk.get('volume_group_name'), disk.get('volume_group_uuid')]):
                raise ValueError()

            elif any([disk.get('storage_container_name'), disk.get('storage_container_uuid')]):
                if all([disk.get('storage_container_name'), disk.get('storage_container_uuid')]):
                    raise ValueError()

                elif disk.get('storage_container_name'):
                    logger.debug('searching for container named "{0}"'.format(disk.get('storage_container_name')))
                    containers_obj = StorageContainer(api_client=self.api_client)
                    container = containers_obj.search_name(name=disk.get('storage_container_name'), clusteruuid=clusteruuid)
                    if container:
                        logger.debug('found container named "{0}"'.format(disk.get('storage_container_name')))
                        disk.pop('storage_container_name')
                        disk['storage_container_uuid'] = container.get('storage_container_uuid')
                    else:
                        logger.warning('cannot find container named "{0}"'.format(disk.get('storage_container_name')))
                        raise ValueError()

                elif disk.get('storage_container_uuid'):
                    logger.debug('searching for container "{0}"'.format(disk.get('storage_container_uuid')))
                    containers_obj = StorageContainer(api_client=self.api_client)
                    container = containers_obj.search_uuid(uuid=disk.get('storage_container_uuid'), clusteruuid=clusteruuid)
                    if container:
                        logger.debug('found container "{0}"'.format(disk.get('storage_container_uuid')))
                        disk.pop('storage_container_name')
                        disk['storage_container_uuid'] = disk.get('storage_container_uuid')
                    else:
                        logger.warning('cannot find container "{0}"'.format(disk.get('storage_container_uuid')))
                        raise ValueError()

            elif any([disk.get('image_name'), disk.get('image_uuid')]):
                if all([disk.get('image_name'), disk.get('image_uuid')]):
                    raise ValueError()

                elif disk.get('image_name'):
                    logger.debug('searching for image named "{0}"'.format(disk.get('image_name')))
                    images_obj = Images(api_client=self.api_client)
                    image = images_obj.search_name(name=disk.get('image_name'), clusteruuid=clusteruuid)
                    if image:
                        logger.debug('found image named "{0}"'.format(disk.get('image_name')))
                        disk.pop('image_name')
                        disk['image_uuid'] = image.get('vm_disk_id')
                    else:
                        logger.warning('cannot find image named "{0}"'.format(disk.get('image_name')))
                        raise ValueError()

                elif disk.get('image_uuid'):
                    logger.info('searching for image "{0}"'.format(disk.get('image_uuid')))
                    images_obj = Images(api_client=self.api_client)
                    image = images_obj.search_uuid(uuid=disk.get('image_uuid'), clusteruuid=clusteruuid)
                    if image:
                        logger.debug('found image "{0}"'.format(disk.get('image_uuid')))
                        disk.pop('image_uuid')
                        disk['image_uuid'] = image.get('vm_disk_id')
                    else:
                        logger.warning('cannot find image "{0}"'.format(disk.get('image_uuid')))
                        raise ValueError()

            elif any([disk.get('volume_group_name'), disk.get('volume_group_uuid')]):
                if all([disk.get('volume_group_name'), disk.get('volume_group_uuid')]):
                    raise ValueError()

                elif disk.get('volume_group_name'):
                    logger.info('searching for volume group named "{0}"'.format(disk.get('volume_group_name')))
                    volume_group_obj = StorageVolume(api_client=self.api_client)
                    volume_group = volume_group_obj.search_volume_groups_name(name=disk.get('volume_group_name'), clusteruuid=clusteruuid)
                    if volume_group:
                        logger.debug('found volume group named "{0}"'.format(disk.get('volume_group_name')))
                        disk.pop('volume_group_name')
                        vg = {
                            'index': disk['index'],
                            'uuid': volume_group.get('uuid'),
                        }
                        vg_attach.append(vg)

                    else:
                        logger.warning('cannot find volume group named "{0}"'.format(disk.get('volume_group_name')))
                        raise ValueError()

                elif disk.get('volume_group_uuid'):
                    logger.info('searching for volume group "{0}"'.format(disk.get('volume_group_uuid')))
                    volume_group_obj = StorageVolume(api_client=self.api_client)
                    volume_group = volume_group_obj.search_volume_groups_uuid(uuid=disk.get('volume_group_uuid'), clusteruuid=clusteruuid)
                    if volume_group:
                        logger.debug('found volume group "{0}"'.format(disk.get('volume_group_uuid')))
                        disk.pop('volume_group_uuid')
                        vg = {
                            'index': disk['index'],
                            'uuid': volume_group.get('uuid'),
                        }
                        vg_attach.append(vg)
                    else:
                        logger.warning('cannot find volume group "{0}"'.format(disk.get('volume_group_uuid')))
                        raise ValueError()

            if any([disk.get('storage_container_name'), disk.get('storage_container_uuid'), disk.get('image_name'), disk.get('image_uuid'), ]):
                disk_spec = self._vm_disk_spec(**disk)
                payload['vm_disks'].append(disk_spec)

        for nic in nics:
            if all([nic.get('network_uuid'), nic.get('network_name')]):
                raise ValueError()

            elif nic.get('network_name'):
                logger.info('searching for network named "{0}"'.format(nic.get('network_name')))
                networks_obj = Network(api_client=self.api_client)
                network = networks_obj.search_name(name=nic.get('network_name'), clusteruuid=clusteruuid)
                if network:
                    logger.debug('found network named "{0}"'.format(nic.get('network_name')))
                    nic.pop('network_name')
                    nic['network_uuid'] = network.get('uuid')
                else:
                    logger.warning('cannot find network named "{0}"'.format(nic.get('network_name')))
                    raise ValueError()

            elif nic.get('network_uuid'):
                logger.info('searching for network "{0}"'.format(nic.get('network_uuid')))
                networks_obj = Network(api_client=self.api_client)
                network = networks_obj.search_uuid(uuid=nic.get('network_uuid'), clusteruuid=clusteruuid)
                if network:
                    logger.debug('found network named "{0}"'.format(nic.get('network_uuid')))
                    nic.pop('network_uuid')
                    nic['network_uuid'] = nic.get('network_uuid')
                else:
                    logger.warning('cannot find network named "{0}"'.format(nic.get('network_uuid')))
                    raise ValueError()

            payload['vm_nics'].append(self._vm_nic_spec(**nic))

        for gpu in gpus:
            payload['vm_gpus'] = []
            payload['vm_gpus'].append(self._vm_gpu_spec(**gpu))

        for serial_port in serial_ports:
            payload['serial_ports'] = []
            payload['serial_ports'].append(self._vm_serial_port_spec(**serial_port))

        if all([sysprep, cloudinit]):
            raise ValueError('Pleae provide either sysprep or cloudinit NOT both.')

        elif sysprep:
            payload['vm_customization_config'] = {
                'fresh_install': False,
                'userdata': sysprep,
            }

        elif cloudinit:
            payload['vm_customization_config'] = {
                'fresh_install': False,
                'userdata': cloudinit,
            }

        logger.debug('vm to be created: "{0}"'.format(payload))
        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)
        task_uuid = task.get('task_uuid')

        if wait:
            if task_uuid:
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task_uuid, max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task_uuid].get('progress_status').lower() == 'succeeded':
                    logger.debug('vm creation successful')

                    if vg_attach:
                        for vm in task_obj.task_result[task_uuid].get('entity_list'):
                            for vg in vg_attach:
                                self.attach_vg(vm_uuid=vm.get('entity_id'), wait=wait, clusteruuid=clusteruuid, **vg)

                    if power_state == 'on':
                        for vm in task_obj.task_result[task_uuid].get('entity_list'):
                            power_state = self.power_state(uuid=vm.get('entity_id'), desired_state='on', wait=wait, clusteruuid=clusteruuid)
                            if power_state:
                                return True
                            else:
                                logger.warning('vm creation failed ,cleaning up VM. Task details: {0}'.format(task_obj.task_result[task_uuid]))
                                self.delete_uuid(uuid=vm.get('entity_id'), snapshots=True, wait=True, clusteruuid=clusteruuid)
                                return False
                    else:
                        return True
                else:
                    logger.warning('vm creation failed. Task details: {0}'.format(task_obj.task_result[task_uuid]))
                    return False
            else:
                return False

    def delete_name(self, name:str, snapshots:bool=False, vg_detach:bool=True, wait:bool=True, clusteruuid:str=None):
        """Delete an existing virtual machine by name.

        :param name: The name for the VM to be deleted.
        :type name: str
        :param snapshots: Whether to also delete VM snapshots when deleting the VM. (Default=False)
        :type snapshots: bool, optional
        :param vg_detach: Whether to also detatch any connected volume groups when deleting the VM. (Default=True)
        :type vg_detach: bool, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the VM was sucessfully created.
        :rtype: bool
        .. warning:: As VM names are not necessarily unique, the first result returned will be used.
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.delete_name')
        uuid = self.search_name(name=name, clusteruuid=clusteruuid, refresh=True).get('uuid')

        if uuid:
            logger.debug('deleted vm {0} on cluster {1}'.format(name, clusteruuid))
            return self.delete_uuid(uuid=uuid, snapshots=snapshots, wait=wait, vg_detach=vg_detach, clusteruuid=clusteruuid)
        else:
            logger.warning('vm {0} not found on cluster {1}'.format(name, uuid))
            return False

    def delete_uuid(self, uuid:str, snapshots:bool=False, vg_detach:bool=True, wait:bool=True, clusteruuid:str=None):
        """Delete an existing virtual machine by virtual machine uuid.

        :param uuid: The uuid for the VM to be deleted.
        :type uuid: str
        :param snapshots: Whether to also delete VM snapshots when deleting the VM. (Default=False)
        :type snapshots: bool, optional
        :param vg_detach: Whether to also detatch any connected volume groups when deleting the VM. (Default=True)
        :type vg_detach: bool, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the VM was sucessfully created.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.delete_uuid')

        if vg_detach:
            vm = self.search_uuid(uuid=uuid, clusteruuid=clusteruuid, refresh=True)
            if vm:
                for disk in vm.get('vm_disk_info'):
                    if disk.get("disk_address").get('volume_group_uuid'):
                        detach = {
                            'uuid': disk.get("disk_address").get('volume_group_uuid'),
                            'index': disk.get("disk_address").get('device_index'),
                            'vm_uuid': uuid,
                            'wait': True,
                            'clusteruuid': clusteruuid,
                        }
                        self.detach_vg(**detach)

        params = {}
        version = 'v2.0'
        uri = '/vms/{0}'.format(uuid)
        method = 'DELETE'
        payload = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        params['delete_snapshots'] = snapshots
        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)

        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('vm "{0}" deleted successful'.format(uuid))
                    return True
                else:
                    logger.warning('vm "{0}" delete failed. Task details: {1}'.format(uuid, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def add_disks(self, vm_uuid:str, disks:list=None, add_cdrom:bool=False, wait:bool=True, clusteruuid:str=None):
        """Add disks from a dict to an existing virtual machine.

        :param vm_uuid: The uuid for the VM to be have disks added.
        :type vm_uuid: str
        :param disks: A list of vdisks dicts to be added to this VM (default='null').

            The dictionary format per-vDisk is as follows::
                - bus (str, optional, default='scsi'). The bus to use for the vDisk. Choice of 'scsi', 'ide', 'pci', 'sata', 'spapr', 'nvme'
                - size_gb (int, optional). Size of vDisk in GB. Use this when creating a new disk or cloning from an image. Can be used to increase the size of vDisk created from an image
                - storage_container_name (str, optional). Name of Storage Container. Only used when creating a new vDisk. Mutually exclusive with "storage_container_uuid"
                - storage_container_uuid (str, optional). UUID of Storage Container. Only used when creating a new vDisk. Mutually exclusive with "storage_container_name"
                - image_name (str, optional). Name of Image to clone from. Only used when creating a new vDisk from an existing image. Mutually exclusive with "image_uuid"
                - image_uuid (str, optional). UUID of Image to clone from. Only used when creating a new vDisk from an existing image. Mutually exclusive with "image_name"
                - volume_group_name (str, optional). Name of Volume Group to attach. Only used when attaching an existing volume group. Mutually exclusive with "volume_group_uuid"
                - volume_group_uuid (str, optional). UUID of Volume Group to attach. Only used when attaching an existing volume group. Mutually exclusive with "volume_group_name"
                - flash_mode (bool, optional, default=False). True or False
                - label (str, optional). Unknown

            Examples;
                1. Add a single virtual disk - [{'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 50, }, ]
                2. Add multiple virtual disk - [{'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 50, }, {'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 200, }, ]
                3. Add a single virtual disk with flash mode enabled - [{'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 15, 'flash_mode': True}, ]
                4. Add a single virtual disk from an image - [{'bus': 'scsi', 'image_name': 'centos8', }, ]
                5. Add a single virtual disk from an image with a new minimum size - [{'bus': 'scsi', 'image_name': 'centos8', 'size_gb': 500, }, ]
                6. Add a volume group - [{'bus': 'scsi', 'volume_group_name': 'volume_group_database1', }, ]
        :type disks: list, optional
        :param add_cdrom: Whether to add a cdrom drive to this VM (default=True)
        :type add_cdrom: bool, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the disk was successfully added.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.add_disk')

        params = {}
        version = 'v2.0'
        uri = '/vms/{0}/disks/attach'.format(vm_uuid)
        method = 'POST'
        payload = {
            'uuid': vm_uuid,
            'vm_disks': [],
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        device_indexes = {
            'ide': 0,
            'scsi': 0,
            'pci': 0,
            'sata': 0,
            'spapr': 0,
            'nvme': 0,
        }

        vm = self.search_uuid(uuid=vm_uuid, clusteruuid=clusteruuid, refresh=True)
        if vm:
            for existing_disk in vm.get('vm_disk_info'):
                disk_bus = existing_disk.get('disk_address').get('device_bus')
                disk_index = existing_disk.get('disk_address').get('device_index')
                if disk_index > device_indexes[disk_bus]:
                    device_indexes[disk_bus] = disk_index
        else:
            raise ValueError()

        if add_cdrom:
            cdrom_config = {
                'is_cdrom': True,
                'is_empty': True,
                'disk_address': {
                    'device_bus': 'IDE',
                    'device_index': device_indexes['ide'],
                    'is_cdrom': True,
                }
            }
            device_indexes['ide'] += 1
            payload['vm_disks'].append(cdrom_config)

        for disk in disks:
            disk['index'] = device_indexes[disk.get('bus', 'scsi')]

            if any([disk.get('storage_container_name'), disk.get('storage_container_uuid')]) and any([disk.get('image_name'), disk.get('image_uuid')]) and \
                    any([disk.get('volume_group_name'), disk.get('volume_group_uuid')]):
                raise ValueError()

            elif any([disk.get('storage_container_name'), disk.get('storage_container_uuid')]):
                if all([disk.get('storage_container_name'), disk.get('storage_container_uuid')]):
                    raise ValueError()

                elif disk.get('storage_container_name'):
                    logger.debug('searching for container named "{0}"'.format(disk.get('storage_container_name')))
                    containers_obj = StorageContainer(api_client=self.api_client)
                    container = containers_obj.search_name(name=disk.get('storage_container_name'), clusteruuid=clusteruuid)
                    if container:
                        logger.debug('found container named "{0}"'.format(disk.get('storage_container_name')))
                        disk.pop('storage_container_name')
                        disk['storage_container_uuid'] = container.get('storage_container_uuid')
                    else:
                        logger.warning('cannot find container named "{0}"'.format(disk.get('storage_container_name')))
                        raise ValueError()

                elif disk.get('storage_container_uuid'):
                    logger.debug('searching for container "{0}"'.format(disk.get('storage_container_uuid')))
                    containers_obj = StorageContainer(api_client=self.api_client)
                    container = containers_obj.search_uuid(uuid=disk.get('storage_container_uuid'), clusteruuid=clusteruuid)
                    if container:
                        logger.debug('found container "{0}"'.format(disk.get('storage_container_uuid')))
                        disk.pop('storage_container_name')
                        disk['storage_container_uuid'] = disk.get('storage_container_uuid')
                    else:
                        logger.warning('cannot find container "{0}"'.format(disk.get('storage_container_uuid')))
                        raise ValueError()

            elif any([disk.get('image_name'), disk.get('image_uuid')]):
                if all([disk.get('image_name'), disk.get('image_uuid')]):
                    raise ValueError()

                elif disk.get('image_name'):
                    logger.debug('searching for image named "{0}"'.format(disk.get('image_name')))
                    images_obj = Images(api_client=self.api_client)
                    image = images_obj.search_name(name=disk.get('image_name'), clusteruuid=clusteruuid)
                    if image:
                        logger.debug('found image named "{0}"'.format(disk.get('image_name')))
                        disk.pop('image_name')
                        disk['image_uuid'] = image.get('vm_disk_id')
                    else:
                        logger.warning('cannot find image named "{0}"'.format(disk.get('image_name')))
                        raise ValueError()

                elif disk.get('image_uuid'):
                    logger.info('searching for image "{0}"'.format(disk.get('image_uuid')))
                    images_obj = Images(api_client=self.api_client)
                    image = images_obj.search_uuid(uuid=disk.get('image_uuid'), clusteruuid=clusteruuid)
                    if image:
                        logger.debug('found image "{0}"'.format(disk.get('image_uuid')))
                        disk.pop('image_uuid')
                        disk['image_uuid'] = image.get('vm_disk_id')
                    else:
                        logger.warning('cannot find image "{0}"'.format(disk.get('image_uuid')))
                        raise ValueError()

            elif any([disk.get('volume_group_name'), disk.get('volume_group_uuid')]):
                if all([disk.get('volume_group_name'), disk.get('volume_group_uuid')]):
                    raise ValueError()

                elif disk.get('volume_group_name'):
                    logger.info('searching for volume group named "{0}"'.format(disk.get('volume_group_name')))
                    volume_group_obj = StorageVolume(api_client=self.api_client)
                    volume_group = volume_group_obj.search_volume_groups_name(name=disk.get('volume_group_name'), clusteruuid=clusteruuid)
                    if volume_group:
                        logger.debug('found volume group named "{0}"'.format(disk.get('volume_group_name')))
                        disk.pop('volume_group_name')
                        vg = {
                            'index': disk['index'],
                            'uuid': volume_group.get('uuid'),
                        }
                        self.attach_vg(vm_uuid=vm_uuid, wait=wait, clusteruuid=clusteruuid, **vg)
                    else:
                        logger.warning('cannot find volume group named "{0}"'.format(disk.get('volume_group_name')))
                        raise ValueError()

                elif disk.get('volume_group_uuid'):
                    logger.info('searching for volume group "{0}"'.format(disk.get('volume_group_uuid')))
                    volume_group_obj = StorageVolume(api_client=self.api_client)
                    volume_group = volume_group_obj.search_volume_groups_uuid(uuid=disk.get('volume_group_uuid'), clusteruuid=clusteruuid)
                    if volume_group:
                        logger.debug('found volume group "{0}"'.format(disk.get('volume_group_uuid')))
                        disk.pop('volume_group_uuid')
                        vg = {
                            'index': disk['index'],
                            'uuid': volume_group.get('uuid'),
                        }
                        self.attach_vg(vm_uuid=vm_uuid, wait=wait, clusteruuid=clusteruuid, **vg)
                    else:
                        logger.warning('cannot find volume group "{0}"'.format(disk.get('volume_group_uuid')))
                        raise ValueError()

            if any([disk.get('storage_container_name'), disk.get('storage_container_uuid'), disk.get('image_name'), disk.get('image_uuid'), ]):
                payload['vm_disks'].append(self._vm_disk_spec(**disk))
            device_indexes[disk.get('bus', 'scsi')] += 1

        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)

        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('disk added to vm "{0}" successfully'.format(vm_uuid))
                    return True
                else:
                    logger.warning('disk failed to be added to vm "{0}". Task details: {1}'.format(vm_uuid, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def remove_disk(self, vm_uuid:str, bus:str=None, index:int=None, wait:bool=True, clusteruuid:str=None):
        """Remove a disk from a VM

        :param vm_uuid: The uuid for the VM to have a disk removed.
        :type vm_uuid: str
        :param bus: The bus where the disk to be removed is located.
        :type bus: str
        :param index: The index for the disk to be removed.
        :type index: int
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the disk was successfully removed.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.remove_disk')

        params = {}
        version = 'v2.0'
        uri = '/vms/{0}/disks/detach'.format(vm_uuid)
        method = 'POST'
        payload = {
            'uuid': vm_uuid,
            'vm_disks': [],
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        vm = self.search_uuid(uuid=vm_uuid, clusteruuid=clusteruuid, refresh=True)
        if vm:
            for existing_disk in vm.get('vm_disk_info'):
                if existing_disk.get('disk_address').get('device_bus') == bus and existing_disk.get('disk_address').get('device_index') == index:
                    payload['vm_disks'].append(existing_disk)
        else:
            raise ValueError()

        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)

        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('disk removed from vm "{0}" successfully'.format(vm_uuid))
                    return True
                else:
                    logger.warning('disk failed to be removed from vm "{0}". Task details: {1}'.format(vm_uuid, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def attach_vg(self, index:int, uuid:str, vm_uuid:str, wait:bool=True, clusteruuid:str=None):
        """Attach a volume group to an existing virtual machine.

        :param index: The index where the volume groups will be attached.
        :type index: int
        :param uuid: The uuid of the volume group.
        :type uuid: str
        :param vm_uuid: The uuid for the VM to have the volume group attached.
        :type vm_uuid: str
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the volume group was successfully attached.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.attach_vg')

        params = {}
        version = 'v2.0'
        uri = '/volume_groups/{0}/attach'.format(uuid)
        method = 'POST'
        payload = {
            'uuid': uuid,
            'operation': 'ATTACH',
            'vm_uuid': vm_uuid,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        if index:
            payload['index'] = index

        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)

        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.info('vg "{0}" attach to "{1}" successful'.format(uuid, vm_uuid))

                    return True
                else:
                    logger.warning('vg "{0}" attach to "{1}" failed. Task details: {2}'.format(uuid, vm_uuid, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def detach_vg(self, index:int, uuid:str, vm_uuid:str, wait:bool=True, clusteruuid:str=None):
        """Detach a volume group to an existing virtual machine.

        :param index: The index where the volume groups will be attached.
        :type index: int
        :param uuid: The uuid of the volume group.
        :type uuid: str
        :param vm_uuid: The uuid for the VM to have the volume group attached.
        :type vm_uuid: str
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the volume group was successfully detached.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.attach_vg')

        params = {}
        version = 'v2.0'
        uri = '/volume_groups/{0}/detach'.format(uuid)
        method = 'POST'
        payload = {
            'uuid': uuid,
            'operation': 'DETACH',
            'vm_uuid': vm_uuid,
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        if index:
            payload['index'] = index

        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)

        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.info('vg "{0}" detach on "{1}" successful'.format(uuid, vm_uuid))

                    return True
                else:
                    logger.warning('vg "{0}" detach on "{1}" failed. Task details: {2}'.format(uuid, vm_uuid, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def add_nics(self, vm_uuid:str, nics:list=None, wait:bool=True, clusteruuid:str=None):
        """Add one or more nics to an existing virtual machine.

        :param vm_uuid: The uuid for the VM to have the nic attached.
        :type vm_uuid: str
        :param nics: A list of NIC dicts to be added to this VM (default='null').

            The dictionary format per-NIC is as follows::
                - network_name (str, optional). The name of the network or port group to attach the NIC onto. Mutually exclusive with "network_uuid".
                - network_uuid (str, optional). The uuid of the network or port group to attach the NIC onto. Mutually exclusive with "network_name".
                - adaptor_type (str, optional, default='e1000'). The network adaptor type to use for the NIC. Choice of 'e1000', 'e1000e', 'pcnet32', 'vmxnet', 'vmxnet2', 'vmxnet3',
                - connect (bool, optional, default=True). Whether to connect the NIC to the network.
                - mac_address (str, optional, default=None). A user-defined MAC address to use for this NIC.
                - ipam (bool, optional, default=False). Whether to use AHV IPAM to automatically provide an IP address.
                - requested_ip_address (str, optional). A user-defined IP address to use in conjunction with AHV IPAM. Requires 'ipam' to also be set to True.

            Examples;
                1. Create a simple NIC - [{'network_name': 'vm network',}, ]
                2. Create a NIC with AHV IPAM - [{'network_name': 'vm network', 'ipam': True, }, ]
                3. Create multiple NICs with mixed configuration - [{'network_name': 'vm network 1', }, {'network_name': 'vm network 2', 'ipam': True, }, ]
                4. Create a NIC with AHV IPAM and a defined IP address - [{'network_name': 'vm network', 'ipam': True, 'requested_ip_address': '172.16.100.51', }, ]
        :type nics: list, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the nic(s) were successfully added.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.add_nic')

        params = {}
        version = 'v2.0'
        uri = '/vms/{0}/nics'.format(vm_uuid)
        method = 'POST'
        payload = {
            'uuid': vm_uuid,
            'spec_list': [],
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        vm = self.search_uuid(uuid=vm_uuid, clusteruuid=clusteruuid, refresh=True)
        if not vm:
            raise ValueError()

        for nic in nics:
            if all([nic.get('network_uuid'), nic.get('network_name')]):
                raise ValueError()

            elif nic.get('network_name'):
                logger.info('searching for network named "{0}"'.format(nic.get('network_name')))
                networks_obj = Network(api_client=self.api_client)
                network = networks_obj.search_name(name=nic.get('network_name'), clusteruuid=clusteruuid)
                if network:
                    logger.debug('found network named "{0}"'.format(nic.get('network_name')))
                    nic.pop('network_name')
                    nic['network_uuid'] = network.get('uuid')
                else:
                    logger.warning('cannot find network named "{0}"'.format(nic.get('network_name')))
                    raise ValueError()

            elif nic.get('network_uuid'):
                logger.info('searching for network "{0}"'.format(nic.get('network_uuid')))
                networks_obj = Network(api_client=self.api_client)
                network = networks_obj.search_uuid(uuid=nic.get('network_uuid'), clusteruuid=clusteruuid)
                if network:
                    logger.debug('found network named "{0}"'.format(nic.get('network_uuid')))
                    nic.pop('network_uuid')
                    nic['network_uuid'] = nic.get('network_uuid')
                else:
                    logger.warning('cannot find network named "{0}"'.format(nic.get('network_uuid')))
                    raise ValueError()

            payload['spec_list'].append(self._vm_nic_v2(**nic))

        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)

        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('disk added to vm "{0}" successfully'.format(vm_uuid))
                    return True
                else:
                    logger.warning('disk failed to be added to vm "{0}". Task details: {1}'.format(vm_uuid, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def remove_nic(self, vm_uuid:str, mac_address:str, wait:bool=True, clusteruuid:str=None):
        """Remove a single nic from an existing virtual machine.

        :param vm_uuid: The uuid for the VM to have the nic attached.
        :type vm_uuid: str
        :param mac_address: The mac address for the nic to be removed.
        :type mac_address: str
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the nic was successfully removed.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.add_nic')

        params = {}
        version = 'v2.0'
        method = 'DELETE'
        payload = {
            'uuid': vm_uuid,
            'nic_id': [],
        }

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        vm = self.search_uuid(uuid=vm_uuid, clusteruuid=clusteruuid, refresh=True)
        if vm:
            for nic in vm.get('vm_nics'):
                if nic.get('mac_address') == mac_address:
                    payload['nic_id'] = mac_address
                    uri = '/vms/{0}/nics/{1}'.format(vm_uuid, mac_address)

        else:
            raise ValueError()

        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)
        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('disk added to vm "{0}" successfully'.format(vm_uuid))
                    return True
                else:
                    logger.warning('disk failed to be added to vm "{0}". Task details: {1}'.format(vm_uuid, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def power_state(self, uuid:str, desired_state:str='on', wait:bool=True, clusteruuid:str=None):
        """Change the power state of a specific virtual machine.

        :param uuid: The uuid for the virtual machine to have the nic attached.
        :type uuid: str
        :param desired_state: The desired power state for the virtual machine. .
        :type desired_state: str('on', 'off', 'powercycle', 'reset', 'pause', 'suspend', 'resume', 'save', 'acpi_shutdown', 'acpi_reboot')
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the virtual machines power state was successfully changed.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.power_state')

        params = {}
        version = 'v2.0'
        uri = '/vms/{0}/set_power_state'.format(uuid)
        method = 'POST'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        if desired_state not in ["on", "off", "powercycle", "reset", "pause", "suspend", "resume", "save", "acpi_shutdown", "acpi_reboot"]:
            raise ValueError()

        payload = {
            'transition': desired_state.upper()
        }
        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)

        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.info('vm power state change to "{0}" successful'.format(desired_state))

                    return True
                else:
                    logger.warning('vm power state change to "{0}" failed. Task details: {1}'.format(desired_state, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def update_name(self, name:str, new_name:str=None, vcpus:int=None, memory_gb:int=None, sockets:int=None, vcpu_reservation_hz:int=None,
                    memory_reservation_gb:int=None, description:str=None, disks:list=[], nics:list=[], gpus:list=[], serial_ports:list=[], timezone:str=None,
                    add_cdrom:bool=None, ha_priority:int=None, force:bool=False, wait:bool=True, clusteruuid:str=None):
        """Updates a specific virtual machine by the vm name provided.

        :param name: The name for the virtual machine to be updated.
        :type name: str
        :param new_name: A new name for the virtual machine.
        :type new_name: str, optional
        :param vcpus: The number of vCPUs to be assigned to this VM
        :type vcpus: int
        :param memory_gb: The amount of memory in GB to be assigne to this VM
        :type memory_gb: int
        :param sockets: The number of virtual CPU sockets to distribute the defined vCPUs over (default=1)
        :type sockets: int, optional
        :param vcpu_reservation_hz: A CPU reservation in hz for this VM. Only applicable on the ESXi hypervisor. (default=0)
        :type vcpu_reservation_hz: int, optional
        :param memory_reservation_gb: An amount of memory to lock to this VM. Only applicable on the ESXi hypervisor. (default=0)
        :type memory_reservation_gb: int, optional
        :param description: A description for the VM (default='')
        :type description: str, optional
        :param add_cdrom: Whether to add a cdrom drive to this VM (default=True)
        :type add_cdrom: bool, optional
        :param disks: A list of vdisks dicts to be added to this VM (default='null').

            The dictionary format per-vDisk is as follows::
                - bus (str, optional, default='scsi'). The bus to use for the vDisk. Choice of 'scsi', 'ide', 'pci', 'sata', 'spapr', 'nvme'
                - size_gb (int, optional). Size of vDisk in GB. Use this when creating a new disk or cloning from an image. Can be used to increase the size of vDisk created from an image
                - storage_container_name (str, optional). Name of Storage Container. Only used when creating a new vDisk. Mutually exclusive with "storage_container_uuid"
                - storage_container_uuid (str, optional). UUID of Storage Container. Only used when creating a new vDisk. Mutually exclusive with "storage_container_name"
                - image_name (str, optional). Name of Image to clone from. Only used when creating a new vDisk from an existing image. Mutually exclusive with "image_uuid"
                - image_uuid (str, optional). UUID of Image to clone from. Only used when creating a new vDisk from an existing image. Mutually exclusive with "image_name"
                - volume_group_name (str, optional). Name of Volume Group to attach. Only used when attaching an existing volume group. Mutually exclusive with "volume_group_uuid"
                - volume_group_uuid (str, optional). UUID of Volume Group to attach. Only used when attaching an existing volume group. Mutually exclusive with "volume_group_name"
                - flash_mode (bool, optional, default=False). True or False
                - label (str, optional). Unknown

            Examples;
                1. Add a single virtual disk - [{'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 50, }, ]
                2. Add multiple virtual disk - [{'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 50, }, {'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 200, }, ]
                3. Add a single virtual disk with flash mode enabled - [{'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 15, 'flash_mode': True}, ]
                4. Add a single virtual disk from an image - [{'bus': 'scsi', 'image_name': 'centos8', }, ]
                5. Add a single virtual disk from an image with a new minimum size - [{'bus': 'scsi', 'image_name': 'centos8', 'size_gb': 500, }, ]
                6. Add a volume group - [{'bus': 'scsi', 'volume_group_name': 'volume_group_database1', }, ]
        :type disks: list, optional
        :param nics: A list of NIC dicts to be added to this VM (default='null').

            The dictionary format per-NIC is as follows::
                - network_name (str, optional). The name of the network or port group to attach the NIC onto. Mutually exclusive with "network_uuid".
                - network_uuid (str, optional). The uuid of the network or port group to attach the NIC onto. Mutually exclusive with "network_name".
                - adaptor_type (str, optional, default='e1000'). The network adaptor type to use for the NIC. Choice of 'e1000', 'e1000e', 'pcnet32', 'vmxnet', 'vmxnet2', 'vmxnet3',
                - connect (bool, optional, default=True). Whether to connect the NIC to the network.
                - mac_address (str, optional, default=None). A user-defined MAC address to use for this NIC.
                - ipam (bool, optional, default=False). Whether to use AHV IPAM to automatically provide an IP address.
                - requested_ip_address (str, optional). A user-defined IP address to use in conjunction with AHV IPAM. Requires 'ipam' to also be set to True.

            Examples;
                1. Create a simple NIC - [{'network_name': 'vm network',}, ]
                2. Create a NIC with AHV IPAM - [{'network_name': 'vm network', 'ipam': True, }, ]
                3. Create multiple NICs with mixed configuration - [{'network_name': 'vm network 1', }, {'network_name': 'vm network 2', 'ipam': True, }, ]
                4. Create a NIC with AHV IPAM and a defined IP address - [{'network_name': 'vm network', 'ipam': True, 'requested_ip_address': '172.16.100.51', }, ]
        :type nics: list, optional
        :param gpus: A list of GPU dicts to be added to the VM (default='null')

            The dictionary format per-GPU is as follows::
                - device_id (int).
                - gpu_type (str, optional, default='null'). The type of GPU to add. Choice of 'pass_through_graphics'
                - gpu_vendor (str, optional, default='null'). The GPU vendor to add. Choice of 'nvidia',
        :type gpus: list, optional
        :param serial_ports: A list of serial port dicts to be added to the VM (default='null')

            The dictionary format per-serial port is as follows::
                - port_index (int).
                - port_type (str, optional, default='null'). The type of serial port to add. Choice of 'null', 'server'
        :type serial_ports: list, optional
        :param timezone: The timezone for the virtual machine (default='UTC').
        :type timezone: str, optional
        :param ha_priority: VM HA priority. Only applicable to ESXi hypervisor (default=0)
        :type ha_priority: int, optional
        :param force: If the VM is not in a power state that will allow the change to be made, force will change the VM power state to apply the update, then
                        return the VM to its original power state once the update has been completed. (defaults=False)
        :type force: bool, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the virtual machine was successfully updated.
        :rtype: bool
        .. warning:: As VM names are not necessarily unique, the first result returned will be used.
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.update')
        config = None

        if not name:
            raise ValueError()

        elif name:
            vm = self.search_name(name=name, refresh=True, clusteruuid=clusteruuid)
            if vm.get('uuid'):
                vm_config = {
                    'uuid': vm.get('uuid'),
                    'new_name': new_name,
                    'vcpus': vcpus,
                    'memory_gb': memory_gb,
                    'sockets': sockets,
                    'vcpu_reservation_hz': vcpu_reservation_hz,
                    'memory_reservation_gb': memory_reservation_gb,
                    'description': description,
                    'disks': disks,
                    'nics': nics,
                    'gpus': gpus,
                    'serial_ports': serial_ports,
                    'timezone': timezone,
                    'add_cdrom': add_cdrom,
                    'ha_priority': ha_priority,
                    'force': force,
                }

                result = self.update_uuid(wait=wait, clusteruuid=clusteruuid, **vm_config)
                return result
            else:
                raise ValueError()

    def update_uuid(self, uuid:str, new_name:str=None, vcpus:int=None, memory_gb:int=None, sockets:int=None, vcpu_reservation_hz:int=None,
                    memory_reservation_gb:int=None, description:str=None, disks:list=[], nics:list=[], gpus:list=[], serial_ports:list=[], timezone:str=None,
                    add_cdrom:bool=None, ha_priority:int=None, force:bool=False, wait:bool=True, clusteruuid:str=None):
        """Updates a specific virtual machine by the uuid provided

        :param uuid: The uuid for the virtual machine to be updated.
        :type uuid: str
        :param new_name: A new name for the virtual machine.
        :type new_name: str, optional
        :param vcpus: The number of vCPUs to be assigned to this VM
        :type vcpus: int
        :param memory_gb: The amount of memory in GB to be assigne to this VM
        :type memory_gb: int
        :param sockets: The number of virtual CPU sockets to distribute the defined vCPUs over (default=1)
        :type sockets: int, optional
        :param vcpu_reservation_hz: A CPU reservation in hz for this VM. Only applicable on the ESXi hypervisor. (default=0)
        :type vcpu_reservation_hz: int, optional
        :param memory_reservation_gb: An amount of memory to lock to this VM. Only applicable on the ESXi hypervisor. (default=0)
        :type memory_reservation_gb: int, optional
        :param description: A description for the VM (default='')
        :type description: str, optional
        :param add_cdrom: Whether to add a cdrom drive to this VM (default=True)
        :type add_cdrom: bool, optional
        :param disks: A list of vdisks dicts to be added to this VM (default='null').

            The dictionary format per-vDisk is as follows::
                - bus (str, optional, default='scsi'). The bus to use for the vDisk. Choice of 'scsi', 'ide', 'pci', 'sata', 'spapr', 'nvme'
                - size_gb (int, optional). Size of vDisk in GB. Use this when creating a new disk or cloning from an image. Can be used to increase the size of vDisk created from an image
                - storage_container_name (str, optional). Name of Storage Container. Only used when creating a new vDisk. Mutually exclusive with "storage_container_uuid"
                - storage_container_uuid (str, optional). UUID of Storage Container. Only used when creating a new vDisk. Mutually exclusive with "storage_container_name"
                - image_name (str, optional). Name of Image to clone from. Only used when creating a new vDisk from an existing image. Mutually exclusive with "image_uuid"
                - image_uuid (str, optional). UUID of Image to clone from. Only used when creating a new vDisk from an existing image. Mutually exclusive with "image_name"
                - volume_group_name (str, optional). Name of Volume Group to attach. Only used when attaching an existing volume group. Mutually exclusive with "volume_group_uuid"
                - volume_group_uuid (str, optional). UUID of Volume Group to attach. Only used when attaching an existing volume group. Mutually exclusive with "volume_group_name"
                - flash_mode (bool, optional, default=False). True or False
                - label (str, optional). Unknown

            Examples;
                1. Add a single virtual disk - [{'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 50, }, ]
                2. Add multiple virtual disk - [{'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 50, }, {'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 200, }, ]
                3. Add a single virtual disk with flash mode enabled - [{'bus': 'scsi', 'storage_container_name': 'default', 'size_gb': 15, 'flash_mode': True}, ]
                4. Add a single virtual disk from an image - [{'bus': 'scsi', 'image_name': 'centos8', }, ]
                5. Add a single virtual disk from an image with a new minimum size - [{'bus': 'scsi', 'image_name': 'centos8', 'size_gb': 500, }, ]
                6. Add a volume group - [{'bus': 'scsi', 'volume_group_name': 'volume_group_database1', }, ]
        :type disks: list, optional
        :param nics: A list of NIC dicts to be added to this VM (default='null').

            The dictionary format per-NIC is as follows::
                - network_name (str, optional). The name of the network or port group to attach the NIC onto. Mutually exclusive with "network_uuid".
                - network_uuid (str, optional). The uuid of the network or port group to attach the NIC onto. Mutually exclusive with "network_name".
                - adaptor_type (str, optional, default='e1000'). The network adaptor type to use for the NIC. Choice of 'e1000', 'e1000e', 'pcnet32', 'vmxnet', 'vmxnet2', 'vmxnet3',
                - connect (bool, optional, default=True). Whether to connect the NIC to the network.
                - mac_address (str, optional, default=None). A user-defined MAC address to use for this NIC.
                - ipam (bool, optional, default=False). Whether to use AHV IPAM to automatically provide an IP address.
                - requested_ip_address (str, optional). A user-defined IP address to use in conjunction with AHV IPAM. Requires 'ipam' to also be set to True.

            Examples;
                1. Create a simple NIC - [{'network_name': 'vm network',}, ]
                2. Create a NIC with AHV IPAM - [{'network_name': 'vm network', 'ipam': True, }, ]
                3. Create multiple NICs with mixed configuration - [{'network_name': 'vm network 1', }, {'network_name': 'vm network 2', 'ipam': True, }, ]
                4. Create a NIC with AHV IPAM and a defined IP address - [{'network_name': 'vm network', 'ipam': True, 'requested_ip_address': '172.16.100.51', }, ]
        :type nics: list, optional
        :param gpus: A list of GPU dicts to be added to the VM (default='null')

            The dictionary format per-GPU is as follows::
                - device_id (int).
                - gpu_type (str, optional, default='null'). The type of GPU to add. Choice of 'pass_through_graphics'
                - gpu_vendor (str, optional, default='null'). The GPU vendor to add. Choice of 'nvidia',
        :type gpus: list, optional
        :param serial_ports: A list of serial port dicts to be added to the VM (default='null')

            The dictionary format per-serial port is as follows::
                - port_index (int).
                - port_type (str, optional, default='null'). The type of serial port to add. Choice of 'null', 'server'
        :type serial_ports: list, optional
        :param timezone: The timezone for the virtual machine (default='UTC').
        :type timezone: str, optional
        :param ha_priority: VM HA priority. Only applicable to ESXi hypervisor (default=0)
        :type ha_priority: int, optional
        :param force: If the VM is not in a power state that will allow the change to be made, force will change the VM power state to apply the update, then
                        return the VM to its original power state once the update has been completed. (defaults=False)
        :type force: bool, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the virtual machine was successfully updated.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.update')

        if not uuid:
            raise ValueError()

        elif uuid:
            vm = self.search_uuid(uuid=uuid, refresh=True, clusteruuid=clusteruuid)
            if not vm.get('uuid'):
                raise ValueError()


        params = {}
        version = 'v2.0'
        uri = '/vms/{0}'.format(uuid)
        method = 'PUT'
        payload = {
            'uuid': uuid,
        }

        current_power_state = vm.get('power_state').lower()
        required_power_state = None

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        if new_name:
            payload['name'] = new_name

        if description:
            payload['description'] = description

        if memory_gb:
            required_power_state = 'off'
            bm_memory_gb = bitmath.GB(memory_gb)
            bm_memory_mb = bm_memory_gb.to_MB()
            payload['memory_mb'] = int(bm_memory_mb)

        if sockets:
            required_power_state = 'off'
            payload['sockets'] = sockets
        else:
            sockets = vm.get('sockets')

        if vcpus:
            required_power_state = 'off'
            payload['num_vcpus'] = (vcpus/sockets)

        if timezone:
            payload['timezone'] = timezone

        if ha_priority:
            payload['ha_priority'] = ha_priority

        if vcpu_reservation_hz:
            payload['vcpu_reservation_hz'] = int(vcpu_reservation_hz)

        if memory_reservation_gb:
            bm_memory_reservation_gb = bitmath.GB(memory_reservation_gb)
            bm_memory_reservation_mb = bm_memory_reservation_gb.to_MB()
            payload['memory_reservation_mb'] = int(bm_memory_reservation_mb)

        if disks:
            self.add_disks(vm_uuid=uuid, disks=disks, add_cdrom=add_cdrom, wait=wait, clusteruuid=clusteruuid)

        if nics:
            self.add_nics(vm_uuid=uuid, nics=nics, wait=wait, clusteruuid=clusteruuid)

        if gpus:
            required_power_state = 'off'
            pass

        if serial_ports:
            required_power_state = 'off'
            pass

        if current_power_state != required_power_state and force:
            self.power_state(uuid=uuid, desired_state=required_power_state, wait=True, clusteruuid=clusteruuid)
        elif current_power_state != required_power_state and not force:
            raise ValueError()

        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)
        if wait or (current_power_state != required_power_state and force):
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('vm "{0}" updated successfully'.format(uuid))
                    return True
                else:
                    logger.warning('vm "{0}" failed to update. Task details: {1}'.format(uuid, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

        if current_power_state != required_power_state and force:
            self.power_state(uuid=uuid, desired_state=current_power_state, wait=True, clusteruuid=clusteruuid)
        elif current_power_state != required_power_state and not force:
            raise ValueError()

    def clone_name(self, source_name:str, name:str, vcpus:int=None, memory_gb:int=None, sockets:int=None, nics:list=[], sysprep:str=None, cloudinit:str=None,
                   wait:bool=True, clusteruuid:str=None):
        """Clones an existing virtual machine based on the provided virtual machine name.

        :param source_name: The name for the virtual machine to be cloned.
        :type source_name: str
        :param name: The name for the new virtual machine.
        :type name: str
        :param vcpus: The number of vCPUs to be assigned to this VM
        :type vcpus: int
        :param memory_gb: The amount of memory in GB to be assigne to this VM
        :type memory_gb: int
        :param sockets: The number of virtual CPU sockets to distribute the defined vCPUs over (default=1)
        :type sockets: int, optional
        :param nics: A list of NIC dicts to be added to this VM (default='null').

            The dictionary format per-NIC is as follows::
                - network_name (str, optional). The name of the network or port group to attach the NIC onto. Mutually exclusive with "network_uuid".
                - network_uuid (str, optional). The uuid of the network or port group to attach the NIC onto. Mutually exclusive with "network_name".
                - adaptor_type (str, optional, default='e1000'). The network adaptor type to use for the NIC. Choice of 'e1000', 'e1000e', 'pcnet32', 'vmxnet', 'vmxnet2', 'vmxnet3',
                - connect (bool, optional, default=True). Whether to connect the NIC to the network.
                - mac_address (str, optional, default=None). A user-defined MAC address to use for this NIC.
                - ipam (bool, optional, default=False). Whether to use AHV IPAM to automatically provide an IP address.
                - requested_ip_address (str, optional). A user-defined IP address to use in conjunction with AHV IPAM. Requires 'ipam' to also be set to True.

            Examples;
                1. Create a simple NIC - [{'network_name': 'vm network',}, ]
                2. Create a NIC with AHV IPAM - [{'network_name': 'vm network', 'ipam': True, }, ]
                3. Create multiple NICs with mixed configuration - [{'network_name': 'vm network 1', }, {'network_name': 'vm network 2', 'ipam': True, }, ]
                4. Create a NIC with AHV IPAM and a defined IP address - [{'network_name': 'vm network', 'ipam': True, 'requested_ip_address': '172.16.100.51', }, ]
        :type nics: list, optional
        :param sysprep: The sysprep XML string to use to customize this VM upon first power on. Only applicable for AHV and a Windows OS. (default='null')
        :type sysprep: str, optional
        :param cloudinit: The cloudinit text string to use to customize this VM upon first power on. Only applicable for AHV and a Linux OS. (default='null')
        :type cloudinit: str, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the VM was successfully cloned.
        :rtype: bool
        .. warning:: As VM names are not necessarily unique, the first result returned will be used.
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.clone_name')
        uuid = self.search_name(name=source_name, clusteruuid=clusteruuid, refresh=True).get('uuid')
        if uuid:
            logger.debug('cloning vm {0} on cluster {1}'.format(name, clusteruuid))
            return self.clone_uuid(source_uuid=uuid, name=name, vcpus=vcpus, memory_gb=memory_gb, sockets=sockets, nics=nics,
                                   sysprep=sysprep, cloudinit=cloudinit, wait=wait, clusteruuid=clusteruuid)
        else:
            logger.warning('vm {0} not found on cluster {1}'.format(name, uuid))
            return False

    def clone_uuid(self, source_uuid:str, name:str, vcpus:int=None, memory_gb:int=None, sockets:int=None, nics:list=[], sysprep:str=None, cloudinit:str=None,
                   wait:bool=True, clusteruuid:str=None):
        """Clones an existing virtual machine based on the provided virtual machine uuid.

        :param source_uuid: The uuid for the virtual machine to be cloned.
        :type source_uuid: str
        :param name: The name for the new virtual machine.
        :type name: str
        :param vcpus: The number of vCPUs to be assigned to this VM
        :type vcpus: int
        :param memory_gb: The amount of memory in GB to be assigne to this VM
        :type memory_gb: int
        :param sockets: The number of virtual CPU sockets to distribute the defined vCPUs over (default=1)
        :type sockets: int, optional
        :param nics: A list of NIC dicts to be added to this VM (default='null').

            The dictionary format per-NIC is as follows::
                - network_name (str, optional). The name of the network or port group to attach the NIC onto. Mutually exclusive with "network_uuid".
                - network_uuid (str, optional). The uuid of the network or port group to attach the NIC onto. Mutually exclusive with "network_name".
                - adaptor_type (str, optional, default='e1000'). The network adaptor type to use for the NIC. Choice of 'e1000', 'e1000e', 'pcnet32', 'vmxnet', 'vmxnet2', 'vmxnet3',
                - connect (bool, optional, default=True). Whether to connect the NIC to the network.
                - mac_address (str, optional, default=None). A user-defined MAC address to use for this NIC.
                - ipam (bool, optional, default=False). Whether to use AHV IPAM to automatically provide an IP address.
                - requested_ip_address (str, optional). A user-defined IP address to use in conjunction with AHV IPAM. Requires 'ipam' to also be set to True.

            Examples;
                1. Create a simple NIC - [{'network_name': 'vm network',}, ]
                2. Create a NIC with AHV IPAM - [{'network_name': 'vm network', 'ipam': True, }, ]
                3. Create multiple NICs with mixed configuration - [{'network_name': 'vm network 1', }, {'network_name': 'vm network 2', 'ipam': True, }, ]
                4. Create a NIC with AHV IPAM and a defined IP address - [{'network_name': 'vm network', 'ipam': True, 'requested_ip_address': '172.16.100.51', }, ]
        :type nics: list, optional
        :param sysprep: The sysprep XML string to use to customize this VM upon first power on. Only applicable for AHV and a Windows OS. (default='null')
        :type sysprep: str, optional
        :param cloudinit: The cloudinit text string to use to customize this VM upon first power on. Only applicable for AHV and a Linux OS. (default='null')
        :type cloudinit: str, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the VM was successfully cloned.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.Vms.clone_uuid')

        params = {}
        version = 'v2.0'
        uri = '/vms/{0}/clone'.format(source_uuid)
        method = 'POST'
        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        vm = self.search_uuid(uuid=source_uuid, clusteruuid=clusteruuid, refresh=True)
        if vm:
            logger.info('vm found "{0}"'.format(vm))
        else:
            raise ValueError()

        spec = {
            'name': name,
            'num_vcpus': vm.get('num_vcpus'),
            'num_cores_per_vcpu': vm.get('num_cores_per_vcpu'),
            'memory_mb': vm.get('memory_mb'),
            'override_network_config': False,
        }

        payload = {
            'uuid': source_uuid,
            'spec_list': [],
        }

        if sockets:
            spec['num_vcpus'] = sockets

        if vcpus:
            spec['num_cores_per_vcpu'] = (vcpus/spec['num_vcpus'])

        if memory_gb:
            bm_memory_gb = bitmath.GB(memory_gb)
            bm_memory_mb = bm_memory_gb.to_MB()
            spec['memory_mb'] = int(bm_memory_mb)

        if nics:
            spec['override_network_config'] = True
            for nic in nics:
                pass

        payload['spec_list'].append(spec)

        if all([sysprep, cloudinit]):
            raise ValueError('Please provide either sysprep or cloudinit NOT both.')

        elif sysprep:
            payload['vm_customization_config'] = {
                'fresh_install': False,
                'userdata': sysprep,
            }

        elif cloudinit:
            payload['vm_customization_config'] = {
                'fresh_install': False,
                'userdata': cloudinit,
            }

        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)
        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('vm "{0}" cloned successful'.format(source_uuid))
                    return True
                else:
                    logger.warning('vm "{0}" clone failed. Task details: {1}'.format(source_uuid, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False


class Images(object):
    """A class to represent a Nutanix Clusters Images

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        logger = logging.getLogger('ntnx_api.prism.Images.__init__')
        self.api_client = api_client
        self.images = {}

    def get(self, clusteruuid=None):
        """Retrieve data for each image in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each image from the specified cluster.
        :rtype: ResponseList

        .. note:: Images are only present for cluster running the AHV hypervisor.
        """
        logger = logging.getLogger('ntnx_api.prism.Images.get')
        logger.info('starting function to retrieve images from cluster api')

        # Remove existing data for this cluster if it exists
        if self.images.get(clusteruuid):
            self.images.pop(clusteruuid)
            logger.info('removing existing data from class dict images for cluster {0}'.format(clusteruuid))

        params = {'length': '2147483647'}
        payload = None
        uri = '/images'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.images[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.images[clusteruuid]

    def search_uuid(self, uuid, clusteruuid=None, refresh=False):
        """Retrieve data for a specific image, in a specific cluster by image uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A image uuid to search for.
        :type uuid: str
        :param refresh: Whether to refresh the data stored in the class prior to performing the search. Defaults to False.
        :type refresh: bool, optional

        :returns: A dictionary describing the found image.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Images.search_uuid')
        logger.info('starting function to search for image by uuid')
        found = {}
        if not self.images.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        for entity in self.images.get(clusteruuid):
            if entity.get('uuid') == uuid:
                found = entity
                break

            if entity.get('vm_disk_id') == uuid:
                found = entity
                break

        if found:
            logger.info('image found: {0}'.format(found))
        else:
            logger.info('image not found: {0}'.format(found))

        return found

    def search_name(self, name, clusteruuid=None, refresh=False):
        """Retrieve data for a specific image, in a specific cluster by image name

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A image name to search for.
        :type name: str
        :param refresh: Whether to refresh the data stored in the class prior to performing the search. Defaults to False.
        :type refresh: bool, optional

        :returns: A dictionary describing the found image.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Images.search_name')
        logger.info('starting function to search for image by name')
        found = {}
        if not self.images.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        for entity in self.images.get(clusteruuid):
            if entity.get('name') == name:
                found = entity
                break

        if found:
            logger.info('image found: {0}'.format(found))
        else:
            logger.info('image not found: {0}'.format(found))

        return found

    def delete_name(self, name, clusteruuid=None, wait=False):
        """Delete an existing image based on the image name provided

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A image name to be deleted.
        :type name: str
        :param wait: Wait for the image task to complete. Defaults to False.
        :type wait: bool, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Images.delete_name')
        image_search = self.search_name(name=name, clusteruuid=clusteruuid, refresh=True)
        if image_search:
            logger.info('image {0} found with uuid {1}'.format(name, image_search.get('uuid')))
            self.delete_uuid(uuid=image_search.get('uuid'), clusteruuid=clusteruuid, wait=wait)

    def delete_uuid(self, uuid, clusteruuid=None, wait=False):
        """Delete an existing image based on the image uuid provided

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A image uuid to be deleted.
        :type uuid: str
        :param wait: Wait for the image task to complete. Defaults to False.
        :type wait: bool, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Images.delete_uuid')
        params = {}
        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        uri = '/images/{0}'.format(uuid)
        method = 'DELETE'

        delete_task = self.api_client.request(uri=uri, api_version='v2.0', params=params, method=method, response_code=200)
        task_uuid = delete_task.get('task_uuid')

        if wait:
            task_obj = Task(api_client=self.api_client)
            thread = threading.Thread(target=task_obj.watch_task(task_uuid=task_uuid, clusteruuid=clusteruuid))
            thread.start()

            task_obj.task_status.wait()
            logger.info('image {0} deleted'.format(task_uuid))
        else:
            logger.info('task created to delete image {0}'.format(task_uuid))

    def upload_from_url(self, name, url, storage_container_uuid, image_type='disk', annotation='', clusteruuid=None, wait=False):
        """ Upload an image from a URL. The target URL needs to be accessible from the CVM network on the target Nutanix cluster.

        :param name: A name for the image to be creted.
        :type name: str
        :param url: A URL that resolves to the file of the image to be created.
        :type url: str
        :param storage_container_uuid: The UUID of the storage container on which to place the image.
        :type storage_container_uuid: str
        :param image_type: The type of image to be created. (default=disk).
        :type image_type: str('disk', 'iso'), optional
        :param annotation: The annotation to set on the image. (default='').
        :type annotation: str, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param wait: Wait for the task to complete. (default=false).
        :type wait: bool, optional

        :return: Result of image upload. If Tur the image was created successfully. If False the image creation was unsuccessful
        :rtype: Bool
        """
        logger = logging.getLogger('ntnx_api.prism.Images.upload_from_url')
        params = {}
        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        if image_type == 'disk':
            image_type = 'DISK_IMAGE'
        else:
            image_type = 'ISO_IMAGE'

        # check image with the same name doesn't already exist
        image_search = self.search_name(name=name, clusteruuid=clusteruuid, refresh=True)
        if image_search:
            logger.warning('image with same name "{0}" already exists'.format(name))
            return False

        else:
            # begin image creation & upload
            uri = '/images'
            method = 'POST'
            image_spec = {
                "storage_container_uuid": storage_container_uuid,
                "url": url
            }
            payload = {
                "annotation": annotation,
                "image_type": image_type,
                "name": name,
                "image_import_spec": image_spec,
                "storage_container_uuid": storage_container_uuid,
            }

            upload_task = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method, response_code=201)
            upload_task_uuid = upload_task.get('task_uuid')

            if wait:
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=upload_task_uuid, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[upload_task_uuid].get('progress_status').lower() == 'succeeded':
                    logger.info('image upload successful')
                    return True
                else:
                    logger.warning('image upload failed')

                    # clean up failed image
                    for image in task_obj.task_result[upload_task_uuid].get('entity_list'):
                        self.delete_uuid(uuid=image.get('entity_id'), clusteruuid=None)
                    return False

            else:
                logger.info('task created to upload image {0}'.format(upload_task_uuid))

    def upload_from_file(self, name, file_path, storage_container_uuid, image_type='disk', annotation='', clusteruuid=None, wait=False):
        """ Upload an image from a file path. The target file path needs to be accessible on the device running this script.

        :param name: A name for the image to be creted.
        :type name: str
        :param file_path: A file path that resolves to the file of the image to be created.
        :type file_path: str
        :param storage_container_uuid: The UUID of the storage container on which to place the image.
        :type storage_container_uuid: str
        :param image_type: The type of image to be created. (default=disk).
        :type image_type: str('disk', 'iso'), optional
        :param annotation: The annotation to set on the image. (default='').
        :type annotation: str, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param wait: Wait for the task to complete. (default=false).
        :type wait: bool, optional

        :return: Result of image upload. If Tur the image was created successfully. If False the image creation was unsuccessful
        :rtype: Bool
        """
        logger = logging.getLogger('ntnx_api.prism.Images.upload_from_file')
        params = {}
        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        if image_type == 'disk':
            image_type = 'DISK_IMAGE'
        else:
            image_type = 'ISO_IMAGE'

        # check image with the same name doesn't already exist
        image_search = self.search_name(name=name, clusteruuid=clusteruuid, refresh=True)
        if image_search:
            logger.warning('image with same name "{0}" already exists'.format(name))
            return False
        else:
            # begin image creation & upload
            uri = '/images'
            method = 'POST'
            payload = {
                "annotation": annotation,
                "image_type": image_type,
                "name": name,
                "storage_container_uuid": storage_container_uuid,
            }

            create_image_task = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method, response_code=201)
            create_image_task_uuid = create_image_task.get('task_uuid')

            task_obj = Task(api_client=self.api_client)
            thread = threading.Thread(target=task_obj.watch_task(task_uuid=create_image_task_uuid, clusteruuid=clusteruuid))
            thread.start()
            task_obj.task_status.wait()

            image = self.search_name(name=name, refresh=True, clusteruuid=clusteruuid)
            logger.info('image found: {0}'.format(image))
            if image:
                logger.info('starting image upload')
                image_uuid = image.get('uuid')

                uri = '/images/{0}/upload'.format(image_uuid)
                method = 'PUT'
                header_dict = {'X-Nutanix-Destination-Container': storage_container_uuid}
                image_upload_task = self.api_client.upload(uri=uri, file_path=file_path, header_dict=header_dict, api_version='v0.8',
                                                           params=params, method=method, response_code=200, timeout=600)

                upload_task_uuid = image_upload_task.get('task_uuid')
                logger.info('Task {0}'.format(image_upload_task))

                if wait:
                    task_obj = Task(api_client=self.api_client)
                    thread = threading.Thread(target=task_obj.watch_task(task_uuid=upload_task_uuid, clusteruuid=clusteruuid))
                    thread.start()

                    task_obj.task_status.wait()
                    if task_obj.task_result[upload_task_uuid].get('progress_status').lower() == 'succeeded':
                        logger.info('image upload successful')
                        return True
                    else:
                        logger.warning('image upload failed')

                        # clean up failed image
                        for image in task_obj.task_result[upload_task_uuid].get('entity_list'):
                            self.delete_uuid(uuid=image.get('entity_id'), clusteruuid=None)
                        return False

                else:
                    logger.info('task created to upload image {0}'.format(upload_task_uuid))
                    return True

            else:
                logger.error('image not found for upload')
                return False


class StoragePool(object):
    """A class to represent a Nutanix Clusters Storage Pool object.

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        logger = logging.getLogger('ntnx_api.prism.StoragePool.__init__')
        self.api_client = api_client
        self.storage_pools = {}

    def get(self, clusteruuid=None):
        """Retrieve data for each storage pool in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each storage pool from the specified cluster.
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.StoragePool.get')

        # Remove existing data for this cluster if it exists
        if self.storage_pools.get(clusteruuid):
            self.storage_pools.pop(clusteruuid)
            logger.info('removing existing data from class dict storage_containers for cluster {0}'.format(clusteruuid))

        params = {'count': '2147483647'}
        payload = None
        uri = '/storage_pools'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.storage_pools[clusteruuid] = self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params).get('entities')
        return self.storage_pools[clusteruuid]

    def search_uuid(self, uuid, clusteruuid=None, refresh=False):
        """Retrieve data for a specific storage pool, in a specific cluster by uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A container uuid to search for.
        :type uuid: str, optional
        :returns: A dictionary describing the found storage pool.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.StoragePool.search_uuid')
        # found = {}
        if not self.storage_pools.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        # for entity in self.storage_pools.get(clusteruuid):
        #     if entity.get('storagePoolUuid') == uuid:
        #         found = entity
        #         break
        found = next((item for item in self.storage_pools.get(clusteruuid) if item.get("storagePoolUuid") == uuid), None)

        return found

    def search_name(self, name, clusteruuid=None, refresh=False):
        """Retrieve data for a specific storage pool, in a specific cluster by uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A storage pool name to search for.
        :type name: str, optional

        :returns: A dictionary describing the found storage pool.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.StoragePool.search_name')
        # found = {}
        if not self.storage_pools.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        # for entity in self.storage_pools.get(clusteruuid):
        #     if entity.get('name') == name:
        #         found = entity
        #         break
        found = next((item for item in self.storage_pools.get(clusteruuid) if item.get("name") == name), None)

        return found


class StorageContainer(object):
    """A class to represent a Nutanix Clusters Storage Container object.

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        logger = logging.getLogger('ntnx_api.prism.StorageContainer.__init__')
        self.api_client = api_client
        self.storage_containers = {}

    def get(self, clusteruuid=None):
        """Retrieve data for each container in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each container from the specified cluster.
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.StorageContainer.get')

        # Remove existing data for this cluster if it exists
        if self.storage_containers.get(clusteruuid):
            self.storage_containers.pop(clusteruuid)
            logger.info('removing existing data from class dict storage_containers for cluster {0}'.format(clusteruuid))

        params = {'count': '2147483647'}
        payload = None
        uri = '/storage_containers'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.storage_containers[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        logger.info('retrived containers for cluster {0}: {1}'.format(clusteruuid, self.storage_containers.get(clusteruuid)))
        return self.storage_containers.get(clusteruuid)

    def search_uuid(self, uuid, clusteruuid=None, refresh=False):
        """Retrieve data for a specific container, in a specific cluster by container uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A container uuid to search for.
        :type uuid: str, optional
        :returns: A dictionary describing the found container.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.StorageContainer.search_uuid')
        if not self.storage_containers.get(clusteruuid) or refresh:
            logger.info('refreshing storage containers')
            self.get(clusteruuid)

        logger.info('searching containers in cluster "{0}" for uuid "{1}".'.format(clusteruuid, uuid))
        logger.info('cluster {0} storage containers: {1}'.format(clusteruuid, self.storage_containers.get(clusteruuid)))
        found = next((item for item in self.storage_containers.get(clusteruuid) if item.get("storage_container_uuid") == uuid), None)
        logger.info('found storage container: {0}'.format(found))
        return found

    def search_name(self, name, clusteruuid=None, refresh=False):
        """Retrieve data for a specific container, in a specific cluster by container uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A container name to search for.
        :type name: str, optional

        :returns: A dictionary describing the found container.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.StorageContainer.search_name')
        if not self.storage_containers.get(clusteruuid) or refresh:
            logger.info('refreshing storage containers')
            self.get(clusteruuid)

        logger.info('searching containers in cluster "{0}" for name "{1}".'.format(clusteruuid, name))
        logger.info('cluster {0} storage containers: {1}'.format(clusteruuid, self.storage_containers.get(clusteruuid)))
        found = next((item for item in self.storage_containers.get(clusteruuid) if item.get("name") == name), None)
        logger.info('found storage container: {0}'.format(found))
        return found

    def create(self, name, rf=2, oplog_rf=2, reserved=None, advertised=None, compression=True, compression_delay=0, dedupe_cache=False, dedupe_capacity=False,
               ecx=False, ecx_delay=None, whitelist=None, storage_pool_uuid=None, clusteruuid=None):
        """Create a new container in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: The name for the new container. Only unique container names are allowed.
        :type name: str
        :param rf: The RF level of the container.
        :type rf: int, optional
        :param oplog_rf: The RF level of the container.
        :type oplog_rf: int, optional
        :param reserved: The reservation size of the container in bytes.
        :type reserved: int, optional
        :param advertised: The advertised size of the container in bytes.
        :type advertised: int, optional
        :param compression: Whether to enable compression.
        :type compression: bool, optional
        :param compression_delay: The amount of time in secs before data is compressed Set to 0 for inline compression.
        :type compression_delay: int, optional
        :param dedupe_cache: Whether to apply deduplication to data in the cache tier.
        :type dedupe_cache: bool, optional
        :param dedupe_capacity: Whether to apply deduplication to data in the capacity tier.
        :type dedupe_capacity: bool, optional
        :param ecx: Whether to enable erasure coding.
        :type ecx: bool, optional
        :param ecx_delay: The age of the data in the capacity tier in seconds before erasure coding is applied.
        :type ecx_delay: int, optional
        :param whitelist: A list of IPs/subnets to whiteist for access to this container. Used for data migration purposes onle.
        :type whitelist: list, optional

        :returns: `True` if the container was sucessfully created, `False` if creation failed.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageContainer.create')
        params = {}
        payload = {}
        uri = '/storage_containers'
        method = 'POST'
        response_code = 201

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        if storage_pool_uuid:
            storage_pool_obj = StoragePool(api_client=self.api_client)
            found_storage_pool = storage_pool_obj.search_uuid(uuid=storage_pool_uuid, clusteruuid=clusteruuid)
            if not found_storage_pool:
                raise ValueError('Storage Pool UUID "{0}" not found on the cluster. Please check inputs and try again.'.format(storage_pool_uuid))

        # Check whether a container with same name already exists
        if not self.search_name(name=name, clusteruuid=clusteruuid, refresh=True):
            payload['name'] = name
            payload['replication_factor'] = int(rf)
            payload['oplog_replication_factor'] = oplog_rf

            if storage_pool_uuid:
                payload['storage_pool_uuid'] = storage_pool_uuid

            if compression:
                payload['compression_enabled'] = 'true'

            if compression:
                payload['compression_delay_in_secs'] = int(compression_delay)

            if advertised:
                payload['advertised_capacity'] = int(advertised)

            if reserved:
                payload['total_explicit_reserved_capacity'] = int(reserved)
            else:
                payload['total_explicit_reserved_capacity'] = 0

            if ecx:
                payload['erasure_code'] = 'on'

                if ecx_delay:
                    payload['erasure_code_delay_secs'] = int(ecx_delay)
            else:
                payload['erasure_code'] = 'off'

            if dedupe_cache:
                payload['finger_print_on_write'] = 'on'

                if dedupe_capacity:
                    payload['on_disk_dedup'] = 'POST_PROCESS'
                else:
                    payload['on_disk_dedup'] = 'OFF'

            else:
                payload['finger_print_on_write'] = 'off'
                payload['on_disk_dedup'] = 'OFF'

            if whitelist:
                if isinstance(whitelist, list):
                    payload['nfs_whitelist'] = whitelist
                else:
                    logger.warning('whitelist {0} is not in the correct format. Please provide a list ["10.0.0.0/24","10.0.0.1/24"]'.format(name, clusteruuid))

            return self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method, response_code=response_code).get('value')

        else:
            raise ValueError('A Storage Pool "{0}" with the same name already exists on this cluster. Please check inputs and try again.'.format(name))

    def update(self, name, reserved=None, advertised=None, compression=True, compression_delay=0, dedupe_cache=False, dedupe_capacity=False, ecx=False,
               ecx_delay=None, whitelist=None, clusteruuid=None):
        """Update a specific container in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: The name for the existing container.
        :type name: str
        :param reserved: The reservation size of the container in bytes.
        :type reserved: int, optional
        :param advertised: The advertised size of the container in bytes.
        :type advertised: int, optional
        :param compression: Whether to enable compression.
        :type compression: bool, optional
        :param compression_delay: The amount of time in secs before data is compressed Set to 0 for inline compression.
        :type compression_delay: int, optional
        :param dedupe_cache: Whether to apply deduplication to data in the cache tier.
        :type dedupe_cache: bool, optional
        :param dedupe_capacity: Whether to apply deduplication to data in the capacity tier.
        :type dedupe_capacity: bool, optional
        :param ecx: Whether to enable erasure coding.
        :type ecx: bool, optional
        :param ecx_delay: The age of the data in the capacity tier in seconds before erasure coding is applied.
        :type ecx_delay: int, optional
        :param whitelist: A list of IPs/subnets to whiteist for access to this container. Used for data migration purposes onle.
        :type whitelist: list, optional

        :returns: `True` if the container was successfully updated, `False` if the update failed.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageContainer.create')
        params = {}
        uri = '/storage_containers'
        method = 'PUT'
        response_code = 200

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        # Check whether a container with same name already exists
        payload = self.search_name(name=name, clusteruuid=clusteruuid, refresh=True)
        logger.debug('container found: {0}'.format(payload))
        if payload:
            remove_keys = [
                'stats',
                'usage_stats',
                'seq_io_preference',
                'ilm_policy',
                'down_migrate_times_in_secs',
                'random_io_preference',
                'marked_for_removal',
                'max_capacity',
            ]
            for key in remove_keys:
                payload.pop(key)

            compression_lookup = {
                'true': True,
                'false': False,
            }
            if compression:
                if compression != compression_lookup.get(payload.get('compression_enabled')):
                    payload['compression_enabled'] = compression
                    logger.info('setting "compression_enabled" to "{0}"'.format(compression))
                else:
                    logger.info('leaving "compression_enabled" at its original value of "{0}"'.format(payload.get('compression_enabled')))

            if compression_delay:
                if int(compression_delay) != int(payload.get('compression_delay_in_secs')) and compression:
                    payload['compression_delay_in_secs'] = int(compression_delay)
                    logger.info('setting "compression_delay_in_secs" to "{0}"'.format(compression_delay))
                else:
                    logger.info('leaving "compression_delay_in_secs" at its original value of "{0}"'.format(payload.get('compression_delay_in_secs')))

            if advertised:
                if int(advertised) != int(payload.get('advertised_capacity')):
                    payload['advertised_capacity'] = int(advertised)
                    logger.info('setting "advertised_capacity" to "{0}"'.format(advertised))
                else:
                    logger.info('leaving "advertised_capacity" at its original value of "{0}"'.format(payload.get('advertised_capacity')))

            if reserved:
                if int(reserved) != int(payload.get('total_explicit_reserved_capacity')):
                    payload['total_explicit_reserved_capacity'] = int(reserved)
                    logger.info('setting "total_explicit_reserved_capacity" to "{0}"'.format(reserved))
                else:
                    logger.info('leaving "total_explicit_reserved_capacity" at its original value of "{0}"'.format(payload.get('total_explicit_reserved_capacity')))

            if dedupe_cache:
                if int(dedupe_cache) != int(payload.get('compression_delay_in_secs')):
                    payload['compression_delay_in_secs'] = int(compression_delay)
                    logger.info('setting "dedupe_cache" to "{0}"'.format(dedupe_cache))
                else:
                    logger.info('leaving "dedupe_cache" at its original value of "{0}"'.format(payload.get('compression_delay_in_secs')))

            dedupe_capacity_lookup = {
                'OFF': False,
                'NONE': False,
                'POST_PROCESS': True,
            }
            if dedupe_capacity:
                if dedupe_capacity != dedupe_capacity_lookup.get(payload.get('dedupe_capacity')):
                    payload['dedupe_capacity'] = dedupe_capacity
                    logger.info('setting "on_disk_dedup" to "{0}"'.format(dedupe_capacity))
                else:
                    logger.info('leaving "dedupe_capacity" at its original value of "{0}"'.format(payload.get('dedupe_capacity')))

            ecx_lookup = {
                'on': True,
                'off': False,
            }
            if ecx:
                if ecx != ecx_lookup.get(payload.get('erasure_code')):
                    payload['erasure_code'] = 'on'
                else:
                    payload['erasure_code'] = 'off'

            if ecx_delay:
                if int(ecx_delay) != int(payload['erasure_code_delay_secs']):
                    payload['erasure_code_delay_secs'] = int(ecx_delay)

            if whitelist:
                if isinstance(whitelist, list):
                    if all(item in whitelist for item in payload.get('nfs_whitelist')):
                        payload['nfs_whitelist'] = whitelist
                else:
                    logger.warning('whitelist {0} is not in the correct format. Please provide a list ["10.0.0.0/24","10.0.0.1/24"]'.format(name, clusteruuid))

            return self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method, response_code=response_code).get('value')

        else:
            raise ValueError('The defined Storage Pool "{0}" was not found on the cluster. Please check inputs and try again.'.format(name))

    def delete_name(self, name, clusteruuid=None):
        """Delete a specific container by its name in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: The name for the container.
        :type name: str

        :returns: `True` if the container was successfully updated, `False` if the update failed.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageContainer.delete_by_name')
        container_uuid = self.search_name(name=name, clusteruuid=clusteruuid, refresh=True).get('storage_container_uuid')

        if container_uuid:
            return self.delete_uuid(uuid=container_uuid, clusteruuid=clusteruuid)
            logger.info('deleted container {0} on cluster {1}'.format(name, clusteruuid))
        else:
            logger.warning('container {0} not found on cluster {1}'.format(name, clusteruuid))
            return False

    def delete_uuid(self, uuid, clusteruuid=None):
        """Delete a specific container by its UUID in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: The uuid for the container.
        :type uuid: str

        :returns: `True` if the container was successfully updated, `False` if the update failed.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageContainer.delete_by_uuid')
        params = {}
        payload = {}
        uri = '/storage_containers/{0}'.format(uuid)
        method = 'DELETE'
        response_code = 204

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        try:
            self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method, response_code=response_code)
            return True

        except:
            return False


class StorageVolume(object):
    """A class to represent a Nutanix Clusters Storage Volumes object.

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.__init__')
        self.api_client = api_client
        self.volume_groups = {}
        self.volumes = {}

    def get(self, clusteruuid=None):
        """Retrieve data for each volume group & all volumes in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.get')
        self.get_volume_groups(clusteruuid)
        self.get_volumes(clusteruuid)

    def get_volume_groups(self, clusteruuid=None):
        """Retrieve data for each volume group in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each volume group from the specified cluster.
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.get_volume_groups')

        # Remove existing data for this cluster if it exists
        if self.volume_groups.get(clusteruuid):
            self.volume_groups.pop(clusteruuid)
            logger.info('removing existing data from class dict volume_groups for cluster {0}'.format(clusteruuid))

        params = {}
        payload = None
        uri = '/volume_groups'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.volume_groups[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        return self.volume_groups[clusteruuid]

    def search_volume_groups_uuid(self, uuid, clusteruuid=None, refresh=False):
        """Retrieve data for a specific volume group, in a specific cluster by volume group uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A volume group uuid to search for.
        :type uuid: str, optional

        :returns: A dictionary describing the found volume group.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.search_volume_groups_uuid')
        found = {}
        if not self.volume_groups.get(clusteruuid) or refresh:
            logger.info('retreving volume group dataset from API')
            self.get_volume_groups(clusteruuid)

        for entity in self.volume_groups.get(clusteruuid):
            if entity.get('uuid') == uuid:
                found = entity
                break

        return found

    def search_volume_groups_name(self, name, clusteruuid=None, refresh=False):
        """Retrieve data for a specific volume group, in a specific cluster by volume group uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A volume group name to search for.
        :type name: str, optional
        :returns: A dictionary describing the found volume group.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.search_volume_groups_name')
        found = {}
        if not self.volume_groups.get(clusteruuid) or refresh:
            self.get_volume_groups(clusteruuid)

        for entity in self.volume_groups.get(clusteruuid):
            if entity.get('name') == name:
                found = entity
                break

        return found

    def get_volumes(self, clusteruuid=None, refresh=False):
        """Retrieve data for each volume in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each volume group from the specified cluster.
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.get_volumes')

        # Remove existing data for this cluster if it exists
        if self.volumes.get(clusteruuid):
            self.volumes.pop(clusteruuid)
            logger.info('removing existing data from class dict volumes for cluster {0}'.format(clusteruuid))

        result = []

        if not self.volume_groups.get(clusteruuid) or refresh:
            self.get_volume_groups(clusteruuid)

        for entity in self.volume_groups.get(clusteruuid):
            volumes = {
                'volume_group': entity.get('name'),
                'disk_list': entity.get('disk_list'),
            }
            result.append(volumes)

        self.volumes[clusteruuid] = result
        return self.volumes[clusteruuid]

    def _disk_config(self, size_gb:int=0, index:int=0, storage_container_name:str=None, storage_container_uuid:str=None, clusteruuid:str=None):
        """
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume._disk_config')

        if size_gb:
            bm_size_gb = bitmath.GiB(size_gb)
            bm_size = bm_size_gb.to_Byte()
        else:
            raise ValueError()

        if all([storage_container_name, storage_container_uuid]):
            raise ValueError()

        elif storage_container_name:
            logger.debug('searching for container named "{0}"'.format(storage_container_name))
            containers_obj = StorageContainer(api_client=self.api_client)
            container = containers_obj.search_name(name=storage_container_name, clusteruuid=clusteruuid)
            if container:
                logger.debug('found container named "{0}"'.format(storage_container_name))
                storage_container_uuid = container.get('storage_container_uuid')
            else:
                logger.warning('cannot find container named "{0}"'.format(storage_container_name))
                raise ValueError()

        elif storage_container_uuid:
            logger.debug('searching for container "{0}"'.format(storage_container_uuid))
            containers_obj = StorageContainer(api_client=self.api_client)
            container = containers_obj.search_uuid(uuid=storage_container_uuid, clusteruuid=clusteruuid)
            if container:
                logger.debug('found container "{0}"'.format(storage_container_uuid))
            else:
                logger.warning('cannot find container "{0}"'.format(storage_container_uuid))
                raise ValueError()

        disk = {
            # 'container_uuid': storage_container_uuid,
            'index': index,
            'create_config': {
                'storage_container_uuid': storage_container_uuid,
                'size': int(bm_size)
            },
            'create_spec': {
                'container_uuid': storage_container_uuid,
                'size': int(bm_size)
            },
        }

        return disk

    def create_volume_group(self, name:str, description:str='', flash_mode:bool=False, load_balancing:bool=True, disks:list=[], vms:list=[],
                            iscsi_initators:list=[], iscsi_target:str=None, iscsi_chap_password:str=None, wait:bool=True, clusteruuid=None):
        """Create a new volume group.

        :param name: A name for the new volume group.
        :type name: str
        :param description: A description for this volume group.
        :type description: str, optional
        :param flash_mode: Whether to enable flash mode on this volume group. (defaults=False)
        :type flash_mode: bool, optional
        :param load_balancing: Whether to enable volume group load balancing on this volume group. (defaults=True)
        :type load_balancing: bool, optional
        :param disks: A list of dicts describing the disks to be added to this volume group.

            The dictionary format per-disk is as follows::
                - size_gb (str). The size of the disk in GB.
                - storage_container_name (str). The name of the storage container on which to place the disk. Mutually exclusive with "storage_container_uuid".
                - storage_container_uuid (str). The uuid of the storage container on which to place the disk. Mutually exclusive with "storage_container_name".
                - index (int, optional). The index of the drive within the volume group.

            Examples;
                1. A single disk - [{'size_gb': 50, 'storage_container_name': 'default',}, ]
                2. Multiple disks - [{'size_gb': 50, 'storage_container_name': 'default',}, {'size_gb': 25, 'storage_container_name': 'default',}, ]
                3. Multiple disks with specific indexes - [{'size_gb': 50, 'storage_container_name': 'default', 'index': 1}, {'size_gb': 25, 'storage_container_name': 'default', , 'index': 0}, ]
        :type disks: list, optional
        :param vms: A list of dicts describing the VMs to be attached to this volume group.

            The dictionary format per-vm is as follows::
                - vm_uuid (str). The uuid of the virtual machine.
                - index (str). The scsi index to attach the volume group with one the VM.

            Examples;
                1. Attach a single VM - [{'vm_uuid': '95764410-db35-48f8-8cf9-217a8fabb547', 'index': 10, }, ]
                2. Attach a multiple VMs - [{'vm_uuid': '95764410-db35-48f8-8cf9-217a8fabb547', 'index': 10, }, {'vm_uuid': 'e3c543e9-c68c-468b-abd1-61a6d039a84d', 'index': 10, }, ]
        :type vms: list, optional
        :param iscsi_initators: A list of the iscsi initiators to be present on this volume group.
        :type iscsi_initators: list, optional
        :param iscsi_target: The iscsi target for this volume group.
        :type iscsi_target: str, optional
        :param iscsi_chap_password: The iscsi CHAP password if wanted for this volume group.
        :type iscsi_chap_password: str, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the volume group was successfully created.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.create_volume_group')

        params = {}
        version = 'v2.0'
        uri = '/volume_groups'
        method = 'POST'
        payload = {
            'name': name,
            'enabled_authentications': [],
            'description': description,
            'flash_mode_enabled': flash_mode,
            'load_balance_vm_attachments': load_balancing,
            'disk_list': []
        }

        if iscsi_initators:
            payload['iscsi_initiator_list'] = iscsi_initators

        if iscsi_target:
            payload['iscsi_target'] = iscsi_target

        if iscsi_chap_password:
            auth = {
                'auth_type': 'CHAP',
                'password': iscsi_chap_password,
            }
            payload['enabled_authentications'].append(auth)
        else:
            auth = {
                'auth_type': 'NONE'
            }
            payload['enabled_authentications'].append(auth)

        disk_indexes = []
        for disk in disks:
            disk_index = 0
            if not disk.get('size_gb'):
                raise ValueError()

            if not disk.get('index'):
                if disk_indexes:
                    while disk_index in disk_indexes:
                        disk_index += 1
            else:
                if disk.get('index') in disk_indexes:
                    raise ValueError()
                disk_index = disk.get('index')
            disk_indexes.append(disk_index)

            disk_config = {
                'size_gb': disk.get('size_gb', 0),
                'index': disk_index,
                'storage_container_uuid': disk.get('storage_container_uuid', None),
                'storage_container_name': disk.get('storage_container_name', None),
            }
            payload['disk_list'].append(self._disk_config(clusteruuid=clusteruuid, **disk_config))

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        logger.info('payload "{0}"'.format(payload))
        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)
        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('volume group "{0}" created successfully'.format(name))

                    for vg in task_obj.task_result[task.get('task_uuid')].get('entity_list'):

                        for vm in vms:
                            attach_config = {
                                'vm_uuid': vm.get('uuid', None),
                                'index': vm.get('index', None),
                                'wait': wait,
                                'clusteruuid': clusteruuid,
                                'vg_uuid': vg.get('entity_id')
                            }
                            self.attach_volume_group(**attach_config)

                    return True
                else:
                    logger.warning('volume group failed to be created "{0}". Task details: {1}'.format(name, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def update_volume_group_name(self, name:str, description:str=None, flash_mode:bool=None, load_balancing:bool=None, iscsi_initiators:list=None,
                                 iscsi_target:str=None, wait:bool=True, clusteruuid=None):
        """Update the configuration of a volume group specified by name.

        :param name: The name for the volume group to be updated.
        :type name: str
        :param description: A description for this volume group.
        :type description: str, optional
        :param flash_mode: Whether to enable flash mode on this volume group. (defaults=False)
        :type flash_mode: bool, optional
        :param load_balancing: Whether to enable volume group load balancing on this volume group. (defaults=True)
        :type load_balancing: bool, optional
        :param iscsi_initiators: A list of the iscsi initiators to be present on this volume group.
        :type iscsi_initatiors: list, optional
        :param iscsi_target: The iscsi target for this volume group.
        :type iscsi_target: str, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the volume group was successfully updated.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.update_volume_group_name')
        vg = self.search_volume_groups_name(name=name, refresh=True, clusteruuid=clusteruuid)
        if vg:
            logger.debug('volume group "{0}" found'.format(name))
            return self.update_volume_group_uuid(uuid=vg.get('uuid'), name=name, description=description, flash_mode=flash_mode, load_balancing=load_balancing,
                                                 iscsi_initiators=iscsi_initiators, iscsi_target=iscsi_target, wait=wait, clusteruuid=clusteruuid)
        else:
            raise ValueError()

    def update_volume_group_uuid(self, uuid:str, name:str=None, description:str=None, flash_mode:bool=None, load_balancing:bool=None, iscsi_initiators:list=None,
                                 iscsi_target:str=None, wait:bool=True, clusteruuid=None):
        """Update the configuration of a volume group specified by uuid.

        :param uuid: The uuid for the volume group to be updated.
        :type uuid: str
        :param name: A new name for the volume group to be updated.
        :type name: str, optional
        :param description: A description for this volume group.
        :type description: str, optional
        :param flash_mode: Whether to enable flash mode on this volume group. (defaults=False)
        :type flash_mode: bool, optional
        :param load_balancing: Whether to enable volume group load balancing on this volume group. (defaults=True)
        :type load_balancing: bool, optional
        :param iscsi_initiators: A list of the iscsi initiators to be present on this volume group.
        :type iscsi_initiators: list, optional
        :param iscsi_target: The iscsi target for this volume group.
        :type iscsi_target: str, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the volume group was successfully updated.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.update_volume_group_uuid')
        params = {}
        uri = '/volume_groups/{0}'.format(uuid)
        method = 'PUT'
        payload = {
            'uuid': uuid
        }

        if name:
            payload['name'] = name

        if description:
            payload['description'] = description

        if type(flash_mode) == bool:
            payload['flash_mode_enabled'] = flash_mode

        if type(load_balancing) == bool:
            payload['load_balance_vm_attachments'] = load_balancing

        if iscsi_initiators:
            payload['iscsi_initiator_name_list'] = iscsi_initiators

        if iscsi_target:
            payload['iscsi_target'] = iscsi_target

        task = self.api_client.request(uri=uri, payload=payload, params=params, method=method)
        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('volume group "{0}" updated successfully'.format(uuid))
                    return True
                else:
                    logger.warning('volume group failed to be updated "{0}". Task details: {1}'.format(uuid, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def delete_volume_group_name(self, name:str, wait:bool=True, clusteruuid=None):
        """Delete a volume group specified by name.

        :param name: The name for the volume group to be deleted.
        :type name: str
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the volume group was successfully deleted.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.delete_volume_group_name')
        vg = self.search_volume_groups_name(name=name, refresh=True, clusteruuid=clusteruuid)
        if vg:
            logger.debug('volume group "{0}" found'.format(name))
            return self.delete_volume_group_uuid(uuid=vg.get('uuid'), wait=wait, clusteruuid=clusteruuid)
        else:
            raise ValueError()

    def delete_volume_group_uuid(self, uuid:str, wait:bool=True, clusteruuid=None):
        """Delete a volume group specified by uuid.

        :param uuid: The uuid for the volume group to be deleted.
        :type uuid: str
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the volume group was successfully deleted.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.delete_volume_group_uuid')
        params = {}
        payload = {}
        uri = '/volume_groups/{0}'.format(uuid)
        method = 'DELETE'
        response_code = 201

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        vg = self.search_volume_groups_uuid(uuid=uuid, refresh=True, clusteruuid=clusteruuid)
        if vg:
            logger.debug('volume group "{0}" found'.format(uuid))
        else:
            raise ValueError()

        task = self.api_client.request(uri=uri, payload=payload, params=params, method=method, response_code=response_code)
        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('volume group "{0}" deleted successfully'.format(uuid))
                    return True
                else:
                    logger.warning('volume group failed to be deleted "{0}". Task details: {1}'.format(uuid, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def attach_volume_group(self, vm_uuid:str, vg_uuid:str, index:int=None, wait:bool=True, clusteruuid:str=None):
        """Attach a VM to a volume group.

        :param vg_uuid: The uuid for the volume group.
        :type vg_uuid: str
        :param vm_uuid: The uuid for the vm to be attached to the volume group.
        :type vm_uuid: str
        :param index: The SCSI index to attached the volume group onto on the VM.
        :type index: int, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the volume group was successfully attached.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.attach_volume_group')
        spec = {
            'vm_uuid': vm_uuid,
            'uuid': vg_uuid,
        }
        if index:
            spec['index'] = index

        vms_obj = Vms(api_client=self.api_client)
        vms_obj.attach_vg(wait=wait, clusteruuid=clusteruuid, **spec)

    def detach_volume_group(self, vm_uuid:str, vg_uuid:str, index:int, wait:bool=True, clusteruuid:str=None):
        """Detach a VM to a volume group.

        :param vg_uuid: The uuid for the volume group.
        :type vg_uuid: str
        :param vm_uuid: The uuid for the vm to be detached to the volume group.
        :type vm_uuid: str
        :param index: The SCSI index for the volume group on this VM to be detached.
        :type index: int, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the volume group was successfully detached.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.detach_volume_group')
        spec = {
            'vm_uuid': vm_uuid,
            'uuid': vg_uuid,
            'index': index,
        }

        vms_obj = Vms(api_client=self.api_client)
        vms_obj.detach_vg(wait=wait, clusteruuid=clusteruuid, **spec)

    def clone_volume_group_name(self, source_name:str, dest_name:str, load_balancing:bool=True, iscsi_chap_password:str=None, iscsi_initiators:list=[],
                                iscsi_target:str=None, wait:bool=True, clusteruuid=None):
        """ Clone a volume group by name.

        :param source_name: The name for the volume group that is to be cloned.
        :type source_name: str
        :param dest_name: The name for the new volume group.
        :type dest_name: str
        :param load_balancing: Whether to enable volume group load balancing on this volume group. (defaults=True)
        :type load_balancing: bool, optional
        :param iscsi_chap_password: The iscsi CHAP password if wanted for this volume group.
        :type iscsi_chap_password: str, optional
        :param iscsi_initiators: A list of the iscsi initiators to be present on this volume group.
        :type iscsi_initiators: list, optional
        :param iscsi_target: The iscsi target for this volume group.
        :type iscsi_target: str, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the volume group was successfully cloned.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.clone_volume_group_name')
        vg = self.search_volume_groups_name(name=source_name, refresh=True, clusteruuid=clusteruuid)
        if vg:
            logger.debug('volume group "{0}" found'.format(source_name))
            return self.clone_volume_group_uuid(source_uuid=vg.get('uuid'), dest_name=dest_name, load_balancing=load_balancing, iscsi_target=iscsi_target,
                                                iscsi_initiators=iscsi_initiators, iscsi_chap_password=iscsi_chap_password, wait=wait, clusteruuid=clusteruuid)
        else:
            raise ValueError()

    def clone_volume_group_uuid(self, source_uuid:str, dest_name:str, load_balancing:bool=True, iscsi_chap_password:str=None, iscsi_initiators:list=[],
                                iscsi_target:str=None, wait:bool=True, clusteruuid=None):
        """ Clone a volume group by name.

        :param source_uuid: The uuid for the volume group that is to be cloned.
        :type source_uuid: str
        :param dest_name: The name for the new volume group.
        :type dest_name: str
        :param load_balancing: Whether to enable volume group load balancing on this volume group. (defaults=True)
        :type load_balancing: bool, optional
        :param iscsi_chap_password: The iscsi CHAP password if wanted for this volume group.
        :type iscsi_chap_password: str, optional
        :param iscsi_initiators: A list of the iscsi initiators to be present on this volume group.
        :type iscsi_initiators: list, optional
        :param iscsi_target: The iscsi target for this volume group.
        :type iscsi_target: str, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the volume group was successfully cloned.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.clone_volume_group_uuid')
        params = {}
        uri = '/volume_groups/{0}/clone'.format(source_uuid)
        method = 'POST'
        version = 'v2.0'
        payload = {
            'name': dest_name,
            'enabled_authentications': [],
            'load_balance_vm_attachments': load_balancing,
        }

        if iscsi_initiators:
            payload['iscsi_initiator_list'] = iscsi_initiators

        if iscsi_target:
            payload['iscsi_target'] = iscsi_target

        if iscsi_chap_password:
            auth = {
                'auth_type': 'CHAP',
                'password': iscsi_chap_password,
            }
            payload['enabled_authentications'].append(auth)
        else:
            auth = {
                'auth_type': 'NONE'
            }
            payload['enabled_authentications'].append(auth)

        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)
        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('volume group "{0}" cloned to {1} successfully'.format(source_uuid, dest_name))
                    return True
                else:
                    logger.warning('volume group "{0}" failed to clone. Task details: {1}'.format(source_uuid, task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def add_disk_by_volume_group_name(self, volume_group_name:str, size_gb:int, index:int=0, storage_container_uuid:str=None, storage_container_name:str=None,
                                      wait:bool=True, clusteruuid=None):
        """Add a new disk to an existing volume group using the volume group name.

        :param volume_group_name: The name of the volume group to which the new disk is to be added.
        :type volume_group_name: str
        :param size_gb: The size of the volume group disk to add in GB.
        :type size_gb: int
        :param index: The SCSI index for the volume group on this VM to be detached.
        :type index: int, optional
        :param storage_container_uuid: The uuid of the container that this volume group disk will be created on. Either this parameter or
                                       'storage_container_name' must be provided.
        :type storage_container_uuid: str, optional
        :param storage_container_name: The name of the container that this volume group disk will be created on. Either this parameter or
                                       'storage_container_uuid' must be provided.
        :type storage_container_name: str, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the disk was successfully added to the volume group.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.add_disk_by_volume_group_name')

        logger.debug('searching for volume group named "{0}"'.format(volume_group_name))
        vg = self.search_volume_groups_name(name=volume_group_name, refresh=True, clusteruuid=clusteruuid)
        if vg:
            logger.debug('found volume group named "{0}"'.format(volume_group_name))
            volume_group_uuid = vg.get('uuid')
        else:
            logger.warning('cannot find volume group named "{0}"'.format(volume_group_name))
            raise ValueError()

        volume_config = {
            'volume_group_uuid': volume_group_uuid,
            'size_gb': size_gb,
            'index': index,
            'storage_container_uuid': storage_container_uuid,
            'storage_container_name': storage_container_name,
        }
        return self.add_disk_by_volume_group_uuid(wait=wait, clusteruuid=clusteruuid, **volume_config)

    def add_disk_by_volume_group_uuid(self, volume_group_uuid:str, size_gb:int, index:int=0, storage_container_uuid:str=None, storage_container_name:str=None,
                                      wait:bool=True, clusteruuid=None):
        """Add a new disk to an existing volume group using the volume group uuid.

        :param volume_group_uuid: The uuid of the volume group to which the new disk is to be added.
        :type volume_group_uuid: str
        :param size_gb: The size of the volume group disk to add in GB.
        :type size_gb: int
        :param storage_container_uuid: The uuid of the container that this volume group disk will be created on. Either this parameter or
                                       'storage_container_name' must be provided.
        :type storage_container_uuid: str, optional
        :param storage_container_name: The name of the container that this volume group disk will be created on. Either this parameter or
                                       'storage_container_uuid' must be provided.
        :type storage_container_name: str, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the disk was successfully added to the volume group.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.add_disk_by_volume_group_uuid')

        logger.debug('searching for volume group "{0}"'.format(volume_group_uuid))
        vg = self.search_volume_groups_uuid(uuid=volume_group_uuid, refresh=True, clusteruuid=clusteruuid)
        if vg:
            logger.debug('found volume group "{0}"'.format(volume_group_uuid))
        else:
            logger.warning('cannot find volume group "{0}"'.format(volume_group_uuid))
            raise ValueError()

        if index:
            if any(item['index'] for item in vg.get('disk_list') if item['index'] == index):
                raise ValueError
        else:
            index = max(item['index'] for item in vg.get('disk_list'))+1

        params = {}
        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        version = 'v2.0'
        uri = '/volume_groups/{0}/disks'.format(volume_group_uuid)
        method = 'POST'
        payload = self._disk_config(size_gb=size_gb, index=index, storage_container_uuid=storage_container_uuid,
                                    storage_container_name=storage_container_name, clusteruuid=clusteruuid)
        payload['volume_group_uuid'] = volume_group_uuid

        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)
        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('disk added to volume group "{0}" successfully'.format(volume_group_uuid))
                    return True
                else:
                    logger.warning('disk failed to be added to volume group "{0}". Task details: {1}'.format(volume_group_uuid,
                                                                                                             task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False

    def remove_disk_by_volume_group_name(self, volume_group_name:str, index:int, wait:bool=True, clusteruuid=None):
        """Remove a disk from a volume group by volume group name.

        :param volume_group_name: The name of the volume group to which the new disk is to be added.
        :type volume_group_name: str
        :param index: The SCSI index for the volume group on this VM to be detached.
        :type index: int, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the disk was successfully removed to the volume group.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.remove_volume_by_volume_group_name')

        logger.debug('searching for volume group named "{0}"'.format(volume_group_name))
        vg = self.search_volume_groups_name(name=volume_group_name, refresh=True, clusteruuid=clusteruuid)
        if vg:
            logger.debug('found volume group named "{0}"'.format(volume_group_name))
            volume_group_uuid = vg.get('uuid')
        else:
            logger.warning('cannot find volume group named "{0}"'.format(volume_group_name))
            raise ValueError()

        volume_config = {
            'volume_group_uuid': volume_group_uuid,
            'index': index,
        }
        return self.remove_disk_by_volume_group_uuid(wait=wait, clusteruuid=clusteruuid, **volume_config)

    def remove_disk_by_volume_group_uuid(self, volume_group_uuid:str, index:int, wait:bool=True, clusteruuid=None):
        """Remove a disk from a volume group by volume group uuid.

        :param volume_group_uuid: The uuid of the volume group to which the new disk is to be added.
        :type volume_group_uuid: str
        :param index: The SCSI index for the volume group on this VM to be detached.
        :type index: int, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the disk was successfully removed to the volume group.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.remove_disk_by_volume_group_uuid')

        logger.debug('searching for volume group "{0}"'.format(volume_group_uuid))
        vg = self.search_volume_groups_uuid(uuid=volume_group_uuid, refresh=True, clusteruuid=clusteruuid)
        if vg:
            logger.debug('found volume group "{0}"'.format(volume_group_uuid))
        else:
            logger.warning('cannot find volume group "{0}"'.format(volume_group_uuid))
            raise ValueError()

        if vg.get('disk_list'):
            index_exists = next(item for item in vg.get('disk_list') if item['index'] == index)
            if index_exists:
                logger.debug('found volume group disk index "{0}". Details "{1}"'.format(index, index_exists))
            else:
                raise ValueError()
        else:
            raise ValueError()

        params = {}
        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        version = 'v2.0'
        uri = '/volume_groups/{0}/disks/{1}'.format(volume_group_uuid, index)
        method = 'DELETE'
        payload = None

        task = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)
        if wait:
            if task.get('task_uuid'):
                task_obj = Task(api_client=self.api_client)
                thread = threading.Thread(target=task_obj.watch_task(task_uuid=task.get('task_uuid'), max_refresh_secs=1, clusteruuid=clusteruuid))
                thread.start()

                task_obj.task_status.wait()
                if task_obj.task_result[task.get('task_uuid')].get('progress_status').lower() == 'succeeded':
                    logger.debug('disk deleted from volume group "{0}" successfully'.format(volume_group_uuid))
                    return True
                else:
                    logger.warning('disk failed to be deleted from volume group "{0}". Task details: {1}'.format(volume_group_uuid,
                                                                                                                 task_obj.task_result[task.get('task_uuid')]))
                    return False
            else:
                return False
        else:
            return True

    def update_disk_by_volume_group_name(self, volume_group_name:str, index:int, size_gb:int=None, preserve_data:bool=True, flash_mode:bool=False,
                                         clusteruuid=None):
        """Add a new disk to an existing volume group using the volume group name.

        :param volume_group_name: The name of the volume group to which the new disk is to be added.
        :type volume_group_name: str
        :param size_gb: The size of the volume group disk to add in GB.
        :type size_gb: int
        :param index: The SCSI index for the volume group on this VM to be detached.
        :type index: int, optional
        :param preserve_data: Whether data on this volume should be preserved during the update. (default=True)
        :type preserve_data: bool, optional
        :param flash_mode: Whether to enable flash mode on this volume group. (defaults=False)
        :type flash_mode: bool, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the disk was successfully updated on the volume group.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.update_disk_by_volume_group_name')

        logger.debug('searching for volume group named "{0}"'.format(volume_group_name))
        vg = self.search_volume_groups_name(name=volume_group_name, refresh=True, clusteruuid=clusteruuid)
        if vg:
            logger.debug('found volume group named "{0}"'.format(volume_group_name))
            volume_group_uuid = vg.get('uuid')
        else:
            logger.warning('cannot find volume group named "{0}"'.format(volume_group_name))
            raise ValueError()

        volume_config = {
            'volume_group_uuid': volume_group_uuid,
            'index': index,
            'size_gb': size_gb,
            'preserve_data': preserve_data,
            'flash_mode': flash_mode,
        }
        return self.update_disk_by_volume_group_uuid(clusteruuid=clusteruuid, **volume_config)

    def update_disk_by_volume_group_uuid(self, volume_group_uuid:str, index:int, size_gb:int=None, preserve_data:bool=True, flash_mode:bool=False,
                                         clusteruuid=None):
        """Add a new disk to an existing volume group using the volume group uuid.

        :param volume_group_uuid: The uuid of the volume group to which the new disk is to be added.
        :type volume_group_uuid: str
        :param size_gb: The size of the volume group disk to add in GB.
        :type size_gb: int
        :param index: The SCSI index for the volume group on this VM to be detached.
        :type index: int, optional
        :param preserve_data: Whether data on this volume should be preserved during the update. (default=True)
        :type preserve_data: bool, optional
        :param flash_mode: Whether to enable flash mode on this volume group. (defaults=False)
        :type flash_mode: bool, optional
        :param wait: Wait for the task to complete. (defaults=True)
        :type wait: bool, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :return: True or False to indicate whether the disk was successfully updated on the volume group.
        :rtype: bool
        """
        logger = logging.getLogger('ntnx_api.prism.StorageVolume.update_disk_by_volume_group_uuid')
        existing_volume = None
        bm_size = None

        logger.debug('searching for volume group "{0}"'.format(volume_group_uuid))
        vg = self.search_volume_groups_uuid(uuid=volume_group_uuid, refresh=True, clusteruuid=clusteruuid)
        if vg:
            logger.debug('found volume group "{0}"'.format(volume_group_uuid))
        else:
            logger.warning('cannot find volume group "{0}"'.format(volume_group_uuid))
            raise ValueError()

        if vg.get('disk_list'):
            existing_volume = next(item for item in vg.get('disk_list') if item['index'] == index)
            if existing_volume:
                logger.debug('found volume group disk index "{0}". Details "{1}"'.format(index, existing_volume))
            else:
                raise ValueError()
        else:
            raise ValueError()

        if size_gb:
            bm_size_gb = bitmath.GiB(size_gb)
            bm_size = bm_size_gb.to_Byte()
            if existing_volume.get('vmdisk_size_bytes') > bm_size:
                raise ValueError()

        params = {}
        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        version = 'v2.0'
        uri = '/volume_groups/{0}/disks'.format(volume_group_uuid)
        method = 'PUT'
        payload = {
            'flash_mode_enabled': flash_mode,
            'index': index,
            'volume_group_uuid': volume_group_uuid,
            'upgrade_spec': {
                'preserve_data': preserve_data,
                'size': int(bm_size) or existing_volume.get('vmdisk_size_bytes'),
            },
        }

        if flash_mode and not vg.get('flash_mode_enabled'):
            logger.warning('cannot enable "flash_mode" as it is not enabled on the parent volume group.')
            payload.pop('flash_mode_enabled')

        result = self.api_client.request(uri=uri, api_version=version, payload=payload, params=params, method=method)

        if result:
            return True
        else:
            return False


class Task(object):
    """A class to represent a Nutanix Clusters Task object.

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        """
        """
        logger = logging.getLogger('ntnx_api.prism.Task.__init__')
        self.api_client = api_client
        self.task_status = threading.Event()
        self.task_result = {}

    def get_task(self, task_uuid, clusteruuid=None):
        """Retrieves a specific task based on provided uuid

        :param task_uuid: The uuid of the task
        :type task_uuid: str
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A dictionaries describing the specified task.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Task.get_task')
        params = {}

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        uri = '/tasks/{0}'.format(task_uuid)
        method = 'GET'
        payload = {}

        return self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method)

    def watch_task(self, task_uuid, clusteruuid=None, max_refresh_secs=60):
        """Watches a specific task based until it finishes. Updates task status in ResponseList self.task_result within the class

        :param task_uuid: The uuid of the task
        :type task_uuid: str
        :param max_refresh_secs: The maximum number of seconds to wait before checking the status of the task. Actual wait time is randomized. (default=60)
        :type max_refresh_secs: int, optional
        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Task.watch_task_thread')
        task_status = None
        task_complete = False
        while not task_complete:
            time.sleep(random() * max_refresh_secs)
            task_status = self.get_task(task_uuid=task_uuid, clusteruuid=clusteruuid)
            if not task_status.get('progress_status').lower() in ['queued', 'running', 'none']:
                task_complete = True
                logger.info('task {0} finished'.format(task_uuid))
                logger.debug('task {0} details {1}'.format(task_uuid, task_status))
            else:
                logger.info('task {0} in {1} state'.format(task_uuid, task_status.get('progress_status').lower()))
        self.task_result[task_uuid] = task_status
        self.task_status.set()


class NetworkSwitch(object):
    """A class to represent a Nutanix Cluster AHV vSwitch object.

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """
    def __init__(self, api_client):
        """
        """
        logger = logging.getLogger('ntnx_api.prism.NetworkSwitch.__init__')
        self.api_client = api_client
        self.task_status = threading.Event()
        self.task_result = {}
        self.bridges = {}

    def get(self, clusteruuid=None):
        """Retrieve data for each vSwitch in a specific AHV cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each network from the specified cluster.
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.NetworkSwitch.get')

        # Remove existing data for this cluster if it exists
        if self.bridges.get(clusteruuid):
            self.bridges.pop(clusteruuid)
            logger.info('removing existing data from class dict self.networks for cluster {0}'.format(clusteruuid))

        params = {}
        payload = {
            "entity_type": "virtual_switch",
            "group_member_attributes": [{"attribute": "name"}],
            "group_member_count": 1000,
            "group_member_offset": 0,
            "query_name": "prism:EBQueryModel"
        }
        uri = '/groups'
        method = 'POST'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        bridges = []
        group_results = self.api_client.request(uri=uri, api_version='v1', payload=payload, params=params, method=method).get('group_results')
        for group_result in group_results:
            for entity in group_result.get('entity_results'):
                for data in entity.get('data'):
                    if data.get('name') == 'name':
                        for values in data.get('values'):
                            for value in values.get('values'):
                                bridges.append(value)
        self.bridges[clusteruuid] = list(set(bridges))
        return self.bridges[clusteruuid]

    def search_name(self, name, clusteruuid=None, refresh=False):
        """Retrieve data for a specific network vSwitch, in a specific cluster by name

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A storage pool name to search for.
        :type name: str, optional

        :returns: A dictionary describing the found storage pool.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.NetworkSwitch.search_name')
        # found = {}
        if not self.bridges.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        found = next((item for item in self.bridges.get(clusteruuid) if item == name), None)

        return found


class Network(object):
    """A class to represent a Nutanix Cluster AHV Network object.

    :param api_client: Initialized API client class
    :type api_client: :class:`ntnx.client.ApiClient`
    """

    def __init__(self, api_client):
        """
        """
        logger = logging.getLogger('ntnx_api.prism.Network.__init__')
        self.api_client = api_client
        self.task_status = threading.Event()
        self.task_result = {}
        self.networks = {}

    def get(self, clusteruuid=None):
        """Retrieve data for each network in a specific cluster

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional

        :returns: A list of dictionaries describing each network from the specified cluster.
        :rtype: ResponseList
        """
        logger = logging.getLogger('ntnx_api.prism.Network.get')

        # Remove existing data for this cluster if it exists
        if self.networks.get(clusteruuid):
            self.networks.pop(clusteruuid)
            logger.info('removing existing data from class dict self.networks for cluster {0}'.format(clusteruuid))

        params = {}
        payload = None
        uri = '/networks'

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        self.networks[clusteruuid] = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params).get('entities')
        logger.info('cluster {0} has networks {1}'.format(clusteruuid, self.networks[clusteruuid]))
        return self.networks[clusteruuid]

    def search_uuid(self, uuid, clusteruuid=None, refresh=False):
        """Retrieve data for a specific network, in a specific cluster by uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: A network uuid to search for.
        :type uuid: str, optional
        :returns: A dictionary describing the found network.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Network.search_uuid')
        if not self.networks.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        return next((item for item in self.networks.get(clusteruuid) if item.get("uuid") == uuid), None)

    def search_name(self, name, clusteruuid=None, refresh=False):
        """Retrieve data for a specific network, in a specific cluster by uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: A network name to search for.
        :type name: str, optional

        :returns: A dictionary describing the found network.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Network.search_name')
        if not self.networks.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        return next((item for item in self.networks.get(clusteruuid) if item.get("name") == name), None)

    def search_vlan(self, vlan, clusteruuid=None, refresh=False):
        """Retrieve data for a specific vlan, in a specific cluster by uuid

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param vlan: A vlan to search for.
        :type vlan: str, optional

        :returns: A dictionary describing the found network.
        :rtype: ResponseDict
        """
        logger = logging.getLogger('ntnx_api.prism.Network.search_vlan')
        if not self.networks.get(clusteruuid) or refresh:
            self.get(clusteruuid)

        return next((item for item in self.networks.get(clusteruuid) if item.get("vlan_id") == vlan), None)

    def create(self, name, vlan=0, vswitch='br0', network_address=None, network_cidr=None, default_gw=None, dhcp_boot_filename=None, dhcp_domain_name=None,
               dhcp_domain_nameservers=None, dhcp_domain_search=None, dhcp_tftp_server_name=None, dhcp_server_override=None, dhcp_pools=None, clusteruuid=None):
        """Create a new network on a specified vSwitch

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: The name of the network to create.
        :type name: str
        :param vlan: The vlan id of the network to be created. To select the native VLAN set this value to 0. (default=0)
        :type vlan: int, optional
        :param vswitch: The name of the vswitch on which to create the network. (default='br0')
        :type vswitch: str, optional
        :param network_address: The network address for the network being created. This is required to enable IP Address Management (IPAM) within AHV.
        :type network_address: str, optional
        :param network_cidr: The CIDR for the network being created. This is required to enable IP Address Management (IPAM) within AHV.
        :type network_cidr: int, optional
        :param default_gw: The default gateway for the network being created. This is required to enable IP Address Management (IPAM) within AHV.
        :type default_gw: str, optional
        :param dhcp_boot_filename: The default gateway for the network being created.
        :type dhcp_boot_filename: str, optional
        :param dhcp_domain_name:
        :type dhcp_domain_name: str, optional
        :param dhcp_domain_nameservers:
        :type dhcp_domain_nameservers: str, optional
        :param dhcp_domain_search:
        :type dhcp_domain_search: str, optional
        :param dhcp_tftp_server_name:
        :type dhcp_tftp_server_name: str, optional
        :param dhcp_server_override:
        :type dhcp_server_override: str, optional
        :param dhcp_pools: A list of dicts describing the ip pool ranges to create. Each dict should be in the format {"start": "w.x.y.z", "end": ""w.x.y.z"}.
        :type dhcp_pools: list, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Network.create')

        params = {}
        payload = {}
        ip_config = {}
        dhcp_options = {}
        uri = '/networks'
        method = 'POST'
        response_code = 201

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        network_vswitch_obj = NetworkSwitch(api_client=self.api_client)
        vswitch_search = network_vswitch_obj.search_name(name=vswitch, clusteruuid=clusteruuid, refresh=True)
        network_search = self.search_name(name=name, clusteruuid=clusteruuid, refresh=True)

        ipam = False
        if not all(v is None for v in [network_address, network_cidr, default_gw]):
            if not all(v is not None for v in [network_address, network_cidr, default_gw]):
                raise ValueError('To enable IPAM "network_address", "network_cidr" and "default_gw" are all required. Please check inputs and try again.')
            else:
                ipam = True
                existing_vlan = self.search_vlan(vlan=vlan, clusteruuid=clusteruuid, refresh=True)
                if existing_vlan:
                    if existing_vlan.get('ip_config').get('network_address'):
                        raise ValueError('Another network configured with VLAN "{0}" already has IPAM enabled. Please check inputs and try again'.format(vlan))

        if not vswitch_search:
            raise ValueError('The provided vSwitch name "{0}" is not present on this cluster. Please check inputs and try again'.format(vswitch))

        if not network_search:
            payload['name'] = name
            payload['vlan_id'] = vlan
            payload['vswitch_name'] = vswitch

            if ipam:
                ip_config['network_address'] = network_address
                ip_config['prefix_length'] = network_cidr
                ip_config['default_gateway'] = default_gw

                if dhcp_server_override:
                    ip_config['dhcp_server_address'] = dhcp_server_override

                if dhcp_boot_filename:
                    dhcp_options['boot_file_name'] = dhcp_boot_filename
                else:
                    dhcp_options['boot_file_name'] = ''

                if dhcp_domain_name:
                    dhcp_options['domain_name'] = dhcp_domain_name
                else:
                    dhcp_options['domain_name'] = ''

                if dhcp_domain_nameservers:
                    dhcp_options['domain_name_servers'] = dhcp_domain_nameservers
                else:
                    dhcp_options['domain_name_servers'] = ''

                if dhcp_domain_search:
                    dhcp_options['domain_search'] = dhcp_domain_search
                else:
                    dhcp_options['domain_search'] = ''

                if dhcp_tftp_server_name:
                    dhcp_options['tftp_server_name'] = dhcp_tftp_server_name
                else:
                    dhcp_options['tftp_server_name'] = ''

                ip_config['dhcp_options'] = dhcp_options

                pools = []
                for dhcp_pool in dhcp_pools:
                    if dhcp_pool.get('start') and dhcp_pool.get('end'):
                        ip_range = {
                            'range': "{0} {1}".format(dhcp_pool.get('start'),dhcp_pool.get('end'))
                        }
                        pools.append(ip_range)
                ip_config['pool'] = pools

                payload['ip_config'] = ip_config

            logger.info('payload of network to be created: {0}'.format(payload))
            return self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method, response_code=response_code).get('network_uuid')

        else:
            raise ValueError('A network "{0}" with the same name already exists on this cluster. Please check inputs and try again.'.format(name))

    def update(self, name, vlan=None, network_address=None, network_cidr=None, default_gw=None, dhcp_boot_filename=None, dhcp_domain_name=None,
               dhcp_domain_nameservers=None, dhcp_domain_search=None, dhcp_tftp_server_name=None, dhcp_server_override=None, dhcp_pools=None, clusteruuid=None):
        """Update the configuration of an existing network.

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: The name of the network to update.
        :type name: str
        :param vlan: The vlan id of the network to be created. To select the native VLAN set this value to 0. (default=0)
        :type vlan: int, optional
        :param network_address: The network address for the network being created. This is required to enable IP Address Management (IPAM) within AHV.
        :type network_address: str, optional
        :param network_cidr: The CIDR for the network being created. This is required to enable IP Address Management (IPAM) within AHV.
        :type network_cidr: int, optional
        :param default_gw: The default gateway for the network being created. This is required to enable IP Address Management (IPAM) within AHV.
        :type default_gw: str, optional
        :param dhcp_boot_filename: The default gateway for the network being created.
        :type dhcp_boot_filename: str, optional
        :param dhcp_domain_name:
        :type dhcp_domain_name: str, optional
        :param dhcp_domain_nameservers:
        :type dhcp_domain_nameservers: str, optional
        :param dhcp_domain_search:
        :type dhcp_domain_search: str, optional
        :param dhcp_tftp_server_name:
        :type dhcp_tftp_server_name: str, optional
        :param dhcp_server_override:
        :type dhcp_server_override: str, optional
        :param dhcp_pools: A list of dicts describing the ip pool ranges to create. Each dict should be in the format {"start": "w.x.y.z", "end": ""w.x.y.z"}.
        :type dhcp_pools: list, optional
        """
        logger = logging.getLogger('ntnx_api.prism.Network.update')
        params = {}
        method = 'PUT'
        response_code = 200

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        payload = self.search_name(name=name, clusteruuid=clusteruuid, refresh=True)
        uri = '/networks/{0}'.format(payload.get('uuid'))
        logger.info('found network to update: {0}'.format(payload))

        configured_ipam = False
        if payload.get('ip_config'):
            if payload.get('ip_config').get('network_address') and payload.get('ip_config').get('default_gateway') \
                    and payload.get('ip_config').get('prefix_length') > 0:
                configured_ipam = True
            else:
                payload.pop('ip_config')

        config_ipam = False
        if not all(v is None for v in [network_address, network_cidr, default_gw]):
            if not all(v is not None for v in [network_address, network_cidr, default_gw]):
                raise ValueError('To enable IPAM "network_address", "network_cidr" and "default_gw" are all required. Please check inputs and try again.')
            else:
                config_ipam = True
                existing_vlan = self.search_vlan(vlan=vlan, clusteruuid=clusteruuid, refresh=True)
                if existing_vlan:
                    if existing_vlan.get('ip_config').get('network_address'):
                        raise ValueError('Another network configured with VLAN "{0}" already has IPAM enabled. Please check inputs and try again'.format(vlan))

        if payload:
            remove_keys = [
                'logical_timestamp',
            ]
            for key in remove_keys:
                payload.pop(key)

            if vlan:
                if payload.get('vlan') != vlan:
                    payload['vlan_id'] = vlan
                else:
                    payload.pop('vlan_id')

            if config_ipam or configured_ipam:
                if not payload.get('ip_config'):
                    payload['ip_config'] = {}

                if dhcp_server_override:
                    if payload.get('ip_config').get('dhcp_server_address') != dhcp_server_override:
                        payload['ip_config']['dhcp_server_address'] = dhcp_server_override

                if network_address:
                    if payload.get('ip_config').get('network_address') != network_address:
                        payload['ip_config']['network_address'] = network_address

                if network_cidr:
                    if payload.get('ip_config').get('prefix_length') != network_cidr:
                        payload['ip_config']['prefix_length'] = network_cidr

                if default_gw:
                    if payload.get('ip_config').get('default_gateway') != default_gw:
                        payload['ip_config']['default_gateway'] = default_gw

                if dhcp_boot_filename:
                    if payload.get('ip_config').get('boot_file_name') != dhcp_boot_filename :
                        payload['ip_config']['boot_file_name'] = dhcp_boot_filename

                if dhcp_domain_name:
                    if payload.get('ip_config').get('domain_name') != dhcp_domain_name:
                        payload['ip_config']['domain_name'] = dhcp_domain_name

                if dhcp_domain_search:
                    if payload.get('ip_config').get('domain_search') != dhcp_domain_search:
                        payload['ip_config']['domain_name_servers'] = dhcp_domain_nameservers

                if dhcp_tftp_server_name:
                    if payload.get('ip_config').get('tftp_server_name') != dhcp_tftp_server_name:
                        payload['ip_config']['tftp_server_name'] = dhcp_tftp_server_name

                if dhcp_domain_search:
                    if payload.get('ip_config').get('domain_search') != dhcp_domain_search:
                        payload['ip_config']['domain_search'] = dhcp_domain_search

                if dhcp_pools:
                    if payload.get('ip_config').get('pool') and dhcp_pools:
                        pools = []
                        for dhcp_pool in dhcp_pools:
                            if dhcp_pool.get('start') and dhcp_pool.get('end'):
                                ip_range = {
                                    'range': "{0} {1}".format(dhcp_pool.get('start'), dhcp_pool.get('end'))
                                }
                                pools.append(ip_range)
                        payload['ip_config']['pool'] = pools

            logger.info('payload of network to be updated: {0}'.format(payload))
            return self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method, response_code=response_code).get('value')

        else:
            raise ValueError('The network "{0}" does not exist on this cluster. Please check inputs and try again.'.format(name))

    def delete_name(self, name, clusteruuid=None):
        """Delete an existing network by name.

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param name: The name of the network to delete.
        :type name: str
        """
        logger = logging.getLogger('ntnx_api.prism.Network.delete')
        network = self.search_name(name=name, clusteruuid=clusteruuid, refresh=True)
        if network:
            return self.delete_uuid(network.get('uuid'), clusteruuid=clusteruuid)
        else:
            return False

    def delete_uuid(self, uuid, clusteruuid=None):
        """Delete an existing network by uuid.

        :param clusteruuid: A cluster UUID to define the specific cluster to query. Only required to be used when the :class:`ntnx.client.ApiClient`
                            `connection_type` is set to `pc`.
        :type clusteruuid: str, optional
        :param uuid: The uuid of the network to delete.
        :type uuid: str
        """
        logger = logging.getLogger('ntnx_api.prism.Network.delete')
        params = {}
        payload = {}
        uri = '/networks/{0}'.format(uuid)
        method = 'DELETE'
        response_code = 204

        if clusteruuid:
            params['proxyClusterUuid'] = clusteruuid

        try:
            result = self.api_client.request(uri=uri, api_version='v2.0', payload=payload, params=params, method=method, response_code=response_code)
            logger.info('result "{0}"'.format(result))
            return True

        except:
            return False
