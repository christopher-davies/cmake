#!/usr/bin/python
#
# Configuration Maker - cmake.py 
# Author: Chris Davies VMB DS
# Started: July 2019
#
# Command line options
# -w = write configs to filesystem
# -d = display configs to display
# -h = Show help
# -c filename.csv = Import a customer data CSV different to the default.
# -b filename.txt = Import a base config file different to the default.
# -s siteRef = Select a single site to process site 1 is the first line of config data below the heading.
#
# Summery of events
# 1. Script imports a customer data CSV named `config-data.csv`, the top row(0) headings become {keys}.
# 2. A base IOS config file is imported with {keys} enclosed in curly brackets.
# 3. Customer data is checked for site individual config filename below a key called template1, if found the additional config template is loaded into a dictionary.
# 4. The {keys} strings are replaced aon the base+individual configs.
# 5. Configs are either displayed to screen or written to the filesystem depending on the command line switch.

# # Import Modules
# required for working with files, folders
import os
# required for working with CSV files
import csv
# required for array use
import array
# required for command line arguments
import sys
# required for command line argument processing
import getopt

# Script Variables /  Define defaults here!
config_data_filename = 'config-data.csv'
base_config_filename = 'base-config.txt'
option_config_data_filename = ''
option_base_config_filename = ''
cwd = os.getcwd()
script_name = os.path.basename(__file__)
version = "16"
title = "Configuration Maker"
write_config_files = "N"
display_config_files = "N"
option_site_request = 0
template1_config = dict()
template1_filename_list = []
template1_filename_list_unique = []

# Collect command line arguments
argument_count = len(sys.argv)
argument_list =  str(sys.argv)

# Title
print("# " + title + " - Version " + version)
print("Argument List: " + argument_list)

# Process command line arguments
def main(argv):
   # Assign global status to variables so they can be used outside of this definition
   global write_config_files
   global display_config_files
   global option_config_data_filename
   global option_base_config_filename
   global config_data_filename
   global base_config_filename
   global option_site_request
   # Collect command line arguments.
   try:
      opts, args = getopt.getopt(argv,"hwdc:b:s:",["cdfile=","bcfile=","site="])
   except getopt.GetoptError:
      print (script_name + ' -c <option_config_data_filename> -b <option_base_config_filename> -w (write configs to FS) -d (display configs)')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print (script_name + ' -c <option_config_data_filename> -b <option_base_config_filename> -w (write configs to FS) -d (display configs)')
         sys.exit()
      elif opt in ("-s", "--site"):
         option_site_request = int(arg)
         print ("Command line option -s | Request site config: " , option_site_request)
      elif opt in ("-c", "--cdfile"):
         option_config_data_filename = config_data_filename = arg
         print ("Command line option -c | Defined config data file: " + option_config_data_filename)
      elif opt in ("-b", "--bcfile"):
         option_base_config_filename = base_config_filename = arg
         print ("Command line option -b | Base template config file: " + option_base_config_filename)
      elif opt == '-w':
         write_config_files = "Y"
         print ("Command line option -w | Write config files to local filesystem.")
      elif opt == '-d':
         display_config_files = "Y"
         print ("Command line option -d | Display config files.")

if __name__ == "__main__":
   main(sys.argv[1:])

# Check config_data_filename exists
from pathlib import Path
my_file = Path(config_data_filename)
if my_file.is_file():
    # file exists
    print ("Confirmed configuration data file exists: " + config_data_filename)
else:
    # File is missing
    exit("Configuration data file is missing, I will now die!")

# Check base config exists
from pathlib import Path
my_base_config_file = Path(base_config_filename)
if my_base_config_file.is_file():
    # file exists
    print ("Confirmed base configuration file exists: " + base_config_filename)
else:
    # File is missing
    exit("Base configuration file is missing, I will now die!")

# Show Display config options
if (display_config_files == "Y"):
   print ("Generated configs WILL be displayed to the screen.")
else:
   print ("Generated configs will NOT be displayed to the screen. Use -d argument to display configs.")

# Show Write config options
if (write_config_files == "Y"):
   print ("Generated configs WILL be written to the filesystem.")
