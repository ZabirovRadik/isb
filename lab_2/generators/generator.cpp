#include <iostream>
#include <vector>
#include <ctime>

#define MAX_SIZE 128

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
    srand(time(NULL));
    generate_random_bits();
    return 0;
}