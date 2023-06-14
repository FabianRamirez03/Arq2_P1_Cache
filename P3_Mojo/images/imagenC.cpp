#include <iostream>
#include <opencv2/opencv.hpp>
#include <chrono>
#include <iomanip>

int main()
{
    // Ruta de la imagen
    std::string ruta_imagen = "perros.jpg";

    // Tiempo inicial de ejecucion
    std::chrono::high_resolution_clock::time_point inicio = std::chrono::high_resolution_clock::now();

    // Leer la imagen
    cv::Mat img = cv::imread(ruta_imagen);

    // Convertir la imagen a escala de grises
    cv::Mat img_gray;
    cv::cvtColor(img, img_gray, cv::COLOR_BGR2GRAY);

    // Aplicar el filtro Sobel
    cv::Mat grad_x, grad_y;
    cv::Sobel(img_gray, grad_x, CV_64F, 1, 0, 3);
    cv::Sobel(img_gray, grad_y, CV_64F, 0, 1, 3);
    cv::Mat img_filtrada = grad_x * 0.5 + grad_y * 0.5;

    // Tiempo total de ejecucion
    std::chrono::high_resolution_clock::time_point fin = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> tiempo_ejecucion = std::chrono::duration_cast<std::chrono::duration<double>>(fin - inicio);
    std::cout << std::setprecision(16);
    std::cout << "Tiempo de ejecucion: " << tiempo_ejecucion.count() << " segundos" << std::endl;

    // Mostrar imagen con el filtro aplicado
    cv::namedWindow("Imagen Filtrada", cv::WINDOW_NORMAL);
    cv::imshow("Imagen Filtrada", img_filtrada);
    cv::waitKey(0);
    cv::destroyAllWindows();

    return 0;
}