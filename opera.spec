# BRANCHES:
# - HEAD - stable version
# - DEVEL - development version
# - WEEKLY - weekly development version
#
# NOTE: to avoid creating unreadable/unmaintainable spec:
# - don't put static version here, create STATIC branch for that for example
# - don't create useless bconds that for example limit SourceX: to current arch only
#

%bcond_without	qt4	#take the qt4 version

%define		ver	10.00
%define		shver	%(echo %{ver} | tr -d .)
%define		buildid	4585

Summary:	World fastest web browser
Summary(pl.UTF-8):	Najszybsza przeglądarka WWW na świecie
Name:		opera
Version:	%{ver}
Release:	4
Epoch:		2
License:	Distributable
Group:		X11/Applications/Networking
Source10:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/final/en/i386/shared/%{name}-%{version}.gcc4-shared-qt3.i386.tar.bz2
# Source10-md5:	abf0e90f6c0620b1b1f95b9860b30189
Source11:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/final/en/x86_64/%{name}-%{version}.gcc4-shared-qt3.x86_64.tar.bz2
# Source11-md5:	6f74e9552ab5b45e4e0177ea4beea05e
Source12:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/final/en/ppc/shared/%{name}-%{version}.gcc4-shared-qt3.ppc.tar.bz2
# Source12-md5:	6b25420f7f7a571b0c305c1f9ac03579
Source13:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/final/en/i386/%{name}-%{version}.gcc4-qt4.i386.tar.bz2
# Source13-md5:	0b484b74ee07e5ac93f153dd33e25437
Source14:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/final/en/x86_64/%{name}-%{version}.gcc4-qt4.x86_64.tar.bz2
# Source14-md5:	af8230636786a5c76b267d813db52614
Source0:	%{name}.desktop
Patch0:		%{name}-wrapper.patch
Patch1:		%{name}-agent-qt4.patch
Patch2:		%{name}-agent.patch
URL:		http://www.opera.com/
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.356
BuildRequires:	sed >= 4.0
Requires:	browser-plugins >= 2.0
Requires:	freetype >= 2
Provides:	wwwbrowser
Obsoletes:	opera-i18n
ExclusiveArch:	%{ix86} %{x8664} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/opera/plugins
%define		_operadocdir	%{_docdir}/%{name}-%{ver}
# alternative arch for plugin32
%define		alt_arch	i386

%description
Opera is world fastest web browser. It supports most of nowaday
extensions of HTML. And it is quite stable. This version is linked
with shared version of Qt.

%description -l pl.UTF-8
Opera jest najszybszą przeglądarką WWW na świecie. Obsługuje większość
dzisiejszych rozszerzeń HTML-a. Dodatkowo jest w miarę stabilna. Ta
wersja jest skonsolidowana dynamicznie z Qt.

%package plugin32
Summary:	Opera 32-bit plugins support
Summary(pl.UTF-8):	Obsługa 32-bitowych wtyczek Opery
Group:		X11/Applications/Networking
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	browser-plugins >= 2.0

%description plugin32
Opera 32-bit plugins support.

%description plugin32 -l pl.UTF-8
Obsługa 32-bitowych wtyczek Opery.

%prep
%ifarch %{ix86}
%if %{with qt4}
%setup -q -T -b 13 -n %{name}-%{version}-%{buildid}.gcc4-qt4.i386
%define		_noautoreq	'libpng12.so.0(.*)'
%else
%setup -q -T -b 10 -n %{name}-%{version}-%{buildid}.gcc4-shared-qt3.i386
%endif
%endif
%ifarch %{x8664}
%if %{with qt4}
%setup -q -T -b 14 -n %{name}-%{version}-%{buildid}.gcc4-qt4.x86_64
%define		_noautoreq	'libpng12.so.0(.*)'
%else
%setup -q -T -b 11 -n %{name}-%{version}-%{buildid}.gcc4-shared-qt3.x86_64
%endif
%endif
%ifarch ppc
%setup -q -T -b 12 -n %{name}-%{version}-%{buildid}.gcc4-shared-qt3.ppc
%endif
%patch0 -p1
%if %{with qt4}
%patch1 -p0
%else
%patch2 -p0
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_sysconfdir}}

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins -b <<'EOF'
# opera does not use for .xpt files
*.xpt

# use mplayerplug-in-opera instead
mplayerplug-in*

# opera uses libjava.so to run java
libjavaplugin_oji.so
EOF

%ifarch %{x8664}
install -d $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/plugins
%browser_plugins_add_browser %{name} -a %{alt_arch} -p %{_prefix}/lib/%{name}/plugins -b <<'EOF'
# opera does not use for .xpt files
*.xpt

