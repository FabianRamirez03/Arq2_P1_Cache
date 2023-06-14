#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <cmath>
#include <Eigen/Dense>

using Eigen::MatrixXd;
using Eigen::VectorXd;

class LogisticRegression {
public:
    LogisticRegression(double learning_rate = 0.01, int num_iterations = 1000) {
        learning_rate_ = learning_rate;
        num_iterations_ = num_iterations;
        weights_ = VectorXd::Zero(2);
        bias_ = 0;
    }

    void leer_archivo_csv() {
        std::ifstream archivo_csv("assets/logistic_regression.csv");
        std::string linea;

        while (std::getline(archivo_csv, linea)) {
            std::vector<int> tmp;
            std::istringstream iss(linea);
            std::string valor;

            while (std::getline(iss, valor, ',')) {
                tmp.push_back(std::stoi(valor));
            }

            datos_.push_back(VectorXd::Map(tmp.data(), tmp.size() - 1));
            etiquetas_.push_back(tmp.back());
        }

        archivo_csv.close();
    }

    double sigmoid(double z) {
        z = std::max(-500.0, std::min(z, 500.0));
        return 1 / (1 + std::exp(-z));
    }

    void initialize_parameters(int n_features) {
        weights_ = VectorXd::Zero(n_features);
        bias_ = 0;
    }

    void fit(const MatrixXd& X, const VectorXd& y) {
        initialize_parameters(X.cols());

        for (int iter = 0; iter < num_iterations_; ++iter) {
            VectorXd linear_model = X * weights_ + bias_;
            VectorXd y_pred = linear_model.unaryExpr([this](double x) { return sigmoid(x); });

            VectorXd dw = (1.0 / X.rows()) * X.transpose() * (y_pred - y);
            double db = (1.0 / X.rows()) * (y_pred - y).sum();

            weights_ -= learning_rate_ * dw;
            bias_ -= learning_rate_ * db;
        }
    }

    std::vector<int> predict(const MatrixXd& X) {
        VectorXd linear_model = X * weights_ + bias_;
        VectorXd y_pred = linear_model.unaryExpr([this](double x) { return sigmoid(x); });
        std::vector<int> y_pred_class(y_pred.size());

        for (int i = 0; i < y_pred.size(); ++i) {
            y_pred_class[i] = (y_pred[i] > 0.5) ? 1 : 0;
        }

        return y_pred_class;
    }

private:
    double learning_rate_;
    int num_iterations_;
    VectorXd weights_;
    double bias_;
    std::vector<VectorXd> datos_;
    std::vector<int> etiquetas_;
};

int main() {
    LogisticRegression model(0.1, 10000);
    model.leer_archivo_csv();

    std::vector<VectorXd> datos = model.datos_;
    VectorXd etiquetas = VectorXd::Map(model.etiquetas_.data(), model.etiquetas_.size());

    // Convertir los datos y etiquetas a una matriz y vector de Eigen
    MatrixXd X_train(datos.size(), datos[0].size());
    VectorXd y_train(etiquetas.size());
    for (int i = 0; i < datos.size(); ++i) {
        X_train.row(i) = datos[i];
        y_train[i] = etiquetas[i];
    }

    model.fit(X_train, y_train);

    // Datos de prueba
    MatrixXd X_test(2, 2);
    X_test << 4, 2,
              500, 6;
    std::vector<int> y_pred = model.predict(X_test);

    // Imprimir las predicciones
    std::cout << "Predicciones:";
    for (int i = 0; i < y_pred.size(); ++i) {
        std::cout << " " << y_pred[i];
    }
    std::cout << std::endl;

    return 0;
}
