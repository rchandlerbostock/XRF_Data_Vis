import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to plot data from a CSV file
def plot_data_from_csv(csv_file_path):
    # Read the CSV file
    data = pd.read_csv(csv_file_path)

    # Display the first few rows of the data
    print(f"Processing {csv_file_path}...")
    print(data.head())

    # Plot the data
    plt.figure(figsize=(10, 6))

    # Assuming the columns are 'Footprinted Sample', 'ddA Ladder', 'ddC Ladder', and 'Space Measure'
    plt.plot(data['Position'], data['Footprinted Sample'], label='Footprinted Sample', color='blue')
    plt.plot(data['Position'], data['ddA Ladder'], label='ddA Ladder', color='orange')
    plt.plot(data['Position'], data['ddC Ladder'], label='ddC Ladder', color='green')
    plt.plot(data['Position'], data['Space Measure'], label='Space Measure', color='red')

    # Adding labels and title
    plt.xlabel('Position')
    plt.ylabel('Value')
    plt.title('Data from FSA File')
    plt.legend()
    plt.grid()

    # Save the plot as a PNG file
    png_file_path = csv_file_path.replace('.csv', '.png')
    plt.savefig(png_file_path)
    plt.close()  # Close the figure to free up memory

    # Alternatively save the plot as an EPS file
    #eps_file_path = csv_file_path.replace('.csv', '.eps')
    #plt.savefig(eps_file_path, format='eps')
    #plt.close()  # Close the figure to free up memory

# Directory containing CSV files
directory = os.getcwd()  # Current working directory or specify another path

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        csv_path = os.path.join(directory, filename)
        plot_data_from_csv(csv_path)

print("Plots saved as PNG files.")
