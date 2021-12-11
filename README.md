# SUMMEDup: The SUMup Dataset Explorer
_Scripts to process and view data from the SUMup snow and firn density dataset_

The developed library `SUMMEDup.py` can be imported into any script and used on its own, but to best explore its functionality, follow the instructions below to use this product in Binder, with Google Colab, or locally in Jupyter.


### Option 1: Binder
1. Go to https://mybinder.org/
2. Copy and paste the following repository URL into the "GitHub repository name or URL" field: https://github.com/MeganTM/SUMMEDup
3. Click "launch"
4. Once loaded, open the notebook `SUMMEDupTutorial.ipynb`.


### Option 2: Google Colab

1. Open Google drive and create a new Google Colab noteboook by clicking New > More > Google Colaboratory.
2. Once the notebook opens, type the following lines and run the cell to clone this repository in your Google Drive:
```
from google.colab import drive
drive.mount('/content/gdrive')
%cd gdrive/My Drive
! git clone https://github.com/MeganTM/SUMMEDup
```
3. A prompt may appear asking, "Permit this notebook to access your Google Drive files?" Click "Connect to Google Drive" and, if prompted, sign in to your account and allow all permissions.
4. Navigate back to your Google Drive and open up the newly created folder called `SUMMEDup`.
5. Double click on the notebook `SUMMEDupTutorial.ipynb` and it should open up within Google Colab.


### Option 3: Jupyter

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
A new folder should appear called `SUMMEDup`.

3. Within the `SUMMEDup` folder, open the notebook `SUMMEDupTutorial.ipynb` in Jupyter.


Once you've completed one of the above options, you are all set to begin running the tutorial. Instructions and helpful comments can be found in the notebook itself. If you have any questions or ideas for new functions, please reach out to Megan Thompson-Munson at metm9666@colorado.edu.

IMPORTANT NOTE FOR JUPYTER USERS: This script was originally designed for Google Colab, and may require some adjustments for use in Jupyter. For example, the first cell in which you set up Google Drive does not need to be run if you're in Jupyter. Future updates to this tool will create a more seamless transition between Google Colab and Jupyter.
