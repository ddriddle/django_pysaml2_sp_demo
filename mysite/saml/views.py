from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from saml2.config import SPConfig
from saml2.client import Saml2Client
from saml2.metadata import create_metadata_string
from saml2.extension.idpdisc import BINDING_DISCO

from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
)


def sp_config():
    url = "https://drone.sandbox.aws.illinois.edu"

    # FIXME -- DO NOT HARDCODE URLS OR PATHS!
    saml_settings = {
        'debug': 1,
        'entityid': '%s/metadata/' % url,
        'service_url': url,
        'metadata': {
            'local': [],
        },
        'service': {
            'sp': {
                'endpoints': {
# TODO: What bindings to we want/need?
# Restrict the views to only accept the bindings specified here!
                    'assertion_consumer_service': [
                        ("%s/acs/" % url, BINDING_HTTP_REDIRECT),
                        ("%s/acs/" % url, BINDING_HTTP_POST)
                    ],
                    'discovery_response': [
                        ("%s/disco/" % url, BINDING_DISCO),
                    ],
                },
#                'idp': ['urn:mace:incommon:uiuc.edu'],
                'allow_unsolicited': True,
                'authn_requests_signed': True,
                'logout_requests_signed': True,
                'want_assertions_signed': False,
                'want_response_signed': False,
            },
        },
        "key_file": "pki/sp.key",
        "cert_file": "pki/sp.crt",
        "xmlsec_binary": "/usr/bin/xmlsec1",
        "metadata": {"local": ["pki/itrust-metadata.xml"]},
        "encryption_keypairs": [
            {
                "key_file": "pki/sp.key",
                "cert_file": "pki/sp.crt",
            },
        ],
    }

    return SPConfig().load(saml_settings)


def metadata(request):
    xmldoc = create_metadata_string(None, config=sp_config())

    return HttpResponse(xmldoc.decode("utf-8"), content_type='text/xml')


@csrf_exempt
def assertion_consumer_service(request):
    saml_client = Saml2Client(config=sp_config())

    authn_response = saml_client.parse_authn_request_response(
            request.POST['SAMLResponse'],
            entity.BINDING_HTTP_POST)

    attrs = ""
    print(authn_response.get_identity())
    for key, value in authn_response.get_identity().iteritems():
        attrs += key + ": " + ', '.join(value) + "\r\n"
    return HttpResponse(attrs, content_type='text/plain')


def discovery_response(request):
    config=sp_config()
    saml_client = Saml2Client(config=config)

    idp = request.GET['entityID']

    reqid, info = saml_client.prepare_for_authenticate(entityid=idp)
    url = dict(info['headers'])['Location']

    return HttpResponseRedirect(url)


def single_sign_on_service(request):
    print("SSO!")
    config=sp_config()
    saml_client = Saml2Client(config=config)

    idp = getattr(config, '_sp_idp', [])

    if len(idp) == 1:
        reqid, info = saml_client.prepare_for_authenticate(
                entityid=config._sp_idp[0])
        url = dict(info['headers'])['Location']
    else:
        return_url = config.getattr('endpoints', 'sp')['discovery_response'][0][0]

        url = saml_client.create_discovery_service_request(
                "https://discovery.itrust.illinois.edu/discovery/DS",
                config.entityid,
                **{'return': return_url}
        )

    return HttpResponseRedirect(url)
