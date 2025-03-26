# XRF_Data_Vis
Codes for visualising data from XRF data

# Rename files
To remove the added folder extension from each .fsa file, run the rename_files.sh script.
Add it into the folder and and run as follows through terminal:
./rename_files.sh

# Visualising Capillary Electrophoresis Files (.fsa)
These files are: convert_fsa_to_csv.py, plot_csvs.py
They will convert and make png's for each file in a folder. 

In each case:
Open terminal at folder containing .fsa files and copy the python codes in
	- In terminal run: python convert_fsa_to_csv.py
	- And then run: plot_csvs.py
  - plot_csvs.py currently outputs png files but there is a commented out code for .eps instead if preferred
  


