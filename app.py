import csv
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# The list where the marketshares are stored
market_share = []

# The list where the dates are stored
date = []

# Opening .csv file using csv module
with open('data.csv') as data:
    #reading the file as a dictreader so we can access the files faster
    data_csv = csv.DictReader(data)

    # to limit the number of data in order to reduce the process time
    # i= 0
    
    # Going through ouw file row by row and chacking for a specific show
    for row in data_csv:
        
        # Checking whether the name matches
        if row['Name of show'] == 'The Big Bang Theory':
            # for x axis we convert the date to a number
            # the number starts from 29/08/2016 and from number 1
            year = (int(row['Date'].split('-')[0]) - 2016) * 365
            month = (int(row['Date'].split('-')[1])) * 30
            day = int(row['Date'].split('-')[2])
            # start from 29/08/2016
            date.append( [year + month + day - 268])
            
            market_share.append(float(row['Market Share_total']))
            
            # breaker for the limit in case we want to 
            # add a specific number of data for training model
            # i += 1
            # if(i == 500):
            #     break


# getting the last element in ordeer to get the error threshhold
error_threshhold_date = [date[-1]]
error_threshhold_market_share = [market_share[-1]]

# Reading from test file
with open('test.csv') as test:
    test_csv = csv.DictReader(test)
    
    # The dates for test file are stored in this list
    test_date = []
    
    for row in test_csv:
        if row['Name of show'] == 'The Big Bang Theory':
            # Same thing for the date as above starting from 29/08/2016
            year = (int(row['Date'].split('-')[0]) - 2016) * 365
            month = (int(row['Date'].split('-')[1])) * 30
            day = int(row['Date'].split('-')[2])
            test_date.append( [year + month + day - 268])


# The function that predicts the market share
def predict_market_share(date, market_share, x):
    # create models using each method we want
    # svr_lin = SVR(kernel='linear', C = 1e3)
    # svr_poly = SVR(kernel='poly', C=1e3, degree=2)
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    
    # train svr models using each model
    # svr_lin.fit(date, market_share)
    # svr_poly.fit(date, market_share)
    svr_rbf.fit(date, market_share)
    
    # create linear regression model
    lin_reg = LinearRegression()
    # train linear model
    lin_reg.fit(date, market_share)
    
    # In this part we plot the data
    plt.scatter(date, market_share, color='black', label='Data')
    # plt.plot(date, svr_lin.predict(date), color='red', label='SVR Linear')
    # plt.plot(date, svr_poly.predict(date), color='blue', label='SVR Poly')
    plt.plot(date, svr_rbf.predict(date), color='green', label='SVR RBF')
    plt.plot(date, lin_reg.predict(date), color='orange', label='Linear Reg')
    plt.xlabel('No. of Days')
    plt.ylabel('Market Share')
    plt.title('Regression')
    plt.legend()
    plt.show()
    
    # In case we want to use more svr methods
    # return svr_lin.predict(x), svr_poly.predict(x), svr_rbf.predict(x), lin_reg.predict(x)
    return svr_rbf.predict(x), lin_reg.predict(x)

predicted_market_share = predict_market_share(date, market_share, error_threshhold_date)
predicted_market_share = predict_market_share(date, market_share, test_date)
# print('actual market share: ', error_threshhold_market_share)
# print('svr_lin: ', predicted_market_share[0], ' - svr_poly: ', predicted_market_share[1],
#     ' - svr_rbf: ', predicted_market_share[2], ' - lin_reg: ', predicted_market_share[3] )

# print('error threshhold of svr_lin: ', abs(predicted_market_share[0] - error_threshhold_market_share) * 100 )
# print('error threshhold of svr_poly: ', abs(predicted_market_share[1] - error_threshhold_market_share) * 100)
# print('error threshhold of svr_rbf: ', abs(predicted_market_share[2] - error_threshhold_market_share) * 100)
# print('error threshhold of lin_reg: ', abs(predicted_market_share[3] - error_threshhold_market_share) * 100)

print('error threshhold of svr_rbf: ', abs(predicted_market_share[0] - error_threshhold_market_share)[0] * 100, '%')
print('error threshhold of lin_reg: ', abs(predicted_market_share[1] - error_threshhold_market_share)[0] * 100, '%')



print('svr_rbf: ', predicted_market_share[0], ' - lin_reg: ', predicted_market_share[1] )

