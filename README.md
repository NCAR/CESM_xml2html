# CESM xml2html

Python tools for auto-generating HTML from CESM and CIME XML configuration files. The jinja2 template files use the CESM web site skins and styles. Modeling groups other than CESM will want to modify the templates for their specific model.



## Requirements
  
- CIME >= maint-5.6
- CESM >= 2.0.beta09
- [jinja2](https://pypi.org/project/Jinja2/)
- git


## Instructions
Copy `paths.default.txt` to a new file called `paths.txt` and update the values for `CIMEROOT CESMROOT OUTROOT` to their respective paths. Then run the scripts below to generate the HTML files. **Note** you must update the paths for each version of CESM you are running the scripts for.

### Python scripts
The following scripts are used to generate each individual HTML file based on the parameters passed.

#### namelist-html.py (previously nmldef2html.py)
Parses a namelist XML file and generates a namelist definition HTML page. These pages will be used as the namelist definition pages on the [Component Configuration Settings page](https://docs.cesm.ucar.edu/models/cesm2/settings/current/) which are the `/models/cesm2/settings/$CESM_VERSION/*_nml.html` pages.

**Note** some namelist values are not valid in XML. The `&` character needs to be manually modified to be `&amp;` in order for the schema checks to work correctly.

Usage:
> python namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/cam/bld/namelist_files/namelist_definition.xml --comp CAM --htmlfile cam_nml.html --compversion 6.0

This example will:
- Set the CESM model version for use in the HTML otutput files
- Set the XML CAM namelist file "namelist_definition.xml" 
- Set the "CAM" component 
- Set the filename to save the HTML file which uses OUTROOT set in paths.txt
- Set the compversion for the CAM component to "6.0"

You can view the file either locally or copy the HTML file to a web server for remote viewing with correct styles and theme.

Help:
> python namelist-html.py -h



#### input-html.py (previously compinputdef2html.py)
Parses a component config XML file and generates a component input parameter HTML page. These pages will be used as the CASEROOT Variable Definitions on the [Component Configuration Settings page](https://docs.cesm.ucar.edu/models/cesm2/settings/current/) which are the `/models/cesm2/settings/$CESM_VERSION/*_input.html` pages.

Usage:
> python input-html.py --cesmmodel 2.1.5 --inputfile $CESMROOT/components/cam/cime_config/config_component.xml --comp CAM --htmlfile cam_input.html --compversion 6.0

This example will:
- Set the CESM model version for use in the HTML otutput files
- Set the XML CAM config file "config_component.xml" 
- Set the "CAM" component 
- Set the filename to save the HTML file which uses OUTROOT set in paths.txt
- Set the compversion for the CAM component to "6.0"

You can view the file either locally or copy the HTML file to a web server for remote viewing with correct styles and theme.

Help:
> python input-html.py -h



#### compset-html.py (previously compsetdef2html.py)
Creates the Component Sets Definitions page based on CESM model version. This page will be used as the Component Sets on the [Configurations & Grids page](https://docs.cesm.ucar.edu/models/cesm2/config/) which are the `/models/cesm2/config/$CESM_VERSION/compsets.html` pages.

Usage:
> python compset-html.py --version 2.1.5 --htmlfile compsets.html

This example will:
- Set the CESM model version for use in the HTML otutput files
- Set the filename to save the HTML file which uses OUTROOT set in paths.txt

You can view the file either locally or copy the HTML file to a web server for remote viewing with correct styles and theme.

This file uses a symlink so that the current version is the default shown. So after the file has been uploaded into the correct CESM version directory, will need to update the symlink:
```
rm /$WEBROOT/models/cesm2/config/compsets.html
ln -s /$WEBROOT/models/cesm2/config/$CESM_VERSION/compsets.html
```

Help:
> python compset-html.py -h



#### grids-html.py (previously griddef2html.py)
Creates the Grid Resolution Definitions page based on CESM model version. This page will be used as the Grid Resolutions on the [Configurations & Grids page](https://docs.cesm.ucar.edu/models/cesm2/config/) which are the `/models/cesm2/config/$CESM_VERSION/grids.html` pages.

Usage:
First will need to generate the grids.txt file for use in the script:
> $CESMROOT/cime/scripts/query_config --grids --long > grids.txt

Then edit the grids.txt to remove all lines up to the first line containing 'alias:'
Once done can run the python script to generate the HTML file:
> python grids-html.py --version 2.1.5 --htmlfile grids.html --txtfile /fully-qualified-path-to/grids.txt

This example will:
- Set the CESM model version for use in the HTML otutput files
- Set the filename to save the HTML file which uses OUTROOT set in paths.txt
- Set the grids.txt file generated in the first step

You can view the file either locally or copy the HTML file to a web server for remote viewing with correct styles and theme.

This file uses a symlink so that the current version is the default shown. So after the file has been uploaded into the correct CESM version directory, will need to update the symlink:
```
rm /$WEBROOT/models/cesm2/config/grids.html
ln -s /$WEBROOT/models/cesm2/config/$CESM_VERSION/grids.html
```

Help:
> python grids-html.py -h



#### machines-html.py (previously machdef2html.py)
Creates the Machine Definitions page based on CESM model version. This page will be used as the Supported Machines and Compilers on the [Configurations & Grids page](https://docs.cesm.ucar.edu/models/cesm2/config/) which are the `/models/cesm2/config/$CESM_VERSION/machines.html` pages.

Usage:
> python machines-html.py --version 2.1.5 --htmlfile machines.html --supported cheyenne,hobart --tested cori,edison,stampede2,bluewaters,theta

This example will:
- Set the CESM model version for use in the HTML otutput files
- Set the filename to save the HTML file which uses OUTROOT set in paths.txt
- Set the list of supported machines
- Set the list of tested machines

You can view the file either locally or copy the HTML file to a web server for remote viewing with correct styles and theme.

This file uses a symlink so that the current version is the default shown. So after the file has been uploaded into the correct CESM version directory, will need to update the symlink:
```
rm /$WEBROOT/models/cesm2/config/machines.html
ln -s /$WEBROOT/models/cesm2/config/$CESM_VERSION/machines.html
```

Help:
> python machines-html.py -h



### Shell scripts
The following scripts are used to generate all HTML files using the python scripts with preset parameters. You will need to edit these to match the version of CESM/Components you are generating the files for as well as the XML file paths.

The model component version values can be found in the CESM Externals.cfg file.

These HTML files uses a symlink so that the current version is the default shown. So after the files has been uploaded into the correct CESM version directory, will need to update the symlink:
```
rm /$WEBROOT/models/cesm2/settings/current
ln -s /$WEBROOT/models/cesm2/settings/$CESM_VERSION current
```

#### namelist-create.sh (previously gen_all_nml)
Uses the `namelist-html.py` script to generate all namelist definition pages using preset parameters for each component.

#### input-create.sh (previously gen_all_input)
Uses the `input-html.py` script to generate all component input pages using preset parameters for each component.



### Include files
With each new version of CESM HTML files created, you will need to update the include files which control the dropdowns for switching between model versions.




