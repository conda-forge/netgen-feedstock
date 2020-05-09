mkdir build -p
cd build


cmake -G "Ninja" \
      -D CMAKE_BUILD_TYPE=Release \
      -D CMAKE_INSTALL_PREFIX:FILEPATH=$PREFIX \
      -D CMAKE_PREFIX_PATH:FILEPATH=$PREFIX \
      -D NG_INSTALL_DIR_INCLUDE:FILEPATH=$PREFIX/include/netgen \
      -D NG_INSTALL_DIR_PYTHON:FILEPATH=${SP_DIR} \
      -D NG_INSTALL_DIR_BIN=bin \
      -D NG_INSTALL_DIR_LIB=lib \
      -D NG_INSTALL_DIR_CMAKE:FILEPATH=lib/cmake/netgen \
      -D NG_INSTALL_DIR_RES=share \
      -D OCC_INCLUDE_DIR:FILEPATH=$PREFIX/include/opencascade \
      -D OCC_LIBRARY_DIR:FILEPATH=$PREFIX/lib \
      -D USE_NATIVE_ARCH:BOOL=OFF \
      -D USE_OCC:BOOL=ON \
      -D USE_PYTHON:BOOL=ON \
      -D USE_GUI:BOOL=OFF \
      -D USE_SUPERBUILD:BOOL=OFF \
      -D BUILD_FOR_CONDA:BOOL=ON \
      -D DYNAMIC_LINK_PYTHON:BOOL=OFF \
      ..

ninja install -v

