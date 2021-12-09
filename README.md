# SUMup
Scripts to process and view data from the SUMup firn and snow density dataset

## 1. Cloning the repository

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

## 2. Downloading the dataset

The SUMup snow and firn density dataset is too large to be stored on GitHub. However, it's available to download for free from the Arctic Data Center.
1. Click on the following link to visit the dataset on the Arctic Data Center: https://arcticdata.io/catalog/view/doi%3A10.18739%2FA2W08WH6N
2. Download the file `sumup_density_2020_v060121.nc`
3. Save the file to your Google Drive (if using Google Colab) or to the cloned repository if using Jupyter locally.


## 3. Using the notebook
Once you've completed steps 1 and 2, you are all set to begin running the notebook. Instructions and helpful comments can be found in the notebook itself. Should you have any questions, please reach out to Megan Thompson-Munson at metm9666@colorado.edu.
