Summary:	Cross Mingw32CE GNU binary utility development utilities - binutils
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - Mingw32CE binutils
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - Mingw32CE binutils
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla Mingw32CE - binutils
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - Mingw32CE binutils
Summary(tr.UTF-8):	GNU geliştirme araçları - Mingw32CE binutils
Name:		crossmingw32ce-binutils
Version:	2.17.50
Release:	0.1
License:	GPL
Group:		Development/Tools
#Source0:	ftp://ftp.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
# https://cegcc.svn.sourceforge.net/svnroot/cegcc/trunk/cegcc/src/binutils
Source0:	binutils-20070226.907.tar.bz2
# Source0-md5:	cf3b51a289913f1e2052dc5165fe8f60
URL:		http://sources.redhat.com/binutils/
BuildRequires:	automake
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-tools
# not necessary unless we patch .texi docs; but they are not packaged here anyway
#BuildRequires:	texinfo >= 4.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		arm-wince-mingw32ce
%define		arch		%{_prefix}/%{target}

%description
crossmingw32ce is a complete cross-compiling development system for
building stand-alone Microsoft Windows CE applications under Linux
using the Mingw32CE build libraries. This includes a binutils, gcc
with g++ and objc, and libstdc++, all cross targeted to
i386-mingw32ce, along with supporting Win32 CE libraries in 'coff'
format from free sources.

This package contains cross targeted binutils.

%description -l pl.UTF-8
crossmingw32ce jest kompletnym systemem do kroskompilacji, pozwalającym
budować aplikacje MS Windows CE pod Linuksem używając bibliotek
mingw32ce. System składa się z binutils, gcc z g++ i objc, libstdc++ -
wszystkie generujące kod dla platformy i386-mingw32ce, oraz z bibliotek
w formacie COFF.

Ten pakiet zawiera binutils generujące skrośnie binaria dla Win32 CE.

%prep
%setup -q -n binutils

%build
cp /usr/share/automake/config.sub .

# Because of a bug in binutils-2.9.1, a cross libbfd.so* is not named
# lib<target>bfd.so*. To prevent confusion with native binutils, we
# forget about shared libraries right now, and do not install libbfd.a
# [the same applies to binutils 2.10.1.0.4]

# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
./configure \
	--disable-shared \
	--disable-nls \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--host=%{_target_platform} \
	--build=%{_target_platform} \
	--target=%{target}

%{__make} all \
	tooldir=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL='$$s/install-sh -c' \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

# remove this man page unless we cross-build for netware platform.
# however, this should be done in Makefiles.
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/*nlmconv.1

# libiberty.a is ELF not PE
rm -f $RPM_BUILD_ROOT%{arch}/lib/libiberty.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%dir %{arch}
%dir %{arch}/lib
%dir %{arch}/bin
%attr(755,root,root) %{arch}/bin/*
%{arch}/lib/ldscripts
%attr(755,root,root) %{_bindir}/%{target}-*
%{_mandir}/man1/%{target}-*
