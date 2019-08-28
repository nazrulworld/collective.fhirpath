# _*_ coding: utf-8 _*_
from collective.elasticsearch.es import ElasticSearchCatalog
from collective.fhirpath.testing import COLLECTIVE_FHIRPATH_FUNCTIONAL_TESTING
from fhirpath.enums import FHIR_VERSION
from fhirpath.enums import SortOrderType
from fhirpath.fql import Q_
from fhirpath.fql import sort_
from fhirpath.fql import T_
from fhirpath.interfaces import IElasticsearchEngineFactory
from plone import api
from plone.app.fhirfield.tests.base import BaseFunctionalTesting
from zope.component import queryMultiAdapter


__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


class FhirPathPloneQueryFunctionalTest(BaseFunctionalTesting):
    """ """
    layer = COLLECTIVE_FHIRPATH_FUNCTIONAL_TESTING

    def get_es_catalog(self):
        """ """
        return ElasticSearchCatalog(api.portal.get_tool("portal_catalog"))

    def get_engine(self):
        """ """
        factory = queryMultiAdapter(
            (self.get_es_catalog(),), IElasticsearchEngineFactory
        )
        engine = factory(fhir_version=FHIR_VERSION.STU3)
        return engine

    def test_iter_result(self):
        """ """
        self.load_contents()
        engine = self.get_engine()
        builder = Q_(resource="Organization", engine=engine)
        builder = (
            builder.where(T_(
                "Organization.meta.profile",
                "http://hl7.org/fhir/Organization"))
            .sort(sort_("Organization.meta.lastUpdated", SortOrderType.DESC))
        )
        count = 0

        for resource in builder(async_result=False, unrestricted=True):
            count += 1
            assert resource.__class__.__name__ == "OrganizationModel"

        self.assertEqual(count, 2)

    def test_fetchall(self):
        """ """
        self.load_contents()
        engine = self.get_engine()
        builder = Q_(resource="Organization", engine=engine)
        builder = (
            builder.where(T_(
                "Organization.meta.profile",
                "http://hl7.org/fhir/Organization"))
            .sort(sort_("Organization.meta.lastUpdated", SortOrderType.DESC))
        )
        result = builder(async_result=False, unrestricted=True).fetchall()
        self.assertEqual(result.header.total, 2)
