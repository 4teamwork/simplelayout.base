from zope.formlib import form
from plone.fieldsets.fieldsets import FormFieldsets
from zope.interface import implements
from zope.component import getUtility, getMultiAdapter
from zope.schema.fieldproperty import FieldProperty
from persistent import Persistent

from interfaces import ISimplelayoutConfiguration, \
                       ISimplelayoutConfigurationOneColumn, \
                       ISimplelayoutConfigurationTwoColumn
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.validators import null_validator
from zope.event import notify
from plone.protect import CheckAuthenticator
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.controlpanel.events import ConfigurationChangedEvent

from simplelayout.base import websiteMessageFactory as _


def getConfigUtil(context):
    return getUtility(ISimplelayoutConfiguration, name='sl-config')


class SimpleLayoutConfigurationForm(ControlPanelForm):
    """Use plone.app.controlpanel.form.ControlPanelForm and plone.fieldsets
    for a plone look adn feel

    """

    baseSets = FormFieldsets(ISimplelayoutConfiguration)
    baseSets.label = _(u'Basic options')
    baseSets.id = 'basic_options'

    OneColumnSets = FormFieldsets(ISimplelayoutConfigurationOneColumn)
    OneColumnSets.label = _(u'config for one column design')
    OneColumnSets.id = 'one_column_sizes'

    TwoColumnsSets = FormFieldsets(ISimplelayoutConfigurationTwoColumn)
    TwoColumnsSets.label = _(u'config for two column design')
    TwoColumnsSets.id = 'two_column_sizes'

    label = _(u"Simplelayout configuration")
    form_name = _(u'Simplelayout configuration form')
    description = _(u'This form is used to configure the simplelayout')

    form_fields = FormFieldsets(baseSets, OneColumnSets, TwoColumnsSets)

    @form.action(_(u'label_save'), name=u'save')
    def handle_edit_action(self, action, data):
        CheckAuthenticator(self.request)
        if form.applyChanges(self.context, self.form_fields, data,
                             self.adapters):
            self.status = _("Changes saved.")
            notify(ConfigurationChangedEvent(self, data))
            self._on_save(data)
        else:
            self.status = _("No changes made.")

    @form.action(_(u'label_cancel'),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        IStatusMessage(self.request).addStatusMessage(_("Changes canceled."),
                                                      type="info")
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url + '/plone_control_panel')
        return ''


class SimpleLayoutConfiguration(Persistent):
    """Define a object with the given attributes to store our data

    """
    implements(
        ISimplelayoutConfiguration,
        ISimplelayoutConfigurationOneColumn,
        ISimplelayoutConfigurationTwoColumn)

    show_design_tab = FieldProperty(
        ISimplelayoutConfiguration['show_design_tab'])
    show_design_tab_roles = FieldProperty(
        ISimplelayoutConfiguration['show_design_tab_roles'])

    small_size = FieldProperty(
        ISimplelayoutConfigurationOneColumn['small_size'])
    middle_size = FieldProperty(
        ISimplelayoutConfigurationOneColumn['middle_size'])
    full_size = FieldProperty(
        ISimplelayoutConfigurationOneColumn['full_size'])

    small_size_two = FieldProperty(
        ISimplelayoutConfigurationTwoColumn['small_size_two'])
    middle_size_two = FieldProperty(
        ISimplelayoutConfigurationTwoColumn['middle_size_two'])
    full_size_two = FieldProperty(
        ISimplelayoutConfigurationTwoColumn['full_size_two'])
