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

%define		ver	12.00
%define		shver	%(echo %{ver} | tr -d .)
%define		buildid	1467

Summary:	World fastest web browser
Summary(hu.UTF-8):	A világ leggyorsabb webböngészője
Summary(pl.UTF-8):	Najszybsza przeglądarka WWW na świecie
Name:		opera
Version:	%{ver}
Release:	1
Epoch:		2
License:	Distributable
Group:		X11/Applications/Networking
Source10:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{name}-%{version}-%{buildid}.i386.linux.tar.xz
# Source10-md5:	869274a8a021e965fd56519894851bfb
Source11:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{name}-%{version}-%{buildid}.x86_64.linux.tar.xz
# Source11-md5:	c9a4a298e525ee61cbcd58059562c2b8
Source0:	%{name}.desktop
Patch0:		%{name}-wrapper.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-pluginpath.patch
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
Requires:	freetype >= 2
Suggests:	gstreamer-theora
Suggests:	gstreamer-vorbis
Provides:	wwwbrowser
Obsoletes:	opera-i18n
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0

%define		_plugindir	%{_libdir}/opera/plugins
%define		_operadocdir	%{_docdir}/%{name}-%{ver}
# alternative arch for plugin32
%define		alt_arch	i386

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

%package plugin32
Summary:	Opera 32-bit plugins support
Summary(hu.UTF-8):	Opera 32-bites plugin támogatás
Summary(pl.UTF-8):	Obsługa 32-bitowych wtyczek Opery
Group:		X11/Applications/Networking
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	browser-plugins >= 2.0

%description plugin32
Opera 32-bit plugins support.

%description plugin32 -l hu.UTF-8
Opera 32-bites plugin támogatás.

%description plugin32 -l pl.UTF-8
Obsługa 32-bitowych wtyczek Opery.

%prep
%ifarch %{ix86}
%setup -q -T -b 10 -n %{name}-%{version}-%{buildid}.i386.linux
%endif

%ifarch %{x8664}
%setup -q -T -b 11 -n %{name}-%{version}-%{buildid}.x86_64.linux
%endif

sed -i -e '
	s,@@{PREFIX},%{_prefix},g
	s,@@{SUFFIX},,
	s,@@{_SUFFIX},,
' share/{applications/*.desktop,mime/packages/*.xml}

sed -i -e 's,kfmclient exec,xdg-open,' share/opera/defaults/filehandler.ini

%patch0 -p1
%patch1 -p1

# remove lib32/lib64 paths so patch2 can apply (i386 build contained lib64 as well, oh well)
%{__sed} -i -e '/lib32\|lib64/d;$d' share/opera/defaults/pluginpath.ini
%patch2 -p1

