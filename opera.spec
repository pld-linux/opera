# BRANCHES:
# - HEAD - stable version
# - DEVEL - development version
# - WEEKLY - weekly development version (sometimes it's on DEVEL)
%bcond_without	distributable	# distributable or not

%define		subver		1065
%define		subverdir	coffeecode_12.00-1065
%define		rel		1
Summary:	World fastest web browser
Summary(pl.UTF-8):	Najszybsza przeglądarka WWW na świecie
Name:		opera-next
Version:	12.00
Release:	0.%{subver}.%{rel}
Epoch:		2
License:	Distributable
Group:		X11/Applications/Networking
Source0:	http://snapshot.opera.com/unix/%{subverdir}/%{name}-%{version}-%{subver}.i386.linux.tar.xz
# Source0-md5:	b15b9de45cd984fff831a3e24074d71d
%{!?with_distributable:NoSource:	0}
Source1:	http://snapshot.opera.com/unix/%{subverdir}/%{name}-%{version}-%{subver}.x86_64.linux.tar.xz
# Source1-md5:	9ad974de58a74d270792a0861d0d2136
%{!?with_distributable:NoSource:	1}
Patch0:		opera-wrapper.patch
Patch1:		opera-desktop.patch
Patch2:		opera-pluginpath.patch
URL:		http://www.opera.com/
BuildRequires:	rpmbuild(macros) >= 1.356
BuildRequires:	sed >= 4.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
Requires:	browser-plugins >= 2.0
Requires:	freetype >= 2
Suggests:	gstreamer-theora
Suggests:	gstreamer-vorbis
Provides:	wwwbrowser
Obsoletes:	opera-i18n
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0

%define		_plugindir		%{_libdir}/opera-next/plugins
%define		_operadocdir	%{_docdir}/%{name}-%{version}

%description
Opera is world fastest web browser. It supports most of nowaday
extensions of HTML. And it is quite stable.

%description -l pl.UTF-8
Opera jest najszybszą przeglądarką WWW na świecie. Obsługuje większość
dzisiejszych rozszerzeń HTML-a. Dodatkowo jest w miarę stabilna.

%package plugin32
Summary:	Opera 32-bit plugins support
Summary(pl.UTF-8):	Obsługa 32-bitowych wtyczek Opery
Group:		X11/Applications/Networking
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description plugin32
Opera 32-bit plugins support.

%description plugin32 -l pl.UTF-8
Obsługa 32-bitowych wtyczek Opery.

%prep
%ifarch %{ix86}
%setup -q -T -b0 -n %{name}-%{version}-%{subver}.i386.linux
%endif
%ifarch %{x8664}
%setup -q -T -b1 -n %{name}-%{version}-%{subver}.x86_64.linux
%endif

%patch0 -p1
%patch1 -p1

sed -i -e '
	s,@@{PREFIX},%{_prefix},g
	s,@@{SUFFIX},-next,
	s,@@{_SUFFIX}, Next,
' share/{applications/*.desktop,mime/packages/*.xml}

sed -i -e 's,kfmclient exec,xdg-open,' share/opera-next/defaults/filehandler.ini

# remove lib32/lib64 paths so patch2 can apply (i386 build contained lib64 as well, oh well)
%{__sed} -i -e '/lib32\|lib64/d;$d' share/opera-next/defaults/pluginpath.ini
%patch2 -p1

