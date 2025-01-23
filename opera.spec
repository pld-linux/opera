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
Version:	116.0.5366.51
Release:	1
Epoch:		2
License:	Distributable
Group:		X11/Applications/Networking
Source10:	https://ftp.opera.com/pub/opera/desktop/%{version}/linux/%{name}-stable_%{version}_amd64.deb
# Source10-md5:	bd46b0a0a6170dfcabac2a1119f4fe2b
Source1:	%{name}.sh
Source2:	find-lang.sh
Patch1:		%{name}-desktop.patch
URL:		http://www.opera.com/
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.356
BuildRequires:	sed >= 4.0
BuildRequires:	xz
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	browser-plugins >= 2.0
Requires:	desktop-file-utils
Provides:	wwwbrowser
Obsoletes:	opera-i18n
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		find_lang	sh find-lang.sh %{buildroot}

%define		_enable_debug_packages	0
%define		no_install_post_strip	1

%description
Opera is a fast, secure and user-friendly web browser. It includes web
developer tools, news aggregation, and the ability to compress data
via Opera Turbo on congested networks.

%description -l hu.UTF-8
Opera a világ leggyorsabb webböngészője. A manapság elterjedt
HTML-kiterjesztések túlnyomó többségét támogatja. És elég stabili is.
Ez a verzió a Qt megosztott verziójához linkelődik.

%description -l pl.UTF-8
Opera jest najszybszą przeglądarką WWW na świecie. Obsługuje większość
dzisiejszych rozszerzeń HTML-a. Dodatkowo jest w miarę stabilna. Ta
wersja jest skonsolidowana dynamicznie z Qt.

%package l10n
Summary:	%{name} language packages
Group:		I18n
Requires:	%{name} = %{epoch}:%{version}-%{release}
BuildArch:	noarch

%description l10n
This package contains language packages for 56 languages:

af, az, be, bg, bn, ca, cs, da, de, el, en-GB, es-419, es, fi, fil,
fr-CA, fr, fy, gd, he, hi, hr, hu, id, it, ja, kk, ko, lt, lv, me, mk,
ms, nb, nl, nn, pa, pl, pt-BR, pt-PT, ro, ru, sk, sr, sv, sw, ta, te,
th, tr, uk, uz, vi, zh-CN, zh-TW, zu.

%prep
%setup -qcT
%ifarch %{x8664}
SOURCE=%{S:10}
%endif

ar x $SOURCE
tar xf control.tar.xz && rm control.tar.xz
tar xf data.tar.xz && rm data.tar.xz

version=$(awk '/Version:/{print $2}' control)
test $version = %{version}

mkdir -p lib doc
%{__mv} usr/lib/*/%{name}/* lib/
%{__mv} usr/share/icons .
%{__mv} usr/share/pixmaps/%{name}.xpm .
%{__mv} usr/share/applications/%{name}.desktop .
%{__mv} usr/share/doc/opera-stable/* doc/

%patch -P 1 -p1

%{__sed} -e 's#/usr/lib/opera#%{_libdir}/opera#g' %{_sourcedir}/%{name}.sh > %{name}.sh
%{__sed} -e 's,@localedir@,%{_datadir}/%{name}/localization,' %{_sourcedir}/find-lang.sh > find-lang.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_libdir}/%{name}/plugins,%{_datadir}/%{name}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_iconsdir},%{_desktopdir}}

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins -b <<'EOF'
# opera does not use for .xpt files
*.xpt
EOF

cp -a lib/localization lib/resources $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}/%{name}
%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/{localization,resources}
ln -s %{_datadir}/%{name}/localization $RPM_BUILD_ROOT%{_libdir}/%{name}/localization
ln -s %{_datadir}/%{name}/resources $RPM_BUILD_ROOT%{_libdir}/%{name}/resources

install -p %{name}.sh $RPM_BUILD_ROOT%{_bindir}/%{name}
cp -p %{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -a icons/* $RPM_BUILD_ROOT%{_iconsdir}

# find locales
%find_lang %{name}.lang
# always package en-US
%{__sed} -i -e '/en-US.pak/d' %{name}.lang

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
%doc doc/copyright
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%attr(755,root,root) %{_bindir}/%{name}
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*.png

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/resources
%dir %{_datadir}/%{name}/localization
%{_datadir}/%{name}/localization/en-US.pak

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/icudtl.dat
%{_libdir}/%{name}/snapshot_blob.bin
%{_libdir}/%{name}/*.pak
%{_libdir}/%{name}/localization
%{_libdir}/%{name}/resources
%attr(755,root,root) %{_libdir}/%{name}/chrome_crashpad_handler
%attr(755,root,root) %{_libdir}/%{name}/libEGL.so
%attr(755,root,root) %{_libdir}/%{name}/libffmpeg.so
%attr(755,root,root) %{_libdir}/%{name}/libGLESv2.so
%attr(755,root,root) %{_libdir}/%{name}/libqt5_shim.so
%attr(755,root,root) %{_libdir}/%{name}/libqt6_shim.so
%attr(755,root,root) %{_libdir}/%{name}/libvk_swiftshader.so
%attr(755,root,root) %{_libdir}/%{name}/libvulkan.so.1
%{_libdir}/%{name}/vk_swiftshader_icd.json
%{_libdir}/%{name}/v8_context_snapshot.bin
%dir %{_libdir}/%{name}/plugins

%attr(755,root,root) %{_libdir}/%{name}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/%{name}_crashreporter

%attr(755,root,root) %{_libdir}/%{name}/%{name}_autoupdate
%{_libdir}/%{name}/%{name}_autoupdate.licenses
%{_libdir}/%{name}/%{name}_autoupdate.version

# These unique permissions are intentional and necessary for the sandboxing
%attr(4555,root,root) %{_libdir}/%{name}/%{name}_sandbox

%files l10n -f %{name}.lang
%defattr(644,root,root,755)
