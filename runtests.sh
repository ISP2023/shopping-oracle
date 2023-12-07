#!/bin/bash

TESTMODULE="test_shopping_cart.py"

if [ ! -f $TESTMODULE ]; then
	echo "No tests code $TESTMODULE"
	exit 9
fi

# arrays to record results. Elements are appended in runtests()
expect=("")
actual=("")

echo "No variant codes to test yet."
