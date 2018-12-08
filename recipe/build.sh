mkdir build -p
cd build

if [[ ${c_compiler} != "toolchain_c" ]]; then
    declare -a CMAKE_PLATFORM_FLAGS
    if [[ ${HOST} =~ .*darwin.* ]]; then
        CMAKE_PLATFORM_FLAGS+=(-DCMAKE_OSX_SYSROOT="${CONDA_BUILD_SYSROOT}")
    else
        CMAKE_PLATFORM_FLAGS+=(-DCMAKE_TOOLCHAIN_FILE="${RECIPE_DIR}/cross-linux.cmake")
    fi
fi

cmake .. -G "Ninja" \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=$PREFIX \
      -DNG_INSTALL_DIR_INCLUDE=$PREFIX/include/netgen \
      -DNG_INSTALL_DIR_PYTHON=${SP_DIR} \
      -DNG_INSTALL_DIR_BIN=bin \
      -DNG_INSTALL_DIR_LIB=lib \
      -DNG_INSTALL_DIR_CMAKE=lib/cmake/netgen \
      -DNG_INSTALL_DIR_RES=share \
      -DOCC_INCLUDE_DIR=$PREFIX/include/opencascade \
      -DOCC_LIBRARY_DIR=$PREFIX/lib \
      -DUSE_NATIVE_ARCH=OFF \
      -DUSE_OCC=ON \
      -DUSE_PYTHON=ON \
      -DUSE_GUI=OFF \
      -DUSE_SUPERBUILD=OFF \
      -DBUILD_WITH_CONDA=ON \
      ${CMAKE_PLATFORM_FLAGS[@]} \
      ..

ninja install

