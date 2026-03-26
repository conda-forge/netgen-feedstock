mkdir build
cd build

REM TODO: can not find tkint.h -> disabling GUI for WIN

cmake -G "Ninja" ^
      -D CMAKE_BUILD_TYPE="Release" ^
      -D INSTALL_DIR_LAYOUT="Unix" ^
      -D CMAKE_PREFIX_PATH:FILEPATH="%PREFIX%" ^
      -D CMAKE_INSTALL_PREFIX:FILEPATH="%LIBRARY_PREFIX%" ^
      -D NG_INSTALL_DIR_INCLUDE:FILEPATH="%LIBRARY_PREFIX%/include/netgen" ^
      -D OCC_INCLUDE_DIR:FILEPATH="%LIBRARY_PREFIX%/include/opencascade" ^
      -D OCC_LIBRARY_DIR:FILEPATH="%LIBRARY_PREFIX%/lib" ^
      -D USE_OCC=ON ^
      -D USE_PYTHON=ON ^
      -D USE_GUI=OFF ^
      -D BUILD_WITH_CONDA=ON ^
      -D USE_SUPERBUILD=OFF ^
      -D DYNAMIC_LINK_PYTHON=ON ^
      ..

if errorlevel 1 exit 1
ninja install
if errorlevel 1 exit 1
