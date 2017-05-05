from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from saml2.config import SPConfig
from saml2.client import Saml2Client
from saml2.metadata import create_metadata_string

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
                    'assertion_consumer_service': [
                        ("%s/acs/" % url, BINDING_HTTP_REDIRECT),
                        ("%s/acs/" % url, BINDING_HTTP_POST)
                    ],
                },
                'allow_unsolicited': True,
                'authn_requests_signed': False,
                'logout_requests_signed': True,
                'want_assertions_signed': False,
                'want_response_signed': False,
            },
        },
        "key_file": "pki/sp.key",
        "cert_file": "pki/sp.crt",
        "xmlsec_binary": "/usr/bin/xmlsec1",
        "metadata": {"local": ["pki/idp.xml"]},
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


def single_sign_on_service(request):
    saml_client = Saml2Client(config=sp_config())

    reqid, info = saml_client.prepare_for_authenticate()
    url = dict(info['headers'])['Location']

    return HttpResponseRedirect(url)
