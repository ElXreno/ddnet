### Enable LTO
%bcond_without lto

### Enable Ninja build
%bcond_without ninja_build

%if %{with lto}
%global optflags        %{optflags} -flto
%global build_ldflags   %{build_ldflags} -flto
%endif

Name:           ddnet
Version:        12.8.1
Release:        3%{?dist}
Summary:        DDraceNetwork, a cooperative racing mod of Teeworlds

License:        ASL 2.0 and CC-BY-SA 3.0
URL:            https://ddnet.tw/
Source0:        https://github.com/ddnet/ddnet/archive/%{version}/%{name}-%{version}.tar.gz

Patch1:         0001_ddnet_Disabled-network-lookup-test.patch

BuildRequires:  desktop-file-utils

%if %{with ninja_build}
BuildRequires:  ninja-build
%endif

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  python

BuildRequires:  freetype-devel
BuildRequires:  git-core
BuildRequires:  glew-devel
BuildRequires:  gtest-devel
BuildRequires:  libcurl-devel
BuildRequires:  libogg-devel
BuildRequires:  libwebsockets-devel
BuildRequires:  openssl-devel
BuildRequires:  opus-devel
BuildRequires:  opusfile-devel
BuildRequires:  pnglite-devel
BuildRequires:  SDL2-devel
BuildRequires:  wavpack-devel
BuildRequires:  zlib-devel

Requires:       hicolor-icon-theme
Requires:       %{name}-data = %{version}-%{release}

Provides:       bundled(dejavu-sans-cjkname-fonts)
Provides:       bundled(dejavu-wenquanyi-micro-hei-fonts)


%description
DDraceNetwork, a cooperative racing mod of Teeworlds


%package        data
Summary:        Data files for %{name}

Requires:       %{name} = %{version}-%{release}
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


%build
CMAKE3_EXTRA_FLAGS=""

%if %{with ninja_build}
CMAKE3_EXTRA_FLAGS="${CMAKE3_EXTRA_FLAGS} -GNinja"
%endif

%cmake ${CMAKE3_EXTRA_FLAGS} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DPREFER_BUNDLED_LIBS=OFF \
    -DWEBSOCKETS=ON \
    -DAUTOUPDATE=OFF

%if %{with ninja_build}
%ninja_build
%else
%make_build
%endif


%install
%if %{with ninja_build}
%ninja_install
%else
%make_install
%endif


%check
%if %{with ninja_build}
%ninja_build run_tests
%else
%make_build run_tests
%endif
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license license.txt
%doc README.md man/DDNet.6
%{_bindir}/DDNet
%{_libdir}/%{name}/

%files data
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%files server
%license license.txt
%doc README.md man/DDNet-Server.6
%{_bindir}/DDNet-Server


%changelog
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
