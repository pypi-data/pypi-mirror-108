# -*- coding: utf-8 -*-
from contextlib import contextmanager
import os
from typing import Dict, List, Tuple
from urllib.parse import urljoin

from chaoslib.discovery.discover import (discover_probes,
                                         initialize_discovery_result)
from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, DiscoveredActivities, Discovery, \
    Secrets
from logzero import logger
import requests
import yaml

__version__ = '0.1.1'
__all__ = ["get_session", "discover", "get_default_org"]
RELIABLY_CONFIG_PATH = "~/.config/reliably/config.yaml"
RELIABLY_HOST = "reliably.com"


def get_user(session: requests.Session) -> Dict[str, str]:
    r = session.get(session.reliably_url("/api/v1/userinfo"))
    if r.status_code != 200:
        raise ActivityFailed(
            "Failed to retrieve current user: {}".format(r.text))
    return r.json()


def get_default_org(session: requests.Session) -> Dict[str, str]:
    r = session.get(session.reliably_url("/api/v1/orgs/default"))
    if r.status_code != 200:
        raise ActivityFailed(
            "Failed to retrieve default organisation: {}".format(r.text))
    return r.json()


@contextmanager
def get_session(configuration: Configuration = None,
                secrets: Secrets = None) -> requests.Session:
    host, token = get_auth_info(configuration, secrets)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    with requests.Session() as s:
        s.headers = headers
        s.reliably_url = lambda p: urljoin("https://{}".format(host), p)
        yield s


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Reliably capabilities from this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-reliably")

    discovery = initialize_discovery_result(
        "chaostoolkit-reliably", __version__, "reliably")
    discovery["activities"].extend(load_exported_activities())

    return discovery


###############################################################################
# Private functions
###############################################################################
def get_auth_info(configuration: Configuration = None,
                  secrets: Secrets = None) -> Tuple[str, str]:
    reliably_config_path = None
    reliably_host = None
    reliably_token = None

    configuration = configuration or {}
    reliably_config_path = os.path.expanduser(configuration.get(
        "reliably_config_path", RELIABLY_CONFIG_PATH))
    if reliably_config_path and not os.path.isfile(reliably_config_path):
        reliably_config_path = None

    secrets = secrets or {}
    reliably_secrets = secrets.get("reliably", {})
    reliably_token = reliably_secrets.get("token")
    reliably_host = reliably_secrets.get("host")

    if not reliably_token and reliably_config_path:
        logger.debug("Loading Reliably config from: {}".format(
            reliably_config_path))
        with open(reliably_config_path) as f:
            try:
                config = yaml.safe_load(f)
            except yaml.YAMLError as ye:
                raise ActivityFailed(
                    "Failed parsing Reliably configuration at "
                    "'{}': {}".format(reliably_config_path, str(ye)))
        reliably_host = reliably_host or RELIABLY_HOST
        logger.debug("Connecting to Reliably: {}".format(reliably_host))
        auth_hosts = config.get("auths", {})
        for auth_host, values in auth_hosts.items():
            if auth_host == reliably_host:
                reliably_token = values.get("token")
                break

    if not reliably_config_path and not reliably_token and not reliably_host:
        raise ActivityFailed(
            "Make sure to login against Reliably's services and/or provide "
            "them correct authentication information to the experiment.")

    if not reliably_token:
        raise ActivityFailed(
            "Make sure to provide the Reliably token as a secret or via "
            "the Reliably's configuration's file.")

    if not reliably_host:
        raise ActivityFailed(
            "Make sure to provide the Reliably host as a secret or via "
            "the Reliably's configuration's file.")

    return (reliably_host, reliably_token)


def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions, probes and tolerances
    exposed by this extension.
    """
    activities = []
    activities.extend(discover_probes("chaosreliably.slo.probes"))
    activities.extend(discover_probes("chaosreliably.slo.tolerances"))

    return activities
