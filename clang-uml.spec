### RPM external clang-uml 0.4.1

%define tag 429e1c47a9669438651076a719de29c00fd18f7b
%define branch master

%define github_user bkryza
Source: git+https://github.com/%{github_user}/clang-uml.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake ninja 
Requires: yaml-cpp llvm

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

#GIT_VERSION can be a random string with the correct set of fields
#it is required as the current default in clang-uml cmake system is not
#correctly formated (issue opened)

CMAKE_PREFIX_PATH=${YAML_CPP_ROOT}/lib64/cmake/yaml-cpp/ cmake ../%{n}-%{realversion} \
  -G Ninja \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_FLAGS="" \
  -DCMAKE_EXE_LINKER_FLAGS="" \
  -DLLVM_VERSION= \
  -DCMAKE_VERBOSE_MAKEFILE=true \
  -DGIT_VERSION="0.4.1-9-g205d6de" \
  -DLLVM_CONFIG_PATH= 

ninja -v %{makeprocesses}

%install
cd ../build
ninja %{makeprocesses} install

%post
%{relocateConfig}share/pkgconfig/yaml-cpp.pc
