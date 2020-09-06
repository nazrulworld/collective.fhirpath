# -*- coding: utf-8 -*-
from collective.elasticsearch.es import ElasticSearchCatalog
from collective.fhirpath.utils import FHIRModelServiceMixin
from fhirpath.enums import FHIR_VERSION
from fhirpath.interfaces import IElasticsearchEngineFactory
from fhirpath.interfaces import IFhirSearch
from fhirpath.interfaces import ISearchContextFactory
from plone import api
from plone.restapi.services import Service
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class FHIRSearchService(FHIRModelServiceMixin, Service):
    """ """

    def __init__(self, context, request):
        """ """
        super(FHIRSearchService, self).__init__(context, request)
        self.params = []

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

        factory = queryMultiAdapter((context,), IFhirSearch)
        return factory

    def reply(self):
        """ """
        bundle = self.build_result()
        if self.resource_id:
            if bundle.total == 0:
                return self.reply_no_content(status=404)
            return bundle.entry[0].resource

        return bundle

    def publishTraverse(self, request, name):  # noqa: N802
        # Consume any path segments after /@fhir as parameters
        self.params.append(name)
        return self

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

    def _get_fhir_fieldname(self, resource_type=None):
        """We assume FHIR Field name is ``{resource type}_resource``"""
        resource_type = resource_type or self.resource_type

        return "{0}_resource".format(resource_type.lower())

    def get_query_string(self):
        """ """
        if self.resource_id:
            return "_id={0}".format(self.resource_id)

        return self.request["QUERY_STRING"]

    def build_result(self):
        """ """
        factory = self.get_factory(self.resource_type)

        return factory(query_string=self.get_query_string())
