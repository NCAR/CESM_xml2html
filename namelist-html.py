"""
namelist-html.py (previously nmldef2html.py)

Generator of html files for component namelists
Parses a namelist XML file and generates a html page
HTML pages output will be used in /models/settings/2.Y.Z/*_nml.html

# Required arguments
--nmlfile  : Path to the input namelist xml file
--comp     : Component name
--htmlfile : HTML filename to use as path is set in paths.txt OUTROOT variable

# Example usage
python namelist-html.py 
--cesmmodel 2.1.5
--nmlfile /path/to/CESM2/components/pop/externals/MARBL/defaults/json/settings_latest.json 
--comp MARBL 
--htmlfile marbl_nml.html 
--marbl-json

python namelist-html.py 
--cesmmodel 2.1.5
--nmlfile /path/to/CESM2/components/cam/bld/namelist_files/namelist_definition.xml
--comp CAM 
--htmlfile cam_nml.html 
--compversion 6.0

# Notes
To get the MARBL json will need to run $MARBLROOT/MARBL_tools/yaml_to_json.py
"""



###
# imports and variable setting
###
# initial python imports
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
from CIME.XML.generic_xml import GenericXML

# global variables
_now = datetime.datetime.now().strftime('%Y-%m-%d')
_comps = ['AQUAP','CAM','CLM','CISM','POP2','POP','MARBL','CICE','RTM','MOSART','WW3','Driver','DATM','DESP','DICE','DLND','DOCN','DROF','DWAV']
_cime_comps = ['Driver','DATM','DESP','DICE','DLND','DOCN','DROF','DWAV']
_exclude_defaults_comps = ['POP2']
_exclude_groups = {
    'AQUAP':  [],
    'CAM':    ['cime_driver_inst','seq_cplflds_inparm','seq_cplflds_userspec', 'ccsm_pes','seq_infodata_inparm','seq_timemgr_inparm', 'prof_inparm','papi_inparm','pio_default_inparm', 'drydep_inparm','megan_emis_nl','fire_emis_nl', 'carma_inparm','ndep_inparm','dom_inparm', 'docn_nml','shr_strdata_nml','aquap_nl'],
    'CLM':    [],
    'CISM':   [],
    'POP2':   [],
    'POP':   [],
    'MARBL':  [],
    'CICE':   [],
    'RTM' :   [],
    'MOSART': [],
    'WW3':    [],
    'Driver': [],
    'DATM':   [],
    'DESP':   [],
    'DICE':   [],
    'DLND':   [],
    'DOCN':   [],
    'DROF':   [],
    'DWAV':   []}
logger = logging.getLogger(__name__)
hilight = '<span class="text-primary">'
closehilight = '</span>'



###
# functions
###
# process the command line arguments
def get_arguments():
    # set the description
    parser = argparse.ArgumentParser(description='Read the component namelist file and generate a corresponding HTML file')

    # setup the CIME logger
    CIME.utils.setup_standard_logging_options(parser)

    # handle the arguments that can be passed
    parser.add_argument('--nmlfile', nargs=1, required=True, help='Fully quailfied path to input namelist XML file')
    parser.add_argument('--comp', nargs=1, required=True, choices=_comps, help='Component name')
    parser.add_argument('--htmlfile', nargs=1, required=True, help='Filename to use for HTML output - FILENAME.html')
    parser.add_argument('--comptag', nargs=1, required=False, help='Component tag')
    parser.add_argument('--compversion', nargs=1, required=False, help='Component version - 4.0, 4.5, 5.0, etc...')
    parser.add_argument('--cesmmodel', nargs=1, required=False, help='CESM model version. Example: 2.2.0, 2.1.3, 2.1.2, etc...')
    parser.add_argument('--marbl-json', required=False, action='store_true', dest='JSON', help='Flag to look for MARBL JSON file instead of XML')
    options = parser.parse_args()
    CIME.utils.parse_args_and_handle_standard_logging_options(options)

    # return back
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


# construct a `NamelistDefinition` from an XML file and write to HTML
def _main_(options, dir_current):
    # Initialize variables for the html template
    html_dict = dict()
    cesm_version = 'CESM2'

    # set the xml file from the command line args
    filename = options.nmlfile[0]
    expect(os.path.isfile(filename), "File %s does not exist"%filename)
    basepath = os.path.dirname(filename)

    # get the comp from the command line args
    comp = ''
    if options.comp:
        comp = options.comp[0]
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


    # Create a definition object from the xml file
    # sets the vars
    # schema
    # defaults[]
    # MARBL_args
    #
    # no --marbl-json flag 
    if not options.JSON:
        try:
            definition = GenericXML(infile=filename)
        #except:
            #sys.exit("Error: unable to parse file %s" %filename)
        except Exception as e:
            # Log the exception message
            print(f"Error: unable to parse file {filename}")
            print(f"Exception type: {type(e).__name__}")
            print(f"Exception message: {e}")
            # Optionally, print the full traceback
            #traceback.print_exc()
            sys.exit(1)

        # Determine if have new or old schema
        default_files = glob.glob(os.path.join(basepath,"namelist_defaults*.xml"))
        defaults = []
        if len(default_files) > 0:
            schema = "old"
            if comp not in _exclude_defaults_comps:
                for default_file in default_files:
                    try:
                        default = GenericXML(infile=default_file)
                    except Exception as e:
                        # Log the exception message
                        print(f"Error: unable to parse file {default_file}")
                        print(f"Exception type: {type(e).__name__}")
                        print(f"Exception message: {e}")
                        # Optionally, print the full traceback
                        #traceback.print_exc()
                        sys.exit(1)

                    # if all good then continue
                    default = GenericXML(infile=default_file)
                    default.read(infile=default_file, schema=schema)
                    defaults.append(default)
        else:
            schema = "new"
        # read the file into the definition object
        definition.read(infile=filename, schema=schema)
    # yes --marbl-json flag
    else:
        schema = "MARBL JSON"
        derived_desc = dict()
        derived_entry_root = dict()
        derived_entry_type = dict()
        derived_category = dict()
        derived_default_value = dict()

        import json
        with open(filename) as settings_file:
            MARBL_json_dict = json.load(settings_file)

        # Set up MARBL_settings_file_class object with CESM (gx1v7) default values
        MARBL_root = os.path.join(os.path.dirname(filename), "../..")
        sys.path.append(MARBL_root)
        from MARBL_tools import MARBL_settings_file_class
        MARBL_args=dict()
        MARBL_args["default_settings_file"] = filename
        MARBL_args["input_file"] = None
        MARBL_args["grid"] = "CESM_x1"
        MARBL_args["saved_state_vars_source"] = "settings_file"
        MARBL_default_settings = MARBL_settings_file_class.MARBL_settings_class(**MARBL_args)

    # Create a dictionary with a category key and a list of all entry nodes for each key
    category_dict = dict()
    if schema == "MARBL JSON":
        # Special category for MARBL derived types
        category_dict["MARBL_derived_types"] = dict()
        for category in [key for key in MARBL_json_dict.keys() if key[0] != "_"]:
            for marbl_varname in MARBL_json_dict[category].keys():
                if isinstance(MARBL_json_dict[category][marbl_varname]['datatype'], dict):
                    if marbl_varname not in category_dict["MARBL_derived_types"].keys():
                        category_dict["MARBL_derived_types"][marbl_varname] = dict()
                        category_dict["MARBL_derived_types"][marbl_varname][category] = []
                    for component in [key for key in MARBL_json_dict[category][marbl_varname]["datatype"] if key[0] != "_"]:
                        category_dict["MARBL_derived_types"][marbl_varname][category].append(component)
                else:
                    if category in category_dict.keys():
                        category_dict[category].append(marbl_varname)
                    else:
                        category_dict[category] = [ marbl_varname ]
    else:
        for node in definition.get_children("entry"):
            if schema == "new":
                category = definition.get_element_text("category", root=node)
            elif schema == "old":
                category = definition.get(node, "category")

            if category in category_dict:
                category_dict[category].append(node)
            else:
                category_dict[category] = [ node ]

    # MAIN LOOP
    #pprint(category_dict) # ex-  'wv_sat': [<CIME.XML.generic_xml._Element object at 0x10b0dd850>]}
    #sys.exit()
    # Loop over each category and load up the html_dict
    for category in category_dict:
        #print(category) # aero_data_cam
        #pprint(category_dict[category]) # [<CIME.XML.generic_xml._Element object at 0x1108e5d10>,<CIME.XML.generic_xml._Element object at 0x1108e5c10>]
        #sys.exit()
        # Create a dictionary of groups with a group key and an array of group nodes for each key
        groups_dict = dict()
        if schema == "MARBL JSON":
            if category == "MARBL_derived_types":
                for root_varname in category_dict[category].keys():
                    for real_category in category_dict[category][root_varname].keys():
                        for component in category_dict[category][root_varname][real_category]:
                            MARBL_json_var = MARBL_json_dict[real_category][root_varname]["datatype"][component]
                            if "subcategory" in MARBL_json_dict[real_category][root_varname]["datatype"][component].keys():
                                group = MARBL_json_var["subcategory"]
                                if group not in _exclude_groups[comp]:
                                    marbl_varname = "%s%%%s" % (root_varname, component)
                                    derived_desc[marbl_varname] = MARBL_json_var["longname"]
                                    if "autotroph" in root_varname:
                                        derived_entry_root[marbl_varname] = "dtype(%d)" % MARBL_default_settings.settings_dict['autotroph_cnt']
                                        derived_default_value[marbl_varname] = []
                                        for key in ['((autotroph_sname)) == "sp"', '((autotroph_sname)) == "diat"', '((autotroph_sname)) == "diaz"']:
                                            if isinstance(MARBL_json_var["default_value"], dict):
                                                if key in MARBL_json_var["default_value"].keys():
                                                    derived_default_value[marbl_varname].append(MARBL_json_var["default_value"][key])
                                                else:
                                                    derived_default_value[marbl_varname].append(MARBL_json_var["default_value"]["default"])
                                            else:
                                                derived_default_value[marbl_varname].append(MARBL_json_var["default_value"])
                                    elif "zooplankton" in root_varname:
                                        derived_entry_root[marbl_varname] = "dtype(%d)" % MARBL_default_settings.settings_dict['zooplankton_cnt']
                                        derived_default_value[marbl_varname] = []
                                        for key in ['((zooplankton_sname)) == "zoo"']:
                                            if isinstance(MARBL_json_var["default_value"], dict):
                                                if key in MARBL_json_var["default_value"].keys():
                                                    derived_default_value[marbl_varname].append(MARBL_json_var["default_value"][key])
                                                else:
                                                    derived_default_value[marbl_varname].append(MARBL_json_var["default_value"]["default"])
                                            else:
                                                derived_default_value[marbl_varname].append(MARBL_json_var["default_value"])
                                    elif "grazing" in root_varname:
                                        derived_entry_root[marbl_varname] = "dtype(%d,%d)" % \
                                                 (MARBL_default_settings.settings_dict['autotroph_cnt'] ,
                                                  MARBL_default_settings.settings_dict['zooplankton_cnt'])
                                        derived_default_value[marbl_varname] = []
                                        for key in ['((grazing_sname)) == "sp_zoo"', '((grazing_sname)) == "diat_zoo"', '((grazing_sname)) == "diaz_zoo"']:
                                            if isinstance(MARBL_json_var["default_value"], dict):
                                                if key in MARBL_json_var["default_value"].keys():
                                                    derived_default_value[marbl_varname].append(MARBL_json_var["default_value"][key])
                                                else:
                                                    derived_default_value[marbl_varname].append(MARBL_json_var["default_value"]["default"])
                                            else:
                                                derived_default_value[marbl_varname].append(MARBL_json_var["default_value"])
                                    else:
                                        sys.exit("Error: unknown derived type root '%s'" % root_varname)
                                    derived_entry_type[marbl_varname] = MARBL_json_dict[real_category][root_varname]["datatype"][component]["datatype"]
                                    if "_array_shape" in MARBL_json_dict[real_category][root_varname]["datatype"][component].keys():
                                        #print(derived_entry_type[marbl_varname])
                                        derived_entry_type[marbl_varname] = derived_entry_type[marbl_varname] + "(%d)" % \
                                                MARBL_get_array_len(MARBL_json_dict[real_category][root_varname]["datatype"][component]["_array_shape"],
                                                                    MARBL_default_settings)
                                    derived_category[marbl_varname] = real_category
                                    if group in groups_dict:
                                        groups_dict[group].append(marbl_varname)
                                    else:
                                        groups_dict[group] = [ marbl_varname ]
            else:
                for marbl_varname in category_dict[category]:
                    if 'subcategory' in MARBL_json_dict[category][marbl_varname].keys():
                            group = MARBL_json_dict[category][marbl_varname]['subcategory']
                            if group not in _exclude_groups[comp]:
                                if group in groups_dict:
                                    groups_dict[group].append(marbl_varname)
                                else:
                                    groups_dict[group] = [ marbl_varname ]
        else:
            for node in category_dict[category]:
                #print(node) # <CIME.XML.generic_xml._Element object at 0x109de5dd0>
                #sys.exit()
                if schema == "new":
                    group = definition.get_element_text("group", root=node)
                elif schema == "old":
                    group = definition.get(node, "group")
                if group not in _exclude_groups[comp]:
                    if group in groups_dict:
                        groups_dict[group].append(node)
                    else:
                        groups_dict[group] = [ node ]

        #print(group) # cam3_aero_data_nl
        #pprint(groups_dict) # {'cam3_aero_data_nl': [<CIME.XML.generic_xml._Element object at 0x1050d5990>,<CIME.XML.generic_xml._Element object at 0x1050d5890>]}
        #sys.exit()
        # Loop over the keys
        group_list = list()
        for group_name in groups_dict:
            #print(group_name) # cam3_aero_data_nl
            #sys.exit()
            # Loop over the nodes in each group
            for node in groups_dict[group_name]:
                #print(node) # <CIME.XML.generic_xml._Element object at 0x1024d9750>
                #sys.exit()

                # Determine the name
                # @ is used in a namelist to put the same namelist variable in multiple groups
                # in the write phase, all characters in the namelist variable name after
                # the @ and including the @ should be removed
                if schema == "MARBL JSON":
                    name = node
                    #print name
                else:
                    name = definition.get(node, "id")
                if "@" in name:
                    name = re.sub('@.+$', "", name)

                #print(name) # bndtvaer
                #sys.exit()

                # Create the information for this node - start with the description
                if schema == "MARBL JSON":
                    if category == "MARBL_derived_types":
                        desc = derived_desc[node]
                    else:
                        if MARBL_json_dict[category][node]['subcategory'] == group_name:
                            desc = MARBL_json_dict[category][node]['longname']
                else:
                    if schema == "new":
                        raw_desc = definition.get_element_text("desc", root=node)
                    elif schema == "old":
                        raw_desc = definition.text(node)
                    desc = re.sub(r"{{ hilight }}", hilight, raw_desc)
                    desc = re.sub(r"{{ closehilight }}", closehilight, desc)

                #print(desc) # Full pathname of time-variant boundary dataset for aerosol masses. Default: set by build-namelist.
                #sys.exit()

                # add type
                if schema == "new":
                    entry_type = definition.get_element_text("type", root=node)
                elif schema == "old":
                    entry_type = definition.get(node, "type")
                elif schema == "MARBL JSON":
                    if category == "MARBL_derived_types":
                        entry_type = "%s%%%s" % (derived_entry_root[node], derived_entry_type[node])
                    else:
                        if MARBL_json_dict[category][node]['subcategory'] == group_name:
                            entry_type = MARBL_json_dict[category][node]['datatype']
                            # Is this an array?
                            if "_array_shape" in MARBL_json_dict[category][node].keys():
                                entry_type = entry_type + "(%d)" % \
                                        MARBL_get_array_len(MARBL_json_dict[category][node]["_array_shape"],
                                                            MARBL_default_settings)
                
                #DEVVVVV
                #print()
                #print(schema) # old
                #print()
                #print(entry_type) # char*256
                #print()
                #sys.exit()
                

                # add valid_values
                if schema == "new":
                    valid_values = definition.get_element_text("valid_values", root=node)
                elif schema == "old":
                    valid_values = definition.get(node, "valid_values")
                if schema == "MARBL JSON":
                    if category == "MARBL_derived_types":
                        valid_values = ''
                    else:
                        if MARBL_json_dict[category][node]["subcategory"] == group_name:
                            if "valid_values" in MARBL_json_dict[category][node].keys():
                                valid_values = ",".join(MARBL_json_dict[category][node]["valid_values"])
                            else:
                                valid_values = None

                if entry_type == "logical":
                    valid_values = ".true.,.false."
                else:
                    if not valid_values:
                        if category == "MARBL_derived_types":
                            valid_values = "any " + derived_entry_type[node]
                        else:
                            #print(entry_type)
                            valid_values = "any " + entry_type

                        #print(valid_values)
                        if "char" in valid_values:
                            valid_values = "any char"

                if valid_values is not None:
                    valid_values = valid_values.split(',')

                # add default values
                values = ""
                if schema == "new":
                    value_nodes = definition.get(node,'value')
                    if value_nodes is not None and len(value_nodes) > 0:
                        for value_node in value_nodes:
                            try:
                                value = value_node.text.strip()
                            except:
                                value = 'undefined'
                            if value_node.attrib:
                                values += " is %s for: %s <br/>" %(value, value_node.attrib)
                            else:
                                values += " %s <br/>" %(value)
                elif schema == "MARBL JSON":
                    if node in MARBL_default_settings.settings_dict.keys():
                        values = MARBL_default_settings.settings_dict[node]
                        #print "%s = %s" % (node, values)
                    else:
                        if category == "MARBL_derived_types":
                            if node in derived_default_value.keys():
                                default_values = derived_default_value[node]
                            else:
                                default_values = []
                        else:
                            if "default_value" in MARBL_json_dict[category][node].keys():
                                if isinstance(MARBL_json_dict[category][node]["default_value"], dict):
                                    if 'PFT_defaults == "CESM2"' in MARBL_json_dict[category][node]["default_value"].keys():
                                        default_values = MARBL_json_dict[category][node]["default_value"]['PFT_defaults == "CESM2"']
                                    elif 'GCM == "CESM"' in MARBL_json_dict[category][node]["default_value"].keys():
                                        default_values = MARBL_json_dict[category][node]["default_value"]['GCM == "CESM"']
                                    else:
                                        default_values = MARBL_json_dict[category][node]["default_value"]["default"]
                                else:
                                    default_values = MARBL_json_dict[category][node]["default_value"]
                        if isinstance(default_values, list):
                            values = []
                            for value in default_values:
                                if type(value) == type (u''):
                                    values.append(value)
                                else:
                                    values.append(value)
                        elif type(default_values) == type (u''):
                            values = default_values

                # exclude getting CAM and POP default value - it is included in the description text
                elif comp not in _exclude_defaults_comps:
                    for default in defaults:
                        for node in default.get_children(name=name):
                            if default.attrib(node):
                                values += " is %s for: %s <br/>" %(default.text(node), default.attrib(node))
                            else:
                                values += " %s <br/>" %(default.text(node))

                # create the node dictionary
                node_dict = { 'name'           : name,
                              'desc'           : desc,
                              'entry_type'     : entry_type,
                              'valid_values'   : valid_values,
                              'default_values' : values,
                              'group_name'     : group_name }

                # append this node_dict to the group_list
                group_list.append(node_dict)
                if category == "MARBL_derived_types":
                    real_category = derived_category[node]

            # update the group_list for this category in the html_dict
            if category == "MARBL_derived_types":
                category_group = real_category
            else:
                category_group = category
            html_dict[category_group] = group_list


    # ERROR WITH CICE causing issues on {% for category, var_list in html_dict|dictsort %} in template file
    #for row in html_dict:
    #    print(row)
    #return 0
    # Fix for CICE to remove none entires
    html_dict = {k: v for k, v in html_dict.items() if k is not None}

    # load up jinja template
    templateLoader = jinja2.FileSystemLoader( searchpath='{0}/templates'.format(dir_current) )
    templateEnv = jinja2.Environment( loader=templateLoader )

    # populate the template variables
    tmplFile = 'namelist.tmpl'
    template = templateEnv.get_template( tmplFile )
    templateVars = { 'html_dict'    : html_dict,
                     'today'        : _now,
                     'cesm_version' : cesm_version,
                     'cesmmodel'   : cesmmodel,
                     'comp'         : comp,
                     'comptag'      : comptag,
                     'compversion'  : compversion,
                     'hilight'      : hilight,
                     'closehilight' : closehilight
                 }

    # render the template
    nml_tmpl = template.render( templateVars )

    # set the full path of the HTML file
    html_filepath = os.path.join(OUTROOT, options.htmlfile[0])

    # write the output file
    with open( html_filepath, 'w') as html:
        html.write(nml_tmpl)

    return "HTML file created at " + html_filepath

###############################################################################
def MARBL_get_array_len(array_len, MARBL_settings):
###############################################################################
    if isinstance(array_len,int):
        return array_len
    if array_len == "_tracer_list":
        return MARBL_settings.get_tracer_cnt()
    if array_len in MARBL_settings.settings_dict.keys():
            return MARBL_settings.settings_dict[array_len]
    sys.exit("ERROR: %s is unknown array length" % array_len)

###############################################################################



###
# main ops
###
if __name__ == "__main__":
    # set the arguments
    options = get_arguments()

    # set the current directory
    dir_current = os.getcwd()

    # try the main function
    try:
        status = _main_(options, dir_current)
        sys.exit(status)
    except Exception as error:
        print(str(error))
        traceback.print_exc()
        sys.exit(1)




