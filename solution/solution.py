from typing import List, Tuple

import numpy as np
import cirq


def matrix_to_sycamore_operations(
    target_qubits: List[cirq.GridQubit], matrix: np.ndarray
) -> Tuple[cirq.OP_TREE, List[cirq.GridQubit]]:
    """A method to convert a unitary matrix to a list of Sycamore operations.

    This method will return a list of `cirq.Operation`s using the qubits and (optionally) ancilla
    qubits to implement the unitary matrix `matrix` on the target qubits `qubits`.
    The operations are also supported by `cirq.google.gate_sets.SYC_GATESET`.

    Args:
        target_qubits: list of qubits the returned operations will act on. The qubit order defined by the list
            is assumed to be used by the operations to implement `matrix`.
        matrix: a matrix that is guaranteed to be unitary and of size (2**len(qs), 2**len(qs)).
    Returns:
        A tuple of operations and ancilla qubits allocated.
            Operations: In case the matrix is supported, a list of operations `ops` is returned.
                `ops` acts on `qs` qubits and for which `cirq.unitary(ops)` is equal to `matrix` up
                 to certain tolerance. In case the matrix is not supported, it might return NotImplemented to
                 reduce the noise in the judge output.
            Ancilla qubits: In case ancilla qubits are allocated a list of ancilla qubits. Otherwise
                an empty list.
        .
    """

    ops = NotImplemented

    if len(target_qubits) == 1:
        ops = cirq.single_qubit_matrix_to_gates(matrix)
        for i, x in enumerate(ops):
            ops[i] = cirq.GateOperation(x, [target_qubits[0]])
    
    elif len(target_qubits) == 2:
        ops = cirq.two_qubit_matrix_to_operations(
            target_qubits[0],
            target_qubits[1],
            matrix,
            allow_partial_czs=False,
            atol=1e-4
        )
    
    elif len(target_qubits) == 3:
        ops = cirq.three_qubit_matrix_to_operations(
            target_qubits[0],
            target_qubits[1],
            target_qubits[2],
            matrix,
            atol=1e-4
        )

    return ops, []
