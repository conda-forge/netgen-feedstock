mkdir build -p
cd build

# Source tarball has no .git; avoid wrong fallback in generate_version_file.cmake
: "${PKG_VERSION:?PKG_VERSION must be set}"
NETGEN_VERSION_GIT="v${PKG_VERSION}-0"

if [[ "$(uname -s)" == "Darwin" ]]; then
  _RPATH_EXTRA=(
    -D "CMAKE_INSTALL_RPATH=${PREFIX}/lib"
    -D CMAKE_INSTALL_RPATH_USE_LINK_PATH=ON
    -D CMAKE_BUILD_WITH_INSTALL_RPATH=ON
    -D CMAKE_MACOSX_RPATH=ON
  )
else
  _RPATH_EXTRA=(
    -D "CMAKE_INSTALL_RPATH=${PREFIX}/lib"
    -D CMAKE_INSTALL_RPATH_USE_LINK_PATH=ON
  )
fi

cmake -G "Ninja" \
      -D CMAKE_BUILD_TYPE=Release \
      -D NETGEN_VERSION_GIT="${NETGEN_VERSION_GIT}" \
      -D CMAKE_INSTALL_PREFIX="$PREFIX" \
      -D CMAKE_PREFIX_PATH="$PREFIX" \
      -D NG_INSTALL_DIR_INCLUDE="$PREFIX/include/netgen" \
      -D NG_INSTALL_DIR_PYTHON="${SP_DIR}" \
      -D NG_INSTALL_DIR_BIN=bin \
      -D NG_INSTALL_DIR_LIB=lib \
      -D NG_INSTALL_DIR_CMAKE=lib/cmake/netgen \
      -D NG_INSTALL_DIR_RES=share \
      -D OCC_INCLUDE_DIR="$PREFIX/include/opencascade" \
      -D OCC_LIBRARY_DIR="$PREFIX/lib" \
      -D USE_NATIVE_ARCH=OFF \
      -D USE_OCC=ON \
      -D USE_PYTHON=ON \
      -D USE_GUI=OFF \
      -D USE_SUPERBUILD=OFF \
      -D BUILD_FOR_CONDA=ON \
      -D Python3_ROOT_DIR="$PREFIX" \
      "${_RPATH_EXTRA[@]}" \
      ${CMAKE_PLATFORM_FLAGS[@]} \
      ..

ninja install -v
