# start by pulling the python image
FROM python:3.9

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# copy the requirements file into the image
COPY ./requirements.txt /Facerecognition/requirements.txt

# switch working directory
WORKDIR /Facerecognition

RUN pip install --upgrade pip

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt --ignore-installed embedchain

#RUN pip install tensorrt
# copy every content from the local file to the image
COPY . /Facerecognition

RUN mkdir -p src/images/users
RUN mkdir -p src/images/verification
RUN wget https://www.dropbox.com/scl/fi/nrs2mlr38wnxkuddcja77/siamesemodelv2.h5?rlkey=fxgo4ggo618svxloc9xkf7t9g -O src/modelFiles/siamesemodelv2.h5
RUN wget https://www.dropbox.com/scl/fi/nrs2mlr38wnxkuddcja77/siamesemodelv2.h5?rlkey=fxgo4ggo618svxloc9xkf7t9g -O src/modelFiles/siamesemodelv3.h5
# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]
