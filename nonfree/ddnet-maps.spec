%global commit         8e66897be14e62d705419890037e7e06868e88b7
%global shortcommit    %(c=%{commit}; echo ${c:0:7})
%global date           20191218

Name:           ddnet-maps
Version:        0
Release:        2.%{date}git%{shortcommit}%{?dist}
Summary:        Additional maps for ddnet

# Not sure, but I think it is nonfree
# https://github.com/ddnet/ddnet-maps/issues/3
License:        nonfree
URL:            https://github.com/ddnet/ddnet-maps
Source0:        https://github.com/ddnet/ddnet-maps/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildArch:      noarch

%description
Additional maps for ddnet.


%prep
%autosetup


%install
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a types %{buildroot}%{_datadir}/%{name}


%files
# %%license add-license-file-here
%doc README.md
%{_datadir}/%{name}/



%changelog
* Wed Dec 18 2019 ElXreno <elxreno@gmail.com> - 0-2.20191218git8e66897
- Updated to commit 8e66897be14e62d705419890037e7e06868e88b7

* Sun Dec  8 2019 ElXreno <elxreno@gmail.com> - 0-1.20191202git3ae2b53
- Initial packaging from ddnet.spec
