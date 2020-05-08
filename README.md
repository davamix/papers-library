# Papers Library (WIP) #

Get the paper information from [arXiv.org](https://arxiv.org/) based on the ID, take your notes about the paper and save it into a MongoDB database.

Working on the model to analyze paper's data.

![Screenshot](papers_library.webp "Papers Library screenshot")

## Quick Start ##

Build
```
docker-compose build
```

Run
```
docker-compose up
```

Navigate to `http://127.0.0.1:5000/library`

To reset the DB
```
docker-compose down --volumes
```

## Tools ##
* [arxiv-downloader.py](https://github.com/davamix/Scripts/blob/master/arxiv-downloader.py): Script to download pdf papers from [arXiv](https://export.arxiv.org)

* [pdf-image.py](https://github.com/davamix/Scripts/blob/master/pdf-image.py): This script converts all the pdf's from the source folder into images

* [split-data.py](https://github.com/davamix/Scripts/blob/master/split-data.py): This script split the data from a source folder into a training set and validation set.


## TODO: ##

* Analyze the text and extract other sections in addition to the abstract
