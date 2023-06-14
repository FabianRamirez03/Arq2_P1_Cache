all: run

clean: 
	rm -rf out

build: clean
	mkdir out
	g++ -o out/logistic_regression  logistic_regression.cpp -I /usr/include/eigen3

run: build
	./out/logistic_regression
