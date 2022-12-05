### RPM external vecgeom v1.2.0
## INCLUDE compilation_flags
%define tag 14d3a5c3d851794da4ca48d7659980dbf73384d4
Source: git+https://gitlab.cern.ch/VecGeom/VecGeom.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake gmake
%define keep_archives true
%define vecgeom_backend Scalar
Patch0: vecgeom-fix-vector

%prep
%setup -n %{n}-%{realversion}

%patch0 -p1

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_CXX_STANDARD:STRING="17" \
  -DCMAKE_AR=$(which gcc-ar) \
  -DCMAKE_RANLIB=$(which gcc-ranlib) \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
%if "%{?arch_build_flags}"
  -DCMAKE_CXX_FLAGS="%{arch_build_flags}" \
%endif
%ifarch x86_64
%if "%{vecgeom_backend}" == "Vc"
  -DVECGEOM_VECTOR=sse3 \
%endif
%endif
  -DVECGEOM_NO_SPECIALIZATION=ON \
  -DVECGEOM_BUILTIN_VECCORE=ON \
  -DVECGEOM_BACKEND=%{vecgeom_backend} \
  -DVECGEOM_GEANT4=OFF \
  -DVECGEOM_ROOT=OFF

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1

%post
%{relocateConfig}lib/cmake/VecGeom/*.cmake
