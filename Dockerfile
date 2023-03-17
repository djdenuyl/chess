FROM mambaorg/micromamba:latest

ARG MAMBA_DOCKERFILE_ACTIVATE=1
ENV PYTHONUNBUFFERED=1

COPY --chown=$MAMBA_USER:$MAMBA_USER . /opt/chess/

RUN micromamba create -y --file /opt/chess/conda.yml && \
    micromamba clean --all --yes

# set the environment name as env var after mamba installation
ENV ENV_NAME=chess
#ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "python", "/opt/chess/app.py"]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app