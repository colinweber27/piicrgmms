# piicrgmms

A package for implementing Gaussian mixture models as a data 
analysis tool in PI-ICR mass spectrometry experiments. piicrgmms 
was first developed in the Fall of 2020 to be used in PI-ICR 
experiments at the Canadian Penning Trap (CPT) mass 
spectrometer at Argonne National Laboratory (Lemont, IL, U.S.). 
It was originally published as 
[GMMClusteringAlgorithms](https://pypi.org/project/GMMClusteringAlgorithms/), 
but was repackaged as piicrgmms in preparation for the 
publication of an upcoming journal article about its use.

At piicrgmms' core is a modified version of the ['mixture' module 
from the package scikit-learn.](https://scikit-learn.org/stable/modules/mixture.html)
The modified version, *sklearn_mixture_piicr*, retains all 
the same components as the 
original version. In addition, it contains two classes with 
restricted fitting algorithms: a Gaussian mixture model fit using 
the expectation-maximization algorithm where the phase 
dimension of the component means is _not_ a parameter, and a
Bayesian Gaussian Mixture fit where the number of components is 
_not_ a parameter.

The rest of the package facilitates
quick, intuitive use of the Gaussian mixture model algorithms 
through the use of 4 classes, with visualization methods for 
displaying results and debugging.

#### 1. DataFrame
* This class is responsible for processing the raw data from 
  the position-sensitive micro-channel plate (PS-MCP) 
  detector. It currently only works with List Mode (.lmf) 
  files, which is the file type used by CoboldPC, the 
  software used at the CPT to record data from the 
  position-sensitive microchannel plate (PS-MCP). 
  As attributes, it holds the processed data in both array and 
  pandas DataFrame form, as well as any data cuts. CoboldPC is 
  a product of [RoentDek.](http://www.roentdek.com)
  
#### 2. GaussianMixtureModel
* This class fits Gaussian mixture models to the 
  DataFrame object. As parameters, it takes:
  1. Cartesian/Polar coordinates
  2. Number of components to use
  3. Covariance matrix type
  4. Information criterion
* Allows for 'strict' fits, i.e. fits where the number 
  of components is specified.
* Includes a progress bar when clustering data.
  
#### 3. BayesianGaussianMixture
* Exact same as the GaussianMixtureModel class, but 
  uses the BayesianGaussianMixture class from scikit-learn
  instead of the GaussianMixtureModel class.
* No progress bar.
  
#### 4. PhaseFirstGaussianModel
* Implements a fit where the phase dimension is fit to
  first, followed by a GMM fit to both spatial dimensions
  in which the phase dimension of the component means is
  fixed. This type of fit was found to work especially 
  well with data sets in which there are many species.
* Only works with Polar coordinates
* Progress bar included.

Each model class also includes the ability to visualize
results in several ways (clustering results, one-dimensional
histograms, probability density functions) and the ability to
copy fit results to the clipboard for pasting into an Excel
spreadsheet.

### Examples
#### DataFrame
As this package is designed to be used in PI-ICR 
experiments, and many such experiments already rely on 
RoentDek technology, it is assumed that data has already been 
collected and stored in .lmf files. The first step is to read 
and process the files, which can be done with the following code:
```
import piicrgmms.classes as pgc

file = 'C:\here\is\the\path\to\the_file.lmf'
df = pgc.DataFrame(file)
df.process_lmf()
```
After processing the .lmf file, the object 'df' will have 
additional attributes. One of these is 'data_array_', which is a 
numpy array containing the locations of the ion hits on the 
detector. It has shape (n_samples, 4), and the four columns 
correspond to the x-, y-, radius, and phase dimensions, in that 
order. 

Other options, such as defining the trap center and data cuts, 
can be passed to the initialization of the DataFrame as 
keyword arguments. For example, to move the location of the trap 
center to (1, 1) in Cartesian coordinates, give the 
trap center location an uncertainty of 0.02, restrict the 
data set to shots on the PS-MCP in which there was at least 1 
ion but less than 5, and output the phase dimension in radians:
```
center = (1, 1)
center_uncertainty = (0.02, 0.02)
ion_cut = (0, 5)
# Note that the ion_cut values are *not* inclusive.
df = pgc.DataFrame(file, center=center, center_unc=center_uncertainty), 
                   ion_cut=ion_cut, phase_units='rad')
df.process_lmf()
```
Alternatively, the line `StartTime, EndTime = df.process_lmf()` 
processes the .lmf file and outputs the times that data recording 
began and ended.

Following processing, the DataFrame object can export the data 
in more meaningful formats. The following block of code returns 
the 'data_array_' in the form of a pandas.ExcelWriter object, 
returns and shows a 2D histogram of the locations of the ion hits 
on the detector, and saves both objects:
```
spreadsheet = df.return_processed_data_excel()
spreadsheet.save()

fig, save_string = df.get_data_figure()
plt.savefig(save_sring)
plt.show()
```

#### GaussianMixtureModel / BayesianGaussianMixture / PhaseFirstGaussianModel
Once the data has been processed using the function 
`df.process_lmf()`, it is ready to be clustered. This 
is done with an eight-component Gaussian Mixture Model in 
Cartesian coordinates, for example, using the following code:
```
model = GaussianMixtureModel(n_components=8, coordinates='Cartesian')
model.cluster_data(data_frame_object=df)
```
Other clustering algorithms are used by changing the model that 
is initialized to either `BayesianGaussianMixture()` or 
`PhaseFirstGaussianModel()`. The function `cluster_data` gives 
the model object several important attributes, such as:
* `model.centers_array_`, which is a numpy array of shape 
  (n_components, 9) containing the locations of the cluster 
  centers. Each row corresponds to one cluster, and from left to 
  right the values in each row give the x-location, x uncertainty, 
  y-location, y uncertainty, radius location, radius uncertainty, 
  phase location, phase uncertainty, and overall cluster 
  uncertainty (x unc. and y unc. added in quadrature) of a 
  particular cluster.
* `model.ips_` is an array-like object of length (n_components,)
  where each value is the number of ions in that cluster. It 
  should be noted that the order of clusters in each attribute 
  is the same, such that the 0th row of `model.centers_array_` 
  corresponds to the 0th entry in `model.ips_`, and so on.
* `model.weights_, model.means_, model.covariances_` are the 
  fit parameters of the Gaussian mixture model.
* `model.labels_` are the cluster assignment of each ion in the 
  data set.
  
Other attributes from the fit are listed in the documentation. 

The centers of the clusters don't have to be taken directly from 
the fit results. Instead, the centers of the clusters can be 
recalculated by running 
`model.recalculate_centers_uncertainties(data_frame_object=df, indices=None)`, 
where the argument `indices` is either `None` if all centers are 
to be recalculated, or a list giving the cluster indices to 
change. This function works by taking the cluster assignments 
obtained from the `model.cluster_data()` command and fitting 
two one-dimensional Gaussians to each cluster in order to find 
the cluster centers and uncertainties. All attributes are then 
updated accordingly.

Other useful functions associated with the model classes that 
can be called following clustering are:
* `model.cluster_data_strict()`, which is the exact same as 
`model.cluster_data()` except it forces the model to have the 
  number of components given by the argument `n_components`.
  
* `fig, save_string = model.get_results_fig(data_frame_object=df)`, 
which returns a plot of the ion hits showing their cluster 
  assignments, the cluster centers, and cluster center 
  uncertainties. It also returns a suggested string to use 
  when saving the figure.
  
* `fig, save_string = model.cluster_merger(data_frame_object=df)`, 
which activates a GUI that allows for clusters to be merged 
  together in the event that the Gaussian mixture model fails 
  to cluster the data set reasonably. After running, follow 
  the prompts on the command line to go through this process. 
  * ***WARNING:*** This function should not be used under 
    typical circumstances, as it overrides the 
    mathematically-supported results from the Gaussian mixture 
    models. While the models aren't perfect, their results 
    should not be thrown away lightly in the event that they 
    don't agree with a preferred clustering outcome.
    
All together, a typical block of code that reads the .lmf, clusters 
the data, and outputs and saves an image looks something like 
this:
```
import piicrgmms.classes as pgc

# Set constants
xC = 1
yC = 1
xC_unc = 0.02
yC_unc = 0.02

center = (xC, yC)
center_unc = (xC_unc, yC_unc)

ion_cut = (0, 5)

file = 'C:\here\is\the\path\to\the_file.lmf'

df = pgc.DataFrame(file=file, center=center, center_unc=center_unc, 
                   ion_cut=ion_cut, phase_units='rad')
StartTime, EndTime = df.process_lmf()

model = pgc.GaussianMixtureModel(n_components=8)
model.cluster_data(data_frame_object=df)
fig, save_string = model.get_results_fig(data_frame_object=df)
plt.savefig(save_string, bbox_inches='tight')
plt.show()
```


### Installation
####  Dependencies
piicrgmms requires:
* Python (>=3.6)
* scikit-learn (>=0.23.2)
* pandas (>=1.2.0)
* matplotlib (>=3.3.0)
* lmfit (>=1.0.0)
* joblib (>=1.0.0)
* tqdm (>=4.56.0)
* pillow (>=8.1.0)
* webcolors(>=1.11.1)

#### User Installation
Assuming Python and `pip` have already been installed, decide
whether you want a system-wide or local installation, and 
which Python distribution (e.g. Anaconda) you want to 
install under. Then, open the Command Prompt (for regular 
Python distribution) or the Prompt for another distribution 
(e.g. Anaconda Prompt for Anaconda), and run either:
* `pip install piicrgmms` for a system-wide 
installation (works for regular Python distributions only),
  **OR**
* `pip install -U piicrgmms` for a local 
    installation.
  
If you want to install in a virtual environment instead, 
then navigate to the virtual environment's directory, activate 
the virtual environment, and install with the commands above.

### Source code
You can check the latest source code with the command  
`git clone https://github.com/colinweber27/piicrgmms`

