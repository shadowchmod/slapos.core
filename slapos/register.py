# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 Vifib SARL and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
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


import base64
from getpass import getpass
from optparse import OptionParser, Option
import os
import pkg_resources
import shutil
import sys
import urllib2


class SlapError(Exception):
  """
  Slap error
  """
  def __init__(self, message):
    self.msg = message

class UsageError(SlapError):
  pass

class ExecError(SlapError):
  pass

class Parser(OptionParser):
  """
  Parse all arguments.
  """
  def __init__(self, usage=None, version=None):
    """
    Initialize all options possibles.
    """
    OptionParser.__init__(self, usage=usage, version=version,
                          option_list=[
      Option(None,"--interface-name",
             help="Interface name to access internet",
             default='eth0',
             type=str),
      Option(None,"--master-url",
             help="URL of vifib master",
             default='https://slap.vifib.com',
             type=str),
      Option(None,"--partition-number",
             help="Number of partition on computer",
             default='10',
             type=int),
      Option(None,"--ipv4-local-network",
             help="Base of ipv4 local network",
             default='10.0.0.0/16',
             type=str),
      Option(None,"--ipv6-interface",
             help="Interface name to get ipv6",
             default = '',
             type=str),
      Option("-n", "--dry-run",
             help="Simulate the execution steps",
             default=False,
             action="store_true"),
   ])

  def check_args(self):
    """
    Check arguments
    """
    (options, args) = self.parse_args()
    if len(args) != 1:
      self.error("Incorrect number of arguments")
    node_name = args[0]
    
    if options.ipv6_interface != '' :
      options.ipv6_interface = ('ipv6_interface = ' + options.ipv6_interface)

    return options, node_name


# Get user id and encode it for basic identification
def get_login():
  login = raw_input("""Vifib Login: """)
  password = getpass()
  identification = base64.encodestring('%s:%s' % (login, password))[:-1]
  return identification

# Check if logged correctly on vifib
def check_login(identification):
  check_url = "https://www.vifib.net"
  request = urllib2.Request(check_url)
  # Prepare header for basic authentification
  authheader =  "Basic %s" % identification
  request.add_header("Authorization", authheader)
  home_page_url = urllib2.urlopen(request).read()
  if 'Logout' in home_page_url:
    return 1
  else : return 0
  
# Download certificates on vifib master
def get_certificates(identification,node_name):
  register_server_url = "https://www.vifib.net/add-a-server/WebSection_registerNewComputer?dialog_id=WebSection_viewServerInformationDialog&dialog_method=WebSection_registerNewComputer&title={}&object_path=/erp5/web_site_module/hosting/add-a-server&update_method=&cancel_url=https%3A//www.vifib.net/add-a-server/WebSection_viewServerInformationDialog&Base_callDialogMethod=&field_your_title=Essai1&dialog_category=None&form_id=view".format(node_name)
  request = urllib2.Request(register_server_url)
  # Prepare header for basic authentification
  authheader =  "Basic %s" % identification
  request.add_header("Authorization", authheader)  
  url = urllib2.urlopen(request)  
  page = url.read()
  return page



# Parse html gotten from vifib to make certificate and key files
def parse_certificates(source):
  c_start = source.find("Certificate:")
  c_end = source.find("</textarea>",c_start)
  k_start = source.find("-----BEGIN PRIVATE KEY-----")
  k_end = source.find("</textarea>",k_start)
  return [source[c_start:c_end],source[k_start:k_end]]

# Parse certificate to get computer name and return it
def get_computer_name(certificate):
  k=certificate.find("COMP-")
  i=certificate.find("/email",k)
  return certificate[k:i]

def save_former_config():
  # Check for config file in /etc/slapos/
  if os.path.exists('/etc/slapos/slapos.cfg'):
    former_slapos_configuration='/etc/slapos'
  elif os.path.exists('/etc/opt/slapos/slapos.cfg'): 
    former_slapos_configuration='/etc/opt/slapos'
  else : former_slapos_configuration = 0
  if former_slapos_configuration:
    saved_slapos_configuration = former_slapos_configuration + '.old'
    print "Former slapos configuration detected in %s moving to %s" % (former_slapos_configuration,saved_slapos_configuration)
    # Will remove former .old
    if os.path.exists(saved_slapos_configuration):
      shutil.rmtree(saved_slapos_configuration)
    shutil.move(former_slapos_configuration,saved_slapos_configuration)
    


