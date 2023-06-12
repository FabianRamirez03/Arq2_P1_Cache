#include <iostream>
#include <chrono>
#include <random>
#include <string>

// Función para multiplicar dos matrices
double **multiplyMatrices(double **matrix_a, double **matrix_b, int size)
{
    double **result = new double *[size];
    for (int i = 0; i < size; i++)
    {
        result[i] = new double[size];
        for (int j = 0; j < size; j++)
        {
            result[i][j] = 0.0;
            for (int k = 0; k < size; k++)
            {
                result[i][j] += matrix_a[i][k] * matrix_b[k][j];
            }
        }
    }
    return result;
}

// Función para liberar memoria de las matrices
void freeMatrices(double **matrix, int size)
{
    for (int i = 0; i < size; i++)
    {
        delete[] matrix[i];
    }
    delete[] matrix;
}

int main()
{
    // Tamaño de la matriz
    int matrix_size = 1000;

    // Crear dos matrices aleatorias
    double **matrix_a = new double *[matrix_size];
    double **matrix_b = new double *[matrix_size];
    for (int i = 0; i < matrix_size; i++)
    {
        matrix_a[i] = new double[matrix_size];
        matrix_b[i] = new double[matrix_size];
        for (int j = 0; j < matrix_size; j++)
        {
            matrix_a[i][j] = static_cast<double>(rand()) / RAND_MAX;
            matrix_b[i][j] = static_cast<double>(rand()) / RAND_MAX;
        }
    }

    // Medir tiempo de ejecución
    auto start = std::chrono::high_resolution_clock::now();

    // Multiplicar las matrices
    double **result = multiplyMatrices(matrix_a, matrix_b, matrix_size);

    auto end = std::chrono::high_resolution_clock::now();

    // Calcular el tiempo transcurrido en segundos
    std::chrono::duration<double> duration = end - start;
    double execution_time = duration.count();

    std::cout << "Tamano de la matriz: " << matrix_size << "x" << matrix_size << std::endl;
    std::cout << "Tiempo de ejecucion: " << execution_time << " segundos" << std::endl;

    // Liberar memoria de las matrices
    freeMatrices(matrix_a, matrix_size);
    freeMatrices(matrix_b, matrix_size);
    freeMatrices(result, matrix_size);

    return 0;
}
