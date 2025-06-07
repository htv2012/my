#!/usr/bin/env python3
import base64
import contextlib
import copy
import csv
import dataclasses
import functools
import hashlib
import http
import ipaddress
import itertools
import json
import logging
import os
import pathlib
import pprint
import random
import re
import shlex
import string
import sys
import tempfile
import time
import types
import urllib.parse
import uuid
from contextlib import ExitStack, contextmanager
from functools import partial
from typing import TypedDict, Union
from urllib.parse import urlparse

# ======================================================================
# Fixed up the PYTHONPATH (sys.path)
# ======================================================================
here = pathlib.Path("~/code/data-plane/declarative-ext-api/qe/functional").expanduser()
here = str(here)
sys.path.append(here)
sys.path.append(f"{here}/springer")
sys.path.append(str(pathlib.Path("~/myenv/lib").expanduser()))

# ======================================================================
# Imports which should happens after PYTHONPATH fixup
# ======================================================================
from jq import jq

from e2e.helper import generate_certs
from e2e.helper import get_certs_data
from local_libs import common
from local_libs import rbac_helper
from local_libs.common import create_test_data
from local_libs.common import generate_host_port
from local_libs.common import generate_names
from local_libs.common import is_validate_address
from local_libs.common import make_ref_list
from local_libs.common import post_and_save_response_data
from local_libs.common import reason
from local_libs.common import update_if_not_none
from local_libs.common import validate_response_data
from local_libs.jsontools import ExpectedJson
from local_libs.skip_test import skip_if_not_enough_instance_groups
from local_libs.skip_test import skip_unsupported_ipv6_platform
from local_libs.test_data.crud_e2e_test_data import CERT_REF
from local_libs.test_data.crud_e2e_test_data import IG_REF
from local_libs.test_data.crud_e2e_test_data import NAME_TEST_DATA
from local_libs.test_data.crud_e2e_test_data import TAG_NAME_TEST_DATA
from local_libs.test_data.crud_e2e_test_data import TAGS_TEST_DATA
from local_libs.test_data.crud_e2e_test_data import TEMPLATES_DIR
from local_libs.test_data.crud_e2e_test_data import TEST_TCPUDP_PORTS
from local_libs.test_data.crud_e2e_test_data import TEST_WEB_PORTS
from local_libs.test_data.crud_e2e_test_data import USECASES_DIR
from local_libs.test_data.crud_e2e_test_data import WLG_NAME_ERROR_MESSAGE
from local_libs.test_data.crud_e2e_test_data import WORKLOAD_GROUP_NAME_TEST_DATA
from local_libs.utils import curl
from local_libs.utils import instance_helper
from local_libs.utils import nginx_config
from local_libs.utils import oidclib
from local_libs.utils import socat_lib
from local_libs.utils import socat_stream_server
from local_libs.utils.clusterlib import create_cluster
from local_libs.utils.component_helper import verify_bad_request
from local_libs.utils.component_helper import verify_elapsed
from local_libs.utils.generate_traffic import send_curl_request
from local_libs.utils.generate_traffic import send_traffic
from local_libs.utils.instance_helper import create_containerized_instance
from local_libs.utils.instance_helper import create_instance_group
from local_libs.utils.instance_helper import get_instance_group_instances
from local_libs.utils.instance_helper import get_random_instance
from local_libs.utils.instance_helper import set_nonlocal_binding
from local_libs.utils.nginx_config import get_stream_listen_directive_from_ingress_port
from local_libs.utils.nginx_config import HTTP_NGINX_CONFIG_FILE
from local_libs.utils.nginx_config import verify_stream_instance_configs
from local_libs.utils.numberlib import get_random_int
from local_libs.utils.numberlib import NumericRange
from local_libs.utils.portlib import next_port
from local_libs.utils.randomlib import generate_name
from local_libs.utils.remotelib import get_controller_host, get_datapath_hosts, install_package
from local_libs.utils.socat_lib import install_socat_host
from local_libs.v1 import application
from local_libs.v1 import base
from local_libs.v1 import component
from local_libs.v1 import environment
from local_libs.v1 import environment, application, gateway, web_component, component
from local_libs.v1 import gateway
from local_libs.v1 import licenselib
from local_libs.v1 import role
from local_libs.v1 import site
from local_libs.v1 import tcpudp_component
from local_libs.v1 import use_case
from local_libs.v1 import user
from local_libs.v1 import web_component
from local_libs.v1.application import application_payload
from local_libs.v1.application import create_application
from local_libs.v1.base import ADMBaseAPI
from local_libs.v1.base import ADMBaseConfig
from local_libs.v1.base import BaseAPI
from local_libs.v1.base import PlatformBaseAPI
from local_libs.v1.base import PlatformBaseConfig
from local_libs.v1.component import generate_payload_uri
from local_libs.v1.component import generate_uris_from_list_of_dicts
from local_libs.v1.environment import create_environment
from local_libs.v1.environment import environment_payload
from local_libs.v1.gateway import create_gateway
from local_libs.v1.gateway import gateway_meta_payload
from local_libs.v1.gateway import gateway_payload
from local_libs.v1.gateway import GatewaysConfigAPI
from local_libs.v1.gateway import generate_host
from local_libs.v1.metrics import APP_CENTRIC_METRICS
from local_libs.v1.metrics import get_avr_metrics
from local_libs.v1.metrics import make_query
from local_libs.v1.metrics import MetricsAPI
from local_libs.v1.metrics import verify_app_centric_metrics_presence
from local_libs.v1.metrics import verify_upstream_metrics
from local_libs.v1.site import create_site
from local_libs.v1.site import site_payload
from local_libs.v1.site import SitesConfigAPI
from local_libs.v1.tcpudp_component import create_tcpudp_component
from local_libs.v1.tcpudp_component import tcpudp_component_meta_payload
from local_libs.v1.tcpudp_component import TCPUDP_PROTOCOLS_TEST_SET
from local_libs.v1.tcpudp_component import TCPUDPComponentsAPI
from local_libs.v1.tcpudp_component import TCPUDPComponentsConfigAPI
from local_libs.v1.web_component import create_web_component
from local_libs.v1.web_component import web_component_meta_payload
from local_libs.v1.web_component import WebComponentsConfigAPI
from springer.api.rest.base import BaseAPI
from springer.api.rest.config_base import BaseConfig
from springer.nms.api import LicenseConfig
from springer.nms.api import systems
from springer.nms.api.certs.payload.v1 import CertPayload
from springer.nms.api.certs.rest.config import CertConfig
from springer.nms.api.certs.rest.http import CertsAPI
from springer.nms.api.instance_groups import InstanceGroupsConfig
from springer.nms.api.instance_groups.rest.http import InstanceGroupsAPI
from springer.nms.api.instances import InstanceConfig
from springer.nms.api.instances.rest.meta import InstanceMetadata
from springer.parsers.config import Directive
from utils import crypto
from utils import dnsserver
from utils import host
from utils import poll
from utils import random
from utils import request
from utils import request as utils_request
from utils import symbols
from utils import url as url_utils
from utils.crypto.descriptors.oscrypto import OSCryptoAlgorithm
from utils.host import Host
from utils.random import alphanumeric
from utils.request import RequestHandler
from utils.request import Response
from utils.symbols import Symbols
from utils.user_request import UserRequestHandler
from workloads.testserver.http import HttpTestServerCluster
from workloads.testserver.https import HttpsTestServerCluster


sys.ps1 = ">>>> "

# ======================================================================
# Generics
# ======================================================================
def display_hook(value):
    """Display a nicer repr."""
    if value is None:
        return
    pprint.pprint(value, indent=4)
    __builtins__._ = value


def source(path):
    """Source a file into the global namespace."""
    path = pathlib.Path(path).expanduser().resolve()
    with open(path, "r", encoding="utf-8") as stream:
        raw_code = stream.read()
    exec(raw_code, globals())


# ======================================================================
# Main
# ======================================================================
for path in sys.argv[1:]:
    source(path)
