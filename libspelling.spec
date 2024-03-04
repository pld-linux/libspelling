#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Spellchecking library for GTK 4
Summary(pl.UTF-8):	Biblioteka sprawdzania pisowni dla GTK 4
Name:		libspelling
Version:	0.2.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libspelling/0.2/%{name}-%{version}.tar.xz
# Source0-md5:	94cb8c37d83c432e8b8935c3952bf4a4
URL:		https://gitlab.gnome.org/chergert/libspelling
BuildRequires:	enchant2-devel >= 2
%{?with_apidocs:BuildRequires:	gi-docgen}
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gtk4-devel >= 4.8
BuildRequires:	gtksourceview5-devel >= 5.6
BuildRequires:	libicu-devel
BuildRequires:	meson >= 0.62.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.44
BuildRequires:	vala-gtksourceview5 >= 5.6
BuildRequires:	xz
Requires:	gtk4 >= 4.8
Requires:	gtksourceview5 >= 5.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Spellchecking library for GTK 4. It's heavily based upon GNOME Text
Editor and GNOME Builder's spellcheck implementation.

%description -l pl.UTF-8
Biblioteka sprawdzania pisowni dla GTK 4. Jest w dużej części oparta
na implementacji sprawdzania pisowni aplikacji GNOME Text Editor i
GNOME Builder.

%package devel
Summary:	Header files for libspelling library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libspelling
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.0
Requires:	gtk4-devel >= 4.8
Requires:	gtksourceview5-devel >= 5.6

%description devel
Header files for libspelling library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libspelling.

%package -n vala-libspelling
Summary:	Vala API for libspelling library
Summary(pl.UTF-8):	API języka Vala do biblioteki libspelling
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
# with gtk4 binding
Requires:	vala >= 2:0.44
Requires:	vala-gtksourceview5 >= 5.6
BuildArch:	noarch

%description -n vala-libspelling
Vala API for libspelling library.

%description -n vala-libspelling -l pl.UTF-8
API języka Vala do biblioteki libspelling.

%package apidocs
Summary:	API documentation for libspelling library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libspelling
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libspelling library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libspelling.

%prep
%setup -q

%build
%meson build \
	%{!?with_apidocs:-Ddocs=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libspelling-1 $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_libdir}/libspelling-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspelling-1.so.1
%{_libdir}/girepository-1.0/Spelling-1.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspelling-1.so
%{_includedir}/libspelling-1
%{_datadir}/gir-1.0/Spelling-1.gir
%{_pkgconfigdir}/libspelling-1.pc

%files -n vala-libspelling
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libspelling-1.deps
%{_datadir}/vala/vapi/libspelling-1.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libspelling-1
%endif
