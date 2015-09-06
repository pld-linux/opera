# BRANCHES:
# - HEAD - stable version
# - DEVEL - development version
# - WEEKLY - weekly development version
# - NEXT - opera next
#
# NOTE: to avoid creating unreadable/unmaintainable spec:
# - don't put static version here, create STATIC branch for that for example
# - don't create useless bconds that for example limit SourceX: to current arch only
#

Summary:	Opera browser
Summary(hu.UTF-8):	A világ leggyorsabb webböngészője
Summary(pl.UTF-8):	Najszybsza przeglądarka WWW na świecie
Name:		opera
Version:	31.0.1889.174
Release:	0.4
Epoch:		2
License:	Distributable
Group:		X11/Applications/Networking
Source10:	ftp://ftp.opera.com/pub/opera/desktop/%{version}/linux/%{name}-stable_%{version}_amd64.deb
# Source10-md5:	71d13017ca60bbf4619dc3faf58fd94e
Source0:	%{name}.desktop
Source1:	%{name}.sh
Patch1:		%{name}-desktop.patch
URL:		http://www.opera.com/
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.356
BuildRequires:	sed >= 4.0
BuildRequires:	xz
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
Requires:	browser-plugins >= 2.0
Requires:	desktop-file-utils
Provides:	wwwbrowser
Obsoletes:	opera-i18n
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0
%define		no_install_post_strip	1

%description
Opera is world fastest web browser. It supports most of nowaday
extensions of HTML. And it is quite stable. This version is linked
with shared version of Qt.

%description -l hu.UTF-8
Opera a világ leggyorsabb webböngészője. A manapság elterjedt
HTML-kiterjesztések túlnyomó többségét támogatja. És elég stabili is.
Ez a verzió a Qt megosztott verziójához linkelődik.

%description -l pl.UTF-8
Opera jest najszybszą przeglądarką WWW na świecie. Obsługuje większość
dzisiejszych rozszerzeń HTML-a. Dodatkowo jest w miarę stabilna. Ta
wersja jest skonsolidowana dynamicznie z Qt.

%prep
%setup -qcT
%ifarch %{x8664}
SOURCE=%{S:10}
%endif

ar x $SOURCE
tar xf control.tar.gz && rm control.tar.gz
tar xf data.tar.xz && rm data.tar.xz

version=$(awk '/Version:/{print $2}' control)
test $version = %{version}

mv usr/lib/*/%{name}/* .
mv usr/share/icons .
mv usr/share/pixmaps/%{name}.xpm .
mv usr/share/applications/%{name}.desktop .
mv usr/share/doc/opera-stable/* .

%patch1 -p1

sed -e 's#/usr/lib/opera#%{_libdir}/opera#g' %{_sourcedir}/%{name}.sh > %{name}.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_libdir}/%{name}/plugins,%{_datadir}/%{name}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_iconsdir},%{_desktopdir}}

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins -b <<'EOF'
# opera does not use for .xpt files
*.xpt
EOF

cp -a localization resources $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p *.pak *.bin *.dat $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -a lib $RPM_BUILD_ROOT%{_libdir}/%{name}
ln -s %{_datadir}/%{name}/localization $RPM_BUILD_ROOT%{_libdir}/%{name}/localization
ln -s %{_datadir}/%{name}/resources $RPM_BUILD_ROOT%{_libdir}/%{name}/resources
install -p %{name} $RPM_BUILD_ROOT%{_libdir}/%{name}
install -p %{name}_sandbox $RPM_BUILD_ROOT%{_libdir}/%{name}
install -p %{name}.sh $RPM_BUILD_ROOT%{_bindir}/%{name}
cp -p %{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -a icons/* $RPM_BUILD_ROOT%{_iconsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_icon_cache hicolor
	%update_desktop_database
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc copyright
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%attr(755,root,root) %{_bindir}/%{name}
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*.png

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/resources
%{_datadir}/%{name}/resources/*.ico
%{_datadir}/%{name}/resources/*.json
%{_datadir}/%{name}/resources/dictionaries.xml
%{_datadir}/%{name}/resources/inspector
%{_datadir}/%{name}/localization

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/icudtl.dat
%{_libdir}/%{name}/natives_blob.bin
%{_libdir}/%{name}/snapshot_blob.bin
%{_libdir}/%{name}/*.pak
%{_libdir}/%{name}/localization
%{_libdir}/%{name}/resources
%dir %{_libdir}/%{name}/lib
%attr(755,root,root) %{_libdir}/%{name}/lib/libffmpeg.so.*
%attr(755,root,root) %{_libdir}/%{name}/lib/libmalloc_wrapper.so
%dir %{_libdir}/%{name}/plugins

%attr(755,root,root) %{_libdir}/%{name}/%{name}
# These unique permissions are intentional and necessary for the sandboxing
%attr(4555,root,root) %{_libdir}/%{name}/%{name}_sandbox
