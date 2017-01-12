# CozmoProj

This is a project that interprets user emotions and attempts to reciprocate using a Cozmo robot. Obviously, a Cozmo is required to run it, but otherwise it also makes use of TensorFlow and OpenCV.

The models are bundled in the repository, so you don't need to train anything. Once you have all of the dependencies installed and setup, simply run "study1.py" with your Cozmo connected and in SDK mode
Study1 interprets facial expressions using the built-in webcam of a laptop and listens to speech using the laptop's microphone (interpretation is done with Google's API, so an Internet connection is required).
Study2 uses expressions only, and study 3 uses language only.

Because sometimes speech interpretation takes a while, you may wish to alter the amount of time that I have hard-coded to allow for users to respond. Ideally the system will wait for a gap in speech to respond, but due to time constraints I was unable to get this into the project.
