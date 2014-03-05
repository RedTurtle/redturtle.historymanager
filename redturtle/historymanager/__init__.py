# -*- coding: utf-8 -*-
"""Init and utils."""
from logging import getLogger
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('redturtle.historymanager')
logger = getLogger('redturtle.historymanager')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
