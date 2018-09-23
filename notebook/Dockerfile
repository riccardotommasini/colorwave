FROM  jupyter/datascience-notebook:latest

RUN pip install websocket-client
RUN pip install plotly
RUN pip install rdflib
RUN pip install rdflib-jsonld

ENTRYPOINT ["start-notebook.sh","--NotebookApp.token=''"]
