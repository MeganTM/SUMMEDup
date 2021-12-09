# SUMup
Scripts to process and view data from the SUMup firn and snow density dataset

## Cloning the repository

### Option 1: Google Colab

1. Open your Google Drive open a Google Colab noteboook by clicking New > More > Google Colaboratory.
3. Once the notebook opens, type the following lines to clone this repository in your Google Drive:

```
from google.colab import drive
drive.mount('/content/gdrive')
%cd gdrive/My Drive
! git clone https://github.com/MeganTM/SUMup
```
3. Navigate back to your Google Drive and there should be a folder called `SUMup`.
4. Within the new folder, double click on the notebook `ExamineSUMup.ipynb` and it should open up within Google Colab.


### Option 2: Jupyter

### Required libraries:
* xarray
* numpy
* pandas
* matplotlib
* cartopy
* simplekml

1. Install the required libraries (if not already installed)
2. In a terminal window, clone the repository:
```
git clone https://github.com/MeganTM/SUMup
```
3. Open the notebook `ExamineSUMup.ipynb` in Jupyter.
