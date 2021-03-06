%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary         : The GNU macro processor
Name            : m4
Version         : 1.4.16
Release         : 1
License         : GPL
Vendor          : Freescale
Packager        : Stuart Hughes
Group           : Applications/Text
Source          : %{name}-%{version}.tar.gz
BuildRoot       : %{_tmppath}/%{name}
Prefix          : %{pfx}

%Description
%{summary}

%Prep
%setup


%Build
ac_cv_header_stdc=yes ./configure --prefix=%{_prefix}
make

%Install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/%{pfx}/%{_prefix}

%Clean
rm -rf $RPM_BUILD_ROOT


%Files
%defattr(-,root,root)
%{pfx}/*


