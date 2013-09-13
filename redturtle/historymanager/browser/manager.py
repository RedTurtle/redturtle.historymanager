# -*- coding: utf-8 -*-
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
        del self.historiesstorage._getShadowStorage()._storage[history_id]

    def purge_all(self, history_id=None):
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


class PurgeDeletedView(Manager):
    ''' Purge all the revisions for this context
    '''
    def __call__(self):
        ''' Not to be done like this
        '''
        return 1


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
        self.purge_all(history_id)
        return "Cleared %s versions" % len_before


class DereferenceView(Manager):
    ''' Expose the dereference method in this context
    '''
    def __call__(self):
        ''' Expose the dereference method in this context
        '''
        return self.dereference()
