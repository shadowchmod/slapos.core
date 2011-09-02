import unittest
from testVifibSlapWebService import TestVifibSlapWebServiceMixin

class TestVifibSlapOpenOrderRequest(TestVifibSlapWebServiceMixin):

  ########################################
  # OpenOrder.request
  ########################################

# LoginTestVifibDeveloper
# SelectNewSoftwareReleaseUri
# CreateSoftwareRelease
# Tic
# SubmitSoftwareRelease
# Tic
# CreateSoftwareProduct
# Tic
# ValidateSoftwareProduct
# Tic
# SetSoftwareProductToSoftwareRelease
# PublishByActionSoftwareRelease
# Logout
# LoginTestVifibAdmin
# CreateComputer
# Tic
# Logout
# SlapLoginCurrentComputer
# FormatComputer
# Tic
# SlapLogout
# LoginTestVifibAdmin
# RequestSoftwareInstallation
# Tic
# Logout
# SlapLoginCurrentComputer
# ComputerSoftwareReleaseAvailable
# Tic
# SlapLogout
# 
#   def test_OpenOrder_request_noFreePartition(self):
#     """
#     Check that first call to request raises NotReady response
#     """
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
#       LoginTestVifibCustomer
#       RequestOpenOrderNotFoundResponse \
#     '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)




















