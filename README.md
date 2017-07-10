## Description
This project takes in a database and uses a Python file to manipulate the data
in that database in order to provide information. This information includes
number of views per article, number of views per author via their articles, and
the percentage of HTTP requests that returned a '404 NOT FOUND' per day if it
exceeded 1%.

The database that data is being extracted from consists of three tables: one
for articles and their views, another for authors and their information, and
the last for logging all the HTTP requests the host site is receiving with
various data included such as URI being visited or HTTP code returned.

## How to run the program
Follow these steps to run the project:
    1) Download the project into a directory of your choice
    2) Navigate to that directory through Terminal or Git Bash
    3) Run the command `vagrant up` in the window to boot the vagrant machine
    4) Run the command `vagrant ssh` to access the machine
    5) A database is included with the machine. To access it, run the command
    `psql -d news -f newsdata.sql` to create an SQL file with the information
    6) Type `cd /vagrant` to access the shared folder
    7) Navigate to the `PROJECT` directory
    8) Run the command `python newsdata.py` to run the program

## Note
You can also control which tests are run by commenting/uncommenting the
appropriate commands in `__main__` at the bottom of `newsdata.py`