mv lib/opera/plugins/README README.plugins
mv share/opera/defaults/license.txt .
mv share/doc/opera/* .

# nobody wants scalable huge icons
rm -rf share/icons/hicolor/scalable

# opera packaging tools we don't need runtime
mv share/opera/package-id.ini .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_datadir},%{_pixmapsdir},%{_desktopdir},%{_sysconfdir}}

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins -b <<'EOF'
# opera does not use for .xpt files
*.xpt

# use mplayerplug-in-opera instead
mplayerplug-in*
EOF

install -p opera* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/opera $RPM_BUILD_ROOT%{_libdir}
cp -a share/* $RPM_BUILD_ROOT%{_datadir}
#cp -a etc/*.ini $RPM_BUILD_ROOT%{_sysconfdir}

sed -i -e 's#/usr/lib/opera#%{_libdir}/opera#g' $RPM_BUILD_ROOT%{_bindir}/opera

cat << 'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/operaprefs_default.ini
[ISP]
Id="DISTRO"
EOF

%if "%{pld_release}" == "ti"
sed -i -e 's#DISTRO#PLD/Titanium#g' $RPM_BUILD_ROOT/etc/operaprefs_default.ini
%else
%if "%{pld_release}" == "ac"
sed -i -e 's#DISTRO#PLD/2.0 (Ac)#g' $RPM_BUILD_ROOT/etc/operaprefs_default.ini
%else
sed -i -e 's#DISTRO#PLD/3.0 (Th)#g' $RPM_BUILD_ROOT/etc/operaprefs_default.ini
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_mime_database
%update_icon_cache hicolor
%update_desktop_database_post
%update_browser_plugins

%postun
%update_mime_database
%update_icon_cache hicolor
%update_desktop_database_postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%post plugin32
%update_browser_plugins

%postun plugin32
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc LICENSE
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/opera*ini

# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%attr(755,root,root) %{_bindir}/opera
#%attr(755,root,root) %{_bindir}/opera-widget-manager
%dir %{_libdir}/opera
%ifarch %{x8664}
%exclude %{_libdir}/opera/*-ia32-*
%endif
%attr(755,root,root) %{_libdir}/opera/*.so
%attr(755,root,root) %{_libdir}/opera/opera*
%attr(755,root,root) %{_libdir}/opera/pluginwrapper/*
%dir %{_libdir}/opera/pluginwrapper
%dir %{_plugindir}
%dir %{_libdir}/opera/gstreamer
%dir %{_libdir}/opera/gstreamer/plugins
%attr(755,root,root) %{_libdir}/opera/gstreamer/plugins/libgstoperamatroska.so
%attr(755,root,root) %{_libdir}/opera/gstreamer/plugins/libgstoperavp8.so
%dir %{_datadir}/opera
%{_datadir}/mime/packages/opera-extension.xml
%{_datadir}/opera/*.*
%{_datadir}/opera/defaults
%{_datadir}/opera/extra
%{_datadir}/opera/skin
#%{_datadir}/opera/scripts
%{_datadir}/opera/styles
%{_datadir}/opera/ui
#%{_datadir}/opera/unite
%dir %{_datadir}/opera/locale
%{_datadir}/opera/locale/en
%lang(af) %{_datadir}/opera/locale/af
%lang(ar) %{_datadir}/opera/locale/ar
%lang(az) %{_datadir}/opera/locale/az
%lang(be) %{_datadir}/opera/locale/be
%lang(bg) %{_datadir}/opera/locale/bg
%lang(bn) %{_datadir}/opera/locale/bn
%lang(cs) %{_datadir}/opera/locale/cs
%lang(da) %{_datadir}/opera/locale/da
%lang(de) %{_datadir}/opera/locale/de
%lang(el) %{_datadir}/opera/locale/el
%lang(en_GB) %{_datadir}/opera/locale/en-GB
%lang(es_ES) %{_datadir}/opera/locale/es-ES
%lang(es_LA) %{_datadir}/opera/locale/es-LA
%lang(et) %{_datadir}/opera/locale/et
%lang(fa) %{_datadir}/opera/locale/fa
%lang(fi) %{_datadir}/opera/locale/fi
%lang(fr) %{_datadir}/opera/locale/fr
%lang(fr_CA) %{_datadir}/opera/locale/fr-CA
%lang(fy) %{_datadir}/opera/locale/fy
%lang(gd) %{_datadir}/opera/locale/gd
%lang(he) %{_datadir}/opera/locale/he
%lang(hi) %{_datadir}/opera/locale/hi
%lang(hr) %{_datadir}/opera/locale/hr
%lang(hu) %{_datadir}/opera/locale/hu
%lang(id) %{_datadir}/opera/locale/id
%lang(it) %{_datadir}/opera/locale/it
%lang(ja) %{_datadir}/opera/locale/ja
%lang(ka) %{_datadir}/opera/locale/ka
%lang(kk) %{_datadir}/opera/locale/kk
%lang(ko) %{_datadir}/opera/locale/ko
%lang(lt) %{_datadir}/opera/locale/lt
%lang(me) %{_datadir}/opera/locale/me
%lang(mk) %{_datadir}/opera/locale/mk
%lang(ms) %{_datadir}/opera/locale/ms
%lang(nb) %{_datadir}/opera/locale/nb
%lang(nl) %{_datadir}/opera/locale/nl
%lang(nn) %{_datadir}/opera/locale/nn
%lang(pa) %{_datadir}/opera/locale/pa
%lang(pl) %{_datadir}/opera/locale/pl
%lang(pt) %{_datadir}/opera/locale/pt
%lang(pt_BR) %{_datadir}/opera/locale/pt-BR
%lang(ro) %{_datadir}/opera/locale/ro
%lang(ru) %{_datadir}/opera/locale/ru
%lang(sk) %{_datadir}/opera/locale/sk
%lang(sr) %{_datadir}/opera/locale/sr
%lang(sv) %{_datadir}/opera/locale/sv
%lang(sw) %{_datadir}/opera/locale/sw
%lang(ta) %{_datadir}/opera/locale/ta
%lang(te) %{_datadir}/opera/locale/te
%lang(th) %{_datadir}/opera/locale/th
%lang(tl) %{_datadir}/opera/locale/tl
%lang(tr) %{_datadir}/opera/locale/tr
%lang(uk) %{_datadir}/opera/locale/uk
%lang(ur) %{_datadir}/opera/locale/ur
%lang(uz) %{_datadir}/opera/locale/uz
%lang(vi) %{_datadir}/opera/locale/vi
%lang(zh_CN) %{_datadir}/opera/locale/zh-cn
#%lang(zh_HK) %{_datadir}/opera/locale/zh-hk
%lang(zh_TW) %{_datadir}/opera/locale/zh-tw
%lang(zu) %{_datadir}/opera/locale/zu
%{_datadir}/opera/region
#%{_datadir}/mime/packages/opera-widget.xml
#%{_datadir}/mime/packages/opera-unite-application.xml
%{_desktopdir}/*.desktop
%{_mandir}/man1/opera.1*
#%{_mandir}/man1/opera-widget-manager.1*
#%{_pixmapsdir}/opera.xpm
%{_iconsdir}/hicolor/*/*/*.png

%ifarch %{x8664}
%files plugin32
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/opera/*-ia32-*
%endif
