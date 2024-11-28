from sklearn.neighbors import KNeighborsRegressor
import pandas as pd


def mean_error(predictions, values, n):
    diffs = []
    diffs_sqr = []
    for i in range(len(predictions)):
        diffs.append(abs(predictions[i] - values[i]))
        diffs_sqr.append(abs(predictions[i] - values[i]) ** 2)
    print "Mean Error: {} votes".format(sum(diffs) / n)
    print "Mean Squared Error: {} votes^2".format(sum(diffs_sqr) / n)


def knn(num):
    NEIGHBORS = num
    FHEADERS = ['Accepted_Annotations', 'Annotation_Count', 'Comment_Count', 'Followers', 'Length_Referent_Text', 'Number_Contributors', 'Number_Verified_Annotations', 'Page_Views', 'Pyong_Count', 'Release_Date']
    VHEADERS = ['Total_Votes']

    # Training
    #############################################
    vdata = pd.read_csv("./DataSets/train.csv", usecols=VHEADERS)
    numrows = len(list(vdata["Total_Votes"]))
    values = []
    for i in range(numrows):
        values.append(list(vdata.loc[i]))

    fdata = pd.read_csv("./DataSets/train_num_only.csv", usecols=FHEADERS)
    features = []
    for i in range(numrows):
        features.append(list(fdata.loc[i]))

    neigh = KNeighborsRegressor(n_neighbors=NEIGHBORS)
    neigh.fit(features, values)

    # Testing
    #############################################
    tvdata = pd.read_csv("./DataSets/test_clean.csv", usecols=VHEADERS)
    numtests = len(list(tvdata["Total_Votes"]))
    real_values = []
    for i in range(numtests):
        real_values.append(list(tvdata.loc[i])[0])

    tfdata = pd.read_csv("./DataSets/test_clean.csv", usecols=FHEADERS)
    test_features = []
    for i in range(numtests):
        test_features.append(list(tfdata.loc[i]))

    # Get Error
    #############################################
    test_guesses = []
    for i in range(numtests):
        test_guesses.append(neigh.predict([test_features[i]]).tolist()[0][0])

    mean_error(test_guesses, real_values, numtests)


if __name__ == '__main__':
    for j in range(1,6):
        print "{}NN: ".format(j)
        knn(j)
        print "\n"
