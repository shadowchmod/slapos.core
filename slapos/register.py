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


import os
import shutil
import sys
import urllib2
import base64
import pkg_resources
from getpass import getpass


# Utility fonction to get yes/no answers
def get_yes_no (prompt):
  ok= 0
  while not ok:
    answer=raw_input( prompt + " [y,n]: " )
    if answer.upper() in [ 'Y','YES' ]: return True
    if answer.upper() in [ 'N', 'NO' ]: return False


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
def get_certificates(identification):
  server_name = raw_input ("Please enter a unique computer name: ")
  register_server_url = "https://www.vifib.net/add-a-server/WebSection_registerNewComputer?dialog_id=WebSection_viewServerInformationDialog&dialog_method=WebSection_registerNewComputer&title={}&object_path=/erp5/web_site_module/hosting/add-a-server&update_method=&cancel_url=https%3A//www.vifib.net/add-a-server/WebSection_viewServerInformationDialog&Base_callDialogMethod=&field_your_title=Essai1&dialog_category=None&form_id=view".format(server_name)
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

    certificate_repository_path = os.path.join('/'.join([slap_configuration_directory,'ssl']))
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
          partition_amount=config.partition_amount,
          interface=config.interface,
          ipv4_network=config.ipv4_network
          ))
    print "SlapOS configuration: DONE"
  finally:
    return 0

# Class containing all parameters needed for configuration
class Config:
  def setConfig(self,slapos_configuration,
                dry_run,
                computer_id, master_url, interface,
                ipv4_network,
                certificate, key):
    """
    Set options given by parameters.
    """
    self.slapos_configuration = slapos_configuration
    self.dry_run = dry_run
    self.computer_id = computer_id
    self.master_url = master_url
    self.interface = interface
    self.ipv4_network = ipv4_network
    self.certificate = certificate
    self.key = key

  def userConfig(self):
    self.master_url = raw_input("""Master URL [%s] :""" %self.master_url) or self.master_url
    self.partition_amount = raw_input("""Number of SlapOS partitions for this computer? """)
    self.interface = "interface_name = "+ ''.join(raw_input("""Name of interface used to access internet [%s] :""" % self.interface) or self.interface)
    self.ipv4_network = raw_input("Ipv4 sub-network [%s] :" % self.ipv4_network) or self.ipv4_network

  def displayUserConfig(self):
    print "Computer reference : %s" % self.computer_id
    print "Master URL: %s" % self.master_url
    print "Number of partition: %s" % self.partition_amount
    print "%s" % self.interface
    print "Ipv4 sub network: %s" % self.ipv4_network



def register():
  # Get User identification and check them 
  while True :
    print ("Please enter your Vifib login")
    user_id = get_login()
    if check_login(user_id): break
    print ("Wrong login/password")
  
  # Get source code of page having certificate and key 
  certificate_key = get_certificates(user_id)
  # Parse certificate and key and get computer id
  certificate_key = parse_certificates(certificate_key)
  certificate = certificate_key[0]
  key = certificate_key[1]
  COMP = get_computer_name(certificate)
  
  # Getting configuration parameters
  slapos_configuration='/etc/opt/slapos/'
  config= Config()
  config.setConfig(slapos_configuration=slapos_configuration,
                   dry_run=False,
                   computer_id=COMP,
                   master_url="""https://slap.vifib.com""",
                   interface = "eth0",
                   ipv4_network= "10.0.0.0/16",
                   certificate = certificate,
                   key = key
                   )
  while True:
    config.userConfig()
    print "\nThis your configuration: \n"
    config.displayUserConfig()
    if get_yes_no("\nDo you confirm?"):
      break

  # Save former configuration
  save_former_config()

  # Prepare Slapos Configuration
  slapconfig(config)
  


 
if __name__ == "__main__":
  register()
