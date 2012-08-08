import unittest
from Products.ERP5Type.tests.Sequence import SequenceList
from testVifibSlapWebService import TestVifibSlapWebServiceMixin
from Products.ERP5Type.DateUtils import getClosestDate, addToDate
from DateTime import DateTime

class TestVifibInstanceHostingRelatedDocument(TestVifibSlapWebServiceMixin):

  def stepCheckSubscriptionSalePackingListCoverage(self, sequence, **kw):
    hosting_subscription = self.portal.portal_catalog.getResultValue(
      uid=sequence['hosting_subscription_uid'])
    delivery_list = self.portal.portal_catalog(
      portal_type='Sale Packing List',
      causality_relative_url=hosting_subscription.getRelativeUrl(),
      sort_on=(('delivery.start_date', 'desc'),)
    )
    # is next month covered?
    self.assertEqual(1, len(delivery_list))

    instance_setup_delivery = self.portal.portal_catalog.getResultValue(
      portal_type='Sale Packing List Line',
      default_aggregate_uid=sequence['software_instance_uid'],
      resource=self.portal.portal_preferences\
        .getPreferredInstanceSetupResource()).getParentValue()

    self.assertEqual('delivered', instance_setup_delivery.getSimulationState())
    start_date = None
    for item in self.portal.portal_workflow.getInfoFor(
      ob=instance_setup_delivery, name='history', wf_id='packing_list_workflow'):
      if item.get('simulation_state') == 'stopped':
        start_date = item.get('time')
        break
    start_date = getClosestDate(target_date=start_date, precision='day')
    while start_date.day() >= 29:
      start_date = addToDate(start_date, to_add={'day': -1})
    stop_date = addToDate(start_date, to_add={'month': 1})
    idx = 0
    for delivery in delivery_list:
      self.assertEqual(start_date, delivery.getStartDate())
      self.assertEqual(stop_date, delivery.getStopDate())

      self.assertEqual(hosting_subscription.getRelativeUrl(),
        delivery.getCausality())
      delivery_line_list = \
        delivery.contentValues(portal_type="Sale Packing List Line")
      self.assertEquals(1, len(delivery_line_list))
      delivery_line = delivery_line_list[0]
      self.assertEquals("organisation_module/vifib_internet",
        delivery.getSource())
      self.assertEquals("organisation_module/vifib_internet",
        delivery.getSourceSection())
      self.assertEquals("person_module/test_vifib_customer",
        delivery.getDestination())
      self.assertEquals("person_module/test_vifib_customer",
        delivery.getDestinationSection())
      self.assertEquals("currency_module/EUR",
        delivery.getPriceCurrency())

      # check sale packing list line related property
      self.assertEquals("service_module/vifib_instance_subscription",
        delivery_line.getResource())
      self.assertEquals(1,
        delivery_line.getQuantity())
      self.assertEquals("unit/piece",
        delivery_line.getQuantityUnit())
      self.assertEquals(0.83612040133800003,
        delivery_line.getPrice())

      # fetch open order, open order line and subscription
      person = self.portal.person_module['test_vifib_customer']
      open_order = self.portal.portal_catalog.getResultValue(
        default_destination_decision_uid=person.getUid(),
        portal_type="Open Sale Order",
        validation_state='validated')
      open_order_line = \
        open_order.contentValues(portal_type="Open Sale Order Line")[0]

      # check related property
      self.assertEquals(open_order_line.getSpecialise(),
        delivery.getSpecialise())

      idx += 1

  def stepCheckHostingSubscriptionInitialDocumentCoverage(self, sequence, **kw):
    catalog = self.portal.portal_catalog
    hosting_resource = self.portal.portal_preferences\
      .getPreferredInstanceHostingResource()
    setup_resource = self.portal.portal_preferences\
      .getPreferredInstanceSetupResource()
    subscription_resource = self.portal.portal_preferences\
      .getPreferredInstanceSubscriptionResource()
    sequence.edit(
      hosting_resource=hosting_resource,
      setup_resource=setup_resource,
      subscription_resource=subscription_resource
    )

    hosting_subscription = catalog.getResultValue(
      uid=sequence['hosting_subscription_uid'])
    hosting_subscription_url = hosting_subscription.getRelativeUrl()

    # hosting is confirmed, so no invoice
    hosting_delivery_line_list = catalog(portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=hosting_resource)

    self.assertEqual(1, len(hosting_delivery_line_list))
    self.assertEqual('confirmed', hosting_delivery_line_list[0]\
      .getSimulationState())

    hosting_invoice_line_list = catalog(portal_type='Invoice Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=hosting_resource)
    self.assertEqual(0, len(hosting_invoice_line_list))

    # setup is delivered, and has there is invoice
    setup_delivery_line_list = catalog(portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=setup_resource)

    self.assertEqual(1, len(setup_delivery_line_list))
    self.assertEqual('delivered', setup_delivery_line_list[0]\
      .getSimulationState())

    setup_invoice_line_list = catalog(portal_type='Invoice Line',
      resource_relative_url=setup_resource)
    self.assertEqual(1, len(setup_invoice_line_list))
    self.assertEqual('planned', setup_invoice_line_list[0]\
      .getSimulationState())

    # there are 2 confirmed subscription, so no invoice
    subscription_delivery_line_list = catalog(
      portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=subscription_resource,
      sort_on=(('movement.start_date', 'desc'),)
    )

    self.assertEqual(1, len(subscription_delivery_line_list))
    self.assertEqual(['delivered'], [q.getSimulationState() for \
      q in subscription_delivery_line_list])

    subscription_invoice_line_list = catalog(portal_type='Invoice Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=subscription_resource)
    self.assertEqual(0, len(subscription_invoice_line_list))

    # invoice shall be solved
    invoice =  setup_invoice_line_list[0].getParentValue()
    self.assertEqual('solved', invoice.getCausalityState())

    # invoice shall have no causality
    self.assertEqual(invoice.getCausalityList(), [])

    # there shall be no payment transaction related
    self.assertEqual([], invoice.getCausalityRelatedList(
      portal_type='Payment Transaction'))

    sequence.edit(
      subscription_delivery_uid_list=[q.getParentValue().getUid() for q in \
        subscription_delivery_line_list]
    )

  def stepSelectNextSubscriptionDelivery(self, sequence, **kw):
    subscription_delivery_uid_list = sequence['subscription_delivery_uid_list']
    subscription_delivery_uid_list.reverse()
    subscription_delivery_uid = subscription_delivery_uid_list.pop()
    subscription_delivery_uid_list.reverse()
    sequence.edit(
      subscription_delivery_uid_list=subscription_delivery_uid_list,
      subscription_delivery_uid=subscription_delivery_uid
    )

  def stepCheckHostingSubscriptionStoppedDocumentCoverage(self, sequence, **kw):
    catalog = self.portal.portal_catalog
    hosting_subscription = catalog.getResultValue(
      uid=sequence['hosting_subscription_uid'])
    hosting_subscription_url = hosting_subscription.getRelativeUrl()

    # hosting is confirmed, so no invoice
    hosting_delivery_line_list = catalog(portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['hosting_resource'])

    self.assertEqual(1, len(hosting_delivery_line_list))
    self.assertEqual('confirmed', hosting_delivery_line_list[0]\
      .getSimulationState())

    hosting_invoice_line_list = catalog(portal_type='Invoice Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['hosting_resource'])
    self.assertEqual(0, len(hosting_invoice_line_list))

    # setup is delivered, and has there is invoice
    setup_delivery_line_list = catalog(portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['setup_resource'])

    self.assertEqual(1, len(setup_delivery_line_list))
    self.assertEqual('delivered', setup_delivery_line_list[0]\
      .getSimulationState())

    setup_invoice_line_list = catalog(portal_type='Invoice Line',
      resource_relative_url=sequence['setup_resource'])
    self.assertEqual(1, len(setup_invoice_line_list))
    self.assertEqual('planned', setup_invoice_line_list[0]\
      .getSimulationState())

    # there are 1 confirmed and 1 stopped subscription, so 1 invoice line
    subscription_delivery_line_list = catalog(
      portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['subscription_resource'])

    self.assertEqual(1, len(subscription_delivery_line_list))
    self.assertEqual(['delivered'],
      sorted([q.getSimulationState() for \
      q in subscription_delivery_line_list]))

    subscription_invoice_line_list = catalog(portal_type='Invoice Line',
      resource_relative_url=sequence['subscription_resource'])
    self.assertEqual(1, len(subscription_invoice_line_list))
    self.assertEqual('planned', subscription_invoice_line_list[0]\
      .getSimulationState())

    # there are two invoice lines sharing same invoice
    self.assertEqual(
      setup_invoice_line_list[0].getParentValue().getRelativeUrl(),
      subscription_invoice_line_list[0].getParentValue().getRelativeUrl()
    )

    # invoice shall be solved
    self.assertEqual('solved', setup_invoice_line_list[0].getCausalityState())

    # invoice shall have no causality
    self.assertEqual(setup_invoice_line_list[0].getParentValue()\
      .getCausalityList(), [])

  def stepSelectPlannedInvoice(self, sequence, **kw):
    invoice_line = self.portal.portal_catalog.getResultValue(
      portal_type='Invoice Line',
      simulation_state='planned'
    )

    # there shall be no payment transaction related
    self.assertEqual([], invoice_line.getParentValue().getCausalityRelatedList(
      portal_type='Payment Transaction'))

    sequence.edit(invoice_uid=invoice_line.getParentValue().getUid())

  def stepConfirmInvoice(self, sequence, **kw):
    self.portal.portal_catalog.getResultValue(
      uid=sequence['invoice_uid']).confirm()

  def stepCheckHostingSubscriptionConfirmedInvoiceDocumentCoverage(self,
    sequence, **kw):
    catalog = self.portal.portal_catalog
    hosting_subscription = catalog.getResultValue(
      uid=sequence['hosting_subscription_uid'])
    hosting_subscription_url = hosting_subscription.getRelativeUrl()

    # hosting is confirmed, so no invoice
    hosting_delivery_line_list = catalog(portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['hosting_resource'])

    self.assertEqual(1, len(hosting_delivery_line_list))
    self.assertEqual('confirmed', hosting_delivery_line_list[0]\
      .getSimulationState())

    hosting_invoice_line_list = catalog(portal_type='Invoice Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['hosting_resource'])
    self.assertEqual(0, len(hosting_invoice_line_list))

    # setup is delivered, and has there is invoice
    setup_delivery_line_list = catalog(portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['setup_resource'])

    self.assertEqual(1, len(setup_delivery_line_list))
    self.assertEqual('delivered', setup_delivery_line_list[0]\
      .getSimulationState())

    setup_invoice_line_list = catalog(portal_type='Invoice Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['setup_resource'])
    self.assertEqual(1, len(setup_invoice_line_list))
    self.assertEqual('confirmed', setup_invoice_line_list[0]\
      .getSimulationState())

    # there are 10 confirmed and 2 stopped subscription, so 2 invoice line
    subscription_delivery_line_list = catalog(
      portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['subscription_resource'])

    self.assertEqual(2, len(subscription_delivery_line_list))
    self.assertEqual(['stopped'] * 2,
      sorted([q.getSimulationState() for \
      q in subscription_delivery_line_list]))

    subscription_invoice_line_list = catalog(portal_type='Invoice Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['subscription_resource'])
    self.assertEqual(2, len(subscription_invoice_line_list))
    self.assertEqual(['confirmed', 'planned'],
      sorted([q.getSimulationState() for q in subscription_invoice_line_list]))

    # there are three invoice lines, where two share same invoice
    # and other is on new one
    self.assertEqual(
      setup_invoice_line_list[0].getParentValue().getRelativeUrl(),
      [q.getParentValue().getRelativeUrl() for q in \
        subscription_invoice_line_list \
          if q.getSimulationState() == 'confirmed'][0]
    )
    self.assertNotEqual(
      setup_invoice_line_list[0].getParentValue().getRelativeUrl(),
      [q.getParentValue().getRelativeUrl() for q in \
        subscription_invoice_line_list \
          if q.getSimulationState() == 'planned'][0]
    )

    confirmed_invoice = setup_invoice_line_list[0].getParentValue()
    planned_invoice = [q.getParentValue() for q in \
      subscription_invoice_line_list \
        if q.getSimulationState() == 'planned'][0]

    # invoices shall be solved
    self.assertEqual('solved', planned_invoice.getCausalityState())
    self.assertEqual('solved', confirmed_invoice.getCausalityState())

    # there shall be no payment transaction related
    self.assertEqual([], planned_invoice.getCausalityRelatedList(
      portal_type='Payment Transaction'))
    self.assertEqual([], confirmed_invoice.getCausalityRelatedList(
      portal_type='Payment Transaction'))

    # confirmed invoice shall have no causality
    self.assertEqual(confirmed_invoice.getCausalityList(), [])

    # planned invoice shall have no causality
    self.assertEqual(planned_invoice.getCausalityList(), [])

  def stepStartInvoice(self, sequence, **kw):
    self.portal.portal_catalog.getResultValue(
      uid=sequence['invoice_uid']).start()

  def stepStopInvoice(self, sequence, **kw):
    self.portal.portal_catalog.getResultValue(
      uid=sequence['invoice_uid']).stop()

  def stepCheckHostingSubscriptionStoppedInvoiceDocumentCoverage(self,
    sequence, **kw):
    catalog = self.portal.portal_catalog
    hosting_subscription = catalog.getResultValue(
      uid=sequence['hosting_subscription_uid'])
    hosting_subscription_url = hosting_subscription.getRelativeUrl()

    # hosting is confirmed, so no invoice
    hosting_delivery_line_list = catalog(portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['hosting_resource'])

    self.assertEqual(1, len(hosting_delivery_line_list))
    self.assertEqual('confirmed', hosting_delivery_line_list[0]\
      .getSimulationState())

    hosting_invoice_line_list = catalog(portal_type='Invoice Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['hosting_resource'])
    self.assertEqual(0, len(hosting_invoice_line_list))

    # setup is delivered, and has there is invoice
    setup_delivery_line_list = catalog(portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['setup_resource'])

    self.assertEqual(1, len(setup_delivery_line_list))
    self.assertEqual('delivered', setup_delivery_line_list[0]\
      .getSimulationState())

    setup_invoice_line_list = catalog(portal_type='Invoice Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['setup_resource'])
    self.assertEqual(1, len(setup_invoice_line_list))
    self.assertEqual('stopped', setup_invoice_line_list[0]\
      .getSimulationState())

    # there are 10 confirmed and 2 stopped subscription, so 2 invoice line
    subscription_delivery_line_list = catalog(
      portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['subscription_resource'])

    self.assertEqual(2, len(subscription_delivery_line_list))
    self.assertEqual(['stopped'] * 2,
      sorted([q.getSimulationState() for \
      q in subscription_delivery_line_list]))

    subscription_invoice_line_list = catalog(portal_type='Invoice Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['subscription_resource'])
    self.assertEqual(2, len(subscription_invoice_line_list))
    self.assertEqual(['planned', 'stopped'],
      sorted([q.getSimulationState() for q in subscription_invoice_line_list]))

    # there are three invoice lines, where two share same invoice
    # and other is on new one
    self.assertEqual(
      setup_invoice_line_list[0].getParentValue().getRelativeUrl(),
      [q.getParentValue().getRelativeUrl() for q in \
        subscription_invoice_line_list \
          if q.getSimulationState() == 'stopped'][0]
    )
    self.assertNotEqual(
      setup_invoice_line_list[0].getParentValue().getRelativeUrl(),
      [q.getParentValue().getRelativeUrl() for q in \
        subscription_invoice_line_list \
          if q.getSimulationState() == 'planned'][0]
    )

    stopped_invoice = setup_invoice_line_list[0].getParentValue()
    planned_invoice = [q.getParentValue() for q in \
      subscription_invoice_line_list \
        if q.getSimulationState() == 'planned'][0]

    # invoices shall be solved
    self.assertEqual('solved', planned_invoice.getCausalityState())
    self.assertEqual('solved', stopped_invoice.getCausalityState())

    # there shall be no payment transaction related to planned invoice
    self.assertEqual([], planned_invoice.getCausalityRelatedList(
      portal_type='Payment Transaction'))

    # there shall be one payment transaction related to stopped invoice
    payment_transaction_list = stopped_invoice.getCausalityRelatedValueList(
      portal_type='Payment Transaction')
    self.assertEqual(1, len(payment_transaction_list))
    payment_transaction = payment_transaction_list[0]

    # this payment transaction shall be planned and solved
    self.assertEqual('planned', payment_transaction.getSimulationState())
    self.assertEqual('solved', payment_transaction.getCausalityState())

    # only this invoice shall be covered by this payment transaction
    self.assertEqual(stopped_invoice.getRelativeUrl(),
      payment_transaction.getCausality())

    # this payment shall fully pay the invoice
    self.assertEqual(stopped_invoice.getTotalPrice(),
      -1 * payment_transaction.PaymentTransaction_getTotalPayablePrice())

    # Stopped invoice shall have no causality
    self.assertEqual(stopped_invoice.getCausalityList(), [])

    # planned invoice shall have no causality
    self.assertEqual(planned_invoice.getCausalityList(), [])

  def stepCheckHostingSubscriptionTwoStoppedInvoiceDocumentCoverage(self,
    sequence, **kw):
    catalog = self.portal.portal_catalog
    hosting_subscription = catalog.getResultValue(
      uid=sequence['hosting_subscription_uid'])
    hosting_subscription_url = hosting_subscription.getRelativeUrl()

    # hosting is confirmed, so no invoice
    hosting_delivery_line_list = catalog(portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['hosting_resource'])

    self.assertEqual(1, len(hosting_delivery_line_list))
    self.assertEqual('confirmed', hosting_delivery_line_list[0]\
      .getSimulationState())

    hosting_invoice_line_list = catalog(portal_type='Invoice Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['hosting_resource'])
    self.assertEqual(0, len(hosting_invoice_line_list))

    # setup is delivered, and has there is invoice
    setup_delivery_line_list = catalog(portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['setup_resource'])

    self.assertEqual(1, len(setup_delivery_line_list))
    self.assertEqual('delivered', setup_delivery_line_list[0]\
      .getSimulationState())

    setup_invoice_line_list = catalog(portal_type='Invoice Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['setup_resource'])
    self.assertEqual(1, len(setup_invoice_line_list))
    self.assertEqual('stopped', setup_invoice_line_list[0]\
      .getSimulationState())

    # there are 10 confirmed and 2 stopped subscription, so 2 invoice line
    subscription_delivery_line_list = catalog(
      portal_type='Sale Packing List Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['subscription_resource'])

    self.assertEqual(2, len(subscription_delivery_line_list))
    self.assertEqual(['stopped'] * 2,
      sorted([q.getSimulationState() for \
      q in subscription_delivery_line_list]))

    subscription_invoice_line_list = catalog(portal_type='Invoice Line',
      aggregate_relative_url=hosting_subscription_url,
      resource_relative_url=sequence['subscription_resource'])
    self.assertEqual(2, len(subscription_invoice_line_list))
    self.assertEqual(['stopped', 'stopped'],
      sorted([q.getSimulationState() for q in subscription_invoice_line_list]))

    # there are three invoice lines, where two share same invoice
    # and other is on other one
    first_invoice = setup_invoice_line_list[0].getParentValue()
    second_invoice = [q.getParentValue() for q in \
      subscription_invoice_line_list \
      if q.getParentValue().getUid() != first_invoice.getUid()][0]

    # invoices shall be solved
    self.assertEqual('solved', first_invoice.getCausalityState())
    self.assertEqual('solved', second_invoice.getCausalityState())

    # both invoice shall have shared payment transaction
    payment_transaction_list = first_invoice.getCausalityRelatedValueList(
      portal_type='Payment Transaction')
    self.assertEqual(1, len(payment_transaction_list))
    payment_transaction = payment_transaction_list[0]
    self.assertEqual([payment_transaction.getRelativeUrl()],
      second_invoice.getCausalityRelatedList(
        portal_type='Payment Transaction'))

    # this payment transaction shall be planned and solved
    self.assertEqual('planned', payment_transaction.getSimulationState())
    self.assertEqual('solved', payment_transaction.getCausalityState())

    # this payment shall fully pay both invoices
    self.assertEqual(
      first_invoice.getTotalPrice() + second_invoice.getTotalPrice(),
      -1 * payment_transaction.PaymentTransaction_getTotalPayablePrice())

    sequence.edit(payment_transaction_uid=payment_transaction.getUid())

  def stepConfirmPayment(self, sequence, **kw):
    self.portal.portal_catalog.getResultValue(
      uid=sequence['payment_transaction_uid']).confirm()

  def stepCheckPayment(self, sequence, **kw):
    payment_transaction = self.portal.portal_catalog.getResultValue(
      uid=sequence['payment_transaction_uid'])
    self.assertEqual('confirmed', payment_transaction.getSimulationState())
    self.assertEqual('solved', payment_transaction.getCausalityState())

  def stepInvoiceSetStartDatePreviousMonth(self, sequence, **kw):
    invoice = self.portal.portal_catalog.getResultValue(
      uid=sequence['invoice_uid'])
    invoice.setStartDate(getClosestDate(target_date=DateTime())-1)

  def test_OpenOrder_sale_packing_list(self):
    """
    Check that sale_packing_list is generated properly from simulation
    """
    sequence_list = SequenceList()
    sequence_string = \
        self.prepare_installed_computer_partition_sequence_string  + \
        """
        LoginDefaultUser
        CallVifibTriggerBuildAlarm
        Tic
        CheckSubscriptionSalePackingListCoverage

        CallVifibTriggerBuildAlarm
        Tic
        CallVifibUpdateDeliveryCausalityStateAlarm
        CleanTic

        # Nothing shall change
        CheckHostingSubscriptionInitialDocumentCoverage

        # Stop first Subscription delivery and after triggering build check
        # that invoice got updated

        SelectNextSubscriptionDelivery
        Tic

        CallVifibTriggerBuildAlarm
        Tic

        CheckHostingSubscriptionStoppedDocumentCoverage

        # proff that alarm will ignore this month invoices
        CallConfirmPlannedSaleInvoiceTransactionAlarm
        Tic
        CallStopConfirmedSaleInvoiceTransactionAlarm
        Tic
        CheckHostingSubscriptionStoppedDocumentCoverage

        LoginERP5TypeTestCase
        CheckSiteConsistency
        Logout
        """

#        # Confirm current invoice and stop next delivery. After triggering build
#        # new planned invoice shall be available.
#
#        SelectPlannedInvoice
#        ConfirmInvoice
#        Tic
#
#         SelectNextSubscriptionDelivery
#         Tic
# 
#         CallVifibTriggerBuildAlarm
#         Tic
# 
#         CheckHostingSubscriptionConfirmedInvoiceDocumentCoverage
# 
#         # Lets check the payment
# 
#         StartInvoice
#         StopInvoice
#         Tic
# 
#         CallVifibTriggerBuildAlarm
#         Tic
# 
#         CheckHostingSubscriptionStoppedInvoiceDocumentCoverage
# 
#         # Proof that alarm is capable to stop previous month invoice
#         SelectPlannedInvoice
#         InvoiceSetStartDatePreviousMonth
#         Tic
#         CallConfirmPlannedSaleInvoiceTransactionAlarm
#         Tic
#         CallStopConfirmedSaleInvoiceTransactionAlarm
#         Tic
# 
#         # Payment should cover both invoices
#         CallVifibTriggerBuildAlarm
#         Tic
# 
#         CheckHostingSubscriptionTwoStoppedInvoiceDocumentCoverage
# 
#         ConfirmPayment
#         Tic
#         CheckPayment
# 
#         """
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestVifibInstanceHostingRelatedDocument))
  return suite
