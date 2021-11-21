FROM python:3.8

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
	cd /usr/local/bin && \
	ln -s /opt/poetry/bin/poetry && \
	poetry config virtualenvs.create false 

# This needs to be done because poetry install runs before vscode dev container copies the local folders
# to the containers
COPY ./brots /brots
COPY ./renderers /renderers
COPY ./notebooks /notebooks
COPY poetry.lock* pyproject.toml setup.cfg ./
RUN poetry install
