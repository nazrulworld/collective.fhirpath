# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.fhirpath


class CollectiveFhirpathLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.fhirpath)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.fhirpath:default')


COLLECTIVE_FHIRPATH_FIXTURE = CollectiveFhirpathLayer()


COLLECTIVE_FHIRPATH_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_FHIRPATH_FIXTURE,),
    name='CollectiveFhirpathLayer:IntegrationTesting',
)


COLLECTIVE_FHIRPATH_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_FHIRPATH_FIXTURE,),
    name='CollectiveFhirpathLayer:FunctionalTesting',
)


COLLECTIVE_FHIRPATH_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_FHIRPATH_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveFhirpathLayer:AcceptanceTesting',
)
