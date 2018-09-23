# ColorWave - A Stream Reasoning Tutorial

![img](https://media.realitatea.net/multimedia/image/201707/full/colors_64168900.jpg)

This is the initial repository for the tutorial

The structure works as follow

solutions/ folder contians the solution notebooks
partial/   folder contains the partially solved exercises so you can jump straight to the point!
guided/    folder contains notebooks with no code, but each step is commented step-by-step for you to solve
stub/      folder contains almost empty notebooks that just import the correct libraries 

To run this tutorial you need docker and docker-compose. [Here](https://docs.docker.com/get-started/) there is a tutorial for you to learn how!


The tutorial runs 5 containers:

- Jasper - an RSP Engine that will run out continous queries
- ColorStream - a streamer of color instances in RDF. Three of them will be run: Red, Green and Blue.
- StreamHub - A Stream Publishing Service
- MyNotebook - A Jupyter Notebook interface to interact with out rdf streams/rsp engines



## Running the tutorial

Clone this repository or [download it](https://github.com/riccardotommasini/colorwave/archive/master.zip)

From inside the project folder run 

```docker-compose up```

Then go to [MyNotebook](http://localhost:8080)
