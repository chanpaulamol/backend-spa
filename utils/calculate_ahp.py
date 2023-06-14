import numpy as np


def ahp():
    # Comparison matrix
    comparison_matrix = np.array([
        [1.00, 1/2, 1/3, 1/3, 1/4, 1/5],
        [2.00, 1.00, 1/2, 1/2, 1/3, 1/4],
        [3.00, 2.00, 1.00, 2.00, 1/2, 1/3],
        [3.00, 2.00, 1/2, 1.00, 1/3, 1/4],
        [4.00, 3.00, 2.00, 3.00, 1.00, 1/2],
        [5.00, 4.00, 3.00, 4.00, 2.00, 1.00]
    ])

    # Step 1: Normalize the comparison matrix
    normalized_matrix = comparison_matrix / comparison_matrix.sum(axis=0)

    # Step 2: Calculate the priority weights
    priority_weights = normalized_matrix.mean(axis=1)

    # Step 3: Check consistency
    eigenvalue, eigenvector = np.linalg.eig(comparison_matrix)
    max_eigenvalue = max(eigenvalue)
    consistency_index = (max_eigenvalue - len(comparison_matrix)
                         ) / (len(comparison_matrix) - 1)
    # Divide by the consistency index for a 6x6 matrix
    consistency_ratio = consistency_index / 1.24

    # Display the results
    print(normalized_matrix)
    print("\nPriority Weights:")
    print(priority_weights)
    print("\nMaxs:", max_eigenvalue)
    print("\nConsistency Index:", consistency_index)
    print("Consistency Ratio:", consistency_ratio)

    return priority_weights, consistency_index, consistency_ratio


ahp()
