%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Qt
Name            : qt-everywhere-opensource-src
Version         : 5.4.2
Release         : 0
License         : GNU GPL
Vendor          : Freescale
Packager        : Rogerio Pimentel
Group           : System Environment/Libraries
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
URL             : http://get.qt.nokia.com/qt/source/qt-everywhere-opensource-src-5.4.2.tar.gz

%Description
%{summary}

%Prep
%setup

touch .keepme

#Creating mkspec

XPLATFORM=qtbase/mkspecs/linux-none-arm-gnueabi-g++

mkdir -p $XPLATFORM

initscript=$XPLATFORM/qmake.conf
cat > $initscript << EOF
#
# qmake configuration for building with arm-linux-gnueabi-g++
#

MAKEFILE_GENERATOR      = UNIX
CONFIG                 += incremental
QMAKE_INCREMENTAL_STYLE = sublib

include(../common/linux.conf)
include(../common/gcc-base-unix.conf)
include(../common/g++-unix.conf)

# modifications to linux.conf
QMAKE_INCDIR          = $RPM_BUILD_DIR/../../rootfs/usr/include \
			$RPM_BUILD_DIR/../../rootfs/usr/include/freetype2
QMAKE_LIBDIR          = $RPM_BUILD_DIR/../../rootfs/usr/lib
QMAKE_LIBS            = -lglib-2.0 -lgthread-2.0 -lgmodule-2.0 -lgobject-2.0 -lz -lpng

# modifications to g++.conf
QMAKE_CC                = arm-none-linux-gnueabi-gcc
QMAKE_CXX               = arm-none-linux-gnueabi-g++
QMAKE_LINK              = arm-none-linux-gnueabi-g++
QMAKE_LINK_SHLIB        = arm-none-linux-gnueabi-g++

# modifications to linux.conf
QMAKE_AR                = arm-none-linux-gnueabi-ar cqs
QMAKE_OBJCOPY           = arm-none-linux-gnueabi-objcopy
QMAKE_NM                = arm-none-linux-gnueabi-nm -P
QMAKE_STRIP             = arm-none-linux-gnueabi-strip
load(qt_config)
EOF

initscript=$XPLATFORM/qplatformdefs.h
cat > $initscript << EOF
#include "../linux-g++/qplatformdefs.h"
EOF

%Build

export PATH=$UNSPOOF_PATH
export PKG_CONFIG_LIBDIR=${DEV_IMAGE}%{_prefix}/lib/pkgconfig
export PKG_CONFIG_SYSROOT_DIR=${DEV_IMAGE}
export PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1
export PKG_CONFIG_PATH=${DEV_IMAGE}%{_prefix}/lib/pkgconfig
export PKG_CONFIG_SYSROOT_DIR=${DEV_IMAGE}

# Unset compiler to prevent gcc being used when the cross
# tools should be used. (Trolltech issue# 138807)
unset CC CXX LD

# Unset PLATFORM because this is used as host machine.
unset PLATFORM

#Checking what packages are available

CONFIGURE_OPTIONS=" \
	-release \
	-opensource \
	-confirm-license \
	-no-largefile \
	-no-qml-debug \
	"

THIRD_PARTY_LIBRARIES=" \
	-no-mtdev \
	-no-libjpeg \
	-no-harfbuzz \
	"

NO_SKIP_MODULES="qtbase qtserialport"

SKIP_MODULES=" \
	-skip qtandroidextras \
	-skip qtmacextras \
	-skip qtx11extras \
	-skip qtsvg \
	-skip qtxmlpatterns \
	-skip qtdeclarative \
	-skip qtquickcontrols \
	-skip qtwinextras \
	-skip qtactiveqt \
	-skip qtlocation \
	-skip qtsensors \
	-skip qtconnectivity \
	-skip qtwebsockets \
	-skip qtwebchannel \
	-skip qtwebkit \
	-skip qttools \
	-skip qtwebkit-examples \
	-skip qtimageformats \
	-skip qtgraphicaleffects \
	-skip qtscript \
	-skip qtquick1 \
	-skip qtwayland \
	-skip qtenginio \
	-skip qtwebengine \
	-skip qttranslations \
	-skip qtdoc \
	"

NO_FILE_IO_FEATURE=" \
	-no-feature-DOM
	"

NO_WIDGETS_FEATURE=" \
	"

NO_DIALOGS_FEATURE=" \
	-no-feature-FONTDIALOG \
	-no-feature-PRINTDIALOG \
	-no-feature-PRINTPREVIEWDIALOG \
	-no-feature-WIZARD \
	"

NO_ITEMVIEWS_FEATURE=" \
	"

NO_STYLES_FEATURE=" \
	-no-feature-STYLE_FUSION \
	-no-feature-STYLE_WINDOWSXP \
	-no-feature-STYLE_WINDOWSVISTA \
	-no-feature-STYLE_WINDOWSCE \
	-no-feature-STYLE_WINDOWSMOBILE \
	"

NO_PAINTING_FEATURE=" \
	-no-feature-PRINTER \
	-no-feature-CUPS \
	"

NO_NETWORKING_FEATURE=" \
	-no-feature-FTP \
	"

NO_UTILITIES_FEATURE=" \
	-no-feature-DESKTOPSERVICES \
	-no-feature-SYSTEMTRAYICON \
	-no-feature-GESTURES \
	"

NO_FEATURES=" \
	$NO_FILE_IO_FEATURE \
	$NO_WIDGETS_FEATURE \
	$NO_DIALOGS_FEATURE \
	$NO_ITEMVIEWS_FEATURE \
	$NO_STYLES_FEATURE \
	$NO_PAINTING_FEATURE \
	$NO_NETWORKING_FEATURE \
	$NO_UTILITIES_FEATURE \
	"

ADDITIONAL_OPTIONS=" \
	-nomake examples \
	-nomake tools \
	$SKIP_MODULES \
	-no-nis \
	-no-cups \
	-no-iconv \
	-no-icu \
	-no-fontconfig \
	-no-use-gold-linker \
	-no-xcb \
	-no-eglfs
	-no-directfb \
	-no-kms \
	-qpa linuxfb \
	-xplatform linux-none-arm-gnueabi-g++ \
	$NO_FEATURES
	"

./configure --prefix=%{_prefix} $CONFIGURE_OPTIONS $THIRD_PARTY_LIBRARIES $ADDITIONAL_OPTIONS

make

%Install

export PATH=$UNSPOOF_PATH

make install INSTALL_ROOT=$RPM_BUILD_ROOT/%{pfx}

qt_conf=$RPM_BUILD_ROOT/%{pfx}/usr/bin/qt.conf
cat > $qt_conf << EOF
[Paths]
Prefix=..
EOF

export PATH=$SPOOF_PATH

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
