from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing.z2 import installProduct
from simplelayout.base.tests import builders
from zope.configuration import xmlconfig


class SimplelayoutBaseLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import simplelayout.base
        xmlconfig.file(
            'configure.zcml', simplelayout.base, context=configurationContext)
        installProduct(app, 'simplelayout.base')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'simplelayout.base:default')


SL_BASE_FIXTURE = SimplelayoutBaseLayer()
SL_BASE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SL_BASE_FIXTURE, ),
    name="simplelayout.bases:Integration")
SL_BASE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SL_BASE_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="simplelayout.bases:Functional")


class SLTypesLayer(PloneSandboxLayer):
    defaultBases = (SL_BASE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import simplelayout.types.common
        xmlconfig.file(
            'configure.zcml', simplelayout.types.common,
            context=configurationContext)
        installProduct(app, 'simplelayout.types.common')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'simplelayout.types.common:default')


SL_TYPES_FIXTURE = SLTypesLayer()
SL_TYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SL_TYPES_FIXTURE, ),
    name="simplelayout.base:types:Integration")
SL_TYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SL_TYPES_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="simplelayout.base:types:Functional")
