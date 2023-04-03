"""
Author: Fadil Isamotu (v1.0)
November 16, 2021
isamotufadil15@gmail.com

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
 and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import json
from math import ceil

class BinaryMappingGenerator:

    """
    BinaryMappingGenerator is a class that generates binary mappings for segment displays based on user-defined pin
    configurations(How the output pins from your driving device are connected to the display) and given base mappings.

    NB: This class can be used with any number of segments provided the configuration files are set appropriately. 

    Attributes:
        user_config (dict): A dictionary(within a .JSON input file) representing the user's pin configuration.
        base_mapping (dict): A dictionary(within a .JSON input file) representing the base a reference configuration
        for ascii characters.
        output_file (str): The output file name where the generated mapping will be saved.
    """
    def __init__(self, user_config_file, base_mapping_file, output_file):

        """
        Initializes the BinaryMappingGenerator with user's pin configuration, base mapping, and output file.

        Args:
            user_config_file (str): The file path to the JSON file containing the user's pin configuration.
            base_mapping_file (str): The file path to the JSON file containing the base mapping for characters.
            output_file (str): The output file name where the generated mapping will be saved.
        """
        # User's specific mapping.
        self.user_config = self.load_json(user_config_file)
        # Hard codded reference mapping.
        self.base_mapping = self.load_json(base_mapping_file)
        # Retrieves the binary representation of every character.
        self.characters_encoding = self.base_mapping ["characters_encoding"]
        # Retrieves the pin names on the segment display.
        self.pins_on_display = self.base_mapping ['pins_on_display']

        self.word_length = len(self.pins_on_display)
        self.output_file = output_file
        self.validate_user_config()
        

    @staticmethod
    def load_json(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data

    def validate_user_config(self):
        """
        Error handling method to ensure that the user_config file matches the characteristics of the targeted display.
        Returns:
        None
        """
        if len(self.user_config) != len(self.pins_on_display):
            raise ValueError("The number of pins in the user config must be equal to the \
                              number of bits per character in the base mapping."\
                             .replace("                              ", ''))
                                
        
        for (pin_on_driving_device, pin_on_segment_display) in self.user_config.items():
            if pin_on_segment_display not in self.pins_on_display:
                raise ValueError(f'Unknown pin "{pin_on_segment_display}". At least this pin from the user config file does not\
                                    exist in the base mapping file. Make sure to have matching pin names.'\
                                    .replace("                                   ", ''))

    def generate_binary_mapping(self, common = 'common_cathode'):
        """
        generate_binary_mapping iterates through each character and its corresponding binary encoding
        in the base mapping. For each character, it initializes an empty binary string with a length 
        equal to the number of pins/bits in the user configuration. Then, it iterates through the user-defined
        pin configuration and maps the driving device's pin to the corresponding segment pin.

        For each segment pin it assigns the corresponding bit value from the base binary string to the generated
        binary string at the position(index in the word) specified by the driving device's pin.

        Once all the binary mappings for each character have been generated, the method returns a dictionary
        containing the characters as keys and the generated binary strings as values.
        
        Returns
        dict: Generated binary mapping as a dictionary with characters as keys and binary strings as values.     
        """
        common_cathode_mapping = {}
        # The display pins are written the form MSD to LSD in the JSON file for readability.
        # It is reversed her to make sense in the code.
        pins_on_display = list(reversed(self.pins_on_display))
        
        for char, base_binary in self.characters_encoding.items():
            generated_binary = ['0']*self.word_length

            for (pin_on_driving_device, pin_on_segment_display) in self.user_config.items():
                generated_binary[int(pin_on_driving_device)] = base_binary[pins_on_display.index(pin_on_segment_display)]
            common_cathode_mapping[char] = bin(int(''.join(generated_binary),2))
        
        # Generates common anode encoding if specified in arguments.
        if common != 'common_cathode':
            common_anode_mapping = \
            {x: bin(int(y[2:].replace('0','x').replace('1', '0').replace('x', '1'),2))\
             for x, y in common_cathode_mapping.items()}
            return common_anode_mapping
        else:
            return common_cathode_mapping

    def save_generated_mapping(self, generated_mapping, output_type = 'bin_s', z = 0):
        """
        save_generated_mapping writes generated encoding in a .txt file as:
        Character_1 : Binary_encoding
                    :
                    :
                    :
                    :
        Character_n : Binary encoding

        Data can be saved in 8 formats: 
        
        bin:    binary number excluding leading_zeros
        bin_s:  binary number with 0b signature excluding leading_zeros
        bin_z:  binary number including leading_zeros
        bin_sz: binary number with 0b signature including leading zeros

        hex:    hexadecimal number excluding leading_zeros        
        hex_s:  hexadecimal number with 0x signature excluding leading_zeros
        hex_z:  hexadecimal number including leading_zeros
        hex_sz: hexadecimal number with 0x signature including leading zeros

        Ex: Consider n = 0b11011011 for a 14 segment display.

            n = 0b11011011         in "bin" format
            n = 0b11011011         in "bin_s" format
            n = 0000000011011011   in "bin_z" format
            n = 0b0000000011011011 in "bin_sz" format

            n = db                 in "hex" format
            n = 0xdb               in "bin_s" format
            n = 00db               in "hex_z" format
            n = 0x00db             in "hex_sz" format


        To add more leading zeros for any reasons, set the z(extra_leading_zeros) argument.
        to however many more trailing zeros are needed.
        
        For the example above, setting z = x, will add or subtract(as x can be a negative number) x 
        zeros to teh generated binary numbers.
        

        
        Returns:
        None
        """
        with open(self.output_file, 'w') as f:

            if output_type == 'bin':
                for char, binary in generated_mapping.items():
                    f.write(f'{char}: {binary[2:]}\n')

            elif output_type == 'bin_s':
                for char, binary in generated_mapping.items():
                    f.write(f'{char}: {binary}\n')

            elif output_type == 'bin_z':
                for char, binary in generated_mapping.items():
                    f.write(f'{char}: {binary[2:].zfill(self.word_length+z)}\n')

            elif output_type == 'bin_sz':
                for char, binary in generated_mapping.items():
                    f.write(f'{char}: 0b{binary[2:].zfill(self.word_length+z)}\n')


            elif output_type == 'hex':
                for char, binary in generated_mapping.items():
                    f.write(f'{char}: {hex(int(binary[2:], 2))[2:]}\n')

            elif output_type == 'hex_s':
                for char, binary in generated_mapping.items():
                    f.write(f'{char}: {hex(int(binary[2:], 2))}\n')

            elif output_type == 'hex_z':
                for char, binary in generated_mapping.items():
                    f.write(f'{char}: {hex(int(binary[2:], 2))[2:].zfill((4 if self.word_length <= 16 else ceil(self.word_length/4))+z)}\n')

            elif output_type == 'hex_sz':
                for char, binary in generated_mapping.items():
                    f.write(f'{char}: 0x{hex(int(binary[2:], 2))[2:].zfill((4 if self.word_length <= 16 else ceil(self.word_length/4))+z)}\n')

                


if __name__ == '__main__':
    user_config_file = './input_files/user_config_14-segment_display.JSON'
    base_mapping_file = './input_files/base_mapping_14-segment_display.JSON'
    output_file = 'out.txt'

    generator = BinaryMappingGenerator(user_config_file, base_mapping_file, output_file)
    generated_mapping = generator.generate_binary_mapping(common= 'common_cathode')
    
    # Refer to the functions's docstrings for a description of the arguments.
    generator.save_generated_mapping(generated_mapping, output_type = 'bin_sz', z = 0)
