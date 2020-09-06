# -*- coding: utf-8 -*-
from collective.elasticsearch.es import ElasticSearchCatalog
from collective.fhirpath.interfaces import IZCatalogFhirSearch
from collective.fhirpath.utils import FHIRModelServiceMixin
from fhirpath.enums import FHIR_VERSION
from fhirpath.interfaces import IElasticsearchEngineFactory
from fhirpath.interfaces import ISearchContextFactory
from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from plone.restapi.services.locking.locking import is_locked
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import plone.protect.interfaces


@implementer(IPublishTraverse)
class FHIRResourcePatch(FHIRModelServiceMixin, Service):
    """Patch a FHIR Resource object."""

    def __init__(self, context, request):
        """ """
        super(FHIRResourcePatch, self).__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):  # noqa: N802
        # Consume any path segments after /@fhir as parameters
        self.params.append(name)
        return self

    def get_es_catalog(self):
        """ """
        return ElasticSearchCatalog(api.portal.get_tool("portal_catalog"))

    def get_factory(self, resource_type, unrestricted=False):
        """ """
        factory = queryMultiAdapter(
            (self.get_es_catalog(),), IElasticsearchEngineFactory
        )
        engine = factory(fhir_release=FHIR_VERSION.STU3)
        context = queryMultiAdapter((engine,), ISearchContextFactory)(
            resource_type, unrestricted=unrestricted
        )

        factory = queryMultiAdapter((context,), IZCatalogFhirSearch)
        return factory

    @property
    def resource_id(self):
        """ """
        if 1 < len(self.params):
            return self.params[1]
        return None

    @property
    def resource_type(self):
        """ """

        if 0 < len(self.params):
            _rt = self.params[0]
            return _rt
        return None

    def reply(self):
        """ """
        query_string = "_id={0}".format(self.resource_id)

        factory = self.get_factory(self.resource_type)
        brains = factory(query_string=query_string)

        if len(brains) == 0:
            return self.reply_no_content(status=404)

        obj = brains[0].getObject()

        if is_locked(obj, self.request):
            self.request.response.setStatus(403)
            return dict(error=dict(type="Forbidden", message="Resource is locked."))

        data = json_body(self.request)

        # Disable CSRF protection
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)

        fhir_value = getattr(obj, "{0}_resource".format(self.resource_type.lower()))
        fhir_value.patch(data["patch"])

        return self.reply_no_content(status=204)
