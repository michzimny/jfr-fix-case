# JFR Fix Case

Fixes letter case in filenames generated by JFR bridge apps.

Currently by JFR Pary only.

## Usage

To process directories top-down starting from the current working directory, run:

`python3 fix-case.py`

It does not work in file systems that are case insensitive.

## Use case

Some FTP clients (?) breaks letter case in filenames. 
This script fixes such broken filenames.
