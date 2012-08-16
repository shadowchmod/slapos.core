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
import pkg_resources
from shutil import move
from subprocess import call as subprocessCall
import sys
import urllib2



__import__('pkg_resources').declare_namespace(__name__)


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



def _call(cmd_args, stdout=None, stderr=None, dry_run=False):
  """
  Wrapper for subprocess.call() which'll secure the usage of external program's.

  Args:
  cmd_args: list of strings representing the command and all it's needed args
  stdout/stderr: only precise PIPE (from subprocess) if you don't want the
  command to create output on the regular stream
  """
  print "Calling: %s" % ' '.join(cmd_args)
  try:
    if subprocessCall(cmd_args, stdout=stdout, stderr=stderr) != 0:
      raise ValueError('Issues during running %r' % cmd_args)
  except OSError as e:
    raise ExecError('Process respond:"%s" when calling "%s"' % \
                      (str(e), ' '.join(cmd_args)))

# Utility fonction to get yes/no answers
def get_yes_no (prompt):
  ok= 0
  while not ok:
    answer=raw_input( prompt + " [y,n]: " )
    if answer.upper() in [ 'Y','YES' ]: return True
    if answer.upper() in [ 'N', 'NO' ]: return False

# Return OpenSUSE version if it is SuSE
def suse_version(): 
  if os.path.exists('/etc/SuSE-release') :
    with open('/etc/SuSE-release') as f :
      for line in f:
        if "VERSION" in line:
          dist = line.split()
          return float(dist[2])
  else :
    return 0
 
def enable_bridge(slapos_configuration):
  #Create temp file
  slapos_old_path = os.path.join(slapos_configuration,'slapos.cfg')
  slapos_new_path = os.path.join(slapos_configuration,'slapos.cfg.tmp')
  slapos_new = open(slapos_new_path,'w')
  slapos_old = open(slapos_old_path)
  for line in slapos_old:
    slapos_new.write(line.replace("create_tap = false", "#create_tap = false"))
  #close temp file
  slapos_new.close()
  slapos_old.close()
  #Remove original file
  os.remove(slapos_old_path)
  #Move new file
  move(slapos_new_path, slapos_old_path)


# Function to get ssh key
def get_ssh(temp_dir):
  # Downloading ssh_key
  count = 10
  gotten = True
  while count > 0 :
    try:
      print "Enter the url of your public ssh key"
      ssh_web=raw_input('-->  ')
      try:
        ssh_key_all = urllib2.urlopen(''.join(ssh_web))
        gotten= True
      except ValueError, err:
      # add http:// if it is missing (needed by urllib2)
        ssh_web = """http://"""+ssh_web   
        ssh_key_all = urllib2.urlopen(''.join(ssh_web))
        gotten= True
    except urllib2.URLError,err: 
      print "  URL ERROR"
      gotten = False
      count -= 1
    if gotten:
      ssh_pub_key= ssh_key_all.read()
      print ssh_pub_key
      if get_yes_no ('Is this your ssh public key?'):
        break
      else:
        count -=1
  ssh_file=open(os.path.join(temp_dir,"authorized_keys"),"w")
  ssh_file.write(''.join(ssh_pub_key))
  ssh_file.close()
  return 0


