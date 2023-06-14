#include <iostream>
#include <vector>
#include <cmath>

class LogisticRegression {
private:
    double learning_rate;
    int num_iterations;
    std::vector<double> weights;
    double bias;

    double sigmoid(double z) {
        return 1 / (1 + exp(-z));
    }

    void initialize_parameters(int n_features) {
        weights = std::vector<double>(n_features, 0.0);
        bias = 0.0;
    }

public:
    LogisticRegression(double learning_rate = 0.01, int num_iterations = 1000) {
        this->learning_rate = learning_rate;
        this->num_iterations = num_iterations;
        this->weights = std::vector<double>();
        this->bias = 0.0;
    }

    void fit(std::vector<std::vector<double>>& X, std::vector<int>& y) {
        initialize_parameters(X[0].size());

        for (int i = 0; i < num_iterations; i++) {
            std::vector<double> linear_model(X.size(), 0.0);
            std::vector<double> y_pred(X.size(), 0.0);

            for (int j = 0; j < X.size(); j++) {
                for (int k = 0; k < X[0].size(); k++) {
                    linear_model[j] += X[j][k] * weights[k];
                }
                linear_model[j] += bias;
                y_pred[j] = sigmoid(linear_model[j]);
            }

            std::vector<double> dw(X[0].size(), 0.0);
            double db = 0.0;

            for (int j = 0; j < X[0].size(); j++) {
                for (int k = 0; k < X.size(); k++) {
                    dw[j] += (1.0 / X.size()) * X[k][j] * (y_pred[k] - y[k]);
                }
            }

            for (int j = 0; j < X.size(); j++) {
                db += (1.0 / X.size()) * (y_pred[j] - y[j]);
            }

            for (int j = 0; j < X[0].size(); j++) {
                weights[j] -= learning_rate * dw[j];
            }
            bias -= learning_rate * db;
        }
    }

    std::vector<int> predict(std::vector<std::vector<double>>& X) {
        std::vector<int> y_pred(X.size(), 0);

        for (int i = 0; i < X.size(); i++) {
            double linear_model = 0.0;

            for (int j = 0; j < X[0].size(); j++) {
                linear_model += X[i][j] * weights[j];
            }

            linear_model += bias;
            double y_pred_prob = sigmoid(linear_model);
            y_pred[i] = (y_pred_prob > 0.5) ? 1 : 0;
        }

        return y_pred;
    }
};

int main() {
    std::vector<std::vector<double>> X_train = { {2.0, 1.0}, {1.0, 3.0}, {0.0, 2.0}, {1.0, 1.0}, {2.0, 2.0}, {4.0, 3.0}, {6.0, 5.0}, {3.0, 5.0}, {3.0, 3.0}, {6.0, 1.0} };
    std::vector<int> y_train = { 0, 0, 0, 0, 0, 1, 1, 1, 1, 1 };

    LogisticRegression model(0.1, 1000);
    model.fit(X_train, y_train);

    std::vector<std::vector<double>> X_test = { {4.0, 2.0}, {2.0, 1.0} };
    std::vector<int> y_pred = model.predict(X_test);

    std::cout << "Predicciones:";
    for (int i = 0; i < y_pred.size(); i++) {
        std::cout << " " << y_pred[i];
    }
    std::cout << std::endl;

    return 0;
}
