#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <cmath>
#include <Eigen/Dense>

using Eigen::MatrixXd;
using Eigen::VectorXd;

class LinearRegression {
public:
    LinearRegression() {
        coefficients = VectorXd::Zero(2);
    }

    void leer_archivo_csv() {
        std::ifstream archivo_csv("../../assets/lineal_regression.csv");
        std::string linea;

        while (std::getline(archivo_csv, linea)) {
            std::vector<int> tmp;
            std::istringstream iss(linea);
            std::string valor;

            while (std::getline(iss, valor, ',')) {
                tmp.push_back(std::stoi(valor));
            }

            datos.push_back(tmp[0]);
            etiquetas.push_back(tmp[1]);
        }

        archivo_csv.close();
    }

    void fit(const MatrixXd& X, const VectorXd& y) {
        // Agregar una columna de unos a X para el término de sesgo (intercept)
        MatrixXd X_ext(X.rows(), X.cols() + 1);
        X_ext << MatrixXd::Ones(X.rows(), 1), X;

        // Calcular los coeficientes utilizando la fórmula de mínimos cuadrados
        coefficients = (X_ext.transpose() * X_ext).inverse() * X_ext.transpose() * y;
    }

    VectorXd predict(const MatrixXd& X) {
        // Agregar una columna de unos a X para el término de sesgo (intercept)
        MatrixXd X_ext(X.rows(), X.cols() + 1);
        X_ext << MatrixXd::Ones(X.rows(), 1), X;

        // Realizar predicciones utilizando los coeficientes aprendidos
        return X_ext * coefficients;
    }

public:
    VectorXd coefficients;
    std::vector<int> datos;
    std::vector<int> etiquetas;
};

int main() {
    LinearRegression model;
    model.leer_archivo_csv();

    // Datos de entrenamiento
    MatrixXd X_train(model.datos.size(), 1);
    VectorXd y_train(model.etiquetas.size());
    for (int i = 0; i < model.datos.size(); ++i) {
        X_train(i, 0) = model.datos[i];
        y_train(i) = model.etiquetas[i];
    }

    // Crear y entrenar el modelo de regresión lineal
    model.fit(X_train, y_train);

    // Realizar predicciones
    MatrixXd X_test(3, 1);
    X_test << 500, 1500, 7000;  // Nuevos datos para predecir
    VectorXd y_pred = model.predict(X_test);

    // Imprimir las predicciones
    std::cout << "Predicciones:" << std::endl;
    for (int i = 0; i < X_test.rows(); ++i) {
        std::cout << "X_test: " << X_test(i, 0) << " y_pred: " << y_pred(i) << std::endl;
    }

    return 0;
}
