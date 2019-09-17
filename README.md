# Brozzler Admin

Brozzler Admin provides an Interface to help launch and manage new Brozzler jobs. It also provides a command line utlity to help manage and monitoring brozzler job.

## Install
```
git clone https://github.com/arquivo/BrozzlerAdmin/
python setup.py install
```

## Command line Usage
```
bc-resume-job --job-id JOB_ID
bc-get-job-queue --job-id JOB_ID
bc-get-outlinks --job-id JOB_ID --rejected/blocked/accepted
```
To get more options:
```
<command> --help
```
###### It creates collections where within each collection new jobs can be launched incrementally.
![Screenshot1](https://github.com/arquivo/BrozzlerAdmin/blob/master/docs/images/brozzlecontroller_1.png)

###### It provides the configuration used on the last job of the collection, to easly ajdust the configuration or just keep the same!
![Screenshot2](https://github.com/arquivo/BrozzlerAdmin/blob/master/docs/images/brozzlercontroller_2.png)

###### You can browse the new launched job or older jobs through the Brozzler Dashboard.
![Screenshot3](https://github.com/arquivo/BrozzlerAdmin/blob/master/docs/images/brozzlercontroller_6.png)

