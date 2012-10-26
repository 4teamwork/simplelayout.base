from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from zope.configuration import xmlconfig
from plone.testing.z2 import installProduct


class SimplelayoutBaseLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import simplelayout.base
        xmlconfig.file(
            'configure.zcml', simplelayout.base, context=configurationContext)
        installProduct(app, 'simplelayout.base')
        import simplelayout.types.common
        xmlconfig.file(
            'configure.zcml', simplelayout.types.common,
            context=configurationContext)
        installProduct(app, 'simplelayout.types.common')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'simplelayout.base:default')


SL_BASE_FIXTURE = SimplelayoutBaseLayer()
SL_BASE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SL_BASE_FIXTURE, ), name="simplelayout.bases:Integration")
SL_BASE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SL_BASE_FIXTURE, ), name="simplelayout.bases:Functional")
