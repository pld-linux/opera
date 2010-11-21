# BRANCHES:
# - HEAD - stable version
# - DEVEL - development version
# - WEEKLY - weekly development version (sometimes it's on DEVEL)
%bcond_without	distributable	# distributable or not

%define		subver		1104
%define		subverdir	one_step_closer_11.00_1104
%define		rel		1
Summary:	World fastest web browser
Summary(pl.UTF-8):	Najszybsza przeglądarka WWW na świecie
Name:		opera
Version:	11.00
Release:	0.%{subver}.%{rel}
Epoch:		2
License:	Distributable
Group:		X11/Applications/Networking
Source0:	http://snapshot.opera.com/unix/%{subverdir}/%{name}-%{version}-%{subver}.i386.linux.tar.xz
# Source0-md5:	3940907de346dc90ae4892e32c719b47
%{!?with_distributable:NoSource:	0}
Source1:	http://snapshot.opera.com/unix/%{subverdir}/%{name}-%{version}-%{subver}.x86_64.linux.tar.xz
# Source1-md5:	d01ce0b3f248711f0eca6bda3b8d86c9
%{!?with_distributable:NoSource:	1}
Patch0:		%{name}-wrapper.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-pluginpath.patch
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

%define		_plugindir		%{_libdir}/opera/plugins
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
mv share/opera/package .

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

%attr(755,root,root) %{_bindir}/opera
%attr(755,root,root) %{_bindir}/opera-widget-manager
%dir %{_libdir}/opera
%ifarch %{x8664}
%exclude %{_libdir}/opera/*-ia32-*
%endif
%attr(755,root,root) %{_libdir}/opera/*.so
%attr(755,root,root) %{_libdir}/opera/opera*
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
%{_datadir}/opera/unite
%dir %{_datadir}/opera/locale
%{_datadir}/opera/locale/en
%lang(be) %{_datadir}/opera/locale/be
%lang(bg) %{_datadir}/opera/locale/bg
%lang(cs) %{_datadir}/opera/locale/cs
%lang(da) %{_datadir}/opera/locale/da
%lang(de) %{_datadir}/opera/locale/de
%lang(el) %{_datadir}/opera/locale/el
%lang(en_GB) %{_datadir}/opera/locale/en-GB
%lang(es_ES) %{_datadir}/opera/locale/es-ES
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
%lang(vi) %{_datadir}/opera/locale/vi
%lang(zh_CN) %{_datadir}/opera/locale/zh-cn
%lang(zh_HK) %{_datadir}/opera/locale/zh-hk
%lang(zh_TW) %{_datadir}/opera/locale/zh-tw
%{_datadir}/mime/packages/opera-widget.xml
%{_datadir}/mime/packages/opera-unite-application.xml
%{_desktopdir}/*.desktop
%{_mandir}/man1/opera.1*
%{_mandir}/man1/opera-widget-manager.1*
#%{_pixmapsdir}/opera.xpm
%{_iconsdir}/hicolor/*/*/*.png

%ifarch %{x8664}
%files plugin32
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/opera/*-ia32-*
%endif
