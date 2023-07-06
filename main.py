import spectro_input
import vrips_calculation
import barcode_output


def main():
    try:
        print("Starting program...")
        print("Loading and preprocessing spectroscopic data...")
        spectro_data = spectro_input.load_csv_data('data/raw1_fixed.csv')
        concentration_data = spectro_input.load_csv_data('data/conc.csv')
        tidy_spectro_data = spectro_input.reshape_spectro_data(spectro_data)
        merged_data = spectro_input.merge_data(tidy_spectro_data, concentration_data)

        print("Calculating Vietoris-Rips complexes...")
        complexes = vrips_calculation.calculate_all_vietoris_rips_complexes(merged_data)

        print("Plotting persistence diagrams and saving to files...")
        barcode_output.plot_persistence_diagrams(complexes)

        print("Program completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1  # Non-zero return indicates an error occurred

    return 0  # Zero return indicates the program ran successfully


if __name__ == "__main__":
    main()
