#
# There're some problems with "shared" version
#
%define ver	6.0
%define	rel	20020510.1
Summary:	World fastest web browser
Summary(pl):	Najszybsza przegl±darka WWW na ¶wiecie
Name:		opera
Version:	%{ver}.%{rel}
Release:	1
License:	Restricted, see file LICENSE
Group:		X11/Applications/Networking
Source0:	ftp://ftp.opera.com/pub/opera/linux/600/final/en/qt_static/%{name}-%{ver}-%{rel}-static-qt.i386.tar.bz2
URL:		http://www.opera.com/
ExclusiveArch:	%{ix86}
Requires:	freetype >= 2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
NoSource:	0
%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

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
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}
install -d $RPM_BUILD_ROOT%{_prefix}/opera
install -d $RPM_BUILD_ROOT%{_datadir}/opera/{buttons,config,help,images,locale,skin,styles}
install -d $RPM_BUILD_ROOT%{_pixmapsdir}
install -d $RPM_BUILD_ROOT%{_libdir}/{%{version},plugins}
install -d $RPM_BUILD_ROOT%{_mandir}/man1/
install -d $RPM_BUILD_ROOT/usr/share

for i in buttons config help images locale skin styles;
do cp -r $i $RPM_BUILD_ROOT%{_datadir}/opera;
done

cp man/opera.1 $RPM_BUILD_ROOT%{_mandir}/man1/

cp -r plugins $RPM_BUILD_ROOT%{_libdir}
cp opera $RPM_BUILD_ROOT%{_libdir}/%{version}

cp opera6.adr $RPM_BUILD_ROOT%{_datadir}/opera
cp chartables.bin $RPM_BUILD_ROOT%{_datadir}/opera
cp unicode.dat $RPM_BUILD_ROOT%{_datadir}/opera

# niech ktos wymysli jak wygenerowac wrappera z install.sh albo czysto opera bedzie odpalana
# sh install.sh --jakiesopcje $RPM_BUILD_ROOT%{_bindir}/opera
cp opera $RPM_BUILD_ROOT%{_bindir}/opera
cp images/opera.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

# symlink który niweluje burkanie siê opery :>
ln -sf %{_datadir}/opera/ $RPM_BUILD_ROOT/usr/share/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE bugreport
%attr(755,root,root) %{_bindir}/*
%{_datadir}/opera
%{_pixmapsdir}/opera.xpm
/usr/share/opera
