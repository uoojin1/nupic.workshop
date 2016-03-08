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
  "-t",
  "--title",
  default="Just some data...",
  dest="title",
  help="The title of the thing we're making or doing."
)


def parseArgs():
  (options, args) = parser.parse_args(sys.argv[1:])
  if len(args) != 1:
    parser.error("Data file path was not given!")
  return options, args
