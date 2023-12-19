# start by pulling the python image
FROM tensorflow/tensorflow

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# copy the requirements file into the image
COPY ./requirements.txt /Facerecognition/requirements.txt

# switch working directory
WORKDIR /Facerecognition

RUN pip install --upgrade pip

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt --ignore-installed embedchain

# copy every content from the local file to the image
COPY . /Facerecognition

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]
