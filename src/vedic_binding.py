import ctypes
import os

class QuantumInspiredBridge:
    def __init__(self, lib_path=None):
        """
        Initialize the bridge to the Vedic C++ Kernel.
        Defaults to the reorganized 'kernels' directory.
        """
        if lib_path is None:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            self.lib_path = os.path.join(base_path, 'kernels', 'libvedic.so')
        else:
            self.lib_path = lib_path

        if not os.path.exists(self.lib_path):
            raise FileNotFoundError(f"Vedic Shared Library not found at {self.lib_path}")

        self.lib = ctypes.CDLL(self.lib_path)
        self._setup_interface()

    def _setup_interface(self):
        """Map argument and return types for C++ functions."""
        self.lib.normalizepH.argtypes = [ctypes.c_double]
        self.lib.normalizepH.restype = ctypes.c_double

        self.lib.normalizeTurbidity.argtypes = [ctypes.c_double]
        self.lib.normalizeTurbidity.restype = ctypes.c_double

        self.lib.normalizeTDS.argtypes = [ctypes.c_double]
        self.lib.normalizeTDS.restype = ctypes.c_double

        self.lib.calculate_unified_health_field.argtypes = [ctypes.c_double]
        self.lib.calculate_unified_health_field.restype = ctypes.c_double

    def run_prediction(self, ph, turb, tds):
        """Helper to run normalization batch."""
        return {
            'normalized': {
                'pH': self.lib.normalizepH(ph),
                'Turbidity': self.lib.normalizeTurbidity(turb),
                'TDS': self.lib.normalizeTDS(tds)
            }
        }
