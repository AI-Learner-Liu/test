# Reproduction of GLEAMS
Reproduce the function "calculate the distance between the spectrum and evaluate whether it corresponds to the same peptide segment in the evaluation spectrum" in the paper
## Installation
### 1. Create a Conda environment and install the necessary compiler tools and GPU runtime
```
conda env create -f https://raw.githubusercontent.com/bittremieux/GLEAMS/master/environment.yml && conda activate gleams
```
### 2. Install GLEAMS:
```
pip3 install git+https://github.com/bittremieux/GLEAMS.git
```
## Using GLEAMS

For detailed usage information, see the command-line help messages:

```
gleams --help
gleams embed --help
gleams cluster --help
```

### Spectrum embedding

GLEAMS provides the `gleams embed` command to convert MS/MS spectra in peak files to 32-dimensional embeddings. Example:

```
gleams embed *.mzML --embed_name GLEAMS_embed
```

This will read the MS/MS spectra from all matched mzML files and export the results to a two-dimensional NumPy array of dimension _n_ x 32 in file `GLEAMS_embed.npy`, with _n_ the number of MS/MS spectra read from the mzML files.
Additionally, a tabular file `GLEAMS_embed.parquet` will be created containing corresponding metadata for the embedded spectra.

### Embedding clustering

After converting the MS/MS spectra to 32-dimensional embeddings, they can be clustered to group spectra with similar embeddings using the `gleams cluster` command. Example:

```
gleams cluster --embed_name GLEAMS_embed --cluster_name GLEAMS_cluster --distance_threshold 0.3
```

This will perform hierarchical clustering on the embeddings with the given distance threshold.
The output will be written to the `GLEAMS_cluster.npy` NumPy file with cluster labels per embedding (`-1` indicates noise, minimum cluster size 2).
Additionally, a file `GLEAMS_cluster_medoids.npy` will be created containing indexes of the cluster representative spectra (medoids).

### Advanced usage

Full configuration of GLEAMS, including various configurations to train the neural network, can be modified in the `gleams/config.py` file.

## Using Tips
### 1、Version conflict
When the installation package version conflicts, try to modify the version according to the prompts, and try to keep the version of `tensorflow-gpu==2.3.4`,the version of matplotlib can be reduced to accommodate `numpy==1.18.5`
### 2、Incomplete download
when using the command`pip3 install git+https://github.com/bittremieux/GLEAMS.git`,the trained model in `gleams_82c0124b.hdf5` under `/GLEAMS/data` file will not be downloaded,you need to download the file directly from :
```
https://github.com/AI-Learner-Liu/GLEAMS/blob/master/data/gleams_82c0124b.hdf5
```
### 3、Code change
#### 3.1 Modify temporary path to permanent path
Execute the following command to open the code file：
```
cd /nvme/liuweichen/anaconda3/envs/gleams/lib/python3.8/site-packages/gleams-0.0.0-py3.8.egg/gleams
```
Execute the following command to change the code：
```
sudo vi gleams.py
```
Modify the code in the line 61 form `temp_dir = tempfile.mkdtemp()` to:
```
temp_dir = '/nvme/liuweichen/data_test'
```
Delete the code `shutil.rmtree(temp_dir)` in line 102
#### 3.2 Create a folder to store files before Spectrum embedding
Execute the following command to create the folder:
```
mkdir /nuvm/liuweichen/deta_test/
```
#### 3.3 Spectrum embedding
Execute the command to convert MS/MS spectra in peak files to 32-dimensional embeddings:
```
```
```
gleams embed peaks.mgf --embed_name GLEAMS_embed
```
