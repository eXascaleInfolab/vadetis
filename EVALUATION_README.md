# Evaluation

Make sure that Vadetis contains the datasets needed for the experiments, i.e. you can connect with:

```
sudo ssh -L 80:localhost:80 username@diufrm144
```

Then access Vadetis frontend via http://localhost in your browser.

If Vadetis is installed and operating, add the datasets located in the misc/datasets/evaluation folder. 
The test_\*.csv file is the evaluation dataset whereas the train_\*.csv is the training dataset. 
Humidity and Temperature dataset contain an additional loc\*.csv file that contains 
the spatial coordinates of the time series. (However, they should already be available on the diufrm144 server)

In order to run the experiments, the following datasets for scenarios must be available:

## Single Contaminated Time Series

### Temperature

Name | Folder 
--- | --- 
Temperature TS8 | misc/datasets/evaluation/temp1/single_contaminated/ts_number_8
Temperature TS14 | misc/datasets/evaluation/temp1/single_contaminated/ts_number_14
Temperature TS8 CL100 | misc/datasets/evaluation/temp1/single_contaminated/cont_level_100
Temperature TS8 CL150 | misc/datasets/evaluation/temp1/single_contaminated/cont_level_150
Temperature TS8 CL200 | misc/datasets/evaluation/temp1/single_contaminated/cont_level_200
Temperature TS8 CL250 | misc/datasets/evaluation/temp1/single_contaminated/cont_level_250

### Humidity

Name | Folder 
--- | --- 
Humidity | misc/datasets/evaluation/hum1/single_contaminated/ts_number_9
Humidity CL100 | misc/datasets/evaluation/hum1/single_contaminated/cont_level_100
Humidity CL150 | misc/datasets/evaluation/hum1/single_contaminated/cont_level_150
Humidity CL200 | misc/datasets/evaluation/hum1/single_contaminated/cont_level_200
Humidity CL250 | misc/datasets/evaluation/hum1/single_contaminated/cont_level_250

## Multiple Contaminated Time Series

### Temperature

Name | Folder 
--- | --- 
Temperature TS8 Multi | misc/datasets/evaluation/temp1/multiple_contaminated/ts_number_8
Temperature TS14 Multi | misc/datasets/evaluation/temp1/multiple_contaminated/ts_number_14
Temperature TS8 Multi CL100 | misc/datasets/evaluation/temp1/multiple_contaminated/cont_level_100
Temperature TS8 Multi CL150 | misc/datasets/evaluation/temp1/multiple_contaminated/cont_level_150
Temperature TS8 Multi CL200 | misc/datasets/evaluation/temp1/multiple_contaminated/cont_level_200
Temperature TS8 Multi CL250 | misc/datasets/evaluation/temp1/multiple_contaminated/cont_level_250

### Humidity

Name | Folder 
--- | --- 
Humidity Multi | misc/datasets/evaluation/hum1/multiple_contaminated/ts_number_9
Humidity Multi CL100 | misc/datasets/evaluation/hum1/multiple_contaminated/cont_level_100
Humidity Multi CL150 | misc/datasets/evaluation/hum1/multiple_contaminated/cont_level_150
Humidity Multi CL200 | misc/datasets/evaluation/hum1/multiple_contaminated/cont_level_200
Humidity Multi CL250 | misc/datasets/evaluation/hum1/multiple_contaminated/cont_level_250

### A2

Name | Folder 
--- | --- 
A2 Yahoo | misc/datasets/evaluation/a2/multiple_contaminated/ts_number_10
A2 Yahoo Contamination 100 | misc/datasets/evaluation/a2/multiple_contaminated/cont_level_100
A2 Yahoo Contamination 150 | misc/datasets/evaluation/a2/multiple_contaminated/cont_level_150
A2 Yahoo Contamination 200 | misc/datasets/evaluation/a2/multiple_contaminated/cont_level_200
A2 Yahoo Contamination 250 | misc/datasets/evaluation/a2/multiple_contaminated/cont_level_250

## Runtime

Runtime experiment uses same datasets as in the previous scenarios

Name | Folder 
--- | --- 
Temperature TS14 | misc/datasets/evaluation/temp1/single_contaminated/ts_number_14
Humidity | misc/datasets/evaluation/hum1/single_contaminated/ts_number_9

## Perform experiments

### Productive environment

In order to perform the experiments on the productive environment, map the port for Jupyter notebooks
 to your local machine, i.e.:
```
sudo ssh -L 8888:localhost:8888 username@diufrm144
``` 

As soon as you are connected to the machine running the productive environment, just start the venv on you terminal 
(location depends on the folder configured during installation), i.e.:

```
source /usr/local/venvs/venv_vadetis/bin/activate
``` 

Go to the installation folder of productive Vadetis (where the manage.py file is located), i.e.:

```
cd /var/www/vadetis.exascale.info/
```

then run:

```bash
env DJANGO_ALLOW_ASYNC_UNSAFE=true ./manage.py shell_plus --notebook --settings vadetis.settings.development
```

If you are connected on a remote machine, then you will see in the terminal 
the link to start the Juypter notebooks. Copy and paste this in the browser 
of your local machine. The Jupyter notebooks to perform the experiments are located in misc/notebooks/eval


### Development environment


If you want to perform the experiments on your local machine, just start:

```bash
env DJANGO_ALLOW_ASYNC_UNSAFE=true ./manage.py shell_plus --notebook --settings vadetis.settings.production
```
The browser page should be opened automatically, 
then goto the notebook of the experiment which you want to run. 
Don't forget to add the datasets on your local machine as mentioned above.

