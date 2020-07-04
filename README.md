# Table-3-Parser
This is a utility to download and parse the "[United States Code Table III](https://uscode.house.gov/table3/table3years.htm)". Which for our purposes lets us map the sections in a particular bill, to where it resides in the USCode. The process of this "codification" is better explained by the [OLRC](https://uscode.house.gov/codification/legislation.shtml).

This tool will download table3-xml-bulk.zip from the site, and also read the html page for popular names.

It will parse the xml file into an excel file that contains all information contained.

It will output a second excel file that contains a mapping of the Popular Names of the acts. These two things combined will be used to identify references in the USCode and new legislation in the larger project.

## Requirements
- lxml>=4.0.0



## Usage
It will download approximately 15MB of data
```bash
python3 parse_2.py
```