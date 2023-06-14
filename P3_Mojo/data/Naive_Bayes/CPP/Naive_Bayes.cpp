#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <sstream>
#include <algorithm>

class NaiveBayes {
public:
    void fit(const std::vector<std::vector<int>>& X, const std::vector<std::string>& y) {
        num_samples_ = X.size();
        num_features_ = X[0].size();

        classes_ = getUniqueClasses(y);
        num_classes_ = classes_.size();

        class_priors_.resize(num_classes_);
        feature_probs_.resize(num_classes_, std::vector<double>(num_features_));

        for (int i = 0; i < num_classes_; i++) {
            const std::string& c = classes_[i];
            std::vector<std::vector<int>> X_c;
            for (int j = 0; j < num_samples_; j++) {
                if (y[j] == c) {
                    X_c.push_back(X[j]);
                }
            }

            class_priors_[i] = static_cast<double>(X_c.size()) / num_samples_;

            for (int f = 0; f < num_features_; f++) {
                int sum_feature = 0;
                for (int j = 0; j < X_c.size(); j++) {
                    sum_feature += X_c[j][f];
                }
                feature_probs_[i][f] = static_cast<double>(sum_feature) / X_c.size();
            }
        }
    }

    std::vector<std::string> predict(const std::vector<std::vector<int>>& X) {
        std::vector<std::string> predictions;
        for (const auto& sample : X) {
            std::vector<double> sample_probs(num_classes_);
            for (int i = 0; i < num_classes_; i++) {
                double class_prior = class_priors_[i];
                const std::vector<double>& feature_probs = feature_probs_[i];
                double log_prob = 0.0;
                for (int f = 0; f < num_features_; f++) {
                    if (sample[f] == 1) {
                        log_prob += std::log(feature_probs[f]);
                    } else {
                        log_prob += std::log(1.0 - feature_probs[f]);
                    }
                }
                sample_probs[i] = log_prob + std::log(class_prior);
            }
            int max_index = std::max_element(sample_probs.begin(), sample_probs.end()) - sample_probs.begin();
            predictions.push_back(classes_[max_index]);
        }
        return predictions;
    }

private:
    std::vector<std::string> getUniqueClasses(const std::vector<std::string>& y) {
        std::vector<std::string> unique_classes;
        for (const auto& cls : y) {
            if (std::find(unique_classes.begin(), unique_classes.end(), cls) == unique_classes.end()) {
                unique_classes.push_back(cls);
            }
        }
        return unique_classes;
    }

    int num_samples_;
    int num_features_;
    int num_classes_;
    std::vector<std::string> classes_;
    std::vector<double> class_priors_;
    std::vector<std::vector<double>> feature_probs_;
};


// Función para verificar si una cadena es numérica
bool isNumeric(const std::string& str) {
    for (char c : str) {
        if (!std::isdigit(c)) {
            return false;
        }
    }
    return true;
}

// Función para leer los datos de las columnas excepto la última
std::vector<std::vector<int>> readCSV(const std::string& filename) {
    std::ifstream file(filename);
    std::vector<std::vector<int>> data;
    std::string line;

    while (std::getline(file, line)) {
        std::vector<int> row;
        std::istringstream iss(line);
        std::string value;

        while (std::getline(iss, value, ',')) {
            // Verificar si el valor es numérico antes de convertirlo a entero
            if (isNumeric(value)) {
                row.push_back(std::stoi(value));
            }
        }

        // Ignorar la última columna
        row.pop_back();

        data.push_back(row);
    }

    file.close();

    return data;
}

// Función para leer la última columna (etiquetas)
std::vector<std::string> readLabelsCSV(const std::string& filename) {
    std::ifstream file(filename);
    std::vector<std::string> labels;
    std::string line;

    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::string value;

        while (std::getline(iss, value, ',')) {
            // Leer únicamente la última columna
            labels.push_back(value);
        }
    }

    file.close();

    return labels;
}
void savePredictions(const std::vector<std::string>& predictions, const std::string& filename) {
    std::ofstream file(filename);
    for (const auto& prediction : predictions) {
        file << prediction << "\n";
    }
    file.close();
}

int main() {
    // Leer datos de entrenamiento desde archivo CSV
    std::vector<std::vector<int>> X_train = readCSV("../../assets/naive_bayes.csv");
    std::vector<std::string> y_train = readLabelsCSV("../../assets/naive_bayes.csv");

    // Crear y ajustar el modelo Naive Bayes
    NaiveBayes model;
    model.fit(X_train, y_train);

    // Datos de prueba
    std::vector<std::vector<int>> X_test = {
        {1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1},
        {1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0}
    };

    // Realizar predicciones
    std::vector<std::string> y_pred = model.predict(X_test);

    // Guardar las predicciones en un archivo
    savePredictions(y_pred, "predictions.txt");

    std::cout << "Predicciones guardadas en predictions.txt" << std::endl;

    return 0;
}
