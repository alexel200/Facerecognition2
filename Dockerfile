# start by pulling the python image
FROM tensorflow/tensorflow

# copy the requirements file into the image
COPY ./requirements.txt /src/requirements.txt

# switch working directory
WORKDIR /src

RUN pip install --upgrade pip

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt --ignore-installed embedchain

# copy every content from the local file to the image
COPY . /src

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["__init__.py" ]
