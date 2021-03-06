%define pfx /opt/freescale/rootfs/%{_target_cpu}

Summary		: Memory Technology Device tools
Name		: mtd-utils
Version		: 1.5.0
Release		: 1
License		: GPL
Vendor		: Freescale Semiconductor
Packager	: Ross Wille
Group		: Applications/System
Source		: %{name}-%{version}.tar.gz
BuildRoot	: %{_tmppath}/%{name}
Prefix		: %{pfx}

%Description
%{summary}

Extracted source from the git tree: 
  git clone git://git.infradead.org/mtd-utils.git
  SHA1 d769da93a56590c23ce9430a1d970e31e835ae88

%Prep
%setup -n %{name}

%Build
make -j1 WITHOUT_XATTR=1

%Install
rm -rf $RPM_BUILD_ROOT
make -j1 DESTDIR=$RPM_BUILD_ROOT/%{pfx} SBINDIR=%{_prefix}/bin MANDIR=%{_mandir} install
mkdir -p $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/mtd
install -m0644 include/mtd/*.h $RPM_BUILD_ROOT/%{pfx}/%{_prefix}/include/mtd

%Clean
rm -rf $RPM_BUILD_ROOT

%Files
%defattr(-,root,root)
%{pfx}/*
