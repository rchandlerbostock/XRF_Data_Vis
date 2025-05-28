"""
plot_csvs.py

This script reads CSV files containing DNA fragment analysis data and generates corresponding plots saved as PNG images.

Dependencies:
- pandas
- matplotlib

Usage:
    python plot_csvs.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_data_from_csv(csv_file_path):
    """
    Reads a CSV file and plots the data columns, saving the plot as a PNG file.

    Parameters:
        csv_file_path (str): Path to the CSV file to be processed.

    Returns:
        None
    """
    try:
        data = pd.read_csv(csv_file_path)
    except Exception as e:
        print(f"Error reading {csv_file_path}: {e}")
        return

    expected_columns = ['Position', 'Footprinted Sample', 'ddA Ladder', 'ddC Ladder', 'Space Measure']
    if not all(col in data.columns for col in expected_columns):
        print(f"File {csv_file_path} is missing expected columns. Skipping.")
        return

    print(f"Processing {csv_file_path}...")
    print(data.head())

    plt.figure(figsize=(10, 6))
    plt.plot(data['Position'], data['Footprinted Sample'], label='Footprinted Sample', color='blue')
    plt.plot(data['Position'], data['ddA Ladder'], label='ddA Ladder', color='orange')
    plt.plot(data['Position'], data['ddC Ladder'], label='ddC Ladder', color='green')
    plt.plot(data['Position'], data['Space Measure'], label='Space Measure', color='red')

    plt.xlabel('Position')
    plt.ylabel('Value')
    plt.title('Data from FSA File')
    plt.legend()
    plt.grid()

    png_file_path = csv_file_path.replace('.csv', '.png')
    try:
        plt.savefig(png_file_path)
        print(f"Plot saved as {png_file_path}")
    except Exception as e:
        print(f"Error saving plot {png_file_path}: {e}")
    finally:
        plt.close()

    # To save as EPS instead of PNG, uncomment below lines:
    # eps_file_path = csv_file_path.replace('.csv', '.eps')
    # try:
    #     plt.savefig(eps_file_path, format='eps')
    #     print(f"Plot saved as {eps_file_path}")
    # except Exception as e:
    #     print(f"Error saving plot {eps_file_path}: {e}")
    # finally:
    #     plt.close()

def main():
    directory = os.getcwd()
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            csv_path = os.path.join(directory, filename)
            plot_data_from_csv(csv_path)
    print("Plots saved as PNG files.")

if __name__ == "__main__":
    main()


