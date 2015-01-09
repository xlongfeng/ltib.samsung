%define pfx /opt/freescale/rootfs/%{_target_cpu}
Summary         : Freescale extra codec for aac plus
Name            : libfslaacpcodec
Version         : 3.0.7
Release         : 1
License         : LGPL
Vendor          : Freescale Semiconductor
Packager        : Sario Hu
Group           : Applications/System
Source          : %{name}-%{version}-2.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup

%Build
export PKG_CONFIG="`which pkg-config` --static "

./configure --prefix=%{_prefix} --host=$CFGHOST \
	    --build=%{_build}
make

%Install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}/
mv $RPM_BUILD_ROOT/%{pfx}/usr/lib/imx-mm/audio-codec/*.so* $RPM_BUILD_ROOT/%{pfx}/usr/lib/

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
