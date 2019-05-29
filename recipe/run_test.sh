PY_VER=$(python -c "import sys; ver=sys.version_info; print('{}.{}'.format(ver.major, ver.minor))")

if [ `uname` == Darwin ]; then
	otool -L "${CONDA_PREFIX}/lib/python${PY_VER}/site-packages/netgen/libngpy.so"
else
	ldd "${CONDA_PREFIX}/lib/python${PY_VER}/site-packages/netgen/libngpy.so"
fi