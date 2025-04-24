#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int** createRandomMatrix(int n) {
    int** matrix = malloc(n * sizeof(int*));
    for (int i = 0; i < n; i++) {
        matrix[i] = malloc(n * sizeof(int));
        for (int j = 0; j < n; j++) {
            matrix[i][j] = (rand()%2==1?-1:1)*rand() % MAX; // small values for readability
        }
    }
    return matrix;
}

int** createZeroMatrix(int n) {
    int** matrix = malloc(n * sizeof(int*));
    for (int i = 0; i < n; i++) {
        matrix[i] = calloc(n, sizeof(int));
    }
    return matrix;
}

void printMatrix(int** matrix, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%3d ", matrix[i][j]);
        }
        printf("\n");
    }
}

void multiplyMatrices(int** A, int** B, int** C, int n) {
    for (int i = 0; i < n; i++) {           // Row of A
        for (int j = 0; j < n; j++) {       // Column of B
            for (int k = 0; k < n; k++) {   // Iterate over row-col
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

void freeMatrix(int** matrix, int n) {
    for (int i = 0; i < n; i++)
        free(matrix[i]);
    free(matrix);
}

int main() {
    int n = DIM;
    srand(time(NULL)); 

    int** A = createRandomMatrix(n);
    int** B = createRandomMatrix(n);
    int** C = createZeroMatrix(n);

    printf("Matrix A:\n");
    printMatrix(A, n);

    printf("\nMatrix B:\n");
    printMatrix(B, n);

    multiplyMatrices(A, B, C, n);

    printf("\nMatrix A x B:\n");
    printMatrix(C, n);

    freeMatrix(A, n);
    freeMatrix(B, n);
    freeMatrix(C, n);

    return 0;
}
