#include <iostream>
#include <stdio.h>
#include <opencv2/opencv.hpp>

int main()
{
    // Ruta de la imagen
    std::string ruta_imagen = "images/perros.jpg";

    // Tiempo inicial de ejecucion
    double inicio = cv::getTickCount();

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
    double tiempo_ejecucion = (cv::getTickCount() - inicio) / cv::getTickFrequency();
    std::cout << "Tiempo de ejecucion: " << tiempo_ejecucion << " segundos" << std::endl;

    // Mostrar imagen con el filtro aplicado
    cv::namedWindow("Imagen Filtrada", cv::WINDOW_NORMAL);
    cv::imshow("Imagen Filtrada", img_filtrada);
    cv::waitKey(0);
    cv::destroyAllWindows();

    // Agregar el tiempo de ejecucion en el archivo de texto
    std::string nombre_archivo = "images/tiempos_ejecucion.txt";
    std::map<std::string, double> contenido_existente;

    try
    {
        std::ifstream archivo(nombre_archivo);
        if (archivo.is_open())
        {
            std::string contenido((std::istreambuf_iterator<char>(archivo)), std::istreambuf_iterator<char>());
            if (!contenido.empty())
            {
                std::stringstream ss(contenido);
                std::string key;
                double value;
                ss >> key >> value;
                contenido_existente[key] = value;
            }
            archivo.close();
        }
    }
    catch (const std::ifstream::failure& e)
    {
        // Manejo de error al leer el archivo
    }

    contenido_existente["TiempoC"] = tiempo_ejecucion;

    // Escribir el contenido actualizado en el archivo
    try
    {
        std::ofstream archivo(nombre_archivo);
        if (archivo.is_open())
        {
            archivo << "{";
            for (const auto& kvp : contenido_existente)
            {
                archivo << kvp.first << ": " << kvp.second << ", ";
            }
            archivo.seekp(-2, std::ios_base::end);
            archivo << "}";
            archivo.close();
        }
    }
    catch (const std::ofstream::failure& e)
    {
        // Manejo de error al escribir en el archivo
    }

    return 0;
}
