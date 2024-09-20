#!/bin/bash
#
# namelist-create.sh (previously gen_all_nml)
#
# creates the HTML files used for namelist definitions
# https://docs.cesm.ucar.edu/models/cesm2/settings/$CESM_MODEL/*_nml.html
#
# for each component will run namelist-html.py to generate HTML files
#
# uses the paths set in paths.txt for CIME, CESM, and OUTROOT (where HTML files are saved)
#



# read the paths.txt file
# get the paths from the paths.txt file
while IFS='=' read -r key value || [ -n "$key" ]; do
    # set the values
    case "$key" in
        CIMEROOT) CIMEROOT="$value" ;;
        CESMROOT) CESMROOT="$value" ;;
        OUTROOT) OUTROOT="$value" ;;
    esac
done < paths.txt

# quick output of the variables
echo "CIMEROOT is set to: $CIMEROOT"
echo "CESMROOT is set to: $CESMROOT"
echo "OUTROOT  is set to: $OUTROOT"

# make sure paths are good to continue
read -p "Continue with the paths set? (y/n): " confirmation

# check the input
if [[ "$confirmation" =~ ^[Yy]$ ]]; then
    echo "Continuing..."
else
    echo "Exiting..."
    exit 1
fi



# CAM
echo "CAM"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/cam/bld/namelist_files/namelist_definition.xml --comp CAM --htmlfile cam_nml.html --compversion 6.0

# DATM
echo "DATM"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/datm/cime_config/namelist_definition_datm.xml --comp DATM --htmlfile datm_nml.html --compversion 2.0

# CLM5
# also desc elements, need to be pre formatted in order to wrap correctly in the data table
echo "CLM5"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/clm/bld/namelist_files/namelist_definition_clm4_5.xml --comp CLM --htmlfile clm5_0_nml.html
# CLM4
#echo "CLM4"
#python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/clm/bld/namelist_files/namelist_definition_clm4_0.xml --comp CLM --htmlfile clm4_0_nml.html
# CLM4.5
# Error: unable to parse file namelist_definition_clm4_5.xml
#echo "CLM4.5"
#python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/clm/bld/namelist_files/namelist_definition_clm4_5.xml --comp CLM --htmlfile clm4_5_nml.html

# DLND
echo "DLND"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/dlnd/cime_config/namelist_definition_dlnd.xml --comp DLND --htmlfile dlnd_nml.html --compversion 2.0

# MOSART
echo "MOSART"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/mosart/cime_config/namelist_definition_mosart.xml --comp MOSART --htmlfile mosart_nml.html

# RTM
echo "RTM"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/rtm/cime_config/namelist_definition_rtm.xml --comp RTM --htmlfile rtm_nml.html

# DROF
echo "DROF"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/drof/cime_config/namelist_definition_drof.xml --comp DROF --htmlfile drof_nml.html --compversion 2.0

# POP2
echo "POP"
# pop namelist required *a lot* of manual edits to get it to parse through the CIME tools and namelist_defaults.xml is kinda hopeless
# python namelist-html.py --cesmmodel 2.1.5 --nmlfile ./pop_namelist_files/namelist_definition_pop.xml --comp POP2 --htmlfile pop2_nml.html --comptag pop2_cesm2_1_rel_n06
# TODO FIND POP2 XML FILES
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/pop/bld/namelist_files/namelist_definition_pop.xml --comp POP --htmlfile pop2_nml.html --compversion 2.0

# MARBL
# need to run the $MARBLROOT/MARBL_tools/yaml_to_json.py script first
echo "MARBL"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/pop/externals/MARBL/defaults/json/settings_latest.json --comp MARBL --htmlfile marbl_nml.html --marbl-json

# DOCN
echo "DOCN"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/docn/cime_config/namelist_definition_docn.xml --comp DOCN --htmlfile docn_nml.html --compversion 2.0

# CICE
echo "CICE"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/cice/cime_config/namelist_definition_cice.xml --comp CICE --htmlfile cice_nml.html  --compversion 5.0

# DICE
echo "DICE"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/dice/cime_config/namelist_definition_dice.xml --comp DICE --htmlfile dice_nml.html --compversion 2.0

# WW3
echo "WW3"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/ww3/cime_config/namelist_definition_ww3.xml --comp WW3 --htmlfile ww3_nml.html

# DWAV
echo "DWAV"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/dwav/cime_config/namelist_definition_dwav.xml --comp DWAV --htmlfile dwav_nml.html --compversion 2.0

# CISM
echo "CISM"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/cism/bld/namelist_files/namelist_definition_cism.xml --comp CISM --htmlfile cism_nml.html

# Driver
echo "Driver"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/drivers/mct/cime_config/namelist_definition_drv.xml --comp Driver --htmlfile drv_nml.html

# Driver fields
echo "Driver fields"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/drivers/mct/cime_config/namelist_definition_drv_flds.xml --comp Driver --htmlfile drv_fields_nml.html

# DESP 
echo "DESP"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/desp/cime_config/namelist_definition_desp.xml --comp DESP --htmlfile desp_nml.html --compversion 2.0














