all: run

clean: 
	rm -rf out

build: clean
	mkdir out
	g++ -o out/Naive_Bayes  Naive_Bayes.cpp -I /usr/include/eigen3

run: build
	./out/Naive_Bayes
