# SUMMEDup: The SUMup Dataset Explorer
_Scripts to process and view data from the SUMup firn and snow density dataset_

The developed library `SUMMEDup.py` can be imported into any script and used on its own, but to best explore its functionality, follow the instructions below to clone this repository and walkthrough a tutorial developed in a Jupyter notebook.

## 1. Cloning the repository

### Option 1: Google Colab (recommended)

1. Open your Google Drive open a Google Colab noteboook by clicking New > More > Google Colaboratory.
3. Once the notebook opens, type the following lines to clone this repository in your Google Drive:

```
from google.colab import drive
drive.mount('/content/gdrive')
%cd gdrive/My Drive
! git clone https://github.com/MeganTM/SUMMEDup
```
3. Navigate back to your Google Drive and there should be a folder called `SUMMEDup`.
4. Within the new folder, double click on the notebook `SUMMEDupTutorial.ipynb` and it should open up within Google Colab.


### Option 2: Jupyter

#### Required libraries:
* [xarray](http://xarray.pydata.org/en/stable/getting-started-guide/installing.html)
* [numpy](https://numpy.org/install/)
* [pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [matplotlib](https://matplotlib.org/stable/)
* [cartopy](https://scitools.org.uk/cartopy/docs/latest/installing.html)
* [simplekml](https://pypi.org/project/simplekml/)

1. Install the required libraries (if not already installed)
2. In a terminal window, clone the repository:
```
git clone https://github.com/MeganTM/SUMMEDup
```
3. Open the notebook `SUMMEDupTutorial.ipynb` in Jupyter.


### Option 3: Manually download
If you have trouble with either of the above options, simply download the files in this GitHub repository and save them to a local folder on your computer (if you plan to use Jupyter) or a folder on Google Drive (if you plan to use Google Colab). The disadvantage is that you will not be able to update the repository using git commands.


## 2. Downloading the SUMup dataset

The SUMup snow and firn density dataset is too large to be stored on GitHub. However, it's available to download for free from the Arctic Data Center.
1. Click on the following link to visit the dataset on the Arctic Data Center: https://arcticdata.io/catalog/view/doi%3A10.18739%2FA2W08WH6N
2. Download the file `sumup_density_2020_v060121.nc`
3. Save the file to your Google Drive (if using Google Colab) or to the cloned repository (if using Jupyter locally).


## 3. Using the notebook
Once you've completed steps 1 and 2, you are all set to begin running the notebook. Instructions and helpful comments can be found in the notebook itself. If you have any questions or ideas for new functions, please reach out to Megan Thompson-Munson at metm9666@colorado.edu.

IMPORTANT NOTE FOR JUPYTER USERS: This script was originally designed for Google Colab, and may require some adjustments for use in Jupyter. For example, the first cell in which you set up Google Drive does not need to be run if you're in Jupyter. Future updates to this tool will create a more seamless transition between Google Colab and Jupyter.
