# cmake
Cisco Configuration Maker - IOS Configs from CSV

I have written this python script to import a CSV formatted spreadsheet of customer data, like the usual project; hostnames, ip addressing, vlans etc and from this generate config files from templates.

In the CSV file the top row becomes {keys} which will be used to replace text in an imported a base config with the matching {keys} enclosed in curly brackets, {keys} are case-insensitive. 
If the CSV file indicates additional config templates under the 'template1' heading then these files will be loaded per site, handy for sites with different switch stacking. 

See the wiki for more detailed information. 
