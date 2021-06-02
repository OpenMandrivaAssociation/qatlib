# SPDX-License-Identifier: MIT

%global libqat_soversion  0
%global libusdm_soversion 0
Name:             qatlib
Version:          21.05.0
Release:          1
Summary:          Intel QuickAssist user space library
# The entire source code is released under BSD.
# For a breakdown of inbound licenses see the INSTALL file.
License:          BSD and (BSD or GPLv2)
URL:              https://github.com/intel/%{name}
Source0:          https://github.com/intel/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(zlib)
Requires(pre):    shadow

%description
Intel QuickAssist Technology (Intel QAT) provides hardware acceleration
for offloading secpkgurity, authentication and compression services from the
CPU, thus significantly increasing the performance and efficiency of
standard platform solutions.

Its services include symmetric encryption and authentication,
asymmetric encryption, digital signatures, RSA, DH and ECC, and
lossless data compression.

This package provides user space libraries that allow access to
Intel QuickAssist devices and expose the Intel QuickAssist APIs.

%package       devel
Summary:       Headers and libraries to build applications that use qatlib
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description   devel
This package contains headers and libraries required to build applications
that use the Intel QuickAssist APIs.

%prep
%autosetup -p1

%build
export CC=gcc
export CXX=g++
autoreconf -vif
%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build

%install
%make_install
rm %{buildroot}/%{_libdir}/libqat-%{version}.so
rm %{buildroot}/%{_libdir}/libusdm-%{version}.so
rm %{buildroot}/%{_libdir}/libqat.la
rm %{buildroot}/%{_libdir}/libusdm.la

%pre
getent group qat >/dev/null || groupadd -r qat
exit 0

%post
%systemd_post qat.service

%preun
%systemd_preun qat.service

%postun
%systemd_postun_with_restart qat.service

%files
%license LICENSE*
%{_libdir}/libqat.so.%{libqat_soversion}*
%{_libdir}/libusdm.so.%{libusdm_soversion}*
%{_sbindir}/qatmgr
%{_sbindir}/qat_init.sh
%{_unitdir}/qat.service
%{_mandir}/man8/qat_init.sh.8*
%{_mandir}/man8/qatmgr.8*

%files         devel
%{_libdir}/libqat.so
%{_libdir}/libusdm.so
%{_includedir}/qat
