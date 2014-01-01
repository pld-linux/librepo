#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Library for downloading Linux repository metadata and packages
Summary(pl.UTF-8):	Biblioteka do pobierania metadanych repozytoriów roaz pakietów dla Linuksa
Name:		librepo
Version:	1.5.0
%define snap	20131221
Release:	0.%{snap}.1
License:	GPL v2+
Group:		Libraries
#Source0:	https://github.com/Tojaj/librepo/archive/%{version}/%{name}-%{version}.tar.gz
# argh, the latest tagged version is 1.0.0, while current is 1.5.0
Source0:	%{name}.tar.xz
# Source0-md5:	8a2df0be32cdbd2d7cb6124f673c780f
Patch0:		%{name}-link.patch
URL:		http://tojaj.github.io/librepo/
BuildRequires:	attr-devel
BuildRequires:	check-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	curl-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gpgme-devel
BuildRequires:	expat-devel >= 1.95
BuildRequires:	openssl-devel
BuildRequires:	python-devel >= 2
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_apidocs:BuildRequires:	sphinx-pdg}
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

%description apidocs
API documentation for librepo library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki librepo.

%package -n python-librepo
Summary:	Python binding for librepo library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki librepo
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-librepo
Python binding for librepo library.

%description -n python-librepo -l pl.UTF-8
Wiązanie Pythona do biblioteki librepo.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
install -d build
cd build
%cmake ..

%{__make}

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

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

%files -n python-librepo
%defattr(644,root,root,755)
%if %{with apidocs}
%doc build/doc/python/{*.html,_sources,_static}
%endif
%dir %{py_sitedir}/librepo
%attr(755,root,root) %{py_sitedir}/librepo/_librepomodule.so
%{py_sitedir}/librepo/__init__.py[co]