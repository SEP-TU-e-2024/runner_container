import pandas as pd
import numpy as np

# return a matrix
def process_file(file):
    df = pd.read_csv(file)

    non_dep_files = list(df)[1:]

    df = df.drop([index for index, row in df.iterrows() if row['Dependent File'] not in non_dep_files])
    df = df[[col for col in df.columns if (col == df["Dependent File"]).any()]]

    print(df)

    return df.fillna(0).to_numpy(dtype=int), list(df.columns)


def compute_percentages_dependencies(matrix, columns, total_num_files):
    num_files, _ = matrix.shape
    violations = 0

    for i in range(num_files):
        for j in range(num_files):
            if matrix[i][j] != 0 and matrix[j][i] != 0 and i != j:
                violations += 1
                if i > j: # only print this message once
                    print(f"Dependency violation found at position: ({i}, {j}) \t Files:\n{columns[i]}\n{columns[j]}\n")

    return {"Cyclic dependencies": violations / (2 * total_num_files)}