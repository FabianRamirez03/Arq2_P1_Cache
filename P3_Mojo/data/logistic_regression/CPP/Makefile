all: run

clean: 
	rm -rf out

build: clean
	mkdir out
	g++ -o out/logistic_regression  logistic_regression.cpp

run: build
	./out/logistic_regression
