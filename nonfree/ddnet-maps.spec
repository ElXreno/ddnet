%global commit         950f9ec7a40814759c78241816903a236ab8de93
%global shortcommit    %(c=%{commit}; echo ${c:0:7})
%global date           20191202

Name:           ddnet-maps
Version:        0
Release:        1.%{date}git%{shortcommit}%{?dist}
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
* Sun Dec  8 2019 ElXreno <elxreno@gmail.com> - 0-1.20191202git3ae2b53
- Initial packaging from ddnet.spec
