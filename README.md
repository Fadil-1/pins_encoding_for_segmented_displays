# Segment Display Binary Mapping Generator #

This repository contains a Python script to generate binary mappings for segment displays based on user-defined pin configurations and given base mappings. The script works with any number of segments provided the configuration files are set appropriately. It can be used for 7-segment, 14-segment, 16-segment displays, and more(or less).


## Features ##

    * Supports any number of segments, provided the configuration files are set appropriately.
    * Generates common cathode and common anode mappings.
    * Saves the generated binary mappings to a file in different formats.


## Segment Arrangements ##

David Madison's Segmented LED Display - ASCII Library contains great images describing the segments' arrangements
and the configurations in my base mapping examples. You can find the repository [here](https://github.com/dmadison/Segmented-LED-Display-ASCII).

![14-Segment display ASCII library. Credit: David Madison](https://github.com/dmadison/LED-Segment-ASCII/blob/master/Images/All%20Characters/14-Segment-ASCII-All.png)



## Prerequisite ##

    Python 3.x


## Usage ##

1. Clone the repository or download the script and configuration files.
2. Modify or modify a "user_config" file to match your segment display's pin configuration.
3. Run the script with your desired configuration files as input.
4. The script generates binary mappings for your specific segment display configuration and saves them to an output file.


## Default Files ##

The repository includes default base mapping and user configuration files for 7-segment, 14-segment, and 16-segment displays:

- "base_mapping_7-segment_display.json"
- "base_mapping_14-segment_display.json"
- "base_mapping_16-segment_display.json"
- "user_config_7-segment_display.json"
- "user_config_14-segment_display.json"
- "user_config_16-segment_display.json"

These files can be used for testing and as templates to create your own configuration files. 
To demonstrate how the code works, the default user configuration files all contain a pin 
configuration inverse to the default configuration.

Example: Below is the content of user_config_7-segment_display.json file.

{
  "0":"dp",
  "1":"g",
  "2":"f",
  "3":"e",
  "4":"d",
  "5":"c",
  "6":"b",
  "7":"a"
}

It indicates that pin "0" of the driving device is connected to segment "dp" on the display, and
that pin "1" of the driving device is connected to segment "g" on the display, and so on. Match 
your pin configuration to generate the characters contained in the base mapping files. 



## License ##

All contents of this repository are licensed under the terms of the MIT license.

## Acknowledgements ##

[David Madison ](https://github.com/dmadison/LED-Segment-ASCII) for the Segmented-LED-Display-ASCII library, which provided the default character mappings.

## Keywords ##

    Segment display
    Binary mapping
    Custom pin configuration
    LED display
    Common cathode
    Common anode
    EPROM
    EEPROM
