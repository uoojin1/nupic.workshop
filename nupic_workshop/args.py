# ----------------------------------------------------------------------
# Copyright (C) 2016, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
import sys
from optparse import OptionParser

# Options parsing.
parser = OptionParser(
  usage="%prog [options]"
)
parser.add_option(
  "-d",
  "--data-file",
  default=None,
  dest="dataFile",
  help="Which CSV data file to process.")
parser.add_option(
  "-n",
  "--name",
  default="Just some data...",
  dest="name",
  help="What to name the thing we're making or doing."
)


def parseArgs():
  return parser.parse_args(sys.argv[1:])
