# Papers Library (WIP) #

Get the paper information from [arXiv.org](https://arxiv.org/) based on the ID, take your notes about the paper and save it into a MongoDB database.

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


## TODO: ##

* Analyze the text and extract other sections in addition to the abstract
