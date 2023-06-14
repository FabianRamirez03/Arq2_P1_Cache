all: run

clean: 
	rm -rf out

build: clean
	mkdir out
	g++ -o out/lineal_regression  lineal_regression.cpp -I /usr/include/eigen3

run: build
	./out/lineal_regression
	
