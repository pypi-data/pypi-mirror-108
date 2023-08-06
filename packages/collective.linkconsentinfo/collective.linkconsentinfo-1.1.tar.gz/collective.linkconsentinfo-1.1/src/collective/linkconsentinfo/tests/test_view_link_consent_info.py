# -*- coding: utf-8 -*-
from collective.linkconsentinfo.testing import (
    COLLECTIVE_LINKCONSENTINFO_FUNCTIONAL_TESTING,
    COLLECTIVE_LINKCONSENTINFO_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_LINKCONSENTINFO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_link_consent_info_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='link-consent-info'
        )
        self.assertTrue(view.__name__ == 'link-consent-info')
        # self.assertTrue(
        #     'Sample View' in view(),
        #     'Sample View is not found in link-consent-info'
        # )

    def test_link_consent_info_not_matching_interface(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='link-consent-info'
            )


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_LINKCONSENTINFO_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