#   def test_OpenOrder_request_firstNotReady(self):
#     """
#     Check that first call to request raises NotReady response
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrderNotReadyResponse \
#       SlapLogout \
#     '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   # XXX: This test fails because test_vifib_customer security is cached
#   #      and this user is not in SOFTINST-x group. We do not want to clear
#   #      cache in tests.
#   @expectedFailure
#   def test_OpenOrder_request_noParameterInRequest(self):
#     """
#     Check that it is possible to request another Computer Partition
#     from existing one, without passing any parameters and that in such case
#     original's Sofware Instance parameters will be passed.
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrderNotReadyResponse \
#       Tic \
#       SlapLogout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrder \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckSoftwareInstanceAndRelatedOpenOrder \
#       CheckRequestedSoftwareInstanceAndRelatedOpenOrder \
#       Logout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       CheckRequestedOpenOrderCleanParameterList \
#       SlapLogout \
#       \
#       LoginTestVifibCustomer \
#       CheckViewCurrentSoftwareInstance \
#       CheckWriteCurrentSoftwareInstance \
#       Tic \
#       CheckViewRequestedSoftwareInstance \
#       CheckWriteRequestedSoftwareInstance \
#       Tic \
#       Logout \
#     '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_instantiate(self):
#     """
#     Check that after computer partition is requested it is possible to
#     instantiate it and it is started correctly.
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrderNotReadyResponse \
#       Tic \
#       SlapLogout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrder \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckSoftwareInstanceAndRelatedOpenOrder \
#       CheckRequestedSoftwareInstanceAndRelatedOpenOrder \
#       Logout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       CheckRequestedOpenOrderCleanParameterList \
#       Logout \
#       \
#       LoginDefaultUser \
#       SetCurrentSoftwareInstanceRequested \
#       SetSelectedOpenOrder \
#       SelectCurrentlyUsedSalePackingListUid \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceBuilding \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceSetupSalePackingListStarted \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceAvailable \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceSetupSalePackingListStopped \
#       CheckOpenOrderInstanceHostingSalePackingListConfirmed \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceStarted \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceHostingSalePackingListStarted \
#       Logout \
#       '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def stepSetInstanceStateStopped(self, sequence=None, **kw):
#     sequence['instance_state'] = 'stopped'
# 
#   def test_OpenOrder_request_instantiate_state_stopped(self):
#     """
#     Check that after computer partition is requested it is possible to
#     instantiate it and it is stopped correctly, as requested initally.
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
#       SetInstanceStateStopped \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrderNotReadyResponse \
#       Tic \
#       SlapLogout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrder \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckSoftwareInstanceAndRelatedOpenOrder \
#       CheckRequestedSoftwareInstanceAndRelatedOpenOrder \
#       Logout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       CheckRequestedOpenOrderCleanParameterList \
#       Logout \
#       \
#       LoginDefaultUser \
#       SetCurrentSoftwareInstanceRequested \
#       SetSelectedOpenOrder \
#       SelectCurrentlyUsedSalePackingListUid \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceBuilding \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceSetupSalePackingListStarted \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceAvailable \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceSetupSalePackingListStopped \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceStopped \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       stepCheckOpenOrderNoInstanceHostingSalePackingList \
#       Logout \
#       '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_instantiate_stop_later(self):
#     """
#     Check that after computer partition is requested it is possible to
#     instantiate it and it is started correctly, and later it is stopped
#     correctly as requested.
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrderNotReadyResponse \
#       Tic \
#       SlapLogout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrder \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckSoftwareInstanceAndRelatedOpenOrder \
#       CheckRequestedSoftwareInstanceAndRelatedOpenOrder \
#       Logout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       CheckRequestedOpenOrderCleanParameterList \
#       Logout \
#       \
#       LoginDefaultUser \
#       SetCurrentSoftwareInstanceRequested \
#       SetSelectedOpenOrder \
#       SelectCurrentlyUsedSalePackingListUid \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceBuilding \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceSetupSalePackingListStarted \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceAvailable \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceSetupSalePackingListStopped \
#       CheckOpenOrderInstanceHostingSalePackingListConfirmed \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceStarted \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceHostingSalePackingListStarted \
#       Logout \
#       \
#       SetInstanceStateStopped \
#       \
#       LoginDefaultUser \
#       SetCurrentSoftwareInstanceRequester \
#       SetSelectedOpenOrder \
#       SelectCurrentlyUsedSalePackingListUid \
#       Logout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrder \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       SetCurrentSoftwareInstanceRequested \
#       SetSelectedOpenOrder \
#       SelectCurrentlyUsedSalePackingListUid \
#       CheckOpenOrderInstanceHostingSalePackingListStopped \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceStopped \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceHostingSalePackingListDelivered \
#       Logout \
#       \
#       '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_state_is_optional(self):
#     """Checks that state is optional parameter on Slap Tool
#     
#     This ensures backward compatibility with old libraries."""
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = \
#       self.prepare_install_requested_computer_partition_sequence_string + '\
#       SlapLoginCurrentSoftwareInstance \
#       DirectRequestOpenOrderNotReadyResponseWithoutState \
#       Tic \
#       SlapLogout \
#       \
#       '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   # XXX: This test fails because test_vifib_customer security is cached
#   #      and this user is not in SOFTINST-x group. We do not want to clear
#   #      cache in tests.
#   @expectedFailure
#   def test_OpenOrder_request_instantiateStop(self):
#     """
#     Check that after computer partition is requested it is possible to
#     instantiate it and stop.
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrderNotReadyResponse \
#       Tic \
#       SlapLogout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrder \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckSoftwareInstanceAndRelatedOpenOrder \
#       CheckRequestedSoftwareInstanceAndRelatedOpenOrder \
#       Logout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       CheckRequestedOpenOrderCleanParameterList \
#       Logout \
#       \
#       LoginDefaultUser \
#       SetCurrentSoftwareInstanceRequested \
#       SetSelectedOpenOrder \
#       SelectCurrentlyUsedSalePackingListUid \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceBuilding \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceSetupSalePackingListStarted \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceAvailable \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceSetupSalePackingListStopped \
#       CheckOpenOrderInstanceHostingSalePackingListConfirmed \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceStarted \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceHostingSalePackingListStarted \
#       Logout \
#       \
#       LoginTestVifibCustomer \
#       RequestSoftwareInstanceStop \
#       Tic \
#       Logout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceHostingSalePackingListStopped \
#       Logout \
#       \
#       SlapLoginCurrentComputer \
#       SoftwareInstanceStopped \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckOpenOrderInstanceHostingSalePackingListDelivered \
#       Logout \
#       '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_parameterInRequest(self):
#     """
#     Check that it is possible to request another Computer Partition
#     from existing one, with passing parameters and that in such case all
#     passed parameters are available on new Computer Partition and no
#     parameters are copied.
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
#       SelectRequestedReference \
#       SelectRequestedParameterDictRequestedParameter \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrderNotReadyResponse \
#       Tic \
#       RequestOpenOrder \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckSoftwareInstanceAndRelatedOpenOrder \
#       CheckRequestedSoftwareInstanceAndRelatedOpenOrder \
#       Logout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       CheckRequestedOpenOrderRequestedParameter \
#       SlapLogout \
#     '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_twiceSameSourceSameResult(self):
#     """
#     Checks that requesting twice with same arguments from same Computer Partition
#     will return same object."""
#     self.computer_partition_amount = 3
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
#       SelectRequestedReference \
#       SelectEmptyRequestedParameterDict \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrderNotReadyResponse \
#       Tic \
#       RequestOpenOrder \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckSoftwareInstanceAndRelatedOpenOrder \
#       CheckRequestedSoftwareInstanceAndRelatedOpenOrder \
#       Logout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       CheckRequestedOpenOrderCleanParameterList \
#       SlapLogout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrder \
#       Tic \
#       SlapLogout \
#       \
#       LoginDefaultUser \
#       CheckSoftwareInstanceAndRelatedOpenOrder \
#       CheckRequestedSoftwareInstanceAndRelatedOpenOrder \
#       Logout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       CheckRequestedOpenOrderCleanParameterList \
#       SlapLogout \
#     '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_twiceDifferentParent(self):
#     """
#     Checks that requesting twice with same arguments from different Computer
#     Partition will return same object.
# 
#     This test is reproducing scenario:
# 
#             Master
#           /       \
#     ChildrenA   ChildrenB
#           \
#       ChildrenRequestedTwice
# 
#     Then ChildrenB requests ChildrenRequestedTwice, so graph changes to:
# 
#             Master
#           /       \
#     ChildrenA   ChildrenB
#                   /
#       ChildrenRequestedTwice
#     """
#     self.computer_partition_amount = 4
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_children_a_children_b_sequence_string + """
#       # Generate first part of graph
#       #            Master
#       #          /       \
#       #    ChildrenA   ChildrenB
#       #          \
#       #      ChildrenRequestedTwice
# 
#       LoginDefaultUser
#       SetSoftwareInstanceChildrenA
#       SelectRequestedReference
#       SelectEmptyRequestedParameterDict
#       Logout
# 
#       SlapLoginCurrentSoftwareInstance
#       RequestOpenOrderNotReadyResponse
#       Tic
#       RequestOpenOrder
#       Tic
#       SlapLogout
# 
#       LoginDefaultUser
#       SetRequestedOpenOrder
#       CheckOpenOrderChildrenA
#       CheckOpenOrderChildrenBNoChild
#       CheckOpenOrderRequestedDoubleScenarioChildrenA
#       Logout
# 
#       # Generate second part of graph
#       #            Master
#       #          /       \
#       #    ChildrenA   ChildrenB
#       #                  /
#       #      ChildrenRequestedTwice
# 
#       LoginDefaultUser
#       SetRequestedOpenOrder
#       SetSoftwareInstanceChildrenB
#       SelectRequestedReference
#       SelectEmptyRequestedParameterDict
#       Logout
# 
#       SlapLoginCurrentSoftwareInstance
#       RequestOpenOrderNotReadyResponse
#       Tic
#       RequestOpenOrder
#       Tic
#       SlapLogout
# 
#       LoginDefaultUser
#       SetRequestedOpenOrder
#       CheckOpenOrderChildrenANoChild
#       CheckOpenOrderChildrenB
#       CheckOpenOrderRequestedDoubleScenarioChildrenB
#       Logout
#     """
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   # Marked as expectedFailure as implementation is not ready yet
#   @expectedFailure
#   def test_OpenOrder_request_twiceDifferentParentWithoutTic(self):
#     """
#     Checks that requesting twice with same arguments from different Computer
#     Partition will return same object.
# 
#     This test is reproducing scenario:
# 
#             Master
#           /       \
#     ChildrenA   ChildrenB
#           \
#       ChildrenRequestedTwice
# 
#     Then ChildrenB requests ChildrenRequestedTwice, so graph changes to:
# 
#             Master
#           /       \
#     ChildrenA   ChildrenB
#                   /
#       ChildrenRequestedTwice
# 
#     Case without tic between requests.
#     """
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_children_a_children_b_sequence_string + """
#       SelectRequestedReference
#       SelectEmptyRequestedParameterDict
# 
#       SetSoftwareInstanceChildrenA
#       RequestOpenOrderNotReadyResponse
# 
#       SetSoftwareInstanceChildrenB
#       RequestOpenOrderNotReadyResponse
# 
#       Tic
# 
#       SetSoftwareInstanceChildrenA
#       RequestOpenOrder
#       Tic
# 
#       SetSoftwareInstanceChildrenB
#       RequestOpenOrder
#       Tic
#       SetRequestedOpenOrder
#       CheckOpenOrderChildrenA
#       CheckOpenOrderChildrenB
#       CheckOpenOrderRequestedDoubleScenario
#     """
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_differentSourceDifferentResultWithTic(self):
#     """
#     Check that requesting different Computer Partitions from different sources
#     gives different result, because they are requesting different
#     partition_reference.
# 
#     This test is reproducing scenario:
#             Master
#           /       \
#     ChildrenA   ChildrenB
#         |           |
#     ChildChildA  ChildChildB
#     """
#     self.computer_partition_amount = 5
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_children_a_children_b_sequence_string + """
#       # Request ChildChildrenA
#       LoginDefaultUser
#       SetSoftwareInstanceChildrenA
#       SelectRequestedReferenceChildrenAChild
#       SelectEmptyRequestedParameterDict
#       Logout
# 
#       SlapLoginCurrentSoftwareInstance
#       RequestOpenOrderNotReadyResponse
#       Tic
#       RequestOpenOrder
#       Tic
#       SlapLogout
# 
#       LoginDefaultUser
#       SetChildrenAChildOpenOrder
# 
#       # Request ChilChildrenB
#       SetSoftwareInstanceChildrenB
#       SelectRequestedReferenceChildrenBChild
#       SelectEmptyRequestedParameterDict
#       Logout
# 
#       SlapLoginCurrentSoftwareInstance
#       RequestOpenOrderNotReadyResponse
#       Tic
#       RequestOpenOrder
#       Tic
#       SlapLogout
# 
#       LoginDefaultUser
#       SetChildrenBChildOpenOrder
#       # Do assertions
#       CheckOpenOrderChildrenAWithOwnChildren
#       CheckOpenOrderChildrenBWithOwnChildren
#       CheckOpenOrderChildrenAChild
#       CheckOpenOrderChildrenBChild
#       Logout
#     """
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   # Marked as expectedFailure as implementation is not ready yet
#   @expectedFailure
#   def test_OpenOrder_request_differentSourceDifferentResultWithoutTic(
#       self):
#     """
#     Check that requesting different Computer Partitions from different sources
#     gives different result, because they are requesting different
#     partition_reference.
# 
#     This test is reproducing scenario:
#             Master
#           /       \
#     ChildrenA   ChildrenB
#         |           |
#     ChilChildA  ChildChildB
# 
#     Case without tic between requests.
#     """
#     self.computer_partition_amount = 5
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_children_a_children_b_sequence_string + """
#       LoginDefaultUser
#       SetSoftwareInstanceChildrenA
#       SelectRequestedReferenceChildrenAChild
#       SelectEmptyRequestedParameterDict
#       Logout
# 
#       SlapLoginCurrentSoftwareInstance
#       RequestOpenOrderNotReadyResponse
#       RequestOpenOrder
#       Tic
#       SlapLogout
# 
#       LoginDefaultUser
#       SetChildrenAChildOpenOrder
# 
#       SetSoftwareInstanceChildrenB
#       SelectRequestedReferenceChildrenBChild
#       SelectEmptyRequestedParameterDict
#       Logout
# 
#       SlapLoginCurrentSoftwareInstance
#       RequestOpenOrderNotReadyResponse
#       RequestOpenOrder
#       Tic
#       SlapLogout
# 
#       LoginDefaultUser
#       SetChildrenBChildOpenOrder
# 
#       CheckOpenOrderChildrenAWithOwnChildren
#       CheckOpenOrderChildrenBWithOwnChildren
#       CheckOpenOrderChildrenAChild
#       CheckOpenOrderChildrenBChild
#       Logout
#     """
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_serialiseIsCalled(self):
#     """
#     Check that during OpenOrder.request serialise is being called
#     on being choosen Computer Partition.
# 
#     Serialize call is used to protect Computer Partition from being selected
#     as free in case of concurrency connections.
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
#       LoginDefaultUser \
#       SelectRequestedReferenceChildrenA \
#       SelectEmptyRequestedParameterDict \
#       RequestComputerOpenOrderCheckSerializeCalledOnSelected \
#       SlapLogout \
#     '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   ########################################
#   # OpenOrder.request - filter - computer_guid
#   ########################################
#   def test_OpenOrder_request_filter_computer_guid(self):
#     """
#     Check that requesting with filter computer_guid key works as expected
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     # There are two partitions on another computer
#     # so request shall be processed twice correctly, 3rd time it shall
#     # fail
#     sequence_string = \
#     self.prepare_install_requested_computer_partition_sequence_string + \
#       self.prepare_another_computer_sequence_string + '\
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrderNotReadyResponse \
#       Tic \
#       SlapLogout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrder \
#       Tic \
#       SlapLogout \
#       \
#       SelectAnotherRequestedReference \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrderNotReadyResponse \
#       Tic \
#       SlapLogout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrder \
#       Tic \
#       SlapLogout \
#       \
#       SelectYetAnotherRequestedReference \
#       SlapLoginCurrentSoftwareInstance \
#       RequestOpenOrderNotFoundResponse \
#       Tic \
#       SlapLogout \
#       '
# 
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   ########################################
#   # OpenOrder.request - slave
#   ########################################
#   def test_OpenOrder_request_slave_firstNotReady(self):
#     """
#     Check that first call to request raises NotReadyResponse
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_install_requested_computer_partition_sequence_string + '\
#        SlapLoginCurrentSoftwareInstance \
#        SelectEmptyRequestedParameterDict \
#        SetRandomRequestedReference \
#        RequestSlaveInstanceFromOpenOrderNotReadyResponse \
#        SlapLogout \
#     '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_slave_simpleCase(self):
#     """
#     Check the most simple case of request. The behaviour should
#     keep the same as Software Instance.
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = \
#       self.prepare_install_requested_computer_partition_sequence_string +\
#       """
#        SlapLoginCurrentSoftwareInstance
#        SelectEmptyRequestedParameterDict \
#        SetRandomRequestedReference \
#        RequestSlaveInstanceFromOpenOrderNotReadyResponse \
#        Tic \
#        SlapLogout \
#        \
#        SlapLoginCurrentSoftwareInstance \
#        RequestSlaveInstanceFromOpenOrder \
#        Tic \
#        SlapLogout
#        LoginDefaultUser
#        ConfirmOrderedSaleOrderActiveSense
#        Tic
#        SlapLoginCurrentComputer
#        CheckSlaveInstanceListFromOneOpenOrder
#        SlapLogout
#       """
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_slave_instantiate(self):
#     """
#       Check that one Slave Instance is instantiate correctly and the validate
#       the Sale Packing List states
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = \
#       self.prepare_install_requested_computer_partition_sequence_string +\
#       """
#        SlapLoginCurrentSoftwareInstance
#        SelectEmptyRequestedParameterDict
#        SetRandomRequestedReference
#        RequestSlaveInstanceFromOpenOrderNotReadyResponse
#        Tic
#        SlapLogout
# 
#        SlapLoginCurrentSoftwareInstance
#        RequestSlaveInstanceFromOpenOrder
#        Tic
#        SlapLogout
#        LoginDefaultUser
#        ConfirmOrderedSaleOrderActiveSense
# 
#        Tic
#        SlapLoginCurrentSoftwareInstance
#        CheckSlaveInstanceListFromOneOpenOrder
#        SelectSlaveInstanceFromOneOpenOrder
#        SlapLogout
# 
#        LoginDefaultUser
#        SetDeliveryLineAmountEqualTwo
#        CheckOpenOrderInstanceSetupSalePackingListConfirmed
#        SlapLogout
# 
#        SlapLoginCurrentComputer
#        SoftwareInstanceAvailable
#        Tic
#        SlapLogout
# 
#        LoginDefaultUser \
#        CheckOpenOrderInstanceSetupSalePackingListStopped
#        CheckOpenOrderInstanceHostingSalePackingListConfirmed
#        Logout
# 
#        SlapLoginCurrentComputer \
#        SoftwareInstanceStarted \
#        Tic \
#        SlapLogout \
#        \
#        LoginDefaultUser \
#        CheckOpenOrderInstanceHostingSalePackingListStarted \
#        Logout \
#       """
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_slave_same_twice_SR(self):
#     """
#       Check that requesting the same slave instance twice, only one is created
#     """
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = \
#         self.prepare_install_requested_computer_partition_sequence_string +\
#         """
#          SlapLoginCurrentSoftwareInstance
#          SelectEmptyRequestedParameterDict
#          SelectRequestedReference
#          RequestSlaveInstanceFromOpenOrderNotReadyResponse
#          Tic
#          SlapLogout
#          
#          SlapLoginCurrentSoftwareInstance \
#          RequestSlaveInstanceFromOpenOrder \
#          Tic
#          SlapLogout
#          LoginDefaultUser
#          ConfirmOrderedSaleOrderActiveSense
#          Tic
#          SlapLoginCurrentComputer
#          CheckSlaveInstanceListFromOneOpenOrder
#          SlapLogout
# 
#          SlapLoginCurrentSoftwareInstance \
#          RequestSlaveInstanceFromOpenOrder \
#          Tic
#          SlapLogout
#          LoginDefaultUser
#          ConfirmOrderedSaleOrderActiveSense
#          Tic
#          SlapLoginCurrentComputer
#          CheckSlaveInstanceListFromOneOpenOrder
#          SlapLogout
#         """
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_slave_after_destroy_SlaveInstance(self):
#     """
#       Check that a Slave Instance will not be allocated when a Software
#       Instance is destroyed
#     """
#     sequence_list = SequenceList()
#     sequence_string = \
#       self.prepare_installed_computer_partition_sequence_string + """
#         LoginTestVifibCustomer
#         RequestSoftwareInstanceDestroy
#         Tic
#         SlapLogout
#         LoginDefaultUser
#         CheckOpenOrderInstanceCleanupSalePackingListConfirmed
#         SlapLogout
#         SlapLoginCurrentSoftwareInstance
#         SelectEmptyRequestedParameterDict
#         SelectRequestedReference
#         RequestSlaveInstanceFromOpenOrderNotFoundError
#         Tic
#         RequestSlaveInstanceFromOpenOrderNotFoundError
#       """
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_slave_twice_different(self):
#     """
#      Check request 2 different slave instances on same Software 
#      Instance.
#     """
#     simple_request_with_random = """
#          SlapLoginCurrentSoftwareInstance
#          SelectEmptyRequestedParameterDict \
#          SetRandomRequestedReference \
#          RequestSlaveInstanceFromOpenOrderNotReadyResponse \
#          Tic \
#          SlapLogout \
#          \
#          SlapLoginCurrentSoftwareInstance \
#          RequestSlaveInstanceFromOpenOrder \
#          Tic \
#          SlapLogout
#          LoginDefaultUser
#          ConfirmOrderedSaleOrderActiveSense
#          Tic
#          """
# 
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = \
#         self.prepare_install_requested_computer_partition_sequence_string +\
#         simple_request_with_random + """
#           SlapLoginCurrentComputer
#           CheckSlaveInstanceListFromOneOpenOrder
#           SlapLogout
#         """ + \
#         simple_request_with_random + \
#         """
#         SlapLoginCurrentComputer
#         CheckTwoSlaveInstanceListFromOneOpenOrder
#         SlapLogout
#         """
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_slave_NotFound(self):
#     """
#     Check that requesting a Slave Instance works in system capable to fulfill
#     such request, when Software Instance is not installed yet.
#     """
#     sequence_list = SequenceList()
#     sequence_string = self.prepare_formated_computer + """
#         LoginDefaultUser
#         SetRandomOpenOrder
#         SlapLoginCurrentComputer
#         SelectEmptyRequestedParameterDict
#         SetRandomRequestedReference
#         SelectNewSoftwareReleaseUri
#         RequestSlaveInstanceFromOpenOrderNotFoundError
#         SlapLogout
#       """
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def test_OpenOrder_request_slave_state_is_optional(self):
#     """Checks that state is optional parameter on Slap Tool This ensures
#     backward compatibility with old libraries."""
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     sequence_string = \
#       self.prepare_install_requested_computer_partition_sequence_string + '\
#       SlapLoginCurrentSoftwareInstance \
#       DirectRequestOpenOrderNotReadyResponseWithoutStateAndSharedTrue \
#       Tic \
#       SlapLogout \
#       '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)
# 
#   def stepSetRequestedWrongFilterParameterDict(self, sequence):
#         sequence['requested_filter_dict'] = dict(
#           computer_guid="COMP-99999999999999999999999")
# 
#   def test_OpenOrder_request_filter_slave_computer_guid(self):
#     """Check that requesting with filter computer_guid key works as expected.
# 
#     This include tests for slave instance case."""
#     self.computer_partition_amount = 2
#     sequence_list = SequenceList()
#     # There are two partitions on another computer
#     # so request shall be processed twice correctly, 3rd time it shall
#     # fail
#     sequence_string = \
#     self.prepare_install_requested_computer_partition_sequence_string + \
#       self.prepare_another_computer_sequence_string + '\
#       SelectAnotherRequestedReference \
#       SelectEmptyRequestedParameterDict \
#       SlapLoginCurrentSoftwareInstance \
#       RequestSlaveInstanceFromOpenOrderNotFoundError \
#       Tic \
#       SlapLogout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       SetRequestedFilterParameterDict \
#       RequestSlaveInstanceFromOpenOrderNotReadyResponse \
#       Tic \
#       SlapLogout \
#       \
#       SlapLoginCurrentSoftwareInstance \
#       RequestSlaveInstanceFromOpenOrder \
#       Tic \
#       SlapLogout \
#       \
#       SetRequestedWrongFilterParameterDict \
#       SelectYetAnotherRequestedReference \
#       SlapLoginCurrentSoftwareInstance \
#       RequestSlaveInstanceFromOpenOrderNotFoundError \
#       Tic \
#       SlapLogout \
#       '
#     sequence_list.addSequenceString(sequence_string)
#     sequence_list.play(self)

def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestVifibSlapOpenOrderRequest))
  return suite
