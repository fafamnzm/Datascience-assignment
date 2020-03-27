# YapAiTek-assignment
      
      dependencies:
      # pip install -U scikit-learn
      # pip install matplotlib

In this file a set of data (data.csv) is at hand to train a model and  
a set of test data (test.csv) is available to test the trained model  
In this assignment, an attemp is made to use linear regression and   
three SVR (support vector regression) methods (linear, poly and rbf) to train the model and predict the outcome.  
In order to reduce the time of compiling, only the svr_rbf method is used,   
but the rest work perfectly fine if they are uncommented.  
The code plots the training model too, which can be added back by removing from comment   
in order to calculate the error threshold of the trained model,  
the last row for the first show is designated for testing the margin of error, which is printed on the console.  
In order to reduce the time of execution, a limit is set in the variable limit at the top  
which will calculate the limit number of shows on the result.csv  
the current limit value is 10  
