#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	sysprof		# sysprof profiling
#
Summary:	Spellchecking library for GTK 4
Summary(pl.UTF-8):	Biblioteka sprawdzania pisowni dla GTK 4
Name:		libspelling
Version:	0.4.4
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libspelling/0.4/%{name}-%{version}.tar.xz
# Source0-md5:	45ca78b91b903a6c9cac79895cf3c8f0
URL:		https://gitlab.gnome.org/chergert/libspelling
BuildRequires:	enchant2-devel >= 2
%{?with_apidocs:BuildRequires:	gi-docgen}
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gtk4-devel >= 4.15.5
BuildRequires:	gtksourceview5-devel >= 5.10.0
BuildRequires:	libicu-devel
BuildRequires:	meson >= 0.62.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
%{?with_sysprof:BuildRequires:	sysprof-devel >= 3.38}
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.44
BuildRequires:	vala-gtksourceview5 >= 5.10.0
BuildRequires:	xz
Requires:	gtk4 >= 4.15.5
Requires:	gtksourceview5 >= 5.10.0
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
Requires:	gtk4-devel >= 4.15.5
Requires:	gtksourceview5-devel >= 5.10.0

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
Requires:	vala-gtksourceview5 >= 5.10.0
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
	%{!?with_apidocs:-Ddocs=false} \
	%{!?with_sysprof:-Dsysprof=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libspelling-1 $RPM_BUILD_ROOT%{_gidocdir}
%endif

# not supported by glibc (as of 2.40)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_libdir}/libspelling-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspelling-1.so.2
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
