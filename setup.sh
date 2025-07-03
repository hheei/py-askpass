#!/bin/bash
# Check if submodules are initialized and cloned
if [ ! -d "sshpass" ] || [ ! -f "sshpass/configure" ]; then
    echo "Initializing and updating git submodules..."
    git submodule init
    git submodule update
fi

# Build sshpass
echo "Building sshpass..."
cd sshpass
./bootstrap
./configure
make
cd ..

# Install package
echo "Installing py-askpass..."
pip3 install .
