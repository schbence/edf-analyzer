#!/bin/bash


pyh="/usr/include/python2.7/" #Path to Python.h (locate Python.h)


echo Building EDFanalyzer...
echo Swigging 
swig -c++ -python measures.i
gcc -fpic -c measures_wrap.cxx Measures.cpp -I $pyh 
gcc -shared measures_wrap.o Measures.o -o _measures.so -lstdc++

echo Compiling java files
javac *.java

echo "Should be done"

