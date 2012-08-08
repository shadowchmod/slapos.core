# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010, 2011, 2012 Vifib SARL and Contributors.
# All Rights Reserved.
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
import sys
from optparse import OptionParser, Option
import logging
import logging.handlers
import ConfigParser


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
      Option("-l", "--log_file",
             help="The path to the log file used by the script.",
             type=str),
      Option("-v", "--verbose",
             default=False,
             action="store_true",
             help="Verbose output."),
      Option("-c", "--console",
             default=False,
             action="store_true",
             help="Console output."),
      Option("-u", "--database-uri",
             type=str,
             help="URI for sqlite database"),
    ])

  def check_args(self):
    """
    Check arguments
    """
    (options, args) = self.parse_args()
    if len(args) != 1:
      self.error("Incorrect number of arguments")

    return options, args[0]

class Config:
  def setConfig(self, option_dict, configuration_file_path):
    """
    Set options given by parameters.
    """
    # Set options parameters
    for option, value in option_dict.__dict__.items():
      setattr(self, option, value)

    # Load configuration file
    configuration_parser = ConfigParser.SafeConfigParser()
    configuration_parser.read(configuration_file_path)
    # Merges the arguments and configuration
    for section in ("slapproxy", "slapos"):
      configuration_dict = dict(configuration_parser.items(section))
      for key in configuration_dict:
        if not getattr(self, key, None):
          setattr(self, key, configuration_dict[key])

    # set up logging
    self.logger = logging.getLogger("slapproxy")
    self.logger.setLevel(logging.INFO)
    if self.console:
      self.logger.addHandler(logging.StreamHandler())

    if not self.database_uri:
      raise ValueError('database-uri is required.')
    if self.log_file:
      if not os.path.isdir(os.path.dirname(self.log_file)):
        # fallback to console only if directory for logs does not exists and
        # continue to run
        raise ValueError('Please create directory %r to store %r log file' % (
          os.path.dirname(self.log_file), self.log_file))
      else:
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(file_handler)
        self.logger.info('Configured logging to file %r' % self.log_file)

    self.logger.info("Started.")
    if self.verbose:
      self.logger.setLevel(logging.DEBUG)
      self.logger.debug("Verbose mode enabled.")

def run(config):
  from views import app
  app.config['computer_id'] = config.computer_id
  app.config['DATABASE_URI'] = config.database_uri
  app.run(host=config.host, port=int(config.port), debug=True)

def main():
  "Run default configuration."
  usage = "usage: %s [options] CONFIGURATION_FILE" % sys.argv[0]

  try:
    # Parse arguments
    config = Config()
    config.setConfig(*Parser(usage=usage).check_args())

    run(config)
    return_code = 0
  except SystemExit, err:
    # Catch exception raise by optparse
    return_code = err

  sys.exit(return_code)