# Specific function to configure SlapOS Image
def slapserver(config):
  dry_run = config.dry_run
  mount_dir_path = config.mount_dir_path
  try:
    # Setting hostname
    hostname_path = os.path.normpath('/'.join([mount_dir_path,
                                               config.hostname_path]))
    print "Setting hostname in : %s" % hostname_path
    if not dry_run:
      open(hostname_path, 'w').write("%s\n" % config.computer_id)

    # Adding the hostname as a valid address 
    host_path = os.path.normpath('/'.join([mount_dir_path,
                                           config.host_path]))
    print "Creating %r" % host_path
    if not dry_run:
      open(host_path, 'w').write(
        pkg_resources.resource_stream(__name__,
                                      'template/hosts.in').read() % dict(
          computer_id=config.computer_id))

    # Creating safe sshd_config
    sshd_path = os.path.normpath('/'.join([mount_dir_path, 'etc', 'ssh',
                                           'sshd_config']))
    print "Creating %r" % sshd_path
    if not dry_run:
      open(sshd_path, 'w').write(
        pkg_resources.resource_stream(__name__,
                                      'template/sshd_config.in').read())
      os.chmod(sshd_path, 0600)

    # Creating default bridge config
    br0_path = os.path.normpath('/'.join([mount_dir_path, 'etc',
                                          'sysconfig', 'network', 'ifcfg-br0']))
    print "Creating %r" % br0_path
    if not dry_run:
      open(br0_path, 'w').write(
        pkg_resources.resource_stream(__name__,
                                      'template/ifcfg-br0.in').read())

    # Creating boot scripts
    path = os.path.join(config.slapos_configuration, 'slapos')
    print "Creating %r" % path
    if not dry_run:
      open(path, 'w').write(pkg_resources.resource_stream(__name__,
                                                          'script/%s' % 'slapos').read() % dict(
          slapos_configuration=config.slapos_configuration))
      os.chmod(path, 0755)
    path = os.path.join(mount_dir_path, 'etc', 'systemd', 'system','slapos.service')
    print "Creating %r" % path
    if not dry_run:
      open(path, 'w').write(pkg_resources.resource_stream(__name__,
                                                          'script/%s' % 'slapos.service').read() % dict(
          slapos_configuration=config.slapos_configuration))
      os.chmod(path, 0755)

    # Preparing retry slapformat script
    path = os.path.join(config.slapos_configuration,'run_slapformat')    
    print "Creating %r" % path
    if not dry_run:
      open(path, 'w').write(pkg_resources.resource_stream(__name__,
                                                          'script/%s' % 'run_slapformat').read() % dict(
          slapos_configuration=config.slapos_configuration))
      os.chmod(path, 0755)
    path = os.path.join(mount_dir_path,'etc','openvpn','client.conf')    
    print "Creating %r" % path
    if not dry_run:
      open(path, 'a').write("""script-security 3 system
up-restart
up '/bin/bash %(slapos_configuration)s/run_slapformat & echo foo'
log /var/log/openvpn.log""" % dict(
          slapos_configuration=config.slapos_configuration))
      os.chmod(path, 0755)
  
    # Writing ssh key
    if config.need_ssh :
      user_path = os.path.normpath('/'.join([mount_dir_path, 'root']))
      ssh_key_directory = os.path.normpath('/'.join([user_path, '.ssh']))
      ssh_key_path = os.path.normpath('/'.join([ssh_key_directory,
                                                'authorized_keys']))
      stat_info = os.stat(user_path)
      uid, gid = stat_info.st_uid, stat_info.st_gid
      ssh_key_directory = os.path.dirname(ssh_key_path)
      if not os.path.exists(ssh_key_directory):
        print "Creating ssh directory: %s" % ssh_key_directory
        if not dry_run:
          os.mkdir(ssh_key_directory)
      if not dry_run:
        print "Setting uid:gid of %r to %s:%s" % (ssh_key_directory, uid, gid)
        os.chown(ssh_key_directory, uid, gid)
        os.chmod(ssh_key_directory, 0700)
      
      print "Creating file: %s" % ssh_key_path
      if not dry_run:
        open(ssh_key_path,'a').write(''.join(open(config.key_path,'r').read()))
        
      if not dry_run:
        print "Setting uid:gid of %r to %s:%s" % (ssh_key_path, uid, gid)
        os.chown(ssh_key_path, uid, gid)
        os.chmod(ssh_key_path, 0600)

    # Put file to  force VPN if user asked
    if config.force_vpn :
      if not dry_run:
        open(os.path.join(config.slapos_configuration,'openvpn-needed'),'w')

    # Removing line in slapos script activating kvm in virtual 
    if config.virtual:
      if not dry_run:
        path = os.path.join(config.slapos_configuration,'slapos')
        _call(['sed','-i',"$d",path],dry_run=dry_run)
        _call(['sed','-i',"$d",path],dry_run=dry_run)
      
    # Adding slapos_firstboot in case of MultiDisk usage    
    if not config.one_disk :
      for script in ['slapos_firstboot']:
        path = os.path.join(mount_dir_path, 'etc', 'init.d', script)
        print "Creating %r" % path
        if not dry_run:
          open(path, 'w').write(pkg_resources.resource_stream(__name__,
                                                              'script/%s' % script).read())
          os.chmod(path, 0755)	  
    else:
      for script in ['slapos_firstboot']:
        path = os.path.join(mount_dir_path, 'etc', 'init.d', script)
        if os.path.exists(path):
          print "Removing %r" % path
          if not dry_run:
            os.remove(path)
  finally:
    print "SlapOS Image configuration: DONE"
    return 0


