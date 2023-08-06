export ROOT_DIR="$$PWD"

wget "https://github.com/RWTHmediTEC/Carna/archive/refs/tags/$VERSION_CARNA.tar.gz" -O carna.tgz
tar -vzxf carna.tgz
cd "Carna-$VERSION_CARNA"

mkdir -p build/make_debug
mkdir -p build/make_release

cd "$$ROOT_DIR/Carna-$VERSION_CARNA/build/make_debug"
cmake -DCMAKE_BUILD_TYPE=Debug -DBUILD_DOC=OFF -DBUILD_TEST=ON -DBUILD_DEMO=OFF ../.. -DCMAKE_INSTALL_PREFIX=$$PREFIX
make VERBOSE=1
make install

cd "$$ROOT_DIR/Carna-$VERSION_CARNA/build/make_release"
cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_DOC=OFF -DBUILD_TEST=ON -DBUILD_DEMO=OFF ../.. -DCMAKE_INSTALL_PREFIX=$$PREFIX
make VERBOSE=1
make install

cd "$$ROOT_DIR"
$$PYTHON setup.py build
$$PYTHON setup.py install --single-version-externally-managed --root=/
