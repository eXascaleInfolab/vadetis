
# Vadetis

Vadetis is a web application to perform, compare and validate various anomaly detection algorithms using different configurations. It allows users to upload their own datasets as well as training data in order to perform anomaly detection. The datasets can be altered by injecting additional outliers.  Technical details can be found in our ICDE 2021 Demo paper:  <a href = "https://icde2021.gr">VADETIS: An Explainable Evaluator forAnomaly Detection Techniques </a>. The tool can be easily extended with new algorithms, datasets and  metrics.

- Vadetis implements the following
    - *anomaly detectors*: One-Class SVM, LISA (Pearson and DTW), GMM, Histogram, Isolation Forest, and Robust PCA.  
    - *metrics*: Precision, Recall, Accuracy, F1-score, RMSE, NMI, and AUC.
- Users can perform a recommendation for the best technique on a specific dataset using different performance metrics.



[**Prerequisites**](#prerequisites) | [**Deployment**](#deployment)  | [**Extension**](#extension)  | [**Contributors**](#contributors) | [**Citation**](#citation)


___

## Prerequisites

- Ubuntu 16 or Ubuntu 18.
- Clone this repository.
___

## Deployment
### Build

Run the vadetis_install.sh script in the root folder. 

```bash
./vadetis_install.sh
```

### Start and stop the tool

After deployment the tool should be already running. However, you need to enable Vadetis with:
```
sudo a2ensite vadetis
sudo service apache2 reload
```

to disable Vadetis, run:
```
sudo a2dissite vadetis
sudo service apache2 reload
```

___
## Manual Deployment
The individual components of Vadetis can be installed separately. We provide a step-by-step tutorial on how to manually deploy the tool [tutorial](https://github.com/eXascaleInfolab/vadetis/tree/master/vadetis/README.MD)


___

## Extension
The tool can be extended by adding:
- algorithms:
- datasets:
- metrics:
___

## Contributors
Mourad Khayati (mkhayati@exascale.info),  Abdelouahab Khelifati and Adrian Hänni.

___

## Citation
```bibtex
@inproceedings{vadetis2021icde,
  author = {Khelifati, Abdelouahab and Khayati, Mourad and Cudr{\'{e}}{-}Mauroux, Philippe and Hänni, Adrian and Liu, Qian and Hauswirth, Manfred},
  title = {VADETIS: An Explainable Evaluator for Anomaly Detection Techniques},
  booktitle = {Proceedings of the IEEE International Conference on Data Engineering (ICDE 2021)},
  year = {2021},
  address = {Crete, Greece}
}
```
