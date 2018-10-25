#!/usr/bin/env python3

# import argparse
import logging
from os import makedirs
from os.path import dirname, exists, join

import httplib2
from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

l = logging.getLogger(__name__)
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"
credentials_folder = '.credentials'  # Default folder within working directory for authentication key files.
credentials_file = '{}.googleapis.com.json'
Scope = None
discoveryUrl = None
ver = None


def Auth2_0(clientSecretFile, applicationName, app):
    '''
    Performs API OAuth2.0 and Service account authentication for Google APIs.

    :param clientSecretFile: Full path to Google's JSON authentication key.
    :type clientSecretFile: str

    :param applicationName: Identifying Application name
    :type applicationName: str

    :param app:
    :type app: str

    :return: Authenticated session.
    :type: obj
    '''
    try:
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None
        l.info("flags = None")

    l.info('Authenticating Google for {}.'.format(applicationName))
    home_dir = dirname(clientSecretFile)
    credential_dir = join(home_dir, credentials_folder)
    if not exists(credential_dir):  makedirs(credential_dir)
    credential_path = join(credential_dir, credentials_file)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(clientSecretFile, Scope)
        flow.user_agent = applicationName
        if flags:
            credentials = tools.run_flow(flow, store, flags)
            # print('Storing credentials to ' + credential_path)
    http = credentials.authorize(httplib2.Http())
    if discoveryUrl:
        return discovery.build(app, ver, http=http, discoveryServiceUrl=discoveryUrl)
    else:
        return discovery.build(app, ver, http=http)


def service_account(devKey, serviceName):
    return discovery.build(serviceName, ver, developerKey=devKey)
