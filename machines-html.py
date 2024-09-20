"""
machines-html.py (previously machdef2html.py)

Generator of html file for machines
HTML page output will be used in /models/config/2.Y.Z/machines.html

# Required arguments
--htmlfile  : HTML filename to use as path is set in paths.txt OUTROOT variable
--version   : sets the CESM version to use in the HTML
--supported : list of supported machines
--tested    : list of tested machines

# Example usage
python machines-html.py 
--htmlfile machines.html 
--version CESM2.Y.Z
--supported cheyenne,hobart
--tested cori,edison,stampede2,bluewaters,theta
"""



###
# imports and variable setting
###
import os, sys, re, glob
import datetime

# check for jinja2 to make templates with
try:
    import jinja2
except:
    raise SystemExit("ERROR: jinja2 not found, please install and try again")

# open the file with the paths for CIMEROOT CESMROOT OUTROOT
with open('paths.txt') as file:
    paths_data = file.read()

# parse the file to get the vars
paths_lines = paths_data.split('\n')
paths_vars = {}

# loop thru the line and split on the =
for path_line in paths_lines:
    if '=' in path_line:
        key, value = path_line.split('=')
        paths_vars[key.strip()] = value.strip()

# set the path vars
CIMEROOT = paths_vars.get('CIMEROOT')
CESMROOT = paths_vars.get('CESMROOT')
OUTROOT = paths_vars.get('OUTROOT')

# check the vars
if not (CIMEROOT and CESMROOT and OUTROOT):
    raise SystemExit("ERROR: must set CIMEROOT, CESMROOT, and OUTROOT in paths.txt")

# set the CIMEROOT to path for including other python imports
sys.path.append(os.path.join(CIMEROOT, "scripts", "Tools"))

# set the SRCROOT
SRCROOT = os.path.dirname(CIMEROOT)
os.environ['SRCROOT'] = SRCROOT

# CIME python imports
from standard_script_setup import *
from CIME.utils import expect
from CIME.XML.files    import Files
from CIME.XML.machines import Machines

# global variables
_now = datetime.datetime.now().strftime('%Y-%m-%d')
logger = logging.getLogger(__name__)



###
# functions
###
# process the command line arguments
def commandline_options():
    parser = argparse.ArgumentParser(description='Read all the config_machines.xml files and generate a corresponding HTML file.')
    CIME.utils.setup_standard_logging_options(parser)
    parser.add_argument('--htmlfile', nargs=1, required=True, help='Fully quailfied path to output HTML file.')
    parser.add_argument('--version', nargs=1, required=True, help='Model version (e.g. CESM2.0)')
    parser.add_argument('--supported', nargs=1, required=True, help='Comma separated list of supported machines that have passed statistical validation and may be used for large coupled experiments.')
    parser.add_argument('--tested', nargs=1, required=True, help='Comma separated list of tested machines but not necessarily appropriate for large coupled experiments.')
    options = parser.parse_args()
    CIME.utils.parse_args_and_handle_standard_logging_options(options)
    return options

###############################################################################
def _main_func(options, work_dir):
###############################################################################

    """Construct machines html from an XML file."""
        
    # Initialize a variables for the html template
    mach_dict = dict()
    cesmmodel = options.version[0]

    # get the machine config file
    files = Files()
    config_file = files.get_value("MACHINES_SPEC_FILE")
    expect(os.path.isfile(config_file),
           "Cannot find config_file {} on disk".format(config_file))

    # instantiate a machines object and read XML values into a dictionary
    machines = Machines(config_file, machine="Query")
    mach_list = machines.list_available_machines()

    # get all the machine values loaded into the mach_dict
    mach_dict = machines.return_values()

    # intialize the support keys
    for machine in mach_list:
        mach_dict[(machine,'support')] = "Unsupported"

    # loop through the list of supported machines and flag in the dictionary
    supported = options.supported[0].split(',')
    for machine in supported:
        mach_dict[(machine,'support')] = "Scientific"

    # loop through the list of tested machines and flag in the dictionary
    tested = options.tested[0].split(',')
    for machine in tested:
        mach_dict[(machine,'support')] = "Tested"

    # load up jinja template
    templateLoader = jinja2.FileSystemLoader( searchpath='{0}/templates'.format(work_dir) )
    templateEnv = jinja2.Environment( loader=templateLoader )

    # TODO - get the cesm_version for the CIME root
    tmplFile = 'machines.tmpl'
    template = templateEnv.get_template( tmplFile )
    templateVars = { 'mach_list'     : mach_list,
                     'mach_dict'     : mach_dict,
                     'today'         : _now,
                     'cesmmodel' : cesmmodel }
        
    # render the template
    mach_tmpl = template.render( templateVars )

    # set the full path of the HTML file
    html_filepath = os.path.join(OUTROOT, options.htmlfile[0])

    # write the output file
    with open( html_filepath, 'w') as html:
        html.write(mach_tmpl)

    return "HTML file created at " + html_filepath

###############################################################################

if __name__ == "__main__":

    options = commandline_options()
##    work_dir = os.path.join(CIMEROOT,"scripts","Tools","xml2html")
    work_dir = os.getcwd()
    try:
        status = _main_func(options, work_dir)
        sys.exit(status)
    except Exception as error:
        print(str(error))
        sys.exit(1)




