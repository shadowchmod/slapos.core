#!/bin/bash

VERSION=0.25
RECIPE_VERSION=0.87
TARGET_DIRECTORY=/opt/slapos
BUILD_ROOT_DIRECTORY="$(pwd)/build"
BUILD_DIRECTORY=$BUILD_ROOT_DIRECTORY$TARGET_DIRECTORY
BOOTSTRAP_URL='http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py'

#./configure --prefix=/opt/slapos/parts/<NAME>

echo "Preparing source tarball (recipe version: $RECIPE_VERSION)"
echo " Build Directory: $BUILD_DIRECTORY "
echo " Buildroot Directory: $BUILD_ROOT_DIRECTORY "

mkdir -p $BUILD_DIRECTORY
mkdir $BUILD_DIRECTORY/extends-cache
mkdir $BUILD_DIRECTORY/download-cache

echo "$BUILD_DIRECTORY" > ./original_directory


sed  "s/\%RECIPE_VERSION\%/$RECIPE_VERSION/g;s|\%PATCHES_DIRECTORY\%|$PATCHES_DIRECTORY|g;s|\%TARGET_DIRECTORY\%|$TARGET_DIRECTORY|g;s|\%BUILD_ROOT_DIRECTORY\%|$BUILD_ROOT_DIRECTORY|g;s|\%BUILD_DIRECTORY\%|$BUILD_DIRECTORY|g" buildout.cfg.in > $BUILD_DIRECTORY/buildout.cfg 


# Build first time to get download-cache and extends-cache ready
cd $BUILD_DIRECTORY
wget $BOOTSTRAP_URL -O bootstrap.py
python -S bootstrap.py #&& \
    ./bin/buildout -v

cd $BUILD_DIRECTORY/..

# remove all files from build keeping only caches
echo "Deleting unecessary files to reduce source tarball size"

# TODO: Figure out why there is no write permission even for
#       the owner
chmod -R u+w $BUILD_DIRECTORY

# Buildout files
rm -rfv $BUILD_DIRECTORY/downloads

rm -fv $BUILD_DIRECTORY/bootstrap.py $BUILD_DIRECTORY/buildout.cfg \
        $BUILD_DIRECTORY/.installed.cfg \
	$BUILD_DIRECTORY/environment.*

rm -rfv $BUILD_DIRECTORY/parts/
rm -rfv $BUILD_DIRECTORY/eggs/
rm -rfv $BUILD_DIRECTORY/develop-eggs/
rm -rfv $BUILD_DIRECTORY/bin


# Removing empty directories
find $BUILD_DIRECTORY -type d -empty -prune -exec rmdir '{}' ';'


# Prepare buildout 
sed  "s/\%RECIPE_VERSION\%/$RECIPE_VERSION/g;s|\%PATCHES_DIRECTORY\%|$PATCHES_DIRECTORY|g;s|\%TARGET_DIRECTORY\%|$TARGET_DIRECTORY|g;s|\%BUILD_ROOT_DIRECTORY\%|$BUILD_ROOT_DIRECTORY|g;s|\%BUILD_DIRECTORY\%|$BUILD_DIRECTORY|g" buildout.cfg.in > $BUILD_DIRECTORY/buildout.cfg 



cd $BUILD_DIRECTORY && \
    wget $BOOTSTRAP_URL -O bootstrap.py && \
    python -S bootstrap.py 


# Removing Python byte-compiled files (as it will be done upon
# package installation) and static libraries
find $BUILD_DIRECTORY -regextype posix-extended -type f \
	-iregex '.*/*\.(py[co]|[l]?a|exe|bat)$$' -exec rm -fv '{}' ';'





