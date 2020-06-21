FROM  jupyter/datascience-notebook:aa0ebba9a0a4

EXPOSE 8080

USER root

# libav-tools for matplotlib anim
RUN apt-get update && \
    apt-get install -y graphviz

RUN pip install --upgrade pip

USER jovyan

WORKDIR /home/jovyan/work/

COPY setup.py setup.py

COPY setup.py setup.py

COPY rsplib rsplib

RUN ls

RUN pip install -e .

ENTRYPOINT ["start-notebook.sh","--NotebookApp.token=''"]
