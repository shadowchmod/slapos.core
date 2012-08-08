from Products.ERP5Type.tests.Sequence import SequenceList
import unittest
from testVifibSlapWebService import TestVifibSlapWebServiceMixin

class TestVifibSlapComputerPartitionGetState(TestVifibSlapWebServiceMixin):
  ########################################
  # ComputerPartition.getState
  ########################################

  def test_ComputerPartition_getState_emptyPartition(self):
    """
    Check that calling ComputerPartition.getState after just 
    registration raises a NotFoundError
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_formated_computer + '\
      SlapLoginCurrentComputer \
      CheckDestroyedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_SetupResource_ConfirmedState(self):
    """
    Check that calling ComputerPartition.getState works in 
    confirmed state with the setup resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_SetupResource_CancelledState(self):
    """
    Check that calling ComputerPartition.getState works in 
    cancelled state with the setup resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
      LoginDefaultUser \
      SelectCurrentlyUsedSalePackingListUid \
      CancelSalePackingList \
      Tic \
      Logout \
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_SetupResource_StartedState(self):
    """
    Check that calling ComputerPartition.getState works in 
    started state with the setup resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_building_computer_partition_sequence_string + '\
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_SetupResource_StoppedState(self):
    """
    Check that calling ComputerPartition.getState works in 
    stopped state with the setup resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_stopped_computer_partition_sequence_string + '\
      SlapLoginCurrentComputer \
      CheckStoppedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_SetupResource_DeliveredState(self):
    """
    Check that calling ComputerPartition.getState works in 
    delivered state with the setup resource
    """
    sequence_list = SequenceList()

    sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
      LoginTestVifibCustomer \
      SetSequenceSoftwareInstanceStateStopped \
      PersonRequestSoftwareInstance \
      Tic \
      Logout \
      LoginDefaultUser \
      CheckComputerPartitionInstanceSetupSalePackingListDelivered \
      Logout \
      SlapLoginCurrentComputer \
      CheckStoppedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_HostingResource_ConfirmedState(self):
    """
    Check that calling ComputerPartition.getState works in 
    confirmed state with the hosting resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_start_requested_computer_partition_sequence_string + '\
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_HostingResource_CancelledState(self):
    """
    Check that calling ComputerPartition.getState works in 
    cancelled state with the hosting resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_start_requested_computer_partition_sequence_string + '\
      LoginDefaultUser \
      SelectCurrentlyUsedSalePackingListUid \
      CancelSalePackingList \
      Tic \
      Logout \
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_HostingResource_StartedState(self):
    """
    Check that calling ComputerPartition.getState works in 
    started state with the hosting resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_started_computer_partition_sequence_string + '\
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_HostingResource_StoppedState(self):
    """
    Check that calling ComputerPartition.getState works in 
    stopped state with the hosting resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_stop_requested_computer_partition_sequence_string + '\
      SlapLoginCurrentComputer \
      CheckStoppedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_HostingResource_DeliveredState(self):
    """
    Check that calling ComputerPartition.getState works in 
    delivered state with the hosting resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_stopped_computer_partition_sequence_string + '\
      SlapLoginCurrentComputer \
      CheckStoppedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_CleanupResource_ConfirmedState(self):
    """
    Check that calling ComputerPartition.getState works in 
    confirmed state with the cleanup resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_destroy_requested_computer_partition + '\
      SlapLoginCurrentComputer \
      CheckDestroyedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_CleanupResource_CancelledState(self):
    """
    Check that calling ComputerPartition.getState works in 
    cancelled state with the cleanup resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_destroy_requested_computer_partition + '\
      LoginDefaultUser \
      SelectCurrentlyUsedSalePackingListUid \
      CancelSalePackingList \
      Logout \
      SlapLoginCurrentComputer \
      CheckDestroyedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_CleanupResource_StartedState(self):
    """
    Check that calling ComputerPartition.getState works in 
    started state with the cleanup resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_destroy_requested_computer_partition + '\
      LoginDefaultUser \
      SelectCurrentlyUsedSalePackingListUid \
      StartSalePackingList \
      Tic \
      Logout \
      SlapLoginCurrentComputer \
      CheckDestroyedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_CleanupResource_StoppedState(self):
    """
    Check that calling ComputerPartition.getState works in 
    stopped state with the cleanup resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_destroy_requested_computer_partition + '\
      LoginDefaultUser \
      SelectCurrentlyUsedSalePackingListUid \
      StartSalePackingList \
      StopSalePackingList \
      Tic \
      Logout \
      SlapLoginCurrentComputer \
      CheckDestroyedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_CleanupResource_DeliveredState(self):
    """
    Check that calling ComputerPartition.getState works in
    delivered state with the cleanup resource
    """
    sequence_list = SequenceList()
    sequence_string = self\
        .prepare_destroyed_computer_partition + '\
      SlapLoginCurrentComputer \
      CheckDestroyedComputerPartitionGetStateCall \
      SlapLoginCurrentComputer \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_AccountingResource_ConfirmedState(self):
    """
    Check that calling ComputerPartition.getState works in 
    confirmed state with the accounting resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_computer_partition_accounting_resource_sequence_string + '\
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_AccountingResource_CancelledState(self):
    """
    Check that calling ComputerPartition.getState works in 
    cancelled state with the accounting resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_computer_partition_accounting_resource_sequence_string + '\
      LoginDefaultUser \
      CancelSalePackingList \
      Tic \
      Logout \
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_AccountingResource_StartedState(self):
    """
    Check that calling ComputerPartition.getState works in 
    started state with the accounting resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_computer_partition_accounting_resource_started_sequence_string + '\
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_AccountingResource_StoppedState(self):
    """
    Check that calling ComputerPartition.getState works in 
    stopped state with the accounting resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_computer_partition_accounting_resource_stopped_sequence_string + '\
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_AccountingResource_DeliveredState(self):
    """
    Check that calling ComputerPartition.getState works in 
    delivered state with the accounting resource
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_computer_partition_accounting_resource_delivered_sequence_string + '\
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_ComputerPartition_getState_twoSalePackingList(self):
    """
    Check that calling ComputerPartition.getState uses the latest sale packing
    list for calculation
    """
    sequence_list = SequenceList()
    sequence_string = self.prepare_started_computer_partition_sequence_string + '\
      LoginDefaultUser \
      CheckPackingListAmountTwoComputerPartition \
      SetHostingBeforeSetupStartDate \
      Tic \
      Logout \
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginDefaultUser \
      SetHostingAfterSetupStartDate \
      Tic \
      Logout \
      SlapLoginCurrentComputer \
      CheckStartedComputerPartitionGetStateCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestVifibSlapComputerPartitionGetState))
  return suite
