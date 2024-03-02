#include <iostream>
#include <vector>

#define MAX_SIZE 50

/**
 * @brief The built-in c++ generator is used to generate a number of random bits
 *
 * Execution of the program
 * starts here.
 */
void generate_random_bits() {
    for (size_t i = 0; i < MAX_SIZE; i++)
        std::cout << rand() % 2;    
}

int main() {
    srand(MAX_SIZE);
    return 0;
}