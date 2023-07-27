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

    # Round off the normalized matrix to 4 decimal places
    normalized_matrix = np.round(normalized_matrix, decimals=4)

    # Step 2: Calculate the priority weights
    priority_weights = np.mean(normalized_matrix, axis=1)

    # Round off the priority weights to 4 decimal places
    priority_weights = np.round(priority_weights, decimals=4)

    # Step 3: Check consistency
    eigenvalue, eigenvector = np.linalg.eig(comparison_matrix)
    max_eigenvalue = max(eigenvalue)
    print("Maxs", max_eigenvalue)
    consistency_index = np.round(
        (max_eigenvalue - len(comparison_matrix)) / (len(comparison_matrix) - 1), decimals=3)
    index = 1.24
    # Divide by the consistency index for a 6x6 matrix
    consistency_ratio = np.round((consistency_index/index), decimals=4)

    # Display the results
    print("Normalized Matrix:")
    print(normalized_matrix)
    print("\nPriority Weights:")
    print(priority_weights)
    print("\nMaxs:", max_eigenvalue)
    print("\nConsistency Index:", consistency_index)
    print("Consistency Ratio:", consistency_ratio)

    return priority_weights, consistency_index, consistency_ratio


ahp()
