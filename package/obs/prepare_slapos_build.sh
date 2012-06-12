#!/bin/bash

VERSION=0.25
RECIPE_VERSION=0.88

CURRENT_RECIPE_VERSION=$(cat ./slapos-recipe-version)
CURRENT_VERSION=$(cat ./slapos-version)

CURRENT_DIRECTORY="$(pwd)"
TEMPLATES_DIRECTORY=$CURRENT_DIRECTORY/templates
SLAPOS_FORMER_DIRECTORY=slapos-node_$CURRENT_VERSION+$CURRENT_RECIPE_VERSION+0
SLAPOS_DIRECTORY=slapos-node_$VERSION+$RECIPE_VERSION+0


set -e


# Prepare Makefile and offline script
sed "s/\%RECIPE_VERSION\%/$RECIPE_VERSION/g;s/\%VERSION\%/$VERSION/g" $TEMPLATES_DIRECTORY/Makefile.in > $CURRENT_DIRECTORY/$SLAPOS_FORMER_DIRECTORY/slapos/Makefile
sed "s/\%RECIPE_VERSION\%/$RECIPE_VERSION/g;s/\%VERSION\%/$VERSION/g" $TEMPLATES_DIRECTORY/offline.sh.in > $CURRENT_DIRECTORY/$SLAPOS_FORMER_DIRECTORY/slapos/offline.sh


# Prepare Download Cache for SlapOS 
cd $CURRENT_DIRECTORY/$SLAPOS_FORMER_DIRECTORY/slapos/
rm -rf build/
bash offline.sh


# Rename folder and Prepare tarball
cd $CURRENT_DIRECTORY
if [ $RECIPE_VERSION != $CURRENT_RECIPE_VERSION ]
then
mv $SLAPOS_FORMER_DIRECTORY $SLAPOS_DIRECTORY
fi
rm $SLAPOS_FORMER_DIRECTORY.tar.gz
tar -czf $SLAPOS_DIRECTORY.tar.gz $SLAPOS_DIRECTORY


#################    Prepare obs   ###################################
cd $CURRENT_DIRECTORY/home:VIFIBnexedi/SlapOS-Node

# Remove former configuration
osc rm -f $SLAPOS_FORMER_DIRECTORY.tar.gz
osc rm -f slapos.spec

# Prepare new tarball
cp $CURRENT_DIRECTORY/$SLAPOS_DIRECTORY.tar.gz .
osc add $SLAPOS_DIRECTORY.tar.gz

# Prepare new specfile
sed "s/\%RECIPE_VERSION\%/$RECIPE_VERSION/g;s/\%VERSION\%/$VERSION/g" $TEMPLATES_DIRECTORY/slapos.spec.in > slapos.spec
osc add slapos.spec

# Upload new Package
osc commit -m " New SlapOS Recipe $RECIPE_VERSION"

# Save current version
echo "$RECIPE_VERSION" > $CURRENT_DIRECTORY/slapos-recipe-version  
echo "$VERSION" > $CURRENT_DIRECTORY/slapos-version  
