%define major 3

%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

Name:             qatlib
Version:          22.07.0
Release:          2
Summary:          Intel QuickAssist user space library
# The entire source code is released under BSD.
# For a breakdown of inbound licenses see the INSTALL file.
License:          BSD and (BSD or GPLv2)
URL:              https://github.com/intel/qatlib
Source0:          https://github.com/intel/qatlib/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  yasm-devel
Requires(pre):  shadow
Requires:       %{libname} = %{EVRD}

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

%package -n %{libname}
Summary:        Library for Intel QuickAssist Technology (Intel QAT) provides hardware acceleration for offloading.
Group:          System/Libraries
Requires:       %{name} = %{EVRD}

%description -n %{libname}
Intel QuickAssist Technology (Intel QAT) provides hardware acceleration
for offloading secpkgurity, authentication and compression services from the
CPU, thus significantly increasing the performance and efficiency of
standard platform solutions.

%package -n %{devname}
Summary:       Headers and libraries for qatlib - Intel QuickAssist Technology.
Requires:       %{libname} = %{EVRD}
Requires:       %{name} = %{EVRD}

%description -n	%{devname}
This package contains headers and libraries required to build applications
that use the Intel QuickAssist APIs.

%prep
%autosetup -p1

%build
#export CC=gcc
#export CXX=g++
autoreconf -vif
%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build

%install
%make_install
#rm %{buildroot}/%{_libdir}/libqat-%{version}.so
#rm %{buildroot}/%{_libdir}/libusdm-%{version}.so
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
%{_sbindir}/qatmgr
%{_sbindir}/qat_init.sh
%{_unitdir}/qat.service
%{_mandir}/man8/qat_init.sh.8*
%{_mandir}/man8/qatmgr.8*

%files -n %{libname}
%{_libdir}/libqat.so.%{major}*
#{_libdir}/libqat-%{version}.so
%{_libdir}/libusdm.so.0*

%files -n %{devname}
%{_libdir}/libqat.so
%{_libdir}/libusdm.so
%{_includedir}/qat
