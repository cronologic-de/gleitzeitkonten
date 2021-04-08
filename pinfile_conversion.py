import streamlit as st
import pandas as pd
import re
import base64
from datetime import datetime

# convert Altiums pin csv to Xilinx xgc
st.title(f"Altium to Xilinx Pinout File Conversion")
remove_power    = st.checkbox("Remove power",                value=True,  help = "Uncheck if power signals shall be included in the output")
remove_unused   = st.checkbox("Remove unused",               value=True,  help = "Uncheckl to keep signals name 'NetU*_'") 
rename_minus    = st.checkbox("Replace minus by underscore", value=True,  help = "Uncheck if minus shall remain in signal name")
create_vectors  = st.checkbox("Create vectors",              value=True,  help = "Change signals ending in numerals into vectors")
as_comments     = st.checkbox("Output as comments",          value=False, help = "check to format output as comments")

#regex to check whether e pin name is a power signal 
is_power_re  = re.compile(r"GND|VCC|MGTAVTT|MGTAVCC|MGTVCCAUX")
is_unused_re = re.compile(r"NetU\d+_")
vector_re = re.compile(r"(\w*\D)(\d+)(_N$|_P$|$)")

# return True if this Tupel is not a power signal
def is_not_power(pin):
    return is_power_re.match(pin[2]) is None

# return True if the net is not an unused net of format NetU1_ 
def is_used(pin):
    return is_unused_re.match(pin[1]) is None

#replace - by _
def minus_to_underscore(pin):
    return (pin[0], pin[1].replace('-', '_'), pin[2])

#replace signal0_p with signal_p[0]
def create_vector(pin):
    m = vector_re.match(pin[1])
    if m is None:
        return pin
    name = f"{m.group(1)}{m.group(3)}[{m.group(2)}]"
    return(pin[0], name, pin[2])

# crate a list of tuples (pin, net name, pin name) that are not power signals
def read_pinfile(pinfile):
    pins = {}
    df = pd.read_csv(pinfile, comment='#')
    pins = [(row[0], row[1], row[2]) for row in df.values]
    return pins

# we want vectors to show up in the right order
def sort_key(pin):
    m = vector_re.match(pin[1])
    if m is None:
        return pin[1]
    return f"{m.group(1)}{int(m.group(2)):06}{m.group(3)}"

# format pin mappings in XDC format
def create_xdc(pins, prefix):
    lines = list()
    lines.append(f"""
# pin constraints automatically created from Altium pin table {str(datetime.now())}
# see https://github.com/cronologic-de/pinfile_conversion for source code and license of the conversion tool
#
# created by cronologic GmbH & Co. KG
# https://www.cronologic.de
""")
    for pin in pins:    
         lines.append(f"set_property PACKAGE_PIN {pin[0]:<4} [get_ports {pin[1]:<16}]; #{pin[2]}")
    return f"\n{prefix}".join(lines)  # this works because introduction shall not get prefix

# create a download link for a text
def download_txt(txt, filename, linktext):
    b64 = base64.b64encode(txt.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{linktext}</a>'

# main body
pinfile = st.file_uploader("Upload CSV",type=['csv'])
if pinfile is not None:
    "File accepted!"
    pins  = read_pinfile(pinfile)

    if remove_power:
      pins =  filter(is_not_power, pins)  

    if remove_unused: 
      pins =  filter(is_used, pins)  
    
    if rename_minus: 
      pins = list(map(minus_to_underscore, pins ))

    pins = sorted(pins, key=sort_key)

    if create_vectors:
      pins = list(map(create_vector, pins))

    prefix = "# " if as_comments else ""

    # download link
    st.markdown(download_txt(create_xdc(pins, prefix), "pin.xdc", "Download XDC"), unsafe_allow_html=True)

"""
___
# pinfile_conversion
Very simple Conversion tool from Altium pin files to Xilinx xdc constraints.

## Objective
When designing an FPGA PCB projects with Altium Designer you can export a list of the FPGA pins. To make them usable with the Xilinx Vivado desing software, the file needs to be converted to a [Xilinx xdc constraints file](http://www.verien.com/xdc_reference_guide.html).  

The uploaded '.csv' needs ot have the following Fprmat
* pin location in column 0
* signal name in column 2
* pin name in column 2

[cronologic GmbH & Co. KG](https://www.cronologic.de/) is using this utility in the development of its time-to-digital converters and digitizer boards.

## Source Code
The source code of this utility is hosted on [GitHub](https://github.com/cronologic-de/pinfile_conversion). 

## License

The code in this repository is licensed under the [Mozilla Public License 2.0](https://github.com/cronologic-de/pinfile_conversion/blob/main/LICENSE). This more or less means that you can do with this code whatever you want, but if you improve the code you shall make your changes available ot others upon request. Please read the license for additional details. 

We encourage you to contribute to this repository. By uploading to this repository you agree to make your changes available under the beforementioned license.

## Imprint

This online service is provided by:
    cronologic GmbH & Co. KG
    Jahnstraße 49
    60318 Frankfurt
    Germany
    [www.cronologic.de](https://www.cronologic.de/contact)
    ++49 69 173 20 25 61

## Privacy Policy
The online services is hosted by Streamlit. Please refer to their [privacy policy](https://streamlit.io/privacy-policy).
Cronologic does not have access to any data collected by Streamlit. Cronologic itself does not collect any data in conjunction with this service.
Data privacy officer at cronologic is Kolja Sulimma. You can contact him at the address provided above.

"""
