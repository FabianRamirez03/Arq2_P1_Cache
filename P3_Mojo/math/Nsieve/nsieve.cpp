#include <iomanip>
#include <iostream>
#include <sstream>
#include <vector>
#include <chrono>

void nsieve(std::size_t max) {
  // Crear vector para marcar los números no primos
  static std::vector<bool> no_primos;
  no_primos.assign(max, false);
  std::size_t cuenta = 0;

  // Calcular los números primos utilizando la criba de Eratóstenes
  for (std::size_t valor = 2; valor < max; ++valor) {
    if (!no_primos[valor]) {
      ++cuenta;

      // Marcar los múltiplos del número actual como no primos
      for (std::size_t multiple = valor * 2; multiple < max; multiple += valor) {
        no_primos[multiple] = true;
      }
    }
  }

  // Mostrar la cantidad de números primos encontrados
  std::cout << "Primos hasta " << std::setw(8) << max << ' ' << std::setw(8)
            << cuenta << '\n';
}

int main(int argc, char **argv) {
  if (argc != 2) {
    // Verificar la cantidad de argumentos
    std::cerr << "uso: " << argv[0] << " <n>\n";
    return 1;
  }

  // Convertir el argumento a un número entero
  unsigned int limite;
  {
    std::istringstream convertor(argv[1]);
    if (!(convertor >> limite) || !convertor.eof()) {
      std::cerr << "uso: " << argv[0] << " <n>\n";
      std::cerr << "\tn debe ser un número entero\n";
      return 1;
    }
  }

  // Obtener el tiempo de inicio
  auto inicio = std::chrono::high_resolution_clock::now();

  // Calcular y mostrar los números primos para tres valores diferentes
  for (std::size_t i = 0; i < 3; ++i) {
    nsieve(10000 << (limite - i));
  }

  // Obtener el tiempo de finalización y calcular la duración
  auto fin = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double> duracion = fin - inicio;

  // Mostrar la duración de la ejecución
  std::cout << "Tiempo de ejecución: " << duracion.count() << " segundos\n";

  return 0;
}
