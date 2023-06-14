all: data_gen logistic_regression
	echo "Ejecutamos todo satisfactoriamente"

data_gen:
	rm -rf assets/
	mkdir assets
	python3 data_gen/data_gen.py

logistic_regression:
	python3 logistic_regression/Python/logistic_regression.py

lineal_regression:
	python3 lineal_regression/Python/lineal_regression.py

