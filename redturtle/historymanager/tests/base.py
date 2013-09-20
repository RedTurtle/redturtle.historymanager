"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

# When ZopeTestCase configures Zope, it will *not* auto-load products
# in Products/. Instead, we have to use a statement such as:
#   ztc.installProduct('SimpleAttachment')
# This does *not* apply to products in eggs and Python packages (i.e.
# not in the Products.*) namespace. For that, see below.
# All of Plone's products are already set up by PloneTestCase.


@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """

    # Load the ZCML configuration for the example.tests package.
    # This can of course use <include /> to include other packages.

    fiveconfigure.debug_mode = True
    import redturtle.historymanager
    zcml.load_config('configure.zcml', redturtle.historymanager)
    fiveconfigure.debug_mode = False

    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML. Thus, we do it here. Note the use of installPackage()
    # instead of installProduct().
    # This is *only* necessary for packages outside the Products.*
    # namespace which are also declared as Zope 2 products, using
    # <five:registerPackage /> in ZCML.

    # We may also need to load dependencies, e.g.:
    #   ztc.installPackage('borg.localrole')
    ztc.installPackage('redturtle.historymanager')

# The order here is important: We first call the (deferred) function
# which installs the products we need for this product. Then, we let
# PloneTestCase set up this product on installation.

setup_product()
ptc.setupPloneSite(products=['redturtle.historymanager'])


class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """


class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """
    def prepare_folder(self):
        ''' Prepare the contents in the folder
        '''
        return [self.folder.invokeFactory('Document', 'page%s' % idx)
                for idx in range(5)]

    def reset_folder(self):
        ''' Prepare the contents in the folder
        '''
        self.folder.manage_delObjects(self.folder.keys())

    @property
    def request(self):
        '''
        Return a request
        '''
        return self.portal.REQUEST

    def unmemoize_request(self):
        ''' Remove the memoize keys from request annotations
        '''
        self.request.__annotations__.pop('plone.memoize')

    def edit_page(self, page_id):
        ''' Edit a page title
        '''
        obj = self.folder[page_id]
        version = getattr(obj, 'version_id', 'initial')
        new_title = "Version %s" % version
        obj.edit(title=new_title)
        self.portal.portal_repository.applyVersionControl(obj, new_title)

    def afterSetUp(self):
        roles = ('Member', 'Manager')
        self.portal.portal_membership.addMember('admin',
                                                'secret',
                                                roles, [])
