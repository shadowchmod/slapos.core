from Products.ERP5Type.tests.Sequence import SequenceList
import unittest
from testVifibSlapWebService import TestVifibSlapWebServiceMixin

class TestVifibSlapSoftwareReleaseDestroyed(TestVifibSlapWebServiceMixin):
  ########################################
  # SoftwareRelease.destroyed
  ########################################

  def test_SoftwareRelease_destroyed_afterRegister(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_formated_computer + '\
      SlapLoginCurrentComputer \
      SelectNewSoftwareReleaseUri \
      CheckNotFoundSoftwareReleaseDestroyedAfterRegisterCall \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_CleanupResource_ConfirmedState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_cleanup_purchase_packing_list + '\
      SlapLoginCurrentComputer \
      CheckSuccessSoftwareReleaseDestroyedCall \
      Tic \
      SlapLogout \
      LoginDefaultUser \
      CheckDeliveredPurchasePackingList \
      CheckSoftwareReleaseUnavailableForRequest \
      CheckSoftwareReleaseNotInPublicTable \
      Logout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_SetupResource_ConfirmedState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_purchase_packing_list + '\
      SlapLoginCurrentComputer \
      CheckNotFoundSoftwareReleaseDestroyedCall \
      Tic \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSoftwareReleaseUnavailableForRequest \
      CheckSoftwareReleaseNotInPublicTable \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_SetupResource_ConfirmedState_CleanupResource_ConfirmedState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_purchase_packing_list + '\
      LoginDefaultUser \
      SetCurrentPurchasePackingListAsA \
      Logout ' + \
      self.prepare_software_release_cleanup_confirmed_packing_list + '\
      LoginDefaultUser \
      CheckSoftwareReleaseUnavailableForRequest \
      CheckSoftwareReleaseNotInPublicTable \
      SetCurrentPurchasePackingListAsB \
      SlapLoginCurrentComputer \
      CheckSuccessSoftwareReleaseDestroyedCall \
      Tic \
      LoginDefaultUser \
      CheckDeliveredPurchasePackingListA \
      CheckDeliveredPurchasePackingListB \
      CheckSoftwareReleaseUnavailableForRequest \
      CheckSoftwareReleaseNotInPublicTable \
      Logout \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_SetupResource_StartedState_CleanupResource_ConfirmedState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_purchase_packing_list + '\
      LoginDefaultUser \
      StartPurchasePackingList \
      Tic \
      CheckSoftwareReleaseUnavailableForRequest \
      CheckSoftwareReleaseNotInPublicTable \
      SetCurrentPurchasePackingListAsA \
      Logout' + \
      self.prepare_software_release_cleanup_confirmed_packing_list + '\
      SetCurrentPurchasePackingListAsB \
      SlapLoginCurrentComputer \
      CheckSuccessSoftwareReleaseDestroyedCall \
      Tic \
      LoginDefaultUser \
      CheckDeliveredPurchasePackingListA \
      CheckDeliveredPurchasePackingListB \
      CheckSoftwareReleaseUnavailableForRequest \
      CheckSoftwareReleaseNotInPublicTable \
      Logout \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_SetupResource_StoppedState_CleanupResource_ConfirmedState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_purchase_packing_list + '\
      LoginDefaultUser \
      StartPurchasePackingList \
      Tic \
      StopPurchasePackingList \
      Tic \
      CheckSoftwareReleaseInPublicTable \
      CheckSoftwareReleaseAvailableForRequest \
      SetCurrentPurchasePackingListAsA \
      Logout' + \
      self.prepare_software_release_cleanup_confirmed_packing_list + '\
      SetCurrentPurchasePackingListAsB \
      SlapLoginCurrentComputer \
      CheckSuccessSoftwareReleaseDestroyedCall \
      Tic \
      LoginDefaultUser \
      CheckDeliveredPurchasePackingListA \
      CheckDeliveredPurchasePackingListB \
      CheckSoftwareReleaseUnavailableForRequest \
      CheckSoftwareReleaseNotInPublicTable \
      Logout \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_SetupResource_DeliveredState_CleanupResource_ConfirmedState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_purchase_packing_list + '\
      LoginDefaultUser \
      StartPurchasePackingList \
      Tic \
      StopPurchasePackingList \
      Tic \
      CheckSoftwareReleaseAvailableForRequest \
      DeliverPurchasePackingList \
      Tic \
      CheckSoftwareReleaseUnavailableForRequest \
      Logout \
      SetCurrentPurchasePackingListAsA \
      Logout' + \
      self.prepare_software_release_cleanup_confirmed_packing_list + '\
      SetCurrentPurchasePackingListAsB \
      SlapLoginCurrentComputer \
      CheckSuccessSoftwareReleaseDestroyedCall \
      Tic \
      LoginDefaultUser \
      CheckDeliveredPurchasePackingListA \
      CheckDeliveredPurchasePackingListB \
      CheckSoftwareReleaseUnavailableForRequest \
      CheckSoftwareReleaseNotInPublicTable \
      Logout \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_SetupResource_CancelledState_CleanupResource_ConfirmedState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_purchase_packing_list + '\
      LoginDefaultUser \
      CancelPurchasePackingList \
      Tic \
      CheckSoftwareReleaseUnavailableForRequest \
      CheckSoftwareReleaseNotInPublicTable \
      SetCurrentPurchasePackingListAsA \
      Logout' + \
      self.prepare_software_release_cleanup_confirmed_packing_list + '\
      SetCurrentPurchasePackingListAsB \
      SlapLoginCurrentComputer \
      CheckSuccessSoftwareReleaseDestroyedCall \
      Tic \
      LoginDefaultUser \
      CheckCancelledPurchasePackingListA \
      CheckDeliveredPurchasePackingListB \
      CheckSoftwareReleaseUnavailableForRequest \
      CheckSoftwareReleaseNotInPublicTable \
      Logout \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_SetupResource_CancelledState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_purchase_packing_list + '\
      LoginDefaultUser \
      CancelPurchasePackingList \
      Tic \
      CheckSoftwareReleaseUnavailableForRequest \
      CheckSoftwareReleaseNotInPublicTable \
      Logout \
      SlapLoginCurrentComputer \
      CheckNotFoundSoftwareReleaseDestroyedCall \
      Tic \
      SlapLogout \
      LoginDefaultUser \
      CheckCancelledPurchasePackingList \
      CheckSoftwareReleaseUnavailableForRequest \
      CheckSoftwareReleaseNotInPublicTable \
      Logout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_CleanupResource_CancelledState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_cleanup_purchase_packing_list + '\
      LoginDefaultUser \
      CancelPurchasePackingList \
      Tic \
      CheckSoftwareReleaseUnavailableForRequest \
      Logout \
      SlapLoginCurrentComputer \
      CheckNotFoundSoftwareReleaseDestroyedCall \
      Tic \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_available_CleanupResource_StartedState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_cleanup_purchase_packing_list + '\
      LoginDefaultUser \
      StartPurchasePackingList \
      Tic \
      CheckSoftwareReleaseUnavailableForRequest \
      Logout \
      SlapLoginCurrentComputer \
      CheckSuccessSoftwareReleaseDestroyedCall \
      Tic \
      SlapLogout \
      LoginDefaultUser \
      CheckDeliveredPurchasePackingList \
      CheckSoftwareReleaseUnavailableForRequest \
      Logout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_SetupResource_StartedState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_purchase_packing_list + '\
      LoginDefaultUser \
      StartPurchasePackingList \
      Tic \
      CheckSoftwareReleaseUnavailableForRequest \
      Logout \
      SlapLoginCurrentComputer \
      CheckNotFoundSoftwareReleaseDestroyedCall \
      Tic \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_CleanupResource_StoppedState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_cleanup_purchase_packing_list + '\
      LoginDefaultUser \
      StartPurchasePackingList \
      StopPurchasePackingList \
      Tic \
      CheckSoftwareReleaseUnavailableForRequest \
      Logout \
      SlapLoginCurrentComputer \
      CheckNotFoundSoftwareReleaseDestroyedCall \
      Tic \
      SlapLogout \
      LoginDefaultUser \
      CheckStoppedPurchasePackingList \
      CheckSoftwareReleaseUnavailableForRequest \
      Logout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_SetupResource_StoppedState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_purchase_packing_list + '\
      LoginDefaultUser \
      StartPurchasePackingList \
      Tic \
      StopPurchasePackingList \
      Tic \
      Logout \
      SlapLoginCurrentComputer \
      CheckNotFoundSoftwareReleaseDestroyedCall \
      Tic \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_CleanupResource_DeliveredState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_cleanup_purchase_packing_list + '\
      LoginDefaultUser \
      StartPurchasePackingList \
      StopPurchasePackingList \
      DeliverPurchasePackingList \
      Tic \
      Logout \
      SlapLoginCurrentComputer \
      CheckNotFoundSoftwareReleaseDestroyedCall \
      Tic \
      SlapLogout \
      LoginDefaultUser \
      CheckDeliveredPurchasePackingList \
      Logout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_SetupResource_DeliveredState(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_software_release_purchase_packing_list + '\
      LoginDefaultUser \
      StartPurchasePackingList \
      Tic \
      StopPurchasePackingList \
      Tic \
      DeliverPurchasePackingList \
      Tic \
      Logout \
      SlapLoginCurrentComputer \
      CheckNotFoundSoftwareReleaseAvailableCall \
      Tic \
      SlapLogout \
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
    '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

  def test_SoftwareRelease_destroyed_twoPurchasePackingList(self):
    sequence_list = SequenceList()
    sequence_string = self.prepare_two_cleanup_purchase_packing_list + '\
      LoginDefaultUser \
      StepPurchasePackingListBStartDateAfterPurchasePackingListA \
      Tic \
      Logout \
      SlapLoginCurrentComputer \
      CheckSuccessSoftwareReleaseDestroyedCall \
      Tic \
      SlapLogout \
      LoginDefaultUser \
      CheckDeliveredPurchasePackingListA \
      CheckDeliveredPurchasePackingListB \
      Logout\
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
      '
    sequence_list.addSequenceString(sequence_string)
    sequence_string = self.prepare_two_cleanup_purchase_packing_list + '\
      LoginDefaultUser \
      StepPurchasePackingListBStartDateBeforePurchasePackingListA \
      Tic \
      Logout \
      SlapLoginCurrentComputer \
      CheckSuccessSoftwareReleaseDestroyedCall \
      Tic \
      SlapLogout \
      LoginDefaultUser \
      CheckDeliveredPurchasePackingListA \
      CheckDeliveredPurchasePackingListB \
      Logout\
      LoginERP5TypeTestCase \
      CheckSiteConsistency \
      Logout \
      '
    sequence_list.addSequenceString(sequence_string)
    sequence_list.play(self)

def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestVifibSlapSoftwareReleaseDestroyed))
  return suite
