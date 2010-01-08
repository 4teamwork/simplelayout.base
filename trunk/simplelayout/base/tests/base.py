import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_simplelayout():
    """Set up the addition products required for the package.
    """
    
    # Load the ZCML configuration for the package.
    
    fiveconfigure.debug_mode = True
    import simpelayout.base
    zcml.load_config('configure.zcml', simpelayout.base)
    fiveconfigure.debug_mode = False
    
    # Tell the testing framework that the package is available.
    
    ztc.installPackage('simpelayout.base')

    
    
# Call deferred install function and then tell PloneTestCase to set up the product.

setup_simplelayout()
ptc.setupPloneSite(products=['setup_simplelayout',])


class SimplelayoutFunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """

