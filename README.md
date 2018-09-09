# dirbpy

## Description
Dirbpy - URL Bruteforcer

This is a new version of dirb but in python. This version is faster than the normal version in C because it uses thread. Dirbpy is a Web Content Scanner. It looks for hidden Web Objects. It basically works by launching a dictionary based attack against a web server and analizing the response.

Link to the real dirb: https://github.com/v0re/dirb

## Install
`git clone https://github.com/marcolivierbouch/dirbpy.git`

`cd dirbpy`

`pip install -r requirements.txt`

If you want to add it in your system:

`sudo cp dirbpy /usr/bin/`

If you are using the fish shell (https://github.com/fish-shell/fish-shell): 

`sudo cp dirbpy.fish /usr/share/fish/completions`

## Recommendation
I recommend using the SecLists: https://github.com/danielmiessler/SecLists
