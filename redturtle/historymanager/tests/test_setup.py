# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from redturtle.historymanager.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of redturtle.historymanager into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if redturtle.historymanager is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('redturtle.historymanager'))

    def test_uninstall(self):
        """Test if redturtle.historymanager is cleanly uninstalled."""
        self.installer.uninstallProducts(['redturtle.historymanager'])
        self.assertFalse(self.installer.isProductInstalled('redturtle.historymanager'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IRedturtleHistorymanagerLayer is registered."""
        from redturtle.historymanager.interfaces import IRedturtleHistorymanagerLayer
        from plone.browserlayer import utils
        self.failUnless(IRedturtleHistorymanagerLayer in utils.registered_layers())
