from Acquisition import aq_inner, aq_parent
from Products.CMFPlone.utils import isDefaultPage
from plone.app.portlets import manager
from simplelayout.base.interfaces import ISimpleLayoutCapable


def _simplelayout_context(self):
    context = aq_inner(self.context)

    if ISimpleLayoutCapable.providedBy(context):
        return context

    if isDefaultPage(context, self.request):
        return aq_parent(context)
    else:
        return context


manager.ColumnPortletManagerRenderer._context = _simplelayout_context
