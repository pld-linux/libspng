#
# Conditional build:
%bcond_with	miniz		# miniz instead of zlib
%bcond_without	static_libs	# static library
%bcond_with	sse		# SSE instructions
%bcond_with	sse2		# SSE2 instructions
%bcond_with	ssse3		# SSSE3 instructions
%bcond_with	sse41		# SSE4.1 instructions
#
%ifarch pentium3 pentium4 %{x8664} x32
%define	with_sse	1
%endif
%ifarch pentium4 %{x8664} x32
%define	with_sse2	1
%endif
%if %{without sse} || %{without sse2} || %{without ssse3}
%undefine	with_sse41
%endif
%if %{without sse} || %{without sse2}
%undefine	with_ssse3
%endif
%if %{without sse}
%undefine	with_sse2
%endif
Summary:	PNG decoding and encoding library
Summary(pl.UTF-8):	Biblioteka do dekodowania i kodowania PNG
Name:		libspng
Version:	0.6.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/randy408/libspng/releases
Source0:	https://github.com/randy408/libspng/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1300ee3c8f78032e0eff9c65607d2a52
#Patch0:	%{name}-what.patch
URL:		https://github.com/randy408/libspng
BuildRequires:	meson
%{?with_miniz:BuildRequires:	miniz-devel}
BuildRequires:	ninja >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.736
%{!?with_miniz:BuildRequires:	zlib-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libspng is a C library for reading and writing Portable Network
Graphics (PNG) format files with a focus on security and ease of use.

libspng is an alternative to libpng, the projects are separate and the
APIs are not compatible.

%description -l pl.UTF-8
libspng to biblioteka C do odczytu i zapisu plików w formacie PNG
(Portable Network Graphics), skupiająca się na bezpieczeństwie i
łatwości użycia.

libspng to alternatywa dla libpng - projekty są osobne, a API nie są
kompatybilne.

%package devel
Summary:	Header files for libspng library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libspng
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_miniz:Requires:	miniz-devel}
%{!?with_miniz:Requires:	zlib-devel}

%description devel
Header files for libspng library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libspng.

%package static
Summary:	Static libspng library
Summary(pl.UTF-8):	Statyczna biblioteka libspng
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libspng library.

%description static -l pl.UTF-8
Statyczna biblioteka libspng.

%prep
%setup -q

%build
%if %{with sse2}
CPPFLAGS="%{rpmcppflags} -DSPNG_SSE=%{?with_sse41:4}%{!?with_sse41:%{?with_ssse3:3}%{!?with_ssse3:2}}"
%endif
%meson build \
%if %{without sse}
	-Denable_opt=false \
%endif
	%{?with_miniz:-Duse_miniz=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libspng.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspng.so.0

%files devel
%defattr(644,root,root,755)
%doc docs/*.md
%attr(755,root,root) %{_libdir}/libspng.so
%{_includedir}/spng.h
%{_pkgconfigdir}/spng.pc
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libspng.a
%endif
