{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from sklearn import metrics\n",
    "from sklearn.naive_bayes import GaussianNB\n",
    "from sklearn.neighbors import KNeighborsClassifier\n",
    "df = pd.read_csv(\"10_25_data/training_data_10_25.csv\",dtype={'Zipcode':'str'})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "feature_names = [\"Zipcode\", \"ID\", \"Source\", \"TMC\", \"Start_Time\", \"End_Time\",\n",
    "\"Start_Lat\", \"Start_Lng\", \"Distance(mi)\", \"Description\", \"Street\",\n",
    "\"Side\", \"City\", \"County\", \"State\", \"Zipcode\", \"Country\", \"Timezone\",\n",
    "\"Airport_Code\", \"Weather_Timestamp\", \"Temperature(F)\", \"Wind_Chill(F)\",\n",
    "\"Humidity(%)\", \"Pressure(in)\", \"Visibility(mi)\", \"Wind_Direction\",\n",
    "\"Wind_Speed(mph)\", \"Precipitation(in)\", \"Weather_Condition\", \"Amenity\",\n",
    "\"Bump\", \"Crossing\", \"Give_Way\", \"Junction\", \"No_Exit\", \"Railway\",\n",
    "\"Roundabout\", \"Station\", \"Stop\", \"Traffic_Calming\", \"Traffic_Signal\",\n",
    "\"Turning_Loop\", \"Sunrise_Sunset\", \"Civil_Twilight\", \"Nautical_Twilight\",\n",
    "\"Astronomical_Twilight\", \"A00100\", \"A00700\", \"minimum_age\", \"maximum_age\",\n",
    "\"gender\"]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "x_train = []\n",
    "y_train = []"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "x_train = df.drop(columns=[\"Severity\"])\n",
    "y_train = df.drop(columns=feature_names)\n",
    "y_train = y_train.loc[:, ~y_train.columns.str.contains('^Unnamed')]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',\n",
       "                     metric_params=None, n_jobs=None, n_neighbors=5, p=2,\n",
       "                     weights='uniform')"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "from sklearn import preprocessing\n",
    "\n",
    "le = preprocessing.LabelEncoder()\n",
    "en = preprocessing.OneHotEncoder()\n",
    "\n",
    "x_train = x_train.reset_index()\n",
    "y_train = y_train.reset_index()\n",
    "x_train = x_train.apply(le.fit_transform)\n",
    "\n",
    "''' classifying a crash of 3 or 4 as severe and 1 or 2 as not severe '''\n",
    "def classify(num):\n",
    "    if num == 1 or num == 2:\n",
    "        return 0\n",
    "    else:\n",
    "        return 1\n",
    "    \n",
    "y_train = y_train[\"Severity\"].map(classify)\n",
    "\n",
    "clf = KNeighborsClassifier() # n_neighbors=5\n",
    "clf.fit(x_train, y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_csv(\"10_25_data/testing_data_10_25.csv\",dtype={'Zipcode':'str'})\n",
    "x_test = []\n",
    "y_test = []\n",
    "\n",
    "df = df.loc[:, ~df.columns.str.contains('^Unnamed')]\n",
    "df = df.dropna()\n",
    "\n",
    "x_test = df.drop(columns=[\"Severity\"])\n",
    "y_test = df.drop(columns=feature_names)\n",
    "y_test = y_test.loc[:, ~y_test.columns.str.contains('^Unnamed')]\n",
    "\n",
    "le = preprocessing.LabelEncoder()\n",
    "en = preprocessing.OneHotEncoder()\n",
    "\n",
    "x_test = x_test.reset_index()\n",
    "y_test = y_test.reset_index()\n",
    "x_test = x_test.apply(le.fit_transform)\n",
    "\n",
    "def classify(num):\n",
    "    if num == 1 or num == 2:\n",
    "        return 0\n",
    "    else:\n",
    "        return 1\n",
    "\n",
    "y_test = y_test[\"Severity\"].map(classify)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy: 0.6954592515900014\n",
      "Precision: 0.29712041884816753\n",
      "Recall: 0.011193293885601578\n",
      "F1: 0.02157384527656339\n"
     ]
    }
   ],
   "source": [
    "y_pred = clf.predict(x_test)\n",
    "print(\"Accuracy:\", metrics.accuracy_score(y_test, y_pred))\n",
    "print(\"Precision:\", metrics.precision_score(y_test, y_pred))\n",
    "print(\"Recall:\", metrics.recall_score(y_test, y_pred))\n",
    "print(\"F1:\", metrics.f1_score(y_test, y_pred))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Confusion matrix:\n",
      "TN: 46793\n",
      "FP: 537\n",
      "FN: 20053\n",
      "TP: 227\n"
     ]
    }
   ],
   "source": [
    "cm = metrics.confusion_matrix(y_test, y_pred)\n",
    "print(\"Confusion matrix:\")\n",
    "print(f\"TN: {cm[0][0]}\")\n",
    "print(f\"FP: {cm[0][1]}\")\n",
    "print(f\"FN: {cm[1][0]}\")\n",
    "print(f\"TP: {cm[1][1]}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
