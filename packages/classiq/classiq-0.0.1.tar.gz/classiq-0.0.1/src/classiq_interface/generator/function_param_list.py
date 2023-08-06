from typing import Set, Type

from classiq_interface.generator.arithmetic import BitwiseAnd
from classiq_interface.generator.finance import Finance
from classiq_interface.generator.function_params import FunctionParams
from classiq_interface.generator.integer_comparator import IntegerComparator
from classiq_interface.generator.qaoa_ansatz import QaoaAnsatz
from classiq_interface.generator.qft import QFT
from classiq_interface.generator.qft_const_adder import QFTConstAdder
from classiq_interface.generator.state_preparation import StatePreparation
from classiq_interface.generator.state_propagator import StatePropagator
from classiq_interface.generator.twodimensionalentangler import TwoDimensionalEntangler
from classiq_interface.generator.vqe_ansatz import VQEAnsatz
from classiq_interface.generator.amplitude_estimation import AmplitudeEstimation

_function_param_list = {
    StatePreparation,
    VQEAnsatz,
    QaoaAnsatz,
    StatePropagator,
    QFT,
    QFTConstAdder,
    BitwiseAnd,
    TwoDimensionalEntangler,
    IntegerComparator,
    Finance,
    AmplitudeEstimation,
}


def get_function_param_list() -> Set[Type[FunctionParams]]:
    return _function_param_list
