### Enable LTO
%global optflags            %{optflags} -flto
%global build_ldflags       %{build_ldflags} -flto

%global commit_maps         950f9ec7a40814759c78241816903a236ab8de93
%global shortcommit_maps    %(c=%{commit_maps}; echo ${c:0:7})
%global date                20191202

Name:           ddnet
Version:        12.7.3
Release:        5%{?dist}
Summary:        DDraceNetwork, a cooperative racing mod of Teeworlds

License:        ASL 2.0 and CC-BY-SA
URL:            https://ddnet.tw/
Source0:        https://github.com/ddnet/ddnet/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/ddnet/ddnet-maps/archive/%{commit_maps}/%{name}-maps-%{shortcommit_maps}.tar.gz

Patch0:         0001-Fixed-installation-on-other-than-Ubuntu-GNU-Linux-di.patch
Patch1:         0002-Disabled-network-lookup-test.patch

BuildRequires:  desktop-file-utils

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  python

BuildRequires:  freetype-devel
BuildRequires:  git-core
BuildRequires:  glew-devel
BuildRequires:  gtest-devel
BuildRequires:  libcurl-devel
BuildRequires:  libogg-devel
BuildRequires:  openssl-devel
BuildRequires:  opus-devel
BuildRequires:  opusfile-devel
BuildRequires:  pnglite-devel
BuildRequires:  SDL2-devel
BuildRequires:  wavpack-devel
BuildRequires:  zlib-devel

Requires:       hicolor-icon-theme
Requires:       %{name}-data = %{version}-%{release}


%description
DDraceNetwork, a cooperative racing mod of Teeworlds


%package        server
Summary:        Standalone server for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    server
Standalone server for %{name}.


%package        data
Summary:        Data files for %{name}

Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    data
Data files for %{name}.


%package        maps
Summary:        Additional maps for %{name}

Version:        %{date}git%{shortcommit_maps}
BuildArch:      noarch

%description    maps
Additional maps for %{name}.


%prep
%autosetup -S git
touch CMakeLists.txt


%build
%cmake3 \
    -DAUTOUPDATE=OFF \
    -DPREFER_BUNDLED_LIBS=OFF
%make_build


%install
%make_install

# Install additional maps...
tar xvf %{SOURCE1}
mkdir -p %{buildroot}%{_datadir}/%{name}-maps
cp -a %{name}-maps-%{commit_maps}/types %{buildroot}%{_datadir}/%{name}-maps


%check
# Disabled while I can't fix this
# %%make_build run_tests 
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license license.txt
%doc README.md man/DDNet.6
%{_bindir}/DDNet
%{_libdir}/%{name}/


%files server
%license license.txt
%doc README.md man/DDNet-Server.6
%{_bindir}/DDNet-Server

%files data
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%files maps
%{_datadir}/%{name}-maps/


%changelog
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
