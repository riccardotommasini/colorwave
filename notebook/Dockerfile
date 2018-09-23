FROM  jupyter/datascience-notebook:latest

USER root

# libav-tools for matplotlib anim
RUN apt-get update && \
    apt-get install -y graphviz

RUN pip install --upgrade pip

USER jovyan

WORKDIR /home/jovyan/work/

RUN pip install websocket-client
RUN pip install rdflib
RUN pip install pydot
RUN pip install rdflib-jsonld
RUN pip install json2html

ENTRYPOINT ["start-notebook.sh","--NotebookApp.token=''"]