# Base Function to configure slapos in /etc/opt/slapos
def slapconfig(config):
  dry_run = config.dry_run
  try:    
    # Create slapos configuration directory if needed
    slap_configuration_directory = os.path.normpath(config.slapos_configuration)
    slap_configuration_file = os.path.normpath('/'.join([
        slap_configuration_directory, 'slapos.cfg']))
    if not os.path.exists(slap_configuration_directory):
      print "Creating directory: %s" % slap_configuration_directory
      if not dry_run:
        os.mkdir(slap_configuration_directory, 0711)
    
    user_certificate_repository_path = os.path.join('/'.join([slap_configuration_directory,'ssl']))
    if not os.path.exists(user_certificate_repository_path):
      print "Creating directory: %s" % user_certificate_repository_path
      if not dry_run:
        os.mkdir(user_certificate_repository_path, 0711)
 
    key_file = os.path.join(user_certificate_repository_path, 'key') 
    cert_file = os.path.join(user_certificate_repository_path, 'certificate')
    for (src, dst) in [(config.key, key_file), (config.certificate,
        cert_file)]:
      print "Coping to %r, and setting minimum privileges" % dst
      if not dry_run:
        destination = open(dst,'w')
        destination.write(''.join(src))
        destination.close()
        os.chmod(dst, 0600)
        os.chown(dst, 0, 0)

    certificate_repository_path = os.path.join('/'.join([slap_configuration_directory,'ssl','partition_pki']))
    if not os.path.exists(certificate_repository_path):
      print "Creating directory: %s" % certificate_repository_path
      if not dry_run:
        os.mkdir(certificate_repository_path, 0711)
    
    # Put slapgrid configuration file
    print "Creating slap configuration: %s" % slap_configuration_file
    if not dry_run:
      open(slap_configuration_file, 'w').write(
        pkg_resources.resource_stream(__name__,
                                      'register/templates/slapos.cfg.in').read() % dict(
          computer_id=config.computer_id, master_url=config.master_url,
          key_file=key_file, cert_file=cert_file,
          certificate_repository_path=certificate_repository_path,
          partition_amount=config.partition_number,
          interface=config.interface_name,
          ipv4_network=config.ipv4_local_network,
          ipv6_interface=config.ipv6_interface
          ))
    print "SlapOS configuration: DONE"
  finally:
    return 0

# Class containing all parameters needed for configuration
class Config:
  def setConfig(self, option_dict, node_name):
    """
    Set options given by parameters.
    """
    # Set options parameters
    for option, value in option_dict.__dict__.items():
      setattr(self, option, value)
    self.node_name = node_name

  def COMPConfig(self, slapos_configuration,
                   computer_id,
                   certificate,
                   key):
    self.slapos_configuration= slapos_configuration
    self.computer_id=computer_id
    self.certificate=certificate
    self.key=key

  def displayUserConfig(self):
    print "Computer Name : %s" % self.node_name
    print "Master URL: %s" % self.master_url
    print "Number of partition: %s" % self.partition_number
    print "Interface Name: %s" % self.interface_name
    print "Ipv4 sub network: %s" % self.ipv4_local_network
    print "Ipv6 Interface: %s" %self.ipv6_interface

def register(config):
  # Get User identification and check them 
  while True :
    print ("Please enter your Vifib login")
    user_id = get_login()
    if check_login(user_id): break
    print ("Wrong login/password")  
  # Get source code of page having certificate and key 
  certificate_key = get_certificates(user_id,config.node_name)
  # Parse certificate and key and get computer id
  certificate_key = parse_certificates(certificate_key)
  certificate = certificate_key[0]
  key = certificate_key[1]
  COMP = get_computer_name(certificate)  
  # Getting configuration parameters
  slapos_configuration='/etc/opt/slapos/'
  config.COMPConfig(slapos_configuration=slapos_configuration,
                   computer_id=COMP,
                   certificate = certificate,
                   key = key
                   )
  # Save former configuration
  save_former_config()
  # Prepare Slapos Configuration
  slapconfig(config)


def main():
  "Run default configuration."
  usage = "usage: slapos node %s NODE_NAME [options] " % sys.argv[0]

  try:
    # Parse arguments
    config = Config()
    config.setConfig(*Parser(usage=usage).check_args())
    register(config)
    return_code = 0
  except UsageError, err:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "For help use --help"
    return_code = 16
  except ExecError, err:
    print >>sys.stderr, err.msg
    return_code = 16
  except SystemExit, err:
    # Catch exception raise by optparse
    return_code = err

  sys.exit(return_code)
