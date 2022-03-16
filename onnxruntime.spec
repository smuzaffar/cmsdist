### RPM external onnxruntime 1.10.0
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
%define github_user cms-externals
%define branch cms/v%{realversion}
%define tag fefed42f6677be3af5761a04e4d9db8f2b15715d
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&submodules=1&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake ninja
Requires: protobuf py3-numpy py3-wheel py3-onnx zlib libpng py3-pybind11 cuda
%if "%{cmsos}" != "slc7_aarch64"
Requires: cudnn
%endif

%prep
%setup -q -n %{n}-%{realversion}
patch -p1 < %{_sourcedir}/de4089f8cbe0baffe56a363cc3a41595cc8f0809.patch

%build
rm -rf ../build; mkdir ../build; cd ../build

USE_CUDA=OFF
%if "%{cmsos}" != "slc7_aarch64"
if [ "%{cuda_gcc_support}" = "true" ] ; then
USE_CUDA=ON
fi
%endif

cmake ../%{n}-%{realversion}/cmake -GNinja \
   -DPYTHON_EXECUTABLE=${PYTHON3_ROOT}/bin/python3 \
   -DCMAKE_BUILD_TYPE=Release \
   -DCMAKE_INSTALL_PREFIX="%{i}" \
   -DCMAKE_INSTALL_LIBDIR=lib \
   -Donnxruntime_ENABLE_PYTHON=ON \
   -Donnxruntime_BUILD_SHARED_LIB=ON \
   -Donnxruntime_USE_CUDA=${USE_CUDA} \
   -Donnxruntime_CUDA_VERSION="${CUDA_VERSION}" \
   -Donnxruntime_CUDA_HOME="${CUDA_ROOT}" \
   -Donnxruntime_CUDNN_HOME="${CUDNN_ROOT}" \
   -Donnxruntime_BUILD_CSHARP=OFF \
   -Donnxruntime_USE_EIGEN_FOR_BLAS=ON \
   -Donnxruntime_USE_OPENBLAS=OFF \
   -Donnxruntime_USE_MKLML=OFF \
   -Donnxruntime_USE_NGRAPH=OFF \
   -Donnxruntime_USE_OPENMP=OFF \
   -Donnxruntime_USE_TVM=OFF \
   -Donnxruntime_USE_LLVM=OFF \
   -Donnxruntime_ENABLE_MICROSOFT_INTERNAL=OFF \
   -Donnxruntime_USE_BRAINSLICE=OFF \
   -Donnxruntime_USE_NUPHAR=OFF \
   -Donnxruntime_USE_TENSORRT=OFF \
   -Donnxruntime_CROSS_COMPILING=OFF \
   -Donnxruntime_USE_FULL_PROTOBUF=ON \
   -Donnxruntime_DISABLE_CONTRIB_OPS=OFF \
   -Donnxruntime_USE_PREINSTALLED_PROTOBUF=ON \
   -Donnxruntime_PREFER_SYSTEM_LIB=ON \
   -DCMAKE_CUDA_FLAGS="-cudart shared" \
   -DCMAKE_CUDA_RUNTIME_LIBRARY=Shared \
   -DCMAKE_TRY_COMPILE_PLATFORM_VARIABLES="CMAKE_CUDA_RUNTIME_LIBRARY" \
   -DCMAKE_PREFIX_PATH="${ZLIB_ROOT};${LIBPNG_ROOT};${PROTOBUF_ROOT};${PY3_PYBIND11_ROOT}"

ninja -v %{makeprocesses}
python3 ../%{n}-%{realversion}/setup.py build

%install
cd ../build
ninja -v %{makeprocesses} install
mkdir -p %{i}/${PYTHON3_LIB_SITE_PACKAGES}
mv build/lib/onnxruntime %{i}/${PYTHON3_LIB_SITE_PACKAGES}/
