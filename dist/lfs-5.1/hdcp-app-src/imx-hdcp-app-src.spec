%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : freescale hdcp-app source code
Name            : imx-hdcp-app-src
Version         : 3.0.35
Release         : 4.1.0
License         : Proprietary
Vendor          : Freescale
Packager        : Terry Lv
Group           : System/Servers
Source          : %{name}-%{version}-%{release}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
This package provides proprietary libraries, and
application sources.

%{summary}

%Prep
%setup -n %{name}-%{version}-%{release}

%Build

if [ -z "$PKG_KERNEL_KBUILD_PRECONFIG" ]; then
	KERNELDIR="$PWD/../linux"
	KBUILD_OUTPUT="$PWD/../linux"
else
	KERNELDIR="$PKG_KERNEL_PATH_PRECONFIG"
	KBUILD_OUTPUT="$(eval echo ${PKG_KERNEL_KBUILD_PRECONFIG})"
fi

# build the libraries and kernel modules 
PLATFORM_UPPER="$(echo $PLATFORM | awk '{print toupper($0)}')"
INCLUDE="-I$KERNELDIR/arch/arm/plat-mxc/include/mach/"

make PLATFORM=$PLATFORM_UPPER CROSS_COMPILE=$TOOLCHAIN_PREFIX INC="$INCLUDE"

%Install
PLATFORM_UPPER="$(echo $PLATFORM | awk '{print toupper($0)}')"
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{pfx}
make install PLATFORM=$PLATFORM_UPPER DEST_DIR=$RPM_BUILD_ROOT/%{pfx}

# Package up the build results and leave in rpm/SOURCES for hdcp-app-bin spec file
rm -rf imx-hdcp-app-bin-%{version}-%{release}
mkdir imx-hdcp-app-bin-%{version}-%{release}
mv $RPM_BUILD_ROOT/%{pfx}/* imx-hdcp-app-bin-%{version}-%{release}
tar -zcf imx-hdcp-app-bin-%{version}-%{release}.tar.gz imx-hdcp-app-bin-%{version}-%{release}
# todo fix this to use rpmdir or something better than TOP:
cp -f imx-hdcp-app-bin-%{version}-%{release}.tar.gz $TOP/rpm/
cp -f imx-hdcp-app-bin-%{version}-%{release}.tar.gz $TOP/rpm/SOURCES

# Now delete everything we just tarred up.  hdcp-app-bin spec file will install it.
rm -rf $RPM_BUILD_ROOT/%{pfx}
# Create an empty directory for rpm to have something install or it won't be happy.
mkdir -p $RPM_BUILD_ROOT/%{pfx}/usr



%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(755,root,root)
%{pfx}/*
