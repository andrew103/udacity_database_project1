============== DESCRIPTION ================
This project takes in a database and uses a Python file to manipulate the data
in that database in order to provide information. This information includes
number of views per article, number of views per author via their articles, and
the percentage of HTTP requests that returned a '404 NOT FOUND' per day if it
exceeded 1%.

============== DIRECTIONS =================
Follow these steps to run the project:
    1) Download these files into your vagrant directory for your virtual machine
    2) Run the virtual machine and navigate to the shared /vagrant folder
    3) Navigate to the project folder and run the 'python newsdata.py' command

============== NOTE =======================
You can also control which tests are run by commenting/uncommenting the
appropriate commands in the main run() function in newsdata.py
