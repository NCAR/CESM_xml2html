"""
input-html.py (previously compinputdef2html.py)

Generator of html files for component input parameters (CASEROOT Variable Definitions)
Parses a namelist XML file and generates a html page
HTML pages output will be used in /models/settings/2.Y.Z/*_input.html

# Required arguments
--inputfile  : Path to the input namelist xml file
--comp       : Component name
--htmlfile   : HTML filename to use as path is set in paths.txt OUTROOT variable

# Example usage
python input-html.py 
--cesmmodel 2.1.5
--inputfile /path/to/CESM2/components/cam/bld/namelist_files/namelist_definition.xml
--comp CAM 
--htmlfile cam_nml.html 
--compversion 6.0
"""



###
# imports and variable setting
###
import os, sys, re, glob
import datetime
import traceback
import subprocess
# DEV
from pprint import pprint

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

# CIME python imports
from standard_script_setup import *
from CIME.utils import expect
from CIME.XML.component import Component

# global variables
_now = datetime.datetime.now().strftime('%Y-%m-%d')
_comps = ['AQUAP', 'CAM', 'CLM', 'CISM', 'POP2', 'CICE', 'RTM', 'MOSART', 'WW3', 'Driver', 'DATM', 'DESP', 'DICE', 'DLND', 'DOCN', 'DROF', 'DWAV']
logger = logging.getLogger(__name__)
hilight = '<span style="color:blue">'
closehilight = '</span>'



###
# functions
###
# process the command line arguments
def commandline_options():
    parser = argparse.ArgumentParser(description='Read the component namelist file and generate a corresponding HTML file.')
    CIME.utils.setup_standard_logging_options(parser)
    parser.add_argument('--inputfile', nargs=1, required=True, help='Fully nquailfied path to config_component.xml input XML file.')
    parser.add_argument('--comp', nargs=1, required=True, choices=_comps, help='Component name.')
    parser.add_argument('--htmlfile', nargs=1, required=True, help='Fully quailfied path to output HTML file.')
    parser.add_argument('--comptag', nargs=1, required=False, help='Component tag')
    parser.add_argument('--compversion', nargs=1, required=False, help='Component version. Example: 4.0, 4.5, 5.0, etc...')
    parser.add_argument('--cesmmodel', nargs=1, required=False, help='CESM model version. Example: 2.2.0, 2.1.3, 2.1.2, etc...')
    options = parser.parse_args()
    CIME.utils.parse_args_and_handle_standard_logging_options(options)
    return options


# get the git tag based on a directory
def get_git_tag(directory):
    try:
        # Change the working directory to the specified path
        os.chdir(directory)
        
        # Run the git command and capture the output
        tag = subprocess.check_output(['git', 'describe', '--exact-match', '--tags'], stderr=subprocess.STDOUT)
        # Decode the byte string to a regular string
        return tag.strip().decode('utf-8')
    except subprocess.CalledProcessError:
        # Handle the case where there is no tag associated with the current commit
        return None
    except FileNotFoundError:
        # Handle the case where the 'git' command is not found
        print("Git command not found.")
        return None


###############################################################################
def _main_func(options, dir_current):
###############################################################################

    # Initialize variables for the html template
    html_dict = dict()
    cesm_version = 'CESM2'
    comp = ''
    if options.comp:
        comp = options.comp[0]

    # Create a component object from the xml file
    filename = options.inputfile[0]
    expect(os.path.isfile(filename), "File %s does not exist"%filename)
    component = Component(filename, comp)
    helptext, html_dict = component.return_values()
    basepath = os.path.dirname(filename)
    
    # get the component tag from the command line args
    # OLD WAY
    #comptag = ''
    #if options.comptag:
    #    comptag = options.comptag[0]
    comptag = get_git_tag(basepath)

    # get the component version from the command line args
    compversion = ''
    if options.compversion:
        compversion = options.compversion[0]

    # get the cesm model version from the command line args
    cesmmodel = ''
    if options.cesmmodel:
        cesmmodel = options.cesmmodel[0]

    # load up jinja template
    templateLoader = jinja2.FileSystemLoader( searchpath='{0}/templates'.format(dir_current) )
    templateEnv = jinja2.Environment( loader=templateLoader )

    # populate the template variables
    tmplFile = 'input.tmpl'
    template = templateEnv.get_template( tmplFile )
    templateVars = { 'html_dict'    : html_dict,
                     'today'        : _now,
                     'cesm_version' : cesm_version,
                     'cesmmodel'    : cesmmodel,
                     'comp'         : comp,
                     'comptag'      : comptag,
                     'compversion'  : compversion,
                     'hilight'      : hilight,
                     'closehilight' : closehilight,
                     'helptext'     : helptext
                 }
        
    # render the template
    comp_tmpl = template.render( templateVars )

    # set the full path of the HTML file
    html_filepath = os.path.join(OUTROOT, options.htmlfile[0])

    # write the output file
    with open( html_filepath, 'w') as html:
        html.write(comp_tmpl)

    return "HTML file created at " + html_filepath

###############################################################################

if __name__ == "__main__":

    options = commandline_options()
    dir_current = os.getcwd()
    try:
        status = _main_func(options, dir_current)
        sys.exit(status)
    except Exception as error:
        print(str(error))
        sys.exit(1)




