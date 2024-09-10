# CESM xml2html

Python tools for auto-generating HTML from CESM and CIME XML configuration files. The jinja2 template files use the CESM web site skins and styles. Modeling groups other than CESM will want to modify the templates for their specific model.



## Requirements
  
- CIME >= maint-5.6
- CESM >= 2.0.beta09
- [jinja2](https://pypi.org/project/Jinja2/)


## Instructions
Copy `paths.default.txt` to a new file called `paths.txt` and update the values for `CIMEROOT CESMROOT OUTROOT` to their respective paths. Then run the scripts below to generate the HTML files.

### Python scripts
The following scripts are used to generate each individual HTML file based on the parameters passed.

#### namelist-html.py (previously nmldef2html.py)
Parses a namelist XML file and generates a namelist definition HTML page. These pages will be used as the namelist definition pages on the [Component Configuration Settings page](https://docs.cesm.ucar.edu/models/cesm2/settings/current/) which are the `/models/cesm2/settings/$CESM_VERSION/*_nml.html` pages.

**Note** some namelist values are not valid in XML. The `&` character needs to be manually modified to be `&amp;` in order for the schema checks to work correctly.

Usage:
> ./namelist-html.py --cesmmodel 2.1.5 --nmlfile $CESMROOT/components/cam/bld/namelist_files/namelist_definition.xml --comp CAM --htmlfile $OUTROOT/cam_nml.html --compversion 6.0

This example will:
- Set the CESM model version for use in the HTML otutput files
- Set the XML CAM namelist file "namelist_definition.xml" 
- Set the "CAM" component 
- Set the path and filename to save the HTML file 
- Set the compversion for the CAM component to 6.0

You can view the file either locally or copy the HTML file to a web server for remote viewing with correct styles and theme.
  
Help:
> ./namelist-html.py -h


### Shell scripts
The following scripts are used to generate all HTML files using the python scripts with preset parameters. 

#### namelist-create.sh (previously gen_all_nml)
Uses the `namelist-html.py` script to generate all namelist definition pages using preset parameters for each component.


***************************************************
Steps to generate compsets html 

   >compsetdef2html.py --htmlfile compsets.html --version CESM2.Y.Z

Update the /cesmweb/html/models/cesm2/config/2.Y.Z/rows-include-comp.html
files to include the new version in the pulldown option menu

rm /cesmweb/html/models/cesm2/config/compsets.html
ln -s /cesmweb/html/models/cesm2/config/2.Y.Z/compsets.html

***************************************************
Steps to generate the grids html

1. run cime/scripts/query_config --grids --long > grids.txt
2. edit the grids.txt to remove all lines up to the first line containing 'alias:'
2. run griddef2html.py --txtfile /fully-qualified-path-to/grids.txt --htmlfile /fully-qualified-path-to/grids.html --version CESM2.Y.Z

update all the /cesmweb/html/models/cesm2/config/2.Y.Z/grids.html files with new version in pulldown option menu
rm /cesmweb/html/models/cesm2/config/grids.html
ln -s /cesmweb/html/models/cesm2/config/2.Y.Z/grids.html

***************************************************
Steps to generate the machines html

   >machdef2html.py --htmlfile /fully-qualified-path-to/machines.html --version CESM2.Y.Z --supported cheyenne,hobart --tested cori,edison,stampede2,bluewaters,theta

update all the /cesmweb/html/models/cesm2/config/2.Y.Z/machines.html files with new version in pulldown option menu
rm /cesmweb/html/models/cesm2/config/machines.html
ln -s /cesmweb/html/models/cesm2/config/2.Y.Z/machines.html

***************************************************


There are 2 scripts in this repo to generate all namelist definition files and all CASEROOT variable files for all components

   >gen_all_nml
   >gen_all_input

Check the variables CESMROOT and OUTPUT at the top of the files to be sure the directory paths are correct. Also, update the
model component version values to match those in the CESM Externals.cfg file.

Update the /cesmweb/html/models/settings/2.Y.Z/index.html files to include a new dropdown option in the verion menu
rm /cesmweb/html/models/settings/current
ln -s /cesmweb/html/models/settings/2.Y.Z current