class Config:
  def setConfig(self,mount_dir_path,slapos_configuration,
                hostname_path, host_path,
                dry_run,
                key_path, master_url, 
                temp_dir, certificates, server):
    """
    Set options given by parameters.
    """
    self.slapos_configuration = slapos_configuration
    self.hostname_path = hostname_path
    self.host_path = host_path
    self.dry_run = dry_run
    self.key_path = key_path
    self.master_url = master_url
    self.mount_dir_path = mount_dir_path
    self.temp_dir=temp_dir
    self.certificates=certificates
    self.server=server

  def userConfig(self):
    if self.server :
      self.need_ssh = get_yes_no("Do you want a remote ssh access?")
      self.virtual = get_yes_no("Is this a virtual Machine?")
      if not self.virtual:
        self.one_disk = not get_yes_no ("Do you want to use SlapOS with a second disk?")
      else:
        self.one_disk=True
      self.force_vpn = get_yes_no ("Do you want to force the use of vpn to provide ipv6?") 
      self.interface = "bridge_name = br0"
    if self.certificates:
      self.partition_amount = raw_input("""Number of SlapOS partitions for this computer? """)
      if not self.server :
        self.interface = "interface_name = "+ ''.join(raw_input(""" Name of interface used to access internet (eth0, wlan0, br0...)? """))

  def displayUserConfig(self):
    print "Computer reference : %s" %self.computer_id
    print "Suse Server for SlapOS : %s" % self.server
    if self.server:
      print "Ipv6 over VPN: %s" % self.force_vpn
      print "Remote ssh access: %s" % self.need_ssh
      print "Virtual Machine: %s" % self.virtual
      if not self.virtual:
        print "Use a second disk: %s" % (not self.one_disk)
    if self.certificates:
      print "Number of partition: %s" % (self.partition_amount)
      if not self.server :
        print (self.interface)

def slapprepare():
  try:
    temp_directory=os.path.join('/tmp/slaptemp/')
    if not os.path.exists(temp_directory):
      print "Creating directory: %s" % temp_directory
      os.mkdir(temp_directory, 0711)

    # Set preference by asking user
    if suse_version() >= 12.1 :
      is_server = get_yes_no ("Is this a Suse Server for SlapOS?")
    else :
      is_server = False

    certificates = get_yes_no("Automatically register new computer to Vifib?")
    if certificates:      
      slapos_configuration='/etc/opt/slapos/'
    else:
      # Check for config file in /etc/slapos/
      if os.path.exists('/etc/slapos/slapos.cfg'):
        slapos_configuration='/etc/slapos/'
      else:
        slapos_configuration='/etc/opt/slapos/'
 
    config= Config()
    config.setConfig(mount_dir_path = '/',
                     slapos_configuration=slapos_configuration,
                     hostname_path='/etc/HOSTNAME',
                     host_path='/etc/hosts',
                     dry_run=False,
                     key_path=os.path.join(temp_directory,'authorized_keys'),
                     master_url="""https://slap.vifib.com""",
                     temp_dir=temp_directory,
                     certificates=certificates,
                     server=is_server)
    
    while 1:
      config.userConfig()
      print "\nThis your configuration: \n"
      config.displayUserConfig()
      if get_yes_no("\nDo you confirm?"):
        break

    # Prepare Slapos Configuration
    if config.certificates:  
      slapconfig(config)


    # Prepare for bridge
    enable_bridge(config.slapos_configuration)

    # Prepare SlapOS Suse Server confuguration
    if config.server:
      if config.need_ssh :
        get_ssh(temp_directory)
      slapserver(config)
      if not config.one_disk:
        _call(['/etc/init.d/slapos_firstboot'])
      _call(['systemctl','enable','slapos.service'])
      _call(['systemctl','start','slapos.service'])

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
  if os.path.exists(temp_directory):
    print "Deleting directory: %s" % temp_directory
    _call(['rm','-rf',temp_directory])
  sys.exit(return_code)
