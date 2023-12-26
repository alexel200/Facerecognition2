# Face recognition
 Face recognition is a Rest API - Siamese Neural Networks for One-shot Image Recognition, implemented under Flask Python and following the Nicholas Renotte tutorial "Build a Python Facial Recognition App with Tensorflow and Kivy".

 ## Build & Run Docker
 Once the project has been cloned, could run locally through docker and its docker file, Just type the next commands in the Face recognition root path project:

   ### Buil the image
     - `docker image build -t facerecognition .`
 
   ### Run the container
    - `docker run -p 5000:5000 facerecognition`
  
  ## Face recognition endpoints
  For testing, the system has integrated swagger where all the endpoints are documented and could be tested. Please visit http://localhost:5000/swagger

  ## References
    - Nicholas Renotte [Build a Python Facial Recognition App with Tensorflow and Kivy][https://youtu.be/LKispFFQ5GU?si=U1WPU9d-BgTZB3-g]
    - Gregory Koch, Richard Zemel, Ruslan Salakhutdinov [Siamese Neural Networks for One-shot Image Recognition][https://www.cs.cmu.edu/~rsalakhu/papers/oneshot1.pdf]

 
