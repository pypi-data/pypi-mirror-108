#!/usr/bin/env bash

# get enmapbox project
rm -rf context/enmapbox
git clone https://bitbucket.org/hu-geomatics/enmap-box.git ./context/enmapbox
# git clone https://bitbucket.org/hu-geomatics/enmap-box.git --branch develop --single-branch ./context/enmapbox

# get EnPT project
rm -rf context/enpt
git clone git@git.gfz-potsdam.de:EnMAP/GFZ_Tools_EnMAP_BOX/EnPT.git ./context/enpt

# get SICOR project
rm -rf context/sicor
git clone git@git.gfz-potsdam.de:EnMAP/sicor.git ./context/sicor
