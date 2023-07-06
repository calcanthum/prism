import matplotlib.pyplot as plt
from persim import plot_diagrams
import pandas as pd

def plot_persistence_diagrams(complexes):
    """
    This function plots the persistence diagrams for each Vietoris-Rips complex.

    Parameters:
    complexes (dict): A dictionary where the keys are sample_ids and the values are the Vietoris-Rips complexes.
    """
    if not complexes:
        raise ValueError("No complexes provided to plot.")
    try:
        for sample_id, diagrams in complexes.items():
            # Create a new figure
            plt.figure()
            # Plot the persistence diagram
            plot_diagrams(diagrams, show=False)  # Change show to False
            # Set the title to the sample ID
            plt.title(f'Sample ID: {sample_id}')
            # Save the plot as a png file
            plt.savefig(f'{sample_id}_persistence_diagram.png')
            # Save the diagram data to a CSV file
            for dim, diagram in enumerate(diagrams):
                df = pd.DataFrame(diagram, columns=['birth', 'death'])
                df.to_csv(f'{sample_id}_persistence_diagram_dim_{dim}.csv', index=False)
            # Show the plot
            plt.show()
    except Exception as e:
        raise Exception("Failed to plot persistence diagrams due to: ", str(e))
