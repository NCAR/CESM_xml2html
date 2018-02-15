# CESM xml2html

Python tools for auto-generating HTML from CESM and CIME XML configuration files.

## Requirements
  CIME v?
  
  CESM >= 2.0.beta09
  
  jinja2 template python module available from https://pypi.python.org/pypi/Jinja2
  
  >pip install --user jinja2

## Python tools

***************************************************
Steps to generate namelist definitions to html

nmldef2html.py

Synopsis:
  Parses a namelist XML file and generates a html page. Note: some namelist
  values are not valid in XML. The "&" character needs to be manually modified
  to be "&amp;" in order for the schema checks to work correctly. 

Example:
  >./nmldef2html.py 
    --nmlfile ~/cesm2_0_alpha06/cime/src/drivers/mct/cime_config/namelist_definition_drv.xml 
    --comp Driver 
    --htmlfile drv.html

  This example reads the XML namelist file "namelist_definition_drv.xml" for the
  "Driver" component and generates an output html file "drv.html".

  You can view the file either locally using:
  >open drv.html
  
  or copy the drv.html file to a web server for remote viewing.
  
Options:
  >./nmldef2html.py --help

***************************************************
Steps to generate compsets html 

   ./compdef2html.py --htmlfile compsets.html --version CESM2.0

***************************************************
Steps to generate the grids html

1. run query_config --grids --long > ./Tools/xml2html/grids.txt
2. edit the grids.txt to remove all lines up to the first line containing 'alias:'
2. ./griddef2html.py --txtfile grids.txt --htmlfile grids.html --version CESM2.0

***************************************************

Steps to generate the machines html

./machdef2html.py --htmlfile machines.html --version CESM2.0 --supported yellowstone,cheyenne --tested edison,hobart,cori-knl,cori-haswell,yellowstone,cheyenne
