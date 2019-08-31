#! /bin/sh
#
# The gtest package installs the gtest source code to /usr/src/gtest.
# This script is called to build and install gtest static libraries
# from the previously installed source code.
# The default destination is /usr/lib and the package is built in
# /tmp/gtestbuild.$$.
#

BUILDDIR=${BUILDDIR:-"/tmp/gtestbuild.$$"}
DESTROOT=${DESTROOT:-"/usr"}
# Be aware that /usr/src/gtest is a symlink to /usr/src/googletest.
SRC=${SRC:-"/usr/src/gtest"}
PKGNAME="libgtest-dev"
PKGEXISTS=`dpkg-query -W -f '${binary:Package}\n' --no-pager ${PKGNAME}`

if []
if [ ${PKGEXISTS}"x" = "x" ]; then
  echo "${PKGNAME} is not installed. Exiting."
  exit 1
fi

if [ ! -d ${SRC} ]; then
  echo "${SRC} directory does not exist. Exiting."
  exit 1
fi

mkdir -p ${BUILDDIR}
cd ${BUILDDIR}
cmake -DCMAKE_BUILD_TYPE=RELEASE /usr/src/gtest/
make
sudo install -o root -g root -m 644 libgtest.a ${DESTROOT}/lib
sudo install -o root -g root -m 644 libgtest_main.a ${DESTROOT}/lib