mv lib/opera-next/plugins/README README.plugins
mv share/opera-next/defaults/license.txt .
mv share/doc/opera-next/* .

# nobody wants scalable huge icons
rm -rf share/icons/hicolor/scalable

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
cp -a lib/opera-next $RPM_BUILD_ROOT%{_libdir}
cp -a share/* $RPM_BUILD_ROOT%{_datadir}
#cp -a etc/*.ini $RPM_BUILD_ROOT%{_sysconfdir}

sed -i -e 's#/usr/lib/opera-next#%{_libdir}/opera-next#g' $RPM_BUILD_ROOT%{_bindir}/opera-next

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

%files
%defattr(644,root,root,755)
%doc LICENSE
#%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/opera*ini

# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%attr(755,root,root) %{_bindir}/opera-next
%attr(755,root,root) %{_bindir}/opera-next-widget-manager
%dir %{_libdir}/opera-next
%ifarch %{x8664}
%exclude %{_libdir}/opera-next/*-ia32-*
%endif
%attr(755,root,root) %{_libdir}/opera-next/*.so
%attr(755,root,root) %{_libdir}/opera-next/opera*
%dir %{_plugindir}
%dir %{_libdir}/opera-next/gstreamer
%dir %{_libdir}/opera-next/gstreamer/plugins
%attr(755,root,root) %{_libdir}/opera-next/gstreamer/plugins/libgstoperamatroska.so
%attr(755,root,root) %{_libdir}/opera-next/gstreamer/plugins/libgstoperavp8.so
%dir %{_datadir}/opera-next
%{_datadir}/mime/packages/opera-next-extension.xml
%{_datadir}/opera-next/*.*
%{_datadir}/opera-next/defaults
%{_datadir}/opera-next/extra
%{_datadir}/opera-next/skin
#%{_datadir}/opera-next/scripts
%{_datadir}/opera-next/styles
%{_datadir}/opera-next/ui
%{_datadir}/opera-next/unite
%dir %{_datadir}/opera-next/locale
%{_datadir}/opera-next/locale/en
%lang(af) %{_datadir}/opera-next/locale/af
%lang(az) %{_datadir}/opera-next/locale/az
%lang(be) %{_datadir}/opera-next/locale/be
%lang(bg) %{_datadir}/opera-next/locale/bg
%lang(cs) %{_datadir}/opera-next/locale/cs
%lang(da) %{_datadir}/opera-next/locale/da
%lang(de) %{_datadir}/opera-next/locale/de
%lang(el) %{_datadir}/opera-next/locale/el
%lang(en_GB) %{_datadir}/opera-next/locale/en-GB
%lang(es_ES) %{_datadir}/opera-next/locale/es-ES
%lang(es_LA) %{_datadir}/opera-next/locale/es-LA
%lang(et) %{_datadir}/opera-next/locale/et
%lang(fi) %{_datadir}/opera-next/locale/fi
%lang(fr) %{_datadir}/opera-next/locale/fr
%lang(fr_CA) %{_datadir}/opera-next/locale/fr-CA
%lang(fy) %{_datadir}/opera-next/locale/fy
%lang(gd) %{_datadir}/opera-next/locale/gd
%lang(hi) %{_datadir}/opera-next/locale/hi
%lang(hr) %{_datadir}/opera-next/locale/hr
%lang(hu) %{_datadir}/opera-next/locale/hu
%lang(id) %{_datadir}/opera-next/locale/id
%lang(it) %{_datadir}/opera-next/locale/it
%lang(ja) %{_datadir}/opera-next/locale/ja
%lang(ka) %{_datadir}/opera-next/locale/ka
%lang(ko) %{_datadir}/opera-next/locale/ko
%lang(lt) %{_datadir}/opera-next/locale/lt
%lang(me) %{_datadir}/opera-next/locale/me
%lang(mk) %{_datadir}/opera-next/locale/mk
%lang(ms) %{_datadir}/opera-next/locale/ms
%lang(nb) %{_datadir}/opera-next/locale/nb
%lang(nl) %{_datadir}/opera-next/locale/nl
%lang(nn) %{_datadir}/opera-next/locale/nn
%lang(pl) %{_datadir}/opera-next/locale/pl
%lang(pt) %{_datadir}/opera-next/locale/pt
%lang(pt_BR) %{_datadir}/opera-next/locale/pt-BR
%lang(ro) %{_datadir}/opera-next/locale/ro
%lang(ru) %{_datadir}/opera-next/locale/ru
%lang(sk) %{_datadir}/opera-next/locale/sk
%lang(sr) %{_datadir}/opera-next/locale/sr
%lang(sv) %{_datadir}/opera-next/locale/sv
%lang(ta) %{_datadir}/opera-next/locale/ta
%lang(te) %{_datadir}/opera-next/locale/te
%lang(th) %{_datadir}/opera-next/locale/th
%lang(tl) %{_datadir}/opera-next/locale/tl
%lang(tr) %{_datadir}/opera-next/locale/tr
%lang(uk) %{_datadir}/opera-next/locale/uk
%lang(uz) %{_datadir}/opera-next/locale/uz
%lang(vi) %{_datadir}/opera-next/locale/vi
%lang(zh_CN) %{_datadir}/opera-next/locale/zh-cn
#%lang(zh_HK) %{_datadir}/opera-next/locale/zh-hk
%lang(zh_TW) %{_datadir}/opera-next/locale/zh-tw
%{_datadir}/mime/packages/opera-next-widget.xml
%{_datadir}/mime/packages/opera-next-unite-application.xml
%{_desktopdir}/*.desktop
%{_mandir}/man1/opera-next.1*
%{_mandir}/man1/opera-next-widget-manager.1*
#%{_pixmapsdir}/opera.xpm
%{_iconsdir}/hicolor/*/*/*.png

%ifarch %{x8664}
%files plugin32
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/opera-next/*-ia32-*
%endif
