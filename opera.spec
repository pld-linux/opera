#
# There're some problems with "shared" version
#
%define ver	6.10
%define	rel	20021029.1
Summary:	World fastest web browser
Summary(pl):	Najszybsza przegl±darka WWW na ¶wiecie
Name:		opera
Version:	%{ver}.%{rel}
Release:	1
License:	Restricted, see file LICENSE
Group:		X11/Applications/Networking
#Source0:	ftp://ftp.task.gda.pl/pub/opera/linux/602/final/en/qt_static/%{name}-%{ver}-%{rel}-static-qt.i386.tar.gz
#Source0:	http://web.opera.com/download/unix/untested/intel-linux/257-20021010-6.1-P3/%{name}-%{ver}-%{rel}-static-qt.i386.tar.gz
#Source0:	http://gd.tuwien.ac.at/infosys/browsers/opera/linux/610/beta1/en/static/%{name}-%{ver}-%{rel}-static-qt.i386.tar.gz
Source0:	ftp://ftp.task.gda.pl/pub/opera/linux/610/final/en/i386/static/%{name}-%{ver}-%{rel}-static-qt.i386.tar.gz
Source1:	http://web.opera.com/download/unix/locale/pl.qm.gz
Source2:	opera.desktop
URL:		http://www.opera.com/
ExclusiveArch:	%{ix86}
Requires:	freetype >= 2
Requires:	openmotif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
NoSource:	0
%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_plugindir	%{_libdir}/mozilla/opera
%define		_operadocdir	%{_docdir}/%{name}-%{ver}.%{rel}
%define		configfile	%{_datadir}/opera/config/opera6rc

%description
Opera is world fastest web browser. It supports most of nowaday
extensions of HTML. And it is quite stable. Only disadvantage are
advertisements on the top of its window. Version static linked with qt.

%description -l pl
Opera jest najszybsz± przegl±dark± WWW na ¶wiecie. Obs³uguje wiêkszo¶æ
dzisiejszych rozszerzeñ HTMLa. Dodatkowo jest w miarê stabilna. Jedyn±
niedogodno¶ci± s± reklamy ukazuj±ce siê w górze okna. Wersja statycznie
linkowana z qt.

%prep
%setup -q -n %{name}-%{ver}-%{rel}-static-qt.i386

%install
rm -rf $RPM_BUILD_ROOT

sh install.sh \
  --prefix=$RPM_BUILD_ROOT%{_prefix} \
  --wrapperdir=$RPM_BUILD_ROOT%{_bindir} \
  --docdir=$RPM_BUILD_ROOT%{_operadocdir} \
  --sharedir=$RPM_BUILD_ROOT%{_datadir}/opera \
  --exec_prefix=$RPM_BUILD_ROOT%{_datadir}/opera/bin \
  --plugindir=$RPM_BUILD_ROOT%{_plugindir}

# Polish locale
gunzip -c %{SOURCE1} > $RPM_BUILD_ROOT%{_datadir}/opera/locale/pl.qm

# man install
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp man/opera.1 $RPM_BUILD_ROOT%{_mandir}/man1/

# wrapper correction
sed s#$RPM_BUILD_ROOT## > $RPM_BUILD_ROOT%{_bindir}/opera2 $RPM_BUILD_ROOT%{_bindir}/opera
mv $RPM_BUILD_ROOT%{_bindir}/opera2 $RPM_BUILD_ROOT%{_bindir}/opera

# install in kde etc.
install -d $RPM_BUILD_ROOT%{_pixmapsdir}
cp images/opera.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

install -d $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW
install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW

# symlink który niweluje burkanie siê opery :>
#ln -sf %{_datadir}/opera/ $RPM_BUILD_ROOT/usr/share/
#ln -sf %{_libdir}/opera $RPM_BUILD_ROOT/usr/lib/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE bugreport help
%attr(755,root,root) %{_bindir}/*

%attr(755,root,root) %{_datadir}/opera/bin/*
%{_datadir}/opera/buttons
%{_datadir}/opera/config
%{_datadir}/opera/help
%{_datadir}/opera/images
%{_datadir}/opera/java
%{_datadir}/opera/locale
%{_datadir}/opera/skin
%{_datadir}/opera/styles
%attr(755,root,root) %{_datadir}/opera/chartables.bin
%attr(755,root,root) %{_datadir}/opera/opera6.adr

%attr(755,root,root) %{_plugindir}/*

%{_pixmapsdir}/opera.xpm
%dir %{_applnkdir}/Network/WWW/*

%{_mandir}/man1/opera.1.gz