else:
   print ("Generated configs will NOT be written to the filesystem. Use -w argument to write configs.")

# Read config_data_filename CSV into an array - data[{row}][{col}]
with open(config_data_filename, newline='') as csvfile:
    data = list(csv.reader(csvfile))

# If a site ref is requested then create a new data list with just headings row(0) and that site data only
if (option_site_request > 0) and (option_site_request <= len(data)-1):
   mergedlist = []
   mergedlist.append(data[0])
   mergedlist.append(data[option_site_request])
   data = mergedlist

# Count number of sites.
sitecount = len(data)-1
print ("Number of sites found in `" + config_data_filename + "`: ", sitecount)

# Force keys to be lower case
data[0] =  ([x.lower() for x in data[0]])

# Count the number of keys
keycount = len(data[0])
print ("\n# Number of keys found in `" + config_data_filename + "`: ", keycount, "(Keys only Forced to lowercase)")

# Create the keys for replacement in the base config.
for  i in range(len(data[0])):
    # print without newlines
    print(data[0][i], end = ', ')
    i += 1

# # Extract any additional config templates
# Check if template1 exists in the list before finding its index.
if 'template1' in data[0]:
   # template1 exists so lets get the index
   template1_index = data[0].index('template1')
   print ("\n\n# Additional configuration templates, indicated under `template1` is in index: ", template1_index)
   # Create template1_config[t] start at 1 (0 is the header), t = site
   t = 0
   while t < sitecount:
      t += 1
      # Create a variable list of template1 filenames.
      template1_filename_list.append(data[t][template1_index])

   # print the raw template1 filename list
   print (template1_filename_list)

   # Create a unique list of filenames to check they exist quickly by creating a set() of the list[]
   template1_filename_list_unique = set(template1_filename_list)
   print ("\n# List of unique filenames to check if they exist (Not in order): ")
   print (template1_filename_list_unique)

   # Check each individual file exists
   for file in template1_filename_list_unique:
      print ("Checking existance of " + file + "...", end="")
      from pathlib import Path
      my_file = Path(file)
      if my_file.is_file():
         # file exists
         print ("Exists! Loading template1 config into dictionary...")
         # Load the file
         with open (file, "r") as myfile:
            template1_load_config = myfile.read()
         # Create a dictionary with a key of the filename and value of the loaded config
         template1_config[file] = template1_load_config
      else:
         # File does not exist, assume no requirement for additional config for this site.
         print ("File not found! Using a blank template1")
         template1_config[file] = ''


# Read base configuration file into a string variable
with open(base_config_filename, 'r') as file:
    base_config = config = file.read()

# Print the base configuration to the display
print ("\n\n# This is the base configuration, keys are case-insensitive and enclosed in {}:")
print(base_config)

# Parse the config data with the base template and output data + new config to screen.
print ("\n# Parsing the configuration data and replacing the base config {tags}.")

# Loop to go though the config data rows excluding row 0 used for the keys, 1 onwards.
for x in range(len(data)-1):
    x += 1
    # Print the site number ref without a newline.
    print (x, end='')
    # Print the data for that site for ref#
    print (data[x])

    # Load the additional template1 config this one time for this site only.
    config = config + template1_config[data[x][template1_index]]

    # Loop though the key_names replacing the text
    for  y in range(len(data[0])):

        # Case-insensitive replacement
        # Example - string = re.sub('hello', 'bye', 'hello HeLLo HELLO', flags=re.IGNORECASE) = 'bye bye bye'
        # https://stackoverflow.com/questions/919056/case-insensitive-replace
        import re
        config = re.sub("{"+ data[0][y] +"}", data[x][y], config, flags=re.IGNORECASE)

        # Increment y for next tag
        y += 1

    # Print parsed config to display if -d argument set on command line.
    if (display_config_files == "Y"):
       print (config)

    # Output built config files to filesystem if -w argument set on command line.
    if (write_config_files == "Y"):
        new_file=open(data[x][0] + ".txt",mode="w")
        new_file.write(config)
        new_file.close()

    # reset template for next config file.
    config = base_config

# Output parse results.
print ("\n# Count of parsed config data and config:" , x)
