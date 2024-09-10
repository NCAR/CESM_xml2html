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

# Now you can use the variables
echo "CIMEROOT is set to: $CIMEROOT"
echo "CESMROOT is set to: $CESMROOT"
echo "OUTROOT is set to: $OUTROOT"


# CAM UPDATED
echo "CAM"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/cam/bld/namelist_files/namelist_definition.xml --comp CAM --htmlfile $OUTROOT/cam_nml.html --compversion 6.0

# CICE UPDATED
echo "CICE"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/cice/cime_config/namelist_definition_cice.xml --comp CICE --htmlfile $OUTROOT/cice_nml.html  --compversion 5.0

# CISM UPDATED
echo "CISM"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/cism/bld/namelist_files/namelist_definition_cism.xml --comp CISM --htmlfile $OUTROOT/cism_nml.html

# CLM
# had to remove one & manually in input namelist file for clm4_5
# also desc elements, need to be pre formatted in order to wrap correctly in the data table

# NOT UPDATED clm5_0_nml.html not in 2.0.0
echo "SKIPPING CLM5"
#python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/clm/bld/namelist_files/namelist_definition_clm4_5.xml --comp CLM --htmlfile $OUTROOT/clm5_0_nml.html --comptag release-clm5.0.25
# CLM4 UPDATED
echo "CLM4"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/clm/bld/namelist_files/namelist_definition_clm4_0.xml --comp CLM --htmlfile $OUTROOT/clm4_0_nml.html
# CLM4.5 UPDATED
# Error: unable to parse file namelist_definition_clm4_5.xml
echo "CLM4.5"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/clm/bld/namelist_files/namelist_definition_clm4_5.xml --comp CLM --htmlfile $OUTROOT/clm4_5_nml.html

# MARBL NOT UPDATE - MANUAL UPDATE OF HTML
# need to run the $MARBLROOT/MARBL_tools/yaml_to_json.py script first
echo "SKIPPING MARBL"
# python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/pop/externals/MARBL/defaults/json/settings_latest.json --comp MARBL --htmlfile $OUTROOT/marbl_nml.html --comptag cesm2.1-n00 --marbl-json

# MOSART UPDATED
echo "MOSART"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/mosart/cime_config/namelist_definition_mosart.xml --comp MOSART --htmlfile $OUTROOT/mosart_nml.html

# POP2 NOT UPDATED - MANUAL UPDATE OF HTML
echo "SKIPPING POP"
# pop namelist required *a lot* of manual edits to get it to parse through the CIME tools and namelist_defaults.xml is kinda hopeless
# python namelist-html.py --cesmmodel 2.1.5 --nmlfile ./pop_namelist_files/namelist_definition_pop.xml --comp POP2 --htmlfile $OUTROOT/pop2_nml.html --comptag pop2_cesm2_1_rel_n06

# RTM UPDATED
echo "RTM"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/rtm/cime_config/namelist_definition_rtm.xml --comp RTM --htmlfile $OUTROOT/rtm_nml.html

# WW3 UPDATED
echo "WW3"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/ww3/cime_config/namelist_definition_ww3.xml --comp WW3 --htmlfile $OUTROOT/ww3_nml.html

###### data model namelists

# DATM UPDATED
echo "DATM"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/datm/cime_config/namelist_definition_datm.xml --comp DATM --htmlfile $OUTROOT/datm_nml.html --compversion 2.0

# DESP UPDATED
echo "DESP"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/desp/cime_config/namelist_definition_desp.xml --comp DESP --htmlfile $OUTROOT/desp_nml.html --compversion 2.0

# DICE UPDATED
echo "DICE"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/dice/cime_config/namelist_definition_dice.xml --comp DICE --htmlfile $OUTROOT/dice_nml.html --compversion 2.0

# DLND UPDATED
echo "DLND"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/dlnd/cime_config/namelist_definition_dlnd.xml --comp DLND --htmlfile $OUTROOT/dlnd_nml.html --compversion 2.0

# DOCN UPDATED
echo "DOCN"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/docn/cime_config/namelist_definition_docn.xml --comp DOCN --htmlfile $OUTROOT/docn_nml.html --compversion 2.0

# DROF UPDATED
echo "DROF"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/drof/cime_config/namelist_definition_drof.xml --comp DROF --htmlfile $OUTROOT/drof_nml.html --compversion 2.0

# DWAV UPDATED
echo "DWAV"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/components/data_comps/dwav/cime_config/namelist_definition_dwav.xml --comp DWAV --htmlfile $OUTROOT/dwav_nml.html --compversion 2.0

# Driver UPDATED
echo "Driver"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/drivers/mct/cime_config/namelist_definition_drv.xml --comp Driver --htmlfile $OUTROOT/drv_nml.html
# Driver fields UPDATED
echo "Driver fields"
python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/cime/src/drivers/mct/cime_config/namelist_definition_drv_flds.xml --comp Driver --htmlfile $OUTROOT/drv_fields_nml.html



