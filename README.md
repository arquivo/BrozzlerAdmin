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

