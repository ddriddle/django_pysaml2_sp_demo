from django.http import HttpResponse

from saml2.config import SPConfig
from saml2.metadata import create_metadata_string

from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
)


def saml_client():
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
                        ("%s/acs" % url, BINDING_HTTP_REDIRECT),
                        ("%s/acs" % url, BINDING_HTTP_POST)
                    ],
                },
                'allow_unsolicited': True,
                'authn_requests_signed': False,
                'logout_requests_signed': True,
                'want_assertions_signed': True,
                'want_response_signed': False,
            },
        },
        "key_file": "pki/sp.key",
        "cert_file": "pki/sp.crt",
        "xmlsec_binary": "/usr/bin/xmlsec1",
    }

    return SPConfig().load(saml_settings)


def metadata(request):
    config = saml_client()
    xmldoc = create_metadata_string(None, config=config)

    return HttpResponse(xmldoc.decode("utf-8"), content_type='text/xml')


def assertion_consumer_service(request):
    return HttpResponse("In the future this will be an assertion endpoint!")


def single_sign_on_service(request):
    return HttpResponse("In the future this will be a"
                        " single sign on service endpoint!")
