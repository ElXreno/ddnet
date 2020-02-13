# Enable LTO
%bcond_without lto

# Enable Ninja build
%bcond_without ninja_build

%if %{with lto}
%global optflags        %{optflags} -flto=auto
%global build_ldflags   %{build_ldflags} -flto
%endif

Name:           ddnet
Version:        12.9
Release:        2%{?dist}
Summary:        DDraceNetwork, a cooperative racing mod of Teeworlds

#
# zlib
# --------------------------------------
# src/engine/external/md5/
#
# CC-BY-SA
# --------------------------------------
# data/languages/
# data/fonts/DejaVuSansCJKName.ttf
# data/fonts/DejavuWenQuanYiMicroHei.ttf
#
# ASL 2.0
# --------------------------------------
# data/
#
# MIT
# --------------------------------------
# man/
#
# Public domain
# --------------------------------------
# src/base/hash_libtomcrypt.c
#


License:        zlib and CC-BY-SA and ASL 2.0 and MIT and Public Domain
URL:            https://ddnet.tw/
Source0:        https://github.com/ddnet/ddnet/archive/%{version}/%{name}-%{version}.tar.gz

# Disable network lookup test because without internet access tests not pass
Patch1:         0001-disabled-network-lookup-test.patch

# Unbundle md5
Patch2:         0002-unbundled-md5.patch

# Unbundle json-parser
Patch3:         0003-unbundled-json-parser.patch

# Fix build for Rawhide
# PR: https://github.com/ddnet/ddnet/pull/2065
Patch4:         0004-fix-build-for-rawhide.patch

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

%if %{with ninja_build}
BuildRequires:  ninja-build
%endif

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  python

BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(gtest)
BuildRequires:  pkgconfig(json-parser)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(opusfile)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(wavpack)
BuildRequires:  pkgconfig(zlib)

# pkgconfig not available
BuildRequires:  pnglite-devel

Requires:       %{name}-data = %{version}-%{release}

# https://github.com/ddnet/ddnet/issues/2019
Provides:       bundled(dejavu-sans-cjkname-fonts)
Provides:       bundled(dejavu-wenquanyi-micro-hei-fonts)


%description
DDraceNetwork (DDNet) is an actively maintained version of DDRace,
a Teeworlds modification with a unique cooperative gameplay.
Help each other play through custom maps with up to 64 players,
compete against the best in international tournaments, design your
own maps, or run your own server.


%package        data
Summary:        Data files for %{name}

Requires:       %{name} = %{version}-%{release}
Requires:       hicolor-icon-theme

BuildArch:      noarch

%description    data
Data files for %{name}.


%package        server
Summary:        Standalone server for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    server
Standalone server for %{name}.


%prep
%autosetup -S git
touch CMakeLists.txt

# Remove bundled stuff...
rm -rf src/engine/external

mkdir -p %{_target_platform}


%build
# TODO: Add mysql support
# WebSockets disable because it freezes all GUI | https://github.com/ddnet/ddnet/issues/1900
pushd %{_target_platform}
%cmake \
    %{?with_ninja_build: -GNinja} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DPREFER_BUNDLED_LIBS=OFF \
    -DAUTOUPDATE=OFF \
    ..
popd

%if %{with ninja_build}
%ninja_build -C %{_target_platform}
%else
%make_build -C %{_target_platform}
%endif


%install
%if %{with ninja_build}
%ninja_install -C %{_target_platform}
%else
%make_install -C %{_target_platform}
%endif

# Install man pages...
install -Dp -m 0644 man/DDNet.6 %{buildroot}%{_mandir}/man6/DDNet.6
install -Dp -m 0644 man/DDNet-Server.6 %{buildroot}%{_mandir}/man6/DDNet-Server.6


%check
%if %{with ninja_build}
%ninja_build run_tests -C %{_target_platform}
%else
%make_build run_tests -C %{_target_platform}
%endif
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml


%files
%license license.txt
%doc README.md
%{_mandir}/man6/DDNet.6*

%{_bindir}/DDNet
%{_libdir}/%{name}/

%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/*.appdata.xml

%files data
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%files server
%{_mandir}/man6/DDNet-Server.6*

%{_bindir}/DDNet-Server


%changelog
* Thu Feb 13 2020 ElXreno <elxreno@gmail.com> - 12.9-2
- Fixed build error for Rawhide

* Thu Feb 13 2020 ElXreno <elxreno@gmail.com> - 12.9-1
- Updated to version 12.9

* Wed Jan 01 2020 ElXreno <elxreno@gmail.com> - 12.8.1-6
- Applied patch by @atim
- Added license breakdown explanation
- Unbundled md5 and json-parser
- Removed hicolor-icon-theme from main package

* Tue Dec 31 2019 ElXreno <elxreno@gmail.com> - 12.8.1-5
- Added AppData manifest
- Disabled websockets

* Mon Dec 30 2019 ElXreno <elxreno@gmail.com> - 12.8.1-4
- Fixed man pages and license

* Mon Dec 30 2019 ElXreno <elxreno@gmail.com> - 12.8.1-3
- Ninja build

* Mon Dec 30 2019 ElXreno <elxreno@gmail.com> - 12.8.1-2
- WebSockets support for server

* Mon Dec 23 2019 ElXreno <elxreno@gmail.com> - 12.8.1-1
- Updated to version 12.8.1

* Wed Dec 18 2019 ElXreno <elxreno@gmail.com> - 12.8-1
- Updated to version 12.8

* Sun Dec 08 2019 ElXreno <elxreno@gmail.com> - 12.7.3-6
- Extracted ddnet-maps into ddnet-maps.spec, enabled tests

* Sat Dec 07 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 12.7.3-5
- Spec file fixes

* Sat Dec 07 2019 ElXreno <elxreno@gmail.com> - 12.7.3-4
- Updated maps to commit 950f9ec7a40814759c78241816903a236ab8de93

* Fri Dec 06 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 12.7.3-3
- Tim was here :)

* Fri Dec 06 2019 ElXreno <elxreno@gmail.com> - 12.7.3-2
- More docs, tests, and additions

* Sat Nov 30 2019 ElXreno <elxreno@gmail.com> - 12.7.3-1
- Initial packaging
