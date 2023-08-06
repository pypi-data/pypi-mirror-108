export ROOT_DIR="$PWD"

wget "https://github.com/RWTHmediTEC/Carna/archive/refs/tags/3.0.2.tar.gz" -O carna.tgz
tar -vzxf carna.tgz
cd "Carna-3.0.2"

mkdir -p build/make_debug
mkdir -p build/make_release

cd "$ROOT_DIR/Carna-3.0.2/build/make_debug"
cmake -DCMAKE_BUILD_TYPE=Debug -DBUILD_DOC=OFF -DBUILD_TEST=ON -DBUILD_DEMO=OFF ../.. -DCMAKE_INSTALL_PREFIX=$PREFIX
make
make install

cd "$ROOT_DIR/Carna-3.0.2/build/make_release"
cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_DOC=OFF -DBUILD_TEST=ON -DBUILD_DEMO=OFF ../.. -DCMAKE_INSTALL_PREFIX=$PREFIX
make
make install

cd "$ROOT_DIR"
$PYTHON setup.py build
$PYTHON setup.py install
