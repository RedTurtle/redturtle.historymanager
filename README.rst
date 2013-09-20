========================
redturtle.historymanager
========================

A Plone add-on that ...

* `Source code @ GitHub <https://github.com/RedTurtle/redturtle.historymanager>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/redturtle.historymanager>`_

Caveat: developed for Plone 3.2.2
=================================

How it works
============

It gives you some management views you can play with to clean your Data.fs 
from old versions.

Installation
============

To install `redturtle.historymanager` you simply add
``redturtle.historymanager``
to the list of eggs in your buildout, 
to the zcml run buildout 
and restart Plone.

Available views
===============

historymanager-dereference
--------------------------

Calls the dereference method from Products.CMFEditions.utilities
on the view context and returns the history_id

historymanager-purge-this
-------------------------

Purge all the revisions for this context.

historymanager-purge-thispath
-----------------------------

Purge all the revisions for the objects in the subtree of context.
It accepts two parameter to limit the effect of this view:

- portal_type: a string identifying a portal type to be purged
- date_limit: a string that can be converted to a DateTime, e.g.:

  * 2013/09/20
  * 2013/09/20 11:37:04.178 GMT+2

historymanager-purge-deleted
----------------------------
This will delete all the revisions for the deleted stuff
