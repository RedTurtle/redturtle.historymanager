# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.utilities import dereference
from plone.memoize.view import memoize


class Manager(BrowserView):
    '''
    A view that shows the history entries
    '''
    @property
    @memoize
    def archivist(self):
        ''' Return the portal_archivist tool
        '''
        return getToolByName(self.context, 'portal_archivist')

    def get_date_limit(self):
        ''' Get's from the request a date_limit
        If not passed it will be now
        '''
        date_limit = self.request.get('date_limit', '')
        if date_limit:
            return DateTime(date_limit)
        else:
            return DateTime()

    @property
    @memoize
    def historiesstorage(self):
        ''' Return the portal_historiesstorage tool
        '''
        return getToolByName(self.context, 'portal_historiesstorage')

    @property
    @memoize
    def versions_repo(self):
        ''' The repo for the versions
        '''
        return self.historiesstorage._getZVCRepo()

    def dereference(self, target=None):
        ''' Return the portal_historiesstorage tool
        '''
        return dereference(target or self.context)

    def dereference_by_id(self, history_id):
        ''' Dereference an object by history_id
        '''
        return dereference(history_id=history_id,
                           zodb_hook=self.context)

    @property
    @memoize
    def purgepolicy(self):
        ''' Return the portal_historiesstorage tool
        '''
        return getToolByName(self.context, 'portal_purgepolicy')

    @property
    @memoize
    def statistics(self):
        ''' Return the portal_historiesstorage statistics
        '''
        return self.historiesstorage.zmi_getStorageStatistics()

    def get_history_for(self, history_id):
        ''' Get's the history for a given history_id
        '''
        return self.historiesstorage._getShadowHistory(history_id)

    @property
    @memoize
    def deleted_working_copies(self):
        ''' Deleted working copies
        '''
        return self.statistics.get('deleted', [])

    @property
    @memoize
    def existing_working_copies(self):
        ''' Existing working copies
        '''
        return self.statistics.get('existing', [])

    def remove_from_shadowstorage(self, history_id):
        ''' Remove an history_id from the shadow storage
        '''
        storage = self.historiesstorage._getShadowStorage()._storage
        return storage.pop(history_id, None)

    @memoize
    def filtered_history_ids(self):
        ''' This will return a list of history_ids to be purged
        '''
        return []

    def purge_all_revisions(self, history_id=None):
        ''' Nukes the portal history for history_id
        '''
        comment = "Purged by %s" % self.__name__
        metadata = {'sys_metadata': {'comment': comment}}

        if history_id:
            context = self.context
        else:
            context, history_id = self.dereference(context)

        history = self.historiesstorage.getHistory(history_id, countPurged=False)
        for revision in history:
            revision  # pylint
            self.archivist.purge(history_id=history_id,
                                 selector=0,
                                 metadata=metadata)
        self.remove_from_shadowstorage(history_id)

    def __call__(self):
        ''' Not to be done like this
        '''
        history_ids = self.filtered_history_ids()
        if not history_ids:
            return 'No ids'
        map(self.purge_all_revisions, history_ids)
        return '\n'.join(map(str, history_ids))


class DereferenceView(Manager):
    ''' Expose the dereference method in this context
    '''
    def __call__(self):
        ''' Expose the dereference method in this context
        '''
        return self.dereference()


class LocalPurgeView(Manager):
    ''' Purge all the revisions for this context
    '''
    def __call__(self):
        ''' Not to be done like this
        '''
        context, history_id = self.dereference()
        context  # pylint shut up

        history = self.get_history_for(history_id)
        len_before = history.getLength(True)

        self.purge_all_revisions(history_id)
        return "Cleared %s versions" % len_before


class PurgeOlderThanView(Manager):
    ''' Purge all the revisions for objects modifed before some date

    The should be passed in the request

    '''
    @memoize
    def filtered_history_ids(self):
        ''' This will return a list of history_ids to be purged
        '''
        date_limit = self.get_date_limit()
        history_ids = [existing['history_id']
                       for existing in self.existing_working_copies]
        dereferences = [self.dereference_by_id(history_id)
                        for history_id in history_ids]
        return [history_id
                for obj, history_id
                in dereferences if obj.modified() < date_limit]


class PurgeInPathView(Manager):
    ''' Purge stuff under a path
    '''
    @memoize
    def filtered_history_ids(self):
        ''' This will return a list of history_ids to be purged under this path
        You can optionally filter them:
         - by portal_type by passing a portal_type argument in the request
         - by setting a date_limit parameter
        '''
        pc = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        portal_type = self.request.get('portal_type', '')
        max_modified = {'query': self.get_date_limit(),
                        'range': 'max'}

        brains = pc(path=path, portal_type=portal_type, modified=max_modified)
        return [self.dereference(brain.getObject())[1]
                for brain in brains]


class PurgeDeletedView(Manager):
    ''' Purge all the revisions for this context
    '''
    @memoize
    def filtered_history_ids(self):
        ''' This will return a list of history_ids to be purged
        '''
        return [deleted['history_id']
                for deleted in self.deleted_working_copies]