# use mplayerplug-in-opera instead
mplayerplug-in*

# opera uses libjava.so to run java
libjavaplugin_oji.so
EOF
%endif

sh install.sh \
	DESTDIR=$RPM_BUILD_ROOT \
	--prefix=%{_prefix} \
	--exec_prefix=%{_libdir}/%{name}/bin \
	--plugindir=%{_libdir}/%{name}/plugins \
	--docdir=%{_operadocdir}

# install in kde etc.
install %{SOURCE0} $RPM_BUILD_ROOT%{_desktopdir}

install etc/* $RPM_BUILD_ROOT%{_sysconfdir}
install usr/share/pixmaps/*.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

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
%update_browser_plugins

%postun
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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/operaprefs*.ini

# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.%{_target_base_arch}
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.%{_target_base_arch}.blacklist

%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/opera
%dir %{_libdir}/opera/bin
%attr(755,root,root) %{_libdir}/opera/bin/*
%ifarch %{x8664}
%exclude %{_libdir}/opera/bin/*-ia32-*
%endif
%dir %{_plugindir}
%dir %{_datadir}/opera
%{_datadir}/opera/*.*
%{_datadir}/opera/defaults
%{_datadir}/opera/extra
%{_datadir}/opera/java
%{_datadir}/opera/scripts
%{_datadir}/opera/skin
%{_datadir}/opera/styles
%{_datadir}/opera/ui
%dir %{_datadir}/opera/locale
%{_datadir}/opera/locale/en
%lang(be) %{_datadir}/opera/locale/be
%lang(bg) %{_datadir}/opera/locale/bg
%lang(cs) %{_datadir}/opera/locale/cs
%lang(da) %{_datadir}/opera/locale/da
%lang(de) %{_datadir}/opera/locale/de
%lang(el) %{_datadir}/opera/locale/el
%lang(en_GB) %{_datadir}/opera/locale/en-GB
%lang(es) %{_datadir}/opera/locale/es-ES
%lang(es_LA) %{_datadir}/opera/locale/es-LA
%lang(et) %{_datadir}/opera/locale/et
%lang(fi) %{_datadir}/opera/locale/fi
%lang(fr) %{_datadir}/opera/locale/fr
%lang(fr_CA) %{_datadir}/opera/locale/fr-CA
%lang(fy) %{_datadir}/opera/locale/fy
%lang(hi) %{_datadir}/opera/locale/hi
%lang(hr) %{_datadir}/opera/locale/hr
%lang(hu) %{_datadir}/opera/locale/hu
%lang(id) %{_datadir}/opera/locale/id
%lang(it) %{_datadir}/opera/locale/it
%lang(ja) %{_datadir}/opera/locale/ja
%lang(ka) %{_datadir}/opera/locale/ka
%lang(ko) %{_datadir}/opera/locale/ko
%lang(lt) %{_datadir}/opera/locale/lt
%lang(mk) %{_datadir}/opera/locale/mk
%lang(nb) %{_datadir}/opera/locale/nb
%lang(nl) %{_datadir}/opera/locale/nl
%lang(nn) %{_datadir}/opera/locale/nn
%lang(pl) %{_datadir}/opera/locale/pl
%lang(pt) %{_datadir}/opera/locale/pt
%lang(pt_BR) %{_datadir}/opera/locale/pt-BR
%lang(ro) %{_datadir}/opera/locale/ro
%lang(ru) %{_datadir}/opera/locale/ru
%lang(sk) %{_datadir}/opera/locale/sk
%lang(sr) %{_datadir}/opera/locale/sr
%lang(sv) %{_datadir}/opera/locale/sv
%lang(ta) %{_datadir}/opera/locale/ta
%lang(te) %{_datadir}/opera/locale/te
%lang(tr) %{_datadir}/opera/locale/tr
%lang(uk) %{_datadir}/opera/locale/uk
%lang(zh_CN) %{_datadir}/opera/locale/zh-cn
%lang(zh_HK) %{_datadir}/opera/locale/zh-hk
%lang(zh_TW) %{_datadir}/opera/locale/zh-tw
%{_desktopdir}/*.desktop
%{_mandir}/man1/opera.1*
%{_pixmapsdir}/opera.xpm

%ifarch %{x8664}
%files plugin32
%defattr(644,root,root,755)
# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.%{alt_arch}
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.%{alt_arch}.blacklist
%dir %{_prefix}/lib/%{name}
%dir %{_prefix}/lib/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/bin/*-ia32-*
%endif
