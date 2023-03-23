# HousePricePredictor
The HousePricePredictor is a Python application that uses scikit-learn and MySQL to predict house prices based on their features such as number of rooms, area, neighborhood, and built year.

# Project Overview
The project consists of the following components:

* fetchdata.py : A Python script that reads data from the 'shabesh' website and stores it in a MySQL database.
* predict.py : A Python script that asks the user to input the features of a new house and predicts its price using the trained model.

**Note:** To run 'predict.py', you must first run 'fetchdata.py'. Make sure to provide your MySQL database password in 'fetchdata.py' to establish a proper connection. The code will take care of the rest.

**Note:** Use a terminal that supports persian, because you are gonna give neighbourhood to your program in persian text. However, if that is not possible run the program with given in.txt file. You can modify what is inside it. 
``` python predict.py < in.txt ```
