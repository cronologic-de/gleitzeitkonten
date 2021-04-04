# pinfile_conversion
Very simple Conversion tool from Altium pin files to Xilinx xdc constraints.

## Objective
When designing an FPGA PCB projects with Altium Designer you can export a list of the FPGA pins. To make them usable with the Xilinx Vivado desing software, the file needs to be converted to a [Xilinx xdc constraints file](http://www.verien.com/xdc_reference_guide.html).  

[cronologic GmbH & Co. KG](https://www.cronologic.de/) is using this utility in the development of its time-to-digital converters and digitizer boards.

## Usage
### Online
An instance of this project will be hosted on [streamlit.io](https://streamlit.io/).
You can upload an Altium .csv pinout file for your FPGA and download the xdc.

### Local
To run the tool locally on your computer you need to have Python and Streaml.it installed. Copy `pinfile_conversion.py` to your computer or clone this repository and run
```shell
streamlit run pinfile_conversion.py
```

## Source Code
The source code of this utility is hosted on [GitHub](https://github.com/cronologic-de/pinfile_conversion). 

## License

The code in this repository is licensed under the [Mozilla Public License 2.0](LICENSE). This more or less means that you can do with this code whatever you want, but if you improve the code you shall make your changes available ot others upon request. Please read the license for additional details. 

We encourage you to contribute to this repository. By uploading to this repository you agree to make your changes available under the beforementioned license.
