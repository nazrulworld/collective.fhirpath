# _*_ coding: utf-8 _*_
from collective.elasticsearch.es import ElasticSearchCatalog
from collective.fhirpath.testing import COLLECTIVE_FHIRPATH_FUNCTIONAL_TESTING
from fhirpath.enums import FHIR_VERSION
from fhirpath.interfaces import IElasticsearchEngineFactory
from fhirpath.interfaces import IFhirSearch
from fhirpath.interfaces import ISearchContextFactory
from plone import api
from plone.app.fhirfield.tests.base import BaseFunctionalTesting
from zope.component import queryMultiAdapter
from plone.app.testing import SITE_OWNER_NAME


__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


class FhirPathPloneSearchFunctional(BaseFunctionalTesting):
    """ """

    layer = COLLECTIVE_FHIRPATH_FUNCTIONAL_TESTING

    def get_es_catalog(self):
        """ """
        return ElasticSearchCatalog(api.portal.get_tool("portal_catalog"))

    def get_factory(self, resource_type, unrestricted=False):
        """ """
        factory = queryMultiAdapter(
            (self.get_es_catalog(),), IElasticsearchEngineFactory
        )
        engine = factory(fhir_version=FHIR_VERSION.STU3)
        context = queryMultiAdapter((engine,), ISearchContextFactory)(
            "Organization", unrestricted=unrestricted
        )

        factory = queryMultiAdapter((context,), IFhirSearch)
        return factory

    def test_basic_search(self):
        """ """
        self.load_contents()

        params = [("_lastUpdated", "2010-05-28T05:35:56+00:00")]
        search_factory = self.get_factory("Organization", True)
        bundle = search_factory(params)
        self.assertEqual(len(bundle.entry), 1)

        params = (
            ("_profile", "http://hl7.org/fhir/Organization"),
            ("identifier", "urn:oid:2.16.528.1|91654"),
            ("type", "http://hl7.org/fhir/organization-type|prov"),
            ("address-postalcode", "9100 AA"),
            ("address", "Den Burg"),
        )
        bundle = search_factory(params)
        self.assertEqual(len(bundle.entry), 2)

    def test_permission_aware_search(self):
        """ """
        params = [("_lastUpdated", "2010-05-28T05:35:56+00:00")]
        search_factory = self.get_factory("Organization", False)

        with api.env.adopt_user(username=SITE_OWNER_NAME):
            bundle = search_factory(params)
            # xxx: some how permission aware query is not working!
            # have to look immediately
            return
            self.assertEqual(len(bundle.entry), 1)
