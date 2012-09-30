%define		goffice	0.8.17
%define		plugins	fn-derivatives dif excel fn-complex fn-database fn-date fn-eng fn-erlang fn-financial fn-info fn-logical fn-lookup fn-math fn-r fn-random fn-stat fn-string html mps fn-numtheory openoffice

Summary:	Spreadsheet program
Name:		gnumeric
Version:	1.10.17
Release:	2
Epoch:		1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnumeric/1.10/%{name}-%{version}.tar.bz2
# Source0-md5:	aacc0899222c98fa9cdd85c49a6840be
URL:		http://www.gnome.org/projects/gnumeric/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel
BuildRequires:	intltool
# api breakage, does not build
#BuildRequires:	libgda-ui-devel
BuildRequires:	libgoffice-devel >= %{goffice}
BuildRequires:	libgsf-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	pkg-config
BuildRequires:	popt-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	rarian
Requires(post,postun):	glib-gio-gsettings
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gnumeric is a spreadsheet program that is part of the GNOME Free
Software Desktop Project and has Windows installers available.
It is distributed as free software under the GNU GPL license.
It is intended to be a replacement for proprietary spreadsheet
programs such as Microsoft Excel, which it broadly and openly
emulates.

%package libs
Summary:	libspreadsheet library
Group:		Libraries
Requires:	libgoffice >= %{_goffice}

%description libs
libspreadsheet library.

%package devel
Summary:	Header files for libspreadsheet library
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
This is the package containing the header files for libspreadsheet
library.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-schemas-install	\
	--disable-silent-rules		\
	--disable-static		\
	--enable-plugins="%{plugins}"	\
	--without-gnome			\
	--without-paradox		\
	--without-perl			\
	--without-psiconv		\
	--without-python
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=/usr/share/gnome/help/gnumeric/C

rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_pkgconfigdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/*/*/plugins/*/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/mime-info

%find_lang %{name} --with-gnome --with-omf
%find_lang %{name}-functions
cat %{name}-functions.lang >> %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%scrollkeeper_update_post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README

%attr(755,root,root) %{_bindir}/*

%dir %{_libdir}/gnumeric/%{version}/plugins
%dir %{_libdir}/gnumeric/%{version}/plugins/dif
%dir %{_libdir}/gnumeric/%{version}/plugins/excel
%dir %{_libdir}/gnumeric/%{version}/plugins/fn-*
#%dir %{_libdir}/gnumeric/%{version}/plugins/gdaif
#%dir %{_libdir}/gnumeric/%{version}/plugins/gnome-db
%dir %{_libdir}/gnumeric/%{version}/plugins/html
%dir %{_libdir}/gnumeric/%{version}/plugins/mps
%dir %{_libdir}/gnumeric/%{version}/plugins/openoffice

%attr(755,root,root) %{_libdir}/gnumeric/%{version}/plugins/dif/*.so
%attr(755,root,root) %{_libdir}/gnumeric/%{version}/plugins/excel/*.so
%attr(755,root,root) %{_libdir}/gnumeric/%{version}/plugins/fn-*/*.so
#%attr(755,root,root) %{_libdir}/gnumeric/%{version}/plugins/gdaif/*.so
#%attr(755,root,root) %{_libdir}/gnumeric/%{version}/plugins/gnome-db/*.so
%attr(755,root,root) %{_libdir}/gnumeric/%{version}/plugins/html/*.so
%attr(755,root,root) %{_libdir}/gnumeric/%{version}/plugins/mps/*.so
%attr(755,root,root) %{_libdir}/gnumeric/%{version}/plugins/openoffice/*.so

%{_libdir}/gnumeric/%{version}/plugins/dif/*.xml
%{_libdir}/gnumeric/%{version}/plugins/excel/*.xml
%{_libdir}/gnumeric/%{version}/plugins/fn-*/*.xml
#%{_libdir}/gnumeric/%{version}/plugins/gdaif/*.xml
#%{_libdir}/gnumeric/%{version}/plugins/gnome-db/*.xml
%{_libdir}/gnumeric/%{version}/plugins/html/*.xml
%{_libdir}/gnumeric/%{version}/plugins/mps/*.xml
%{_libdir}/gnumeric/%{version}/plugins/openoffice/*.xml

%dir %{_libdir}/goffice/%{goffice}/plugins/gnumeric
%attr(755,root,root) %{_libdir}/goffice/%{goffice}/plugins/gnumeric/gnumeric.so
%{_libdir}/goffice/%{goffice}/plugins/gnumeric/plugin.xml

%{_datadir}/glib-2.0/schemas/org.gnome.gnumeric.dialogs.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnumeric.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnumeric.plugin.gschema.xml

%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/gnumeric.*
%{_pixmapsdir}/*

%{_mandir}/man1/gnumeric.1*
%{_mandir}/man1/ssconvert.1*
%{_mandir}/man1/ssgrep.1*
%{_mandir}/man1/ssindex.1*

%dir %{_datadir}/gnumeric
%dir %{_datadir}/gnumeric/%{version}
%{_datadir}/gnumeric/%{version}/*.xml
%{_datadir}/gnumeric/%{version}/autoformat-templates
%{_datadir}/gnumeric/%{version}/templates
%{_datadir}/gnumeric/%{version}/ui

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/gnumeric
%dir %{_libdir}/gnumeric/%{version}
%attr(755,root,root) %{_libdir}/lib*.so

%if 0
%files -n libspreadsheet-devel
%defattr(644,root,root,755)
#%dir %{_libdir}/gnumeric/%{version}/include
#%%{_libdir}/gnumeric/%{version}/include/*.h
#%%{_includedir}/libspreadsheet-*
%{_pkgconfigdir}/*.pc
%endif

