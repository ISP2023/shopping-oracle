#!/bin/bash

TESTMODULE="test_shopping_cart.py"
PYTHON=python3
PYTHON=python3.11

if [ ! -f $TESTMODULE ]; then
	echo "No tests code $TESTMODULE"
	exit 9
fi

# Target code for tests
TARGET=shopping_cart.py

# Path to oracle code
DIR=./oracle
# My Laptop
DIR=/home/jim/courses/ISP/code/2023/shopping/oracle
if [ ! -d $DIR ]; then
	echo "No oracle code in $DIR"
	exit 9
fi
# Name of instrumented target code
VARIANT_CODE=shopping_cart.py

# Backup student's version of target code (restored in cleanup)
BACKUP=${TARGET}-orig

# Arrays to record results. Elements are appended in runtests()
expect=("")
actual=("")

drawline( ) {
    echo "----------------------------------------------------------------------"
}
runtests( ) {
    if [ ! -f $DIR/$VARIANT_CODE ]; then
        echo "No file ${VARIANT_CODE}"
        exit 1
    fi
	# backup student file
	if [ ! -f ${BACKUP} ]; then
		cp $TARGET ${BACKUP}
	fi
	# copy oracle's code
	if [ "$DIR" != "." ]; then
    	cp $DIR/$VARIANT_CODE $TARGET
		cp $DIR/config.py .
	fi
	for testcase in 0 1 2 3 4 5 6 7 8 9; do
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
		#echo export TESTCASE=$testcase
		export TESTCASE=$testcase
		$PYTHON -m unittest -v $TESTMODULE
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

cleanup() {
	if [ -f $BACKUP ]; then
		/bin/mv $BACKUP $TARGET
	fi
	/bin/rm -f config.py
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
    
	for testcase in ${!expect[@]}; do
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
cleanup
showresults
