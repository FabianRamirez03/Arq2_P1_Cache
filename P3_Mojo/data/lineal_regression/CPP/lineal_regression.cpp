#include <iostream>
#include <Eigen/Dense>  // Se requiere la biblioteca Eigen para el álgebra lineal

class LinearRegression {
private:
    Eigen::VectorXd coefficients;

public:
    LinearRegression() {
        coefficients = Eigen::VectorXd();
    }

    void fit(Eigen::MatrixXd X, Eigen::VectorXd y) {
        // Agregar una columna de unos a X para el término de sesgo (intercept)
        Eigen::MatrixXd ones = Eigen::MatrixXd::Ones(X.rows(), 1);
        X.conservativeResize(X.rows(), X.cols() + 1);
        X.block(0, X.cols() - 1, X.rows(), 1) = ones;

        // Calcular los coeficientes utilizando la fórmula de mínimos cuadrados
        coefficients = (X.transpose() * X).inverse() * X.transpose() * y;
    }

    Eigen::VectorXd predict(Eigen::MatrixXd X) {
        // Agregar una columna de unos a X para el término de sesgo (intercept)
        Eigen::MatrixXd ones = Eigen::MatrixXd::Ones(X.rows(), 1);
        X.conservativeResize(X.rows(), X.cols() + 1);
        X.block(0, X.cols() - 1, X.rows(), 1) = ones;

        // Realizar predicciones utilizando los coeficientes aprendidos
        return X * coefficients;
    }
};

int main() {
    Eigen::MatrixXd X(5, 1);  // Característica: X
    X << 1, 2, 3, 4, 5;

    Eigen::VectorXd y(5);  // Etiqueta: y
    y << 2, 4, 6, 8, 10;

    // Crear y entrenar el modelo de regresión lineal
    LinearRegression model;
    model.fit(X, y);

    // Realizar predicciones
    Eigen::MatrixXd X_test(3, 1);  // Nuevos datos para predecir
    X_test << 6, 7, 8;
    Eigen::VectorXd y_pred = model.predict(X_test);

    // Imprimir las predicciones
    std::cout << "Predicciones:" << std::endl;
    for (int i = 0; i < X_test.rows(); i++) {
        std::cout << "X_test: " << X_test(i, 0) << " y_pred: " << y_pred(i) << std::endl;
    }

    return 0;
}
