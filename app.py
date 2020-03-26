import csv
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# The number of movies to predict for test.csv
limit = 10

# A dictionary which contains name of the show, date and market share
data_dict = {}
# Open the .csv file with csv imported above
with open('data.csv') as data:
    # reading the file as a list
    data_csv = list(csv.reader(data))
    # Removing the first element because it has the titles  and no data
    data_csv = data_csv[1:]
    
    # We go through the file line by line
    for row in data_csv:

        # for x axis we convert the date to a number
        # the number starts from 29/08/2016 and from number 1
        year = (int(row[6].split('-')[0]) - 2016) * 365
        month = (int(row[6].split('-')[1])) * 30
        day = int(row[6].split('-')[2])
        
        # Filling the data dictionary, which has the name of the show as key 
        # and for its values, a list of date and market share
        data_dict.setdefault(row[11],{'date':[],'market share': []})['date'].append([year + month + day - 268])
        data_dict.setdefault(row[11],{'date':[],'market share': []})['market share'].append(float(row[18]))

# getting the last element of the first show in ordeer to get the error threshhold
error_threshhold_date = list(data_dict.values())[0]['date'][-1]
# print(error_threshhold_date)
error_threshhold_market_share = list(data_dict.values())[0]['market share'][-1]
# print(error_threshhold_market_share)

# A dictionary for the test file 
# which has name of the show, date and predicted market share (which is what we want)
test_dict = {}
with open('test.csv') as test:
    # same as above
    test_csv = list(csv.reader(test))
    test_csv = test_csv[1:]
    for row in test_csv:
        year = (int(row[6].split('-')[0]) - 2016) * 365
        month = (int(row[6].split('-')[1])) * 30
        day = int(row[6].split('-')[2])
        test_dict.setdefault(row[11],{'date':[],'predicted market share': {}})['date'].append([year + month + day - 268])

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
    # plt.scatter(date, market_share, color='black', label='Data')
    # # plt.plot(date, svr_lin.predict(date), color='red', label='SVR Linear')
    # # plt.plot(date, svr_poly.predict(date), color='blue', label='SVR Poly')
    # plt.plot(date, svr_rbf.predict(date), color='green', label='SVR RBF')
    # plt.plot(date, lin_reg.predict(date), color='orange', label='Linear Reg')
    # plt.xlabel('No. of Days')
    # plt.ylabel('Market Share')
    # plt.title('Regression')
    # plt.legend()
    # plt.show()
    
    # In case we want to use more svr methods
    # return svr_lin.predict(x), svr_poly.predict(x), svr_rbf.predict(x), lin_reg.predict(x)
    return svr_rbf.predict(x), lin_reg.predict(x)

predicted_market_share = predict_market_share(data_dict[list(data_dict.keys())[0]]['date'], data_dict[list(data_dict.keys())[0]]['market share'], [error_threshhold_date])
print('error threshhold of svr_rbf: ', abs(predicted_market_share[0][0] - error_threshhold_market_share) / error_threshhold_market_share * 100, '%')
print('error threshhold of lin_reg: ', abs(predicted_market_share[1][0] - error_threshhold_market_share) / error_threshhold_market_share * 100, '%')


# As the file is huge, we can limit the number of data 
# so we can finish it faster
i = 0
# We go through the test_dict and run the function for each show
for show, val in test_dict.items():
    
    # These two files were among the hugest, so they were removed from prediction
    # although they can be calculated if the if statement is removed
    # if the if statement is removed, do not forget to correct the indentation
    if show != 'Complأ©ment de programme canadien'\
        and show != 'Complأ©ment de programme':
        # variable that contains a two element list of the svr_rbf and lin_reg predictions
        predicted_market_share = predict_market_share(data_dict[show]['date'], data_dict[show]['market share'], val['date'])
        val['predicted market share']['svr_rbf'] = predicted_market_share[0]
        val['predicted market share']['lin_reg'] = predicted_market_share[1]
        # in order to reduce the volume of the file 
        # and increase the compilation time
        i += 1
        if i >= limit:
            break

j = 0
# writing to a csv file using csv  write imported above
with open('results.csv', 'w') as result:
    csv_writer = csv.writer(result)
    # The headers of the csv file
    headers = ['Name of show', 'date', 'svr_rbf', 'lin_reg']
    csv_writer.writerow(headers)
    for show in test_dict:
        res_rbf = test_dict[show]['predicted market share']['svr_rbf']
        res_lin_reg = test_dict[show]['predicted market share']['lin_reg']
        for index in range(len(res_rbf)):
            res_date = test_dict[show]['date'][index][0] + 268
            res_year = str(res_date // 365 + 2016)
            res_month = str((res_date % 365) // 30)
            if len(res_month) < 1:
                month = '0' + month
            res_day = str((res_date % 365) % 30)
            print_date = res_year + '/' + res_month + '/' + res_day
            csv_writer.writerow([show, print_date, res_rbf[index], res_lin_reg[index]])

        j += 1
        if j >= limit:
            break

