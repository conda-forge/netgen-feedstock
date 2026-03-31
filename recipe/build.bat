mkdir build
cd build

cmake -G "Ninja" ^
      -D CMAKE_BUILD_TYPE="Release" ^
      -D "NETGEN_VERSION_GIT=v%PKG_VERSION%-0" ^
      -D "CMAKE_INSTALL_RPATH=%PREFIX%/lib" ^
      -D CMAKE_INSTALL_RPATH_USE_LINK_PATH=ON ^
      -D INSTALL_DIR_LAYOUT="Unix" ^
      -D CMAKE_PREFIX_PATH:FILEPATH="%PREFIX%" ^
      -D CMAKE_INSTALL_PREFIX:FILEPATH="%PREFIX%" ^
      -D NG_INSTALL_DIR_INCLUDE:FILEPATH="%PREFIX%/include/netgen" ^
      -D NG_INSTALL_DIR_PYTHON=Lib/site-packages ^
      -D NG_INSTALL_DIR_BIN=bin ^
      -D NG_INSTALL_DIR_LIB=lib ^
      -D NG_INSTALL_DIR_CMAKE=lib/cmake/netgen ^
      -D NG_INSTALL_DIR_RES=share ^
      -D Python3_ROOT_DIR:FILEPATH="%PREFIX%" ^
      -D USE_OCC=ON ^
      -D USE_PYTHON=ON ^
      -D USE_GUI=OFF ^
      -D BUILD_FOR_CONDA=ON ^
      -D USE_SUPERBUILD=OFF ^
      ..

if errorlevel 1 exit 1
ninja install
if errorlevel 1 exit 1
