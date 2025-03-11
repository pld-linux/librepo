#
# Conditional build:
%bcond_without	apidocs	# doxygen/sphinx API documentation
%bcond_without	python3 # CPython 3.x module

Summary:	Library for downloading Linux repository metadata and packages
Summary(pl.UTF-8):	Biblioteka do pobierania metadanych repozytoriów oraz pakietów dla Linuksa
Name:		librepo
Version:	1.18.1
Release:	2
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/rpm-software-management/librepo/releases
Source0:	https://github.com/rpm-software-management/librepo/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e33261fe05dd8beea6fd97c3ff3def48
Patch0:		%{name}-link.patch
Patch1:		%{name}-gpgme-pkgconfig.patch
Patch2:		sphinx_executable.patch
URL:		http://rpm-software-management.github.io/librepo/
BuildRequires:	check-devel
BuildRequires:	cmake >= 2.8.5
BuildRequires:	curl-devel >= 7.52
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	glib2-devel >= 1:2.66
# can also use rpm (>= 4.19.0) for PGP operations
BuildRequires:	gpgme-devel
BuildRequires:	libselinux-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.742
%if %{with python3}
BuildRequires:	python3-devel >= 1:3
BuildRequires:	python3-modules >= 1:3
%{?with_apidocs:BuildRequires:	sphinx-pdg-3}
%endif
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zchunk-devel >= 0.9.11
Requires:	curl-libs >= 7.52
Requires:	glib2 >= 1:2.66
Requires:	zchunk-libs >= 0.9.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library providing C and Python (libcURL like) API for downloading
Linux repository metadata and packages.

%description -l pl.UTF-8
Biblioteka udostępniająca API C i Pythona (podobne do libcURL) służące
do pobierania metadanych repozytoriów oraz pakietów dla Linuksa.

%package devel
Summary:	Header files for librepo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki librepo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	curl-devel >= 7.52
Requires:	glib2-devel >= 1:2.66
Requires:	gpgme-devel
Requires:	libxml2-devel >= 2.0
Requires:	openssl-devel
Requires:	zchunk-devel >= 0.9.11

%description devel
Header files for librepo library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki librepo.

%package apidocs
Summary:	API documentation for librepo library
Summary(pl.UTF-8):	Dokumentacja API biblioteki librepo
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for librepo library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki librepo.

%package -n python3-librepo
Summary:	Python 3 binding for librepo library
Summary(pl.UTF-8):	Wiązanie Pythona 3 do biblioteki librepo
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-librepo
Python 3 binding for librepo library.

%description -n python3-librepo -l pl.UTF-8
Wiązanie Pythona 3 do biblioteki librepo.

%package -n python3-librepo-apidocs
Summary:	API documentation for Python librepo binding
Summary(pl.UTF-8):	Dokumentacja API do wiązań Pythona do librepo
Group:		Documentation
BuildArch:	noarch

%description -n python3-librepo-apidocs
API documentation for Python librepo binding.

%description -n python3-librepo-apidocs -l pl.UTF-8
Dokumentacja API do wiązań Pythona do librepo.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1

%build
install -d build
cd build
%cmake .. \
	%{cmake_on_off apidocs ENABLE_DOCS} \
%if %{with python3}
	-DPYTHON_DESIRED=3 \
	-DPYTHON_INSTALL_DIR="%{py3_sitedir}" \
	-DSPHINX_EXECUTABLE=/usr/bin/sphinx-build-3
%endif

%{__make}

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python3}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/librepo.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librepo.so
%{_includedir}/librepo
%{_pkgconfigdir}/librepo.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/c/html/*
%endif

%if %{with python3}
%files -n python3-librepo
%defattr(644,root,root,755)
%dir %{py3_sitedir}/librepo
%attr(755,root,root) %{py3_sitedir}/librepo/_librepo.so
%{py3_sitedir}/librepo/__init__.py
%{py3_sitedir}/librepo/__pycache__

%if %{with apidocs}
%files -n python3-librepo-apidocs
%defattr(644,root,root,755)
%doc build/doc/python/{_static,*.html,*.js}
%endif
%endif
