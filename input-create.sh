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

# quick output of the variables
echo "CIMEROOT is set to: $CIMEROOT"
echo "CESMROOT is set to: $CESMROOT"
echo "OUTROOT is set to: $OUTROOT"

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
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/components/cam/cime_config/config_component.xml --comp CAM --htmlfile $OUTROOT/cam_input.html --compversion 6.0

# DATM
echo "DATM"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/cime/src/components/data_comps/datm/cime_config/config_component.xml --comp DATM --htmlfile $OUTROOT/datm_input.html --compversion 2.1

# CLM
echo "CLM5"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/components/clm/cime_config/config_component.xml --comp CLM --htmlfile $OUTROOT/clm5_0_input.html --comptag release-clm5.0.25

# DLND
echo "DLND"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/cime/src/components/data_comps/dlnd/cime_config/config_component.xml --comp DLND --htmlfile $OUTROOT/dlnd_input.html --compversion 2.0

# MOSART
echo "MOSART"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/components/mosart/cime_config/config_component.xml --comp MOSART --htmlfile $OUTROOT/mosart_input.html

# RTM
echo "RTM"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/components/rtm/cime_config/config_component.xml --comp RTM --htmlfile $OUTROOT/rtm_input.html

# DROF
echo "DROF"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/cime/src/components/data_comps/drof/cime_config/config_component.xml --comp DROF --htmlfile $OUTROOT/drof_input.html --compversion 2.0

# POP2
# pop namelist required *a lot* of manual edits to get it parse through CIME tools and namelist_defaults.xml is kinda hopeless
echo "POP2"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/components/pop/cime_config/config_component.xml --comp POP2 --htmlfile $OUTROOT/pop2_input.html

# DOCN 
# required a tweek to the "QOBS" string in DOCN_MODE desc because the quotes were invalid ascii characters
echo "DOCN"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/cime/src/components/data_comps/docn/cime_config/config_component.xml --comp DOCN --htmlfile $OUTROOT/docn_input.html --compversion 2.0

# CICE
echo "CICE"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/components/cice/cime_config/config_component.xml --comp CICE --htmlfile $OUTROOT/cice_input.html --compversion 5.0

# DICE
echo "DICE"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/cime/src/components/data_comps/dice/cime_config/config_component.xml --comp DICE --htmlfile $OUTROOT/dice_input.html --compversion 2.0

# WW3
echo "WW3"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/components/ww3/cime_config/config_component.xml --comp WW3 --htmlfile $OUTROOT/ww3_input.html

# DWAV
echo "DWAV"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/cime/src/components/data_comps/dwav/cime_config/config_component.xml --comp DWAV --htmlfile $OUTROOT/dwav_input.html --compversion 2.0

# CISM
echo "CISM"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/components/cism/cime_config/config_component.xml --comp CISM --htmlfile $OUTROOT/cism_input.html

# Driver
echo "DRIVER"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/cime/src/drivers/mct/cime_config/config_component.xml --comp Driver --htmlfile $OUTROOT/drv_input.html

# Driver input cesm
echo "DRIVER CESM"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/cime/src/drivers/mct/cime_config/config_component_cesm.xml --comp Driver --htmlfile $OUTROOT/drv_input_cesm.html

# DESP
echo "DESP"
python input-html.py --cesmmodel 2.1.4 --inputfile $CESMROOT/cime/src/components/data_comps/desp/cime_config/config_component.xml --comp DESP --htmlfile $OUTROOT/desp_input.html --compversion 2.0










