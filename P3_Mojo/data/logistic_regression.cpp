#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

class LogisticRegression {
private:
    std::vector<std::vector<double>> X;
    std::vector<int> y;
    std::vector<double> coefficients;

public:
    void fit(const std::vector<std::vector<double>>& inputX, const std::vector<int>& inputY, double learningRate = 0.01, int iterations = 1000) {
        X = inputX;
        y = inputY;

        // Agregar una columna de unos a X para el término de sesgo (intercept)
        for (auto& row : X) {
            row.insert(row.begin(), 1.0);
        }

        // Inicializar los coeficientes con ceros
        coefficients = std::vector<double>(X[0].size(), 0.0);

        // Gradiente descendente
        for (int i = 0; i < iterations; ++i) {
            std::vector<double> predictions = predict(X);
            std::vector<double> errors(X.size());

            for (size_t j = 0; j < X.size(); ++j) {
                errors[j] = predictions[j] - y[j];
            }

            for (size_t j = 0; j < coefficients.size(); ++j) {
                double gradient = 0.0;
                for (size_t k = 0; k < X.size(); ++k) {
                    gradient += errors[k] * X[k][j];
                }
                coefficients[j] -= learningRate * gradient;
            }
        }
    }

    std::vector<double> predict(const std::vector<std::vector<double>>& inputX) {
        std::vector<double> predictions(inputX.size());

        for (size_t i = 0; i < inputX.size(); ++i) {
            double sum = 0.0;
            for (size_t j = 0; j < inputX[i].size(); ++j) {
                sum += coefficients[j] * inputX[i][j];
            }
            predictions[i] = 1.0 / (1.0 + std::exp(-sum));
        }

        return predictions;
    }
};

int main() {
    std::vector<std::vector<double>> X = {{1, 2}, {2, 3}, {3, 1}, {4, 3}, {5, 3}, {6, 2}};
    std::vector<int> y = {0, 0, 0, 1, 1, 1};

    LogisticRegression model;
    model.fit(X, y);

    std::vector<double> predictions = model.predict(X);

    for (size_t i = 0; i < predictions.size(); ++i) {
        std::cout << "Prediction for instance " << i << ": " << predictions[i] << std::endl;
    }

    return 0;
}
