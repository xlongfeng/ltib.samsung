%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : System-wide profiler for Linux systems
Name            : oprofile
Version         : 0.9.8
Release         : 1
License         : GPL
URL             : http://oprofile.sourceforge.net/download/
Vendor          : Freescale
Packager        : Stuart Hughes/WMSG
Group           : Development/Tools
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}
BuildRequires   : popt, binutils

%Description
%{summary}

Note:
binutils is required for libbfd only
This only support 2.6 kernels

%Prep
%setup 

%Build
./configure --prefix=%{_prefix} --host=$CFGHOST --build=%{_build} \
            --with-kernel-support \
            --config-cache --mandir=%{_mandir} \
            --with-binutils=$DEV_IMAGE/usr
make

%Install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/%{pfx}

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
