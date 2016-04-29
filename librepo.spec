#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Library for downloading Linux repository metadata and packages
Summary(pl.UTF-8):	Biblioteka do pobierania metadanych repozytoriów roaz pakietów dla Linuksa
Name:		librepo
Version:	1.7.17
Release:	2
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/rpm-software-management/librepo/releases
Source0:	https://github.com/rpm-software-management/librepo/archive/%{name}-%{version}.tar.gz
# Source0-md5:	8e3b23e44aab8cd516d2b05d62f6f559
#Source0:	http://pkgs.fedoraproject.org/repo/pkgs/librepo/%{name}-%{gitrev}.tar.xz/904628ef27b512e7aed07a6d41613c87/librepo-%{gitrev}.tar.xz
Patch0:		%{name}-link.patch
Patch1:		python-install-dir.patch
Patch2:		sphinx_executable.patch
URL:		http://rpm-software-management.github.io/librepo/
BuildRequires:	attr-devel
BuildRequires:	check-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	curl-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	expat-devel >= 1.95
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gpgme-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with python2}
BuildRequires:	python-devel >= 1:2
%{?with_apidocs:BuildRequires:	sphinx-pdg-2}
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3
%{?with_apidocs:BuildRequires:	sphinx-pdg-3}
%endif
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
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
Requires:	curl-devel
Requires:	expat-devel >= 1.95
Requires:	glib2-devel >= 2.0
Requires:	gpgme-devel
Requires:	openssl-devel

%description devel
Header files for librepo library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki librepo.

%package apidocs
Summary:	API documentation for librepo library
Summary(pl.UTF-8):	Dokumentacja API biblioteki librepo
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for librepo library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki librepo.

%package -n python-librepo
Summary:	Python 2 binding for librepo library
Summary(pl.UTF-8):	Wiązanie Pythona 2 do biblioteki librepo
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-librepo
Python 2 binding for librepo library.

%description -n python-librepo -l pl.UTF-8
Wiązanie Pythona 2 do biblioteki librepo.

%package -n python3-librepo
Summary:	Python 3 binding for librepo library
Summary(pl.UTF-8):	Wiązanie Pythona 3 do biblioteki librepo
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-librepo
Python 3 binding for librepo library.

%description -n python3-librepo -l pl.UTF-8
Wiązanie Pythona 3 do biblioteki librepo.

%prep
%setup -q -n %{name}-%{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d build
cd build
%cmake .. \
%if %{with python2}
	-DPYTHON_DESIRED=2 \
	-DPYTHON_INSTALL_DIR="%{py_sitedir}" \
	-DSPHINX_EXECUTABLE=/usr/bin/sphinx-build-2
%endif

%{__make}

%if %{with apidocs}
%{__make} doc
%endif
cd ..

%if %{with python3}
install -d build-py3
cd build-py3
%cmake .. \
	-DPYTHON_DESIRED=3 \
	-DPYTHON_INSTALL_DIR="%{py3_sitedir}" \
	-DSPHINX_EXECUTABLE=/usr/bin/sphinx-build-3

%{__make}

%if %{with apidocs}
%{__make} doc
%endif
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python3}
%{__make} -C build-py3 install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%py_comp $RPM_BUILD_ROOT%{py_sitedir}/librepo
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/librepo
%py_postclean

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

%if %{with python2}
%files -n python-librepo
%defattr(644,root,root,755)
%if %{with apidocs}
%doc build/doc/python/{*.html,_sources,_static}
%endif
%dir %{py_sitedir}/librepo
%attr(755,root,root) %{py_sitedir}/librepo/_librepomodule.so
%{py_sitedir}/librepo/__init__.py[co]
%endif

%if %{with python3}
%files -n python3-librepo
%defattr(644,root,root,755)
%if %{with apidocs}
%doc build-py3/doc/python/{*.html,_sources,_static}
%endif
%dir %{py3_sitedir}/librepo
%attr(755,root,root) %{py3_sitedir}/librepo/_librepo.so
%{py3_sitedir}/librepo/__init__.py
%endif
