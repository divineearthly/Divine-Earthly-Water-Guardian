#include <iostream>
#include <cmath>

// Urdhva Tiryagbhyam (Vertical and Crosswise) multiplication simplified for double normalization.
// We simulate the 'Vertical and Crosswise' approach by scaling decimals to integers.

double vedic_multiply(double a, double b) {
    // Scaling factor to work with integers for the Vedic algorithm demonstration
    long long scale = 10000;
    long long A = (long long)(a * scale);
    long long B = (long long)(b * scale);
    
    // Vertical and Crosswise logic simulation for integers
    // Result = A * B / (scale * scale)
    return (double)(A * B) / (scale * scale);
}

const double VEDIC_MULTIPLIER = 1.08;

extern "C" {
    double normalizepH(double ph) {
        return vedic_multiply(ph, VEDIC_MULTIPLIER);
    }

    double normalizeTurbidity(double turbidity) {
        return vedic_multiply(turbidity, VEDIC_MULTIPLIER);
    }

    double normalizeTDS(double tds) {
        return vedic_multiply(tds, VEDIC_MULTIPLIER);
    }

    double calculate_unified_health_field(double sensor_val) {
        return vedic_multiply(sensor_val, VEDIC_MULTIPLIER);
    }
}