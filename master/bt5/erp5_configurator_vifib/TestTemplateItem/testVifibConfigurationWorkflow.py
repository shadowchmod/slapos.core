##############################################################################
# Copyright (c) 2011 Nexedi SA and Contributors. All Rights Reserved.
#                     Rafael Monnerat <rafael@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from Products.ERP5Configurator.tests.ConfiguratorTestMixin import \
    TestLiveConfiguratorWorkflowMixin
from Products.ERP5Type.tests.Sequence import SequenceList

class TestVifibConfiguratorWorkflow(TestLiveConfiguratorWorkflowMixin):
  """
    Configurator Mixin Class
  """
  # The list of standard business templates that the configurator should force
  # to install
  user_reference = "demo"
  standard_bt5_list = (
      'erp5_simulation', 
      'erp5_administration', 
      'erp5_pdm', 
      'erp5_trade', 
      'erp5_simulation_test', 
      'erp5_item', 
      'erp5_open_trade', 
      'erp5_forge', 
      'erp5_ingestion_mysql_innodb_catalog', 
      'erp5_ingestion', 
      'erp5_crm', 
      'erp5_jquery', 
      'erp5_jquery_ui', 
      'erp5_knowledge_pad', 
      'erp5_web', 
      'erp5_dms', 
      'erp5_l10n_fr', 
      'erp5_content_translation', 
      'erp5_software_pdm', 
      'erp5_computer_immobilisation', 
      'erp5_accounting', 
      'erp5_accounting_l10n_fr', 
      'erp5_tax_resource', 
      'erp5_discount_resource', 
      'erp5_invoicing', 
      'erp5_ods_style', 
      'erp5_odt_style', 
      'erp5_ooo_import', 
      'erp5_simplified_invoicing', 
      'erp5_legacy_tax_system', 
      'erp5_commerce', 
      'erp5_project', 
      'erp5_xhtml_jquery_style',
      'erp5_credential', 
      'erp5_km', 
      'erp5_web_download_theme', 
      'vifib_mysql_innodb_catalog', 
      'vifib_core', 
      'vifib_base', 
      'vifib_slap', 
      'vifib_forge_release', 
      'vifib_software_pdm', 
      'vifib_web', 
      'vifib_open_trade', 
      'vifib_l10n_fr',
      'vifib_data',
      'vifib_data_category',
      'vifib_data_web',
      'vifib_erp5')

  def getBusinessTemplateList(self):
    return ('erp5_core_proxy_field_legacy',
        'erp5_full_text_myisam_catalog',
        'erp5_base',
        'erp5_workflow',
        'erp5_configurator',
        'erp5_configurator_vifib',)

  def stepCreateBusinessConfiguration(self, sequence=None,\
                   sequence_list=None, **kw):
    """ Create one Business Configuration """
    module = self.portal.business_configuration_module
    business_configuration = module.newContent(
                               portal_type="Business Configuration",
                               title='Test Configurator Vifib Workflow')
    next_dict = {}
    sequence.edit(business_configuration=business_configuration,
                  next_dict=next_dict)

  def stepCheckConfigureInstallationForm(self, sequence=None,\
                    sequence_list=None, **kw):
    """ Check the installation form """
    response_dict = sequence.get("response_dict")
    # configuration is finished. We are at the Install state.
    # On maxma demo, installation is the first slide.
    self.assertEquals('show', response_dict['command'])
    self.assertEquals('Install', response_dict['next'])

  def stepSetVifibWorkflow(self, sequence=None, sequence_list=None, **kw):
    """ Set Consulting Workflow into Business Configuration """
    business_configuration = sequence.get("business_configuration")
    self.setBusinessConfigurationWorkflow(business_configuration,
                          "workflow_module/vifib_configuration_workflow")

  def stepCheckVifibObjectList(self, sequence=None, sequence_list=None, **kw):
    """ Check if objects are placed into the appropriate state """

    self.assertNotEquals(None, getattr(self.portal,
                         "portal_certificate_authority", None))

    self.assertNotEquals(None, getattr(self.portal, "portal_slap", None))

    # Verify if acl_user is appropriatted configured.
    # XXX Not implemented yet

    # Check Gadgets
    for gadget in self.portal.portal_gadgets.searchFolder():
      self.assertEquals('public', gadget.getValidationState(),
                        "%s is not public but %s" % (gadget.getRelativeUrl(), 
                                                     gadget.getValidationState()))
      gadget.Base_checkConsistency()

  ### STEPS
  DEFAULT_SEQUENCE_LIST = """
      stepCreateBusinessConfiguration
      stepTic
      stepSetVifibWorkflow
      stepTic
      stepConfiguratorNext
      stepTic
      stepCheckBT5ConfiguratorItem
      stepCheckConfigureInstallationForm
      stepSetupInstallConfiguration
      stepConfiguratorNext
      stepTic
      stepCheckInstallConfiguration
      stepStartConfigurationInstallation
      stepTic
      stepCheckInstanceIsConfigured%(country)s
      stepCheckVifibObjectList
      """

  def test_vifib_workflow(self):
    """ Test the consulting workflow configuration"""
    self.all_username_list = ["demo"]
    self.accountant_username_list = self.all_username_list
    self.sales_and_purchase_username_list = self.all_username_list
    self.warehouse_username_list = self.all_username_list
    self.simple_username_list = self.all_username_list
    self.restricted_security = 0
    sequence_list = SequenceList()
    sequence_string = self.DEFAULT_SEQUENCE_LIST % dict(country='France')
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

import unittest
def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestVifibConfiguratorWorkflow))
  return suite
