#!/usr/bin/env python

import sys

macros = []

output_buffer = []

#
# this is a simple, not very efficient macro parser
#
# for bigger stuff (like the itemID replacer) we use regular expressions
#
# but the file size of these config files usually is low enough to work with O(n**2)
#
if __name__ == "__main__":
    with open(sys.argv[2], "r") as macro_reader:
        for macro in macro_reader:
            if not macro.find("#") == 0:
                macros.append(macro.replace("\r", "").replace("\n", ""))

    with open(sys.argv[1], "r") as file_reader:
        for line in file_reader:
            for macro in macros:
                if line.find(macro.split(";")[0]) > 0:
                    line = line.replace(macro.split(";")[1], macro.split(";")[2])

            output_buffer.append(line)

    for line in output_buffer:
        sys.stdout.write(line)

