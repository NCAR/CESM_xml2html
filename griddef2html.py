#!/usr/bin/env python

"""Generator of html file for grids
"""

# Typically ignore this.
# pylint: disable=invalid-name

# Disable these because this is our standard setup
# pylint: disable=wildcard-import,unused-wildcard-import,wrong-import-position

import os, sys, re, glob
import datetime

CIMEROOT = os.environ.get("CIMEROOT")
if CIMEROOT is None:
    raise SystemExit("ERROR: must set CIMEROOT environment variable")
sys.path.append(os.path.join(CIMEROOT, "scripts", "Tools"))

SRCROOT = os.environ.get("SRCROOT")
if SRCROOT is None:
    SRCROOT = os.path.dirname(CIMEROOT)
os.environ['SRCROOT'] = SRCROOT

from standard_script_setup import *
from CIME.utils import expect
from CIME.XML.entry_id import GenericXML
from CIME.XML.files    import Files
from CIME.XML.grids    import Grids

# check for  dependency module
try:
    import jinja2
except:
    raise SystemExit("ERROR: griddef2html.py depends on the jinja2 template module. " /
                     "Install using 'pip --user install jinja2'")

# global variables
_now = datetime.datetime.now().strftime('%Y-%m-%d')
logger = logging.getLogger(__name__)


###############################################################################
def commandline_options():
###############################################################################

    """ Process the command line arguments.                                                                                                                                    
    """
    parser = argparse.ArgumentParser(
        description='Read the config_grids.xml file and generate a corresponding HTML file.')

    CIME.utils.setup_standard_logging_options(parser)

    parser.add_argument('--htmlfile', nargs=1, required=True,
                        help='Fully quailfied path to output HTML file.')

    parser.add_argument('--txtfile', nargs=1, required=True,
                        help='Fully quailfied path to input modified text file generated by query_config --grids --long.')

    parser.add_argument('--version', nargs=1, required=True,
                        help='Model version (e.g. CESM2.0)')

    options = parser.parse_args()

    CIME.utils.parse_args_and_handle_standard_logging_options(options)

    return options

###############################################################################
def _main_func(options, work_dir):
###############################################################################

    """Construct grids html from an XML file."""
        
    # Initialize a variables for the html template
    all_grids = dict()
    model_version = options.version[0]

    # read in txtfile with the grids definitions
    txtfile = options.txtfile[0]
    expect((txtfile),
           'Cannot find query_config --grids --long output text file %s' %txtfile)

    # read the grids file looking for aliases and load the all_grids dict
    with open( txtfile, 'r') as f:
        for line in f:
            if "alias:" in line:
                line = line.rstrip('\n')
                alias = line.split(':')
                alias.pop(0)
                key = alias[0].lstrip()
                all_grids[key] = ''
            else:
                all_grids[key] += line
    f.close()


    # load up jinja template
    templateLoader = jinja2.FileSystemLoader( searchpath='{0}/templates'.format(work_dir) )
    templateEnv = jinja2.Environment( loader=templateLoader )

    # TODO - get the cesm_version for the CIME root
    tmplFile = 'griddef2html.tmpl'
    template = templateEnv.get_template( tmplFile )
    templateVars = { 'today'              : _now,
                     'model_version'      : model_version,
                     'all_grids'          : all_grids }
        
    # render the template
    grid_tmpl = template.render( templateVars )

    # write the output file
    with open( options.htmlfile[0], 'w') as html:
        html.write(grid_tmpl)

    return 0

###############################################################################

if __name__ == "__main__":

    options = commandline_options()
    work_dir = os.path.join(CIMEROOT,"scripts","Tools","xml2html")
    try:
        status = _main_func(options, work_dir)
        sys.exit(status)
    except Exception as error:
        print(str(error))
        sys.exit(1)




