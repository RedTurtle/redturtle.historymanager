redturtle.historymanager
========================

Manage portal_historiesstorage
------------------------------

We need to be logged in as Manager
    >>> self.login('admin')

We need some stuff
    >>> from DateTime import DateTime
    >>> from Products.CMFCore.utils import getToolByName
    >>> from redturtle.historymanager.browser.manager import Manager
    >>> manager = Manager(self.portal, self.request)
    
We prepare some documents
    >>> self.prepare_folder()
    ['page0', 'page1', 'page2', 'page3', 'page4']

They are not under version control now
    >>> self.edit_page('page1')
    >>> self.edit_page('page1')
    >>> self.edit_page('page1')
    >>> self.folder.page1.version_id
    2

Now we have some data
    >>> len(manager.existing_working_copies)
    1
    >>> manager.dereference(self.folder.page1)
    (<ATDocument at /plone/Members/test_user_1_/page1>, 1)
    >>> manager.dereference_by_id(1)
    (<ATDocument at /plone/Members/test_user_1_/page1>, 1)

And we can purge them
    >>> manager.purge_all_revisions(1)
    >>> manager.dereference_by_id(1)
    (<ATDocument at /plone/Members/test_user_1_/page1>, 1)
    >>> self.unmemoize_request()
    >>> manager.existing_working_copies
    []

If we edit another page, another id is given
    >>> self.edit_page('page2')
    >>> manager.dereference(self.folder.page2)
    (<ATDocument at /plone/Members/test_user_1_/page2>, 3)

Editing again page1 will restore history data for this object:
    >>> self.edit_page('page1')
    >>> self.folder.page1.version_id
    0
    >>> self.edit_page('page1')
    >>> self.edit_page('page1')
    >>> self.edit_page('page1')
    >>> self.folder.page1.version_id
    3

The history id will be kept
    >>> manager.dereference(self.folder.page1)
    (<ATDocument at /plone/Members/test_user_1_/page1>, 1)

Now we clean the folder
    >>> self.reset_folder()
    >>> self.unmemoize_request()
    >>> len(manager.existing_working_copies)
    0
    >>> len(manager.deleted_working_copies)
    2

And add the same objects again
    >>> self.prepare_folder()
    ['page0', 'page1', 'page2', 'page3', 'page4']
    >>> self.edit_page('page1')
    >>> self.folder.page1.version_id
    0

A new id will be given:
    >>> manager.dereference(self.folder.page1)
    (<ATDocument at /plone/Members/test_user_1_/page1>, 4)

We can clean the deleted working copies, traversing to the view
@@historymanager-purge-deleted

    >>> self.unmemoize_request()
    >>> self.portal.restrictedTraverse('@@historymanager-purge-deleted')()
    '1\n3'
    >>> self.unmemoize_request()
    >>> len(manager.deleted_working_copies)
    0

We can purge the working copies for a single object traversing to the view
@@historymanager-purge-this

    >>> self.unmemoize_request()
    >>> self.folder.page1.restrictedTraverse('@@historymanager-purge-this')()
    'Cleared 1 versions'

We can purge the working copies of the objects under a path, 
traversing to the view
@@historymanager-purge-thispath

    >>> [self.edit_page('page%s' % idx) for idx in range(5)]
    [None, None, None, None, None]
    >>> self.unmemoize_request()
    >>> response = self.folder.restrictedTraverse('@@historymanager-purge-thispath')()
    >>> sorted(response.split(), ['5', '4', '6', '7', '8', '2']
    ['2', '4', '5', '6', '7', '8']

We can pass a date_limit parameter in the request
    >>> self.unmemoize_request()
    >>> view = self.folder.restrictedTraverse('@@historymanager-purge-thispath')
    >>> sorted(view.filtered_history_ids())
    [2, 4, 5, 6, 7, 8]

Without date_limit we have 6 objects.
Setting a date_limit and modyfying 2 objects we expect to have 4 objects 
    >>> self.unmemoize_request()

Now we set the date_limit
    >>> self.request.set('date_limit', str(DateTime()))
    >>> self.edit_page('page0')
    >>> self.edit_page('page2')
    >>> self.unmemoize_request()
    >>> sorted(view.filtered_history_ids())
    [2, 4, 7, 8]

Additionally we can filter by portal_type
    >>> self.request.set('portal_type', 'Document'))
    >>> self.unmemoize_request()
    >>> sorted(view.filtered_history_ids())
    [4, 7, 8]