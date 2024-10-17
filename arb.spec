%define _disable_lto 1
%define major 1
%define libname %mklibname %name %major
%define devname %mklibname -d %name

Name:           arb
Version:        2.8.1
Release:        1
Summary:        Arbitrary-precision floating point ball arithmetic
Group:		Sciences/Mathematics
License:        GPLv2+
URL:            https://fredrikj.net/arb/
Source0:        https://github.com/fredrik-johansson/%{name}/archive/%{version}.tar.gz

BuildRequires:  flint-devel
BuildRequires:  gcc-c++
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
BuildRequires:  ntl-devel
BuildRequires:  python-sphinx

%description
Arb is a C library for arbitrary-precision floating-point ball
arithmetic.  It supports efficient high-precision computation with
polynomials, power series, matrices and special functions over the real
and complex numbers, with automatic, rigorous error control.

%package  -n %devname
Summary:        Headers for developing with arb
Requires:	%{libname} = %{version}-%{release}
Requires:       flint-devel%{?_isa}
Requires:       gmp-devel%{?_isa}
Requires:       mpfr-devel%{?_isa}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %devname
Header files and library links for developing with arb.

%package doc
Summary:        Documentation for arb
BuildArch:      noarch
Provides:       bundled(jquery)

%description doc
Documentation for developers using the arb library.

%libpackage %name %major

%prep
%setup -q

# Avoid symbol collisions with flint and let optflags specify the abi flag
sed -i '/CONFIG_BLAS/d;s/WANT_NTL=1/WANT_NTL=0/;/ABI_FLAG="-m.."/d' configure

# Preserve timestamps
sed -i 's/cp \$/cp -p $/' Makefile.in

# Use the new default sphinx theme
#sed -i "s/'default'/'alabaster'/" doc/source/conf.py

%build
# This is NOT an autoconf-generated script.  Do not use %%configure.
./configure --prefix=%{_prefix} --disable-static --with-flint=%{_prefix} \
  --with-ntl=%{_prefix} ABI=%{__isa_bits} CFLAGS="%{optflags}"
make %{?_smp_mflags} verbose LDFLAGS="$RPM_LD_FLAGS"
make -C doc html PAPER=letter

%install
make install DESTDIR=%{buildroot} LIBDIR=%{_lib}

# Move the headers into a private directory
mkdir -p %{buildroot}%{_includedir}/%{name}
mv %{buildroot}%{_includedir}/*.h %{buildroot}%{_includedir}/%{name}

# Fix permissions
chmod 0755 %{buildroot}%{_libdir}/libarb.so.*.*.*

# Remove hidden documentation build artifacts
rm -f doc/build/html/{.buildinfo,objects.inv}

%files -n %devname
%{_includedir}/%{name}/
%{_libdir}/libarb.so

%files doc
%doc doc/build/html gpl-2.0.txt

%changelog
* Sat Mar 19 2016 Jerry James <loganjerry@gmail.com> - 2.8.1-4
- Rebuild for ntl 9.7.0

* Sat Feb 20 2016 Jerry James <loganjerry@gmail.com> - 2.8.1-3
- Rebuild for ntl 9.6.4

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan  1 2016 Jerry James <loganjerry@gmail.com> - 2.8.1-1
- New upstream version (bz 1295018)

* Tue Dec 29 2015 Jerry James <loganjerry@gmail.com> - 2.8.0-1
- New upstream version

* Fri Dec  4 2015 Jerry James <loganjerry@gmail.com> - 2.7.0-3
- Rebuild for ntl 9.6.2

* Fri Oct 23 2015 Jerry James <loganjerry@gmail.com> - 2.7.0-2
- Build with hardening ld flags

* Fri Oct 16 2015 Jerry James <loganjerry@gmail.com> - 2.7.0-1
- Initial RPM
