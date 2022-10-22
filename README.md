# CS-471, Student Loan System

This application was created as submission for the final project for CS-471, Software Engineering at Kettering University. The project contains four features of a student loan application - a secure login portal, the ability for students to submit loans, the ability for bank officials to approve/reject loans, and a monthly payment calculator for students to keep track of loan payments.

The team responsible for this project includes Alex Keeler, Matthew Muller, Evan Mortier, and Jason Sedluk.

## Install Instructions

Click on the 3 dots next to "clone" and download repository (Remember where you installed this for later!)

The following instructions will be for Windows 10. While we we're able to set the program up on linux and MacOS, we recommend windows for a streamlines process

---

## Setting up database 

1. Go to https://dev.mysql.com/downloads/installer/ and download the windows installer for MySQL. The correct version will be the one with more downloads and will NOT have -web- apart of it. 
2. on setup type click "Full"
3. Follow the installer. It will go ahead and install pre-reqs for you when you hit the "execute" button in the next screen (installation process will take a bit, make/grab a cup of coffee and wait)
4. After you finish setup, you will want to type "mysql" in the windows search bar and look for "mysql command line client" and run it
5. Now you will type in the following commands...


```
SOURCE path/to/loandb.sql
CREATE USER 'loanuser'@'localhost' IDENTIFIED BY 'loanuser';
GRANT ALL PRIVILEGES ON loandb.* TO 'loanuser'@'localhost';
```

---

## Python Setup

1. go to python.org and install the latest python-3.x.x
2. Follow the .exe and make sure to click the box that says "Add Python to PATH"
3. You should have pip installed, if you do not, you will want to follow [these steps](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/#:~:text=Download%20and%20Install%20pip%3A&text=Download%20the%20get%2Dpip.py,where%20the%20above%20file%20exists.&text=and%20wait%20through%20the%20installation,now%20installed%20on%20your%20system) (you can validate this by running "python -m pip --version")
4. Next you want to navigate to where you installed the code repository is installed which should look like it does in this [picture](https://i.imgur.com/qMvs2sz.png)
5. Follow the following commands where we setup a virtual environment to run the project. The following will be commands you will put into your command prompt in the directory of the code.


```
python -m venv venv
venv\Scripts\activate
pip install flask flask-bootstrap flask-wtf mysql-connector-python email_validator
```

---

## Running the program

After both of those parts are setup, you will want to go to your command prompt with "venv" where you were doing the python install and type in the command "flask run"
This will launch the website. The url for the website be "localhost:5000/login"
