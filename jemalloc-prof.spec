%define jemalloc_version 5.2.1
### RPM external jemalloc-prof %{jemalloc_version}
%define tag de1caefb587217f0b519eb425d7a9b3570e5ba28
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/jemalloc.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: autotools
Requires: libunwind

%prep
%setup -n %{n}-%{realversion}

%build

./autogen.sh --enable-shared \
  --disable-static \
  --disable-doc \
  --enable-stats \
  --enable-prof \
  --enable-prof-libunwind \
  --prefix %{i}

%post
%{relocateConfig}bin/jemalloc.sh
%{relocateConfig}bin/jemalloc-config
