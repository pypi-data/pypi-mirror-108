# Introduction

Supsim is a software developed for studying two-predictor suppressor effects via computerized simulations. It is developed by Morteza Nazifi and Hamid Fadishei at University of Bojnord. More information about this project can be found in [the project site](https://supsim.netlify.app/)

# Installation

Supsim can be installed easily by using the Python 3 pip command.

    pip3 install supsim

You can check whether the installation went ok by running this command:

    supsim --help

## Troubleshooting

If you get an error complaining that pip3 command is not available, then you should check your system to see if you have Python3 and pip installed:  

    python3 --version
    pip --version

If you get an error, then you should install them. For example, Debian-based Linux users can run:

    sudo apt install python3 python3-pip

Windows users should install Python 3 from the official site. They should also note that the command is usually python and pip (not python3 and pip3) in their environment

If Supsim is installed without any error, but can not be executed from command line after installation, make sure that you have the python distributed scripts executable path included in your operating system PATH environment variable. Linux users should usually add \$HOME/.local/bin to PATH, for example by adding this line to \$HOME/.bashrc file and re-open the terminal:

    export PATH=$PATH:$HOME/.local/bin

Windows users should edit the system environment variable from Windows settings and add a path like C:\\Users\\\<Username\>\\AppData\\Local\\Programs\\Python\\Python\<Version\>\Scripts\ to PATH variable

# Web-based Version

A web-based Javascript implementation of supsim is also available at [the project site](https://supsim.netlify.app/supsim/) which can be used to see it in action without any hassle.

# Terms of Use

Supsim software is published under the terms of [GNU General Public License v3.0 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.en.html).