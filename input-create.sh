#!/bin/bash
#
# input-create.sh (previously gen_all_input)
#
# creates the HTML files used for input definitions
# https://docs.cesm.ucar.edu/models/cesm2/settings/$CESM_MODEL/*_input.html
#
# for each component will run input-html.py to generate HTML files
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
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/components/cam/cime_config/config_component.xml --comp CAM --htmlfile $OUTROOT/cam_input.html --comptag cam_cesm2_0_rel_02 --compversion 6.0

# CICE UPDATED
echo "CICE"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/components/cice/cime_config/config_component.xml --comp CICE --htmlfile $OUTROOT/cice_input.html --comptag cice5_cesm2_0_rel_01 --compversion 5.0

# CISM UPDATED
echo "CISM"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/components/cism/cime_config/config_component.xml --comp CISM --htmlfile $OUTROOT/cism_input.html --comptag release-cesm2.0.01

# CLM - not sure how to handle CLM4.0 since it wasn't a CIME compliant model and doesn't have a unique config_component.xml file
# CLM5 NOT UPDATED AS NOT IN OG
# NEED TO RUN TO GET clm4_5_input OR MANUAL UPDATE
echo "SKIPPING CLM"
#python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/components/clm/cime_config/config_component.xml --comp CLM --htmlfile $OUTROOT/clm5_0_input.html --comptag release-clm5.0.25
#python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/components/clm/cime_config/??? --comp CLM --htmlfile $OUTROOT/clm4_0_input.html --comptag clm4.0.81

# MOSART UPDATED
echo "MOSART"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/components/mosart/cime_config/config_component.xml --comp MOSART --htmlfile $OUTROOT/mosart_input.html --comptag release-cesm2.0.00

# POP2 UPDATED
# pop namelist required *a lot* of manual edits to get it parse through CIME tools and namelist_defaults.xml is kinda hopeless
echo "POP2"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/components/pop/cime_config/config_component.xml --comp POP2 --htmlfile $OUTROOT/pop2_input.html --comptag pop2_cesm2_0_rel_n02

# RTM UPDATED
echo "RTM"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/components/rtm/cime_config/config_component.xml --comp RTM --htmlfile $OUTROOT/rtm_input.html --comptag release-cesm2.0.00

# WW3 UPDATED
echo "WW3"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/components/ww3/cime_config/config_component.xml --comp WW3 --htmlfile $OUTROOT/ww3_input.html --comptag ww3_cesm2_0_rel_01

###### data model namelists

# DATM NOT UPDATED AS NOT IN OG
echo "SKIPPING DATM"
#python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/cime/src/components/data_comps/datm/cime_config/config_component.xml --comp DATM --htmlfile $OUTROOT/datm_input.html --comptag cime5.6.19 --compversion 2.1

# DESP UPDATED
echo "DESP"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/cime/src/components/data_comps/desp/cime_config/config_component.xml --comp DESP --htmlfile $OUTROOT/desp_input.html --comptag cime_cesm2_0_rel_03 --compversion 2.0

# DICE UPDATED
echo "DICE"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/cime/src/components/data_comps/dice/cime_config/config_component.xml --comp DICE --htmlfile $OUTROOT/dice_input.html --comptag cime_cesm2_0_rel_03 --compversion 2.0

# DLND UPDATED
echo "DLND"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/cime/src/components/data_comps/dlnd/cime_config/config_component.xml --comp DLND --htmlfile $OUTROOT/dlnd_input.html --comptag cime_cesm2_0_rel_03 --compversion 2.0

# DOCN - required a tweek to the "QOBS" string in DOCN_MODE desc because the quotes were invalid ascii characters
# UPDATED
echo "DOCN"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/cime/src/components/data_comps/docn/cime_config/config_component.xml --comp DOCN --htmlfile $OUTROOT/docn_input.html --comptag cime_cesm2_0_rel_03 --compversion 2.0

# DROF UPDATED
echo "DROF"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/cime/src/components/data_comps/drof/cime_config/config_component.xml --comp DROF --htmlfile $OUTROOT/drof_input.html --comptag cime_cesm2_0_rel_03 --compversion 2.0

# DWAV UPDATED
echo "DWAV"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/cime/src/components/data_comps/dwav/cime_config/config_component.xml --comp DWAV --htmlfile $OUTROOT/dwav_input.html --comptag cime_cesm2_0_rel_03 --compversion 2.0

# Driver UPDATED
echo "DRIVER"
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/cime/src/drivers/mct/cime_config/config_component.xml --comp Driver --htmlfile $OUTROOT/drv_input.html --comptag cime_cesm2_0_rel_03
# Driver input cesm UPDATED
python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/cime/src/drivers/mct/cime_config/config_component_cesm.xml --comp Driver --htmlfile $OUTROOT/drv_input_cesm.html --comptag cime_cesm2_0_rel_03
