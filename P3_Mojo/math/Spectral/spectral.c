#define _GNU_SOURCE
#include <math.h>
#include <omp.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define false 0
#define true 1

/* Define el tipo de dato SIMD. 2 doubles encapsulados en un registro XMM */
typedef double v2dt __attribute__((vector_size(16)));
static const v2dt v1 = {1.0, 1.0};

/* Parámetro para las funciones de evaluación */
struct Param {
  double *u;   /* vector fuente */
  double *tmp; /* temporal */
  double *v;   /* vector destino */

  int N;  /* longitud del vector fuente/destino */
  int N2; /* = N/2 */

  int r_begin; /* rango de trabajo para cada hilo */
  int r_end;
};

/* Retorna: 1.0 / (i + j) * (i + j + 1) / 2 + i + 1; */
static double eval_A(int i, int j) {
  int d = (((i + j) * (i + j + 1)) >> 1) + i + 1;
  return 1.0 / d;
}

/*
 * Retorna: 2 doubles en el registro xmm [double1, double2]
 *  double1 = 1.0 / (i + j) * (i + j +1) / 2 + i + 1;
 *  double2 = 1.0 / (i+1 + j) * (i+1 + j +1) / 2 + i+1 + 1;
 */
static v2dt eval_A_i(int i, int j) {
  int d1 = (((i + j) * (i + j + 1)) >> 1) + i + 1;
  int d2 = (((i + 1 + j) * (i + 1 + j + 1)) >> 1) + (i + 1) + 1;
  v2dt r = {d1, d2};
  return v1 / r;
}

/*
 * Retorna: 2 doubles en el registro xmm [double1, double2]
 *  double1 = 1.0 / (i + j) * (i + j +1) / 2 + i + 1;
 *  double2 = 1.0 / (i + j+1) * (i + j+1 +1) / 2 + i + 1;
 */
static v2dt eval_A_j(int i, int j) {
  int d1 = (((i + j) * (i + j + 1)) >> 1) + i + 1;
  int d2 = (((i + j + 1) * (i + j + 1 + 1)) >> 1) + i + 1;
  v2dt r = {d1, d2};
  return v1 / r;
}

/* Esta función es llamada por muchos hilos */
static void eval_A_times_u(struct Param *p) {
  const v2dt *pU = (void *)p->u;
  int i;
  int ie;

  for (i = p->r_begin, ie = p->r_end; i < ie; i++) {
    v2dt sum = {0, 0};
    int j;

    for (j = 0; j < p->N2; j++)
      sum += pU[j] * eval_A_j(i, j * 2);

    {
      double *mem = (void *)&sum;
      p->tmp[i] = mem[0] + mem[1];
    }

    for (j = j * 2; __builtin_expect(j < p->N, false); j++)
      p->tmp[i] += eval_A(i, j) * p->u[j];
  }
}

static void eval_At_times_u(struct Param *p) {
  const v2dt *pT = (void *)p->tmp;
  int i;
  int ie;

  for (i = p->r_begin, ie = p->r_end; i < ie; i++) {
    v2dt sum = {0, 0};
    int j;

    for (j = 0; j < p->N2; j++)
      sum += pT[j] * eval_A_i(j * 2, i);

    {
      double *mem = (void *)&sum;
      p->v[i] = mem[0] + mem[1];
    }

    for (j = j * 2; __builtin_expect(j < p->N, false); j++)
      p->v[i] += eval_A(j, i) * p->tmp[j];
  }
}

static void eval_AtA_times_u(struct Param *p) {
  eval_A_times_u(p);
#pragma omp barrier

  eval_At_times_u(p);
#pragma omp barrier
}

static int GetThreadCount() {
  cpu_set_t cs;
  int i;
  int count = 0;

  CPU_ZERO(&cs);
  sched_getaffinity(0, sizeof(cs), &cs);

  for (i = 0; i < 16; i++)
    if (CPU_ISSET(i, &cs))
      count++;

  return count;
}

static double spectral_game(int N) {
  __attribute__((aligned(64))) double u[N];
  __attribute__((aligned(64))) double tmp[N];
  __attribute__((aligned(64))) double v[N];

  double vBv = 0.0;
  double vv = 0.0;

#pragma omp parallel default(shared) num_threads(GetThreadCount())
  {
    int i;

#pragma omp for schedule(static)
    for (i = 0; i < N; i++)
      u[i] = 1.0;

    int threadid = omp_get_thread_num();
    int threadcount = omp_get_num_threads();
    int chunk = N / threadcount;
    int ite;
    struct Param my_param;

    my_param.tmp = tmp;
    my_param.N = N;
    my_param.N2 = N / 2;
    my_param.r_begin = threadid * chunk;
    my_param.r_end = (threadid < (threadcount - 1)) ? (my_param.r_begin + chunk) : N;

    for (ite = 0; ite < 10; ite++) {
      my_param.u = u;
      my_param.v = v;
      eval_AtA_times_u(&my_param);

      my_param.u = v;
      my_param.v = u;
      eval_AtA_times_u(&my_param);
    }

    {
      int i;

#pragma omp for schedule(static) reduction(+ : vBv, vv) nowait
      for (i = 0; i < N; i++) {
        vv += v[i] * v[i];
        vBv += u[i] * v[i];
      }
    }
  }

  return sqrt(vBv / vv);
}

int main(int argc, char *argv[]) {
  int N = ((argc >= 2) ? atoi(argv[1]) : 2000);
  time_t start, end;
  start = time(NULL);

  printf("%.9f\n", spectral_game(N));
  end = time(NULL);
  double duration = difftime(end, start);

  printf("Duración de ejecución: %.2f segundos\n", duration);

  return 0;
}
