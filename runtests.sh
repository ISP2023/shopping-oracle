#!/bin/bash

TESTMODULE="test_shopping_cart.py"

if [ ! -f $TESTMODULE ]; then
	echo "No tests code $TESTMODULE"
	exit 9
fi

# arrays to record results. Elements are appended in runtests()
expect=("")
actual=("")

# Target and variants
TARGET=shopping_cart.py

# Path to oracle code
if [ -d oracle ]; then
   DIR=oracle
else
   DIR=.
fi
# Name of instrumented target code
VARIANT_CODE=$DIR/shopping_cart.py

drawline( ) {
    echo "----------------------------------------------------------------------"
}
runtests( ) {
    if [ ! -f $VARIANT_CODE ]; then
        echo "No file ${VARIANT_CODE}"
        exit 1
    fi
	# backup student file
	BACKUP=${TARGET}-orig
	if [ ! -f ${BACKUP} ]; then
		cp $TARGET ${BACKUP}
	fi
	# copy oracle's code
	if [ "$DIR" != "." ]; then
    	cp $VARIANT_CODE $TARGET
		cp $DIR/config.py .
	fi
	for testcase in 0 1 2 3 4 5 6; do
        echo ""
        drawline
		case $testcase in
    	0)
			echo "Variant #0: All methods work according to specification. Tests should PASS."
			expect[0]="OK"
       		;;
    	*)
			echo "Variant #${testcase}: Some defect in code. At least one test should FAIL."
			# append to array of expected results
			expect+=("FAIL")
			actual+=("")
			;;
		esac
        drawline
		echo export TESTCASE=$testcase
		export TESTCASE=$testcase
		python3 -m unittest -v $TESTMODULE
		# record status
		if [ $? -eq 0 ]; then
			actual[$testcase]="OK"
		else
			actual[$testcase]="FAIL"
		fi
		# wait til user presses enter?
		#read input
	done
}

showresults() {
    drawline
    echo "Results of Testing All Variant Codes"
    drawline
    echo "OK=all tests pass, FAIL=some tests fail"
    echo ""
    echo " Code#   Expected  Actual"
    failures=0
	numtests=${#expect[@]}
    # is element 0 used?
	#numtests=$(($numtests - 1))
    
	#for testcase in ${!expect[@]}; do
	for testcase in 0 1 2 3 4 5 6; do
        # no results in element 0
        #if [ $testcase -eq 0 ]; then continue; fi
        printf "%4d      %-4s     %s\n" ${testcase} ${expect[$testcase]} ${actual[$testcase]}
        if [ "${expect[$testcase]}" != "${actual[$testcase]}" ]; then
			failures=$(($failures+1))
		fi
	done
    correct=$(($numtests-$failures))
	echo "$correct Correct  $failures Incorrect"
    exit $failures
}

runtests
showresults
