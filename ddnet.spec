### Enable LTO
%global optflags            %{optflags} -flto
%global build_ldflags       %{build_ldflags} -flto

%global commit_maps         3ae2b530fb45c0aee4f1991187679953c76cecf4
%global shortcommit_maps    %(c=%{commit_maps}; echo ${c:0:7})
%global date                20191130

Name:           ddnet
Version:        12.7.3
Release:        1%{?dist}
Summary:        DDraceNetwork, a cooperative racing mod of Teeworlds

License:        ASL 2.0 and CC-BY-SA
URL:            https://ddnet.tw/
Source0:        https://github.com/ddnet/ddnet/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/ddnet/ddnet-maps/archive/%{commit_maps}/%{name}-maps-%{shortcommit_maps}.tar.gz

Patch0:         0001-Fixed-installation-on-other-than-Ubuntu-GNU-Linux-di.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  python

BuildRequires:  freetype-devel
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


%description
DDraceNetwork, a cooperative racing mod of Teeworlds


%package        server
Summary:        Standalone server for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    server
Standalone server for %{name}.


%package        maps
Summary:        Additional maps for %{name}

Version:        %{date}git%{shortcommit_maps}
BuildArch:      noarch

%description    maps
Additional maps for  %{name}.


%prep
%autosetup
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


%files
%license license.txt
%doc README.md
%{_bindir}/DDNet
%{_libdir}/%{name}/*

%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%files server
%license license.txt
%doc README.md
%{_bindir}/DDNet-Server

%files maps
%{_datadir}/%{name}-maps/


%changelog
* Sat Nov 30 2019 ElXreno <elxreno@gmail.com> - 12.7.3-1
- Initial packaging
