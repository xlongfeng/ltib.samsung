%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : Z160 2D driver
Name            : libz160
Version         : 3.0.35
Release         : 4.1.0
License         : Proprietary
Vendor          : Freescale
Packager        : Rob Herring
Group           : System/Servers
Source          : %{name}-%{version}-%{release}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
This package provides proprietary driver library for Z160.

%{summary}

%Prep
%setup -n %{name}-%{version}-%{release}

%Build
make -j1
make VERSION=%{version} pkg-bin 

%Install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT/%{pfx}/%{_prefix} install
install %{name}-bin-%{version}-%{release}.tar.gz $TOP/rpm/
install %{name}-bin-%{version}-%{release}.tar.gz $TOP/rpm/SOURCES

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(755,root,root)
%{pfx}/*
