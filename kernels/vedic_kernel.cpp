// Optimized implementations of Vedic formulas

#include <iostream>
#include <cmath>

const double VEDIC_MULTIPLIER = 1.08;

// Function to calculate turbidity stress
double calculateTurbidityStress(double turbidity) {
    return turbidity * VEDIC_MULTIPLIER;
}

// Function to calculate chlorine stress
double calculateChlorineStress(double chlorine) {
    return chlorine * VEDIC_MULTIPLIER;
}

// Function to compute combined sensor stress
double computeCombinedStress(double turbidity, double chlorine) {
    return calculateTurbidityStress(turbidity) + calculateChlorineStress(chlorine);
}

// Function for unified health field calculation
double calculateUnifiedHealthField(double combinedStress) {
    return combinedStress * VEDIC_MULTIPLIER;
}