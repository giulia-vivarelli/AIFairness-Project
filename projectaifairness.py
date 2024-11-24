# -*- coding: utf-8 -*-
"""ProjectAIFairness.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CwXtnbqYwR5Yf4JyemxYHZobkOxsruSq
"""

!pip install tensorflow
!pip install keras
!pip install imbalanced-learn

"""###Imports"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

#models
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

from xgboost import XGBClassifier

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, Input
from tensorflow.keras.optimizers import Adam
from keras.regularizers import l2
from keras.layers import Dropout

#metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from scipy.stats import chi2_contingency

import shap

random_seed = 15

"""##Dataset Load"""

dataset_path = 'Dataset_2.0_Akkodis.xlsx'

df = pd.read_excel(dataset_path)

#column name
df.columns = df.columns.str.lstrip()
df.columns = df.columns.str.title()

original_df = df

df = original_df.drop_duplicates(subset='Id', keep='last')

df.head()

print("Number of removed duplicates:", original_df.shape[0]-df.shape[0])
print(f"There are {df.shape[0]} rows and {df.shape[1]} columns ")

#Function to get some info abt df
def get_data(dataframe):
  print("\BASIC INFORMATION\n")
  print(dataframe.info())
  print("="*100)
  print("\n")
  print("NULL values check")
  print(dataframe.isnull().sum())
  print("="*100)

# Drop non-useful columns - RESIDENCE
unuseful_columns = ['Id', 'Tag', 'Year Of Insertion', 'Year Of Recruitment', 'Recruitment Request',
                     'Assumption Headquarters', 'Event_Type__Val', 'Linked_Search__Key', 'Job Description',
                       'Candidate Profile', 'Akkodis Headquarters', 'Standing/Position', 'Last Role', 'Study Area.1', 'Years Experience.1']
df = df.drop(columns=unuseful_columns)

# Drop unuseful statuses
statuses_to_remove = ['First contact', 'Imported']
print(df['Candidate State'].unique())
df = df[~df['Candidate State'].isin(statuses_to_remove)] #rimuove tutte le righe che hanno i due stati da rimuovere
print(df['Candidate State'].unique())
df.shape

get_data(df)

# Visualize the new shape
print(f"There are {df.shape[0]} rows and {df.shape[1]} columns")

# Visualize the possible values
for feature in df.columns:
    print(f'Feature: {feature} -- {list(df[feature].unique())}')

"""#### NANs handle"""

columns_with_nan = df.columns[df.isnull().any()].tolist()
print(columns_with_nan)

df['Residence'] = df['Residence'].fillna('Not Specified')
df['Residence'] = df['Residence'].replace('', 'Not Specified')

df['Protected Category'] = df['Protected Category'].fillna('Not a protected category')
df['Protected Category'] = df['Protected Category'].replace('Article 18', 'Article 1')

df['Study Area'] = df['Study Area'].fillna('Not Specified')
df['Sector'] = df['Sector'].fillna('Unemployed')
df['Job Family Hiring'] = df['Job Family Hiring'].fillna('Not Specified')
df['Job Title Hiring'] = df['Job Title Hiring'].fillna('Not Specified')
df['Event_Feedback'] = df['Event_Feedback'].fillna('Not Specified')
df['Overall'] = df['Overall'].fillna('Not Specified')
df['Minimum Ral'] = df['Minimum Ral'].fillna('Not Specified')
df['Ral Maximum'] = df['Ral Maximum'].fillna('Not Specified')
df['Study Level'] = df['Study Level'].fillna('Not Specified')
df['Current Ral'] = df['Current Ral'].fillna('Not Specified')
df['Expected Ral'] = df['Expected Ral'].fillna('Not Specified')
df['Technical Skills'] = df['Technical Skills'].fillna(df['Technical Skills'].mean())
df['Comunication'] = df['Comunication'].fillna(df['Comunication'].mean())
df['Maturity'] = df['Maturity'].fillna(df['Maturity'].mean())
df['Dynamism'] = df['Dynamism'].fillna(df['Dynamism'].mean())
df['Mobility'] = df['Mobility'].fillna(df['Mobility'].mean())
df['English'] = df['English'].fillna(df['English'].mean())

# check
print(f'There are {df.isnull().sum().sum()} NANs')

df.head()

#get the state list
residence_list = df['Residence'].unique()
state_list = [s for s in residence_list if ('(STATE)' in s) or ('(OVERSEAS)' in s) or ('ETHIOPIA' in s) or ('SOUTH AFRICAN REPUBLIC' in s) or ('USSR' in s) or ('YUGOSLAVIA' in s)]
state_list = [s.split(' » ')[0] for s in [s.split(' ~ ')[0] for s in state_list]]
state_list = sorted(set(state_list))
print(state_list)

#get the italian regions list
italy_list = [s for s in residence_list if ('(STATE)' not in s) and ('(OVERSEAS)' not in s) and ('ETHIOPIA' not in s) and ('SOUTH AFRICAN REPUBLIC' not in s) and ('USSR' not in s) and ('YUGOSLAVIA' not in s)]
italy_list = [s.split(' ~ ')[-1] for s in italy_list]
italy_list = sorted(set(italy_list))
print(italy_list)

"""##MAPPING"""

special_mapping = {'Not Specified': 'Not Specified',
                   'Türkiye': 'TURKEY',
                   'USSR': 'RUSSIAN FEDERATION'
                   }
residence_mapping = {region: 'ITALY' for region in italy_list}
residence_mapping.update({state: state for state in state_list})
residence_mapping.update(special_mapping)

print(residence_mapping)

study_area_mapping = {
    'Automation/Mechatronics Engineering' : 'Engineering',
    'computer engineering' : 'Engineering',
    'chemical engineering' : 'Engineering',
    'Legal' : 'Law',
    'Mechanical engineering' : 'Engineering',
    'Telecommunications Engineering' : 'Engineering',
    'Economic - Statistics' : 'Economic',
    'Psychology' : 'Scientific Field',
    'Materials Science and Engineering' : 'Engineering',
    'Other scientific subjects' : 'Scientific Field',
    'Biomedical Engineering' : 'Engineering',
    'electronic Engineering' : 'Engineering',
    'Information Engineering' : 'Engineering',
    'Aeronautical/Aerospace/Astronautics Engineering' : 'Engineering',
    'Energy and Nuclear Engineering' : 'Engineering',
    'Informatics' : 'Informatics',
    'Management Engineering' : 'Engineering',
    'Automotive Engineering' : 'Engineering',
    'industrial engineering' : 'Engineering',
    'Other' : 'Other',
    'Surveyor' : 'NO COLLEGE',
    'Civil/Civil and Environmental Engineering' : 'Engineering',
    'Electrical Engineering' : 'Engineering',
    'Scientific maturity' : 'NO COLLEGE',
    'Chemist - Pharmaceutical' : 'Medical Field',
    'Political-Social' : 'Other Humanities Subjects',
    'Other humanities subjects' : 'Other Humanities Subjects',
    'Geo-Biological' : 'Scientific Field',
    'Linguistics' : 'Linguistics',
    'Agriculture and veterinary' : 'Scientific Field',
    'Literary' : 'Other Humanities Subjects',
    'Humanistic high school diploma' : 'NO COLLEGE',
    'Accounting' : 'NO COLLEGE',
    'Communication Sciences' : 'Other Humanities Subjects',
    'Safety Engineering' : 'Engineering',
    'Architecture' : 'Scientific Field',
    'Mathematics' : 'Scientific Field',
    'construction Engineering' : 'Engineering',
    'Petroleum Engineering' : 'Engineering',
    'Naval Engineering' : 'Engineering',
    'Artistic' : 'NO COLLEGE',
    'Not Specified' : 'Other',
    'Mathematical-physical modeling for engineering' : 'Engineering',
    'Engineering for the environment and the territory' : 'Engineering',
    'Medical' : 'Medical Field',
    'Defense and Security' : 'Other',
    'Physical education' : 'Other',
    'Statistics' : 'Scientific Field',
    'Educational/training sciences' : 'Other Humanities Subjects'

}

age_mapping = {
    '< 20 years': 'Young',
    '20 - 25 years': 'Young',
    '26 - 30 years': 'Young',
    '31 - 35 years': 'Young',
    '36 - 40 years': 'Senior',
    '40 - 45 years': 'Senior',
    '> 45 years': 'Senior'
}

def map_residence(value):
    if isinstance(value, str):
        for key, mapped_value in residence_mapping.items():
            if key in value:
                return mapped_value
    print(value)
    return 'Not Specified'

#Apply mappings to df
df['Residence'] = df['Residence'].apply(map_residence)
df['Study Area'] = df['Study Area'].replace(study_area_mapping)
df['Age Range'] = df['Age Range'].replace(age_mapping)

df.head()

european_countries = [
    'ALBANIA', 'AUSTRIA', 'BELARUS', 'BELGIUM', 'BULGARIA', 'CROATIA', 'CZECH REPUBLIC',
    'FRANCE', 'GERMANY', 'GREAT BRITAIN-NORTHERN IRELAND', 'GREECE', 'ITALY', 'LATVIA',
    'LITHUANIA', 'LUXEMBOURG', 'MALTA', 'MOLDOVA', 'MONACO', 'MONTENEGRO', 'NETHERLANDS',
    'NORWAY', 'POLAND', 'PORTUGAL', 'ROMANIA', 'RUSSIA', 'SAN MARINO', 'SERBIA', 'SLOVAKIA',
    'SLOVENIA', 'SPAIN', 'SWEDEN', 'SWITZERLAND', 'UKRAINE'
]

citizenship_mapping = {country: 'European' if country in european_countries else 'Non-European'
           for country in df['Residence'].unique()}

print(citizenship_mapping)

#add citizenship column
df['Citizenship'] = df['Residence'].map(citizenship_mapping)
df.head()

"""###Cathegorical columns encoding"""

categorical_columns = ['Age Range', 'Residence', 'Sex',
       'Protected Category', 'Study Area', 'Study Title',
       'Years Experience', 'Sector', 'Job Family Hiring',
       'Job Title Hiring', 'Overall',
       'Minimum Ral', 'Ral Maximum', 'Study Level',
       'Current Ral', 'Expected Ral', 'Citizenship']

encoding_mappings = {}  #dizionario per memorizzare mapping

for column in categorical_columns:
    encoder = LabelEncoder()  #un encoder per ogni colonna categorica
    df[f'{column}_encoded'] = encoder.fit_transform(df[column]) #applicazione encoding, un numero int unico per ogni valore. crea nuova colonna, versione encoded della colonna
    encoding_mappings[column] = dict(zip(encoder.classes_, encoder.transform(encoder.classes_))) #salvataggio del mapping

df = df.drop(columns=categorical_columns) #rimozione colonne categoriche

# Get a look at the new dataset
print(f"The new columns of the dataset are: {df.columns}")
df.head()

print(encoding_mappings)

"""###Target Column"""

df['STATUS'] = np.where(
    (df['Candidate State'] == 'Hired') |
    (df['Candidate State'] == 'Economic proposal') |
    (df['Event_Feedback'] == 'OK') |
    (df['Event_Feedback'] == 'OK (live)') |
    (df['Event_Feedback'] == 'OK (waiting for departure)') |
    (df['Event_Feedback'] == 'OK (hired)') |
    (df['Candidate State'] == 'QM'),
    1,
    0
) #crea nuova colonna STATUS

df = df.drop(columns=['Candidate State', 'Event_Feedback']) #rimozione colonne che non servono più

distribution = df['STATUS'].value_counts()  #Calcola distribuzione dei due valori

label_mapping = {0: 'Not Valid', 1: 'Valid'}

labels = [label_mapping[i] for i in distribution.index]

plt.figure(figsize=(4, 4))
plt.pie(
    distribution,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140)
plt.title(f'Distribution of the STATUS column') # 1 means the candidate is considered valid (even if still not hired), 0 the candidate is not considered valid for some reason
plt.show()

df.head()

"""###Data Visualization"""

numerical_columns=[s for s in df.columns if 'encoded' not in s]
numerical_columns.remove('STATUS')

for col in numerical_columns:
  plt.figure(figsize=(10, 6))
  sns.boxplot(x='STATUS', y=col, data=df, palette='Set3')
  plt.title(f'{col} Distribution by STATUS')
  plt.xlabel('STATUS')
  plt.ylabel(col)
  plt.xticks([0, 1], ['Not Hired (0)', 'Hired (1)'])
  plt.show()

"""####Citizenship"""

citizenship_enc_mapping = {v: k for k, v in encoding_mappings['Citizenship'].items()}  #calcola mapping inverso per la colonna Citizenship
distribution = df['Citizenship_encoded'].value_counts()
plt.figure(figsize=(10, 6))
plt.bar(distribution.index, distribution.values, color='skyblue')

# Replace the x-tick labels with the mapped values
plt.xticks(distribution.index, distribution.index.map(citizenship_enc_mapping), rotation=45)

plt.title('Distribution of Citizenship')
plt.xlabel('Citizenship')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

"""####Residence"""

residence_enc_mapping = {v: k for k, v in encoding_mappings['Residence'].items()}
italy_enc = encoding_mappings['Residence']['ITALY']

# 2 subsets
italy_df = df[df['Residence_encoded'] == italy_enc]
other_df = df[df['Residence_encoded'] != italy_enc]

italy_count = len(italy_df)
other_count = len(other_df)

# distribution for pie chart
distribution_torta = [italy_count, other_count]
labels_torta = ['ITALY', 'Other']

# 1st plot
plt.figure(figsize=(10, 6))
plt.pie(
    distribution_torta,
    labels=labels_torta,
    autopct='%1.1f%%',
    startangle=140,
    colors=['lightblue', 'salmon']
)
plt.title('Distribution of Residence (ITALY vs Other)')
plt.show()

# distribution for histogram
other_distribution = other_df['Residence_encoded'].value_counts()

plt.figure(figsize=(10, 6))
plt.bar(other_distribution.index, other_distribution.values, color='salmon')

plt.xticks(other_distribution.index, other_distribution.index.map(residence_enc_mapping), rotation=45, ha='right')

plt.title('Distribution of Residence (Other than ITALY)')
plt.xlabel('Residence')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

"""####Age"""

age_mapping = {v: k for k, v in encoding_mappings['Age Range'].items()}
distribution = df['Age Range_encoded'].value_counts()
plt.figure(figsize=(10, 6))
plt.bar(distribution.index, distribution.values, color='skyblue')

# Replace the x-tick labels with the mapped values
plt.xticks(distribution.index, distribution.index.map(age_mapping), rotation=45)

plt.title('Distribution of Age')
plt.xlabel('Age')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

"""####Gender"""

gender_mapping = {v: k for k, v in encoding_mappings['Sex'].items()}
distribution = df['Sex_encoded'].value_counts()
distribution.index = distribution.index.map(gender_mapping)

plt.figure(figsize=(4, 4))
plt.pie(distribution, labels=distribution.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of the Gender column')
plt.show()

"""####Protected Category"""

pc_mapping = {v: k for k, v in encoding_mappings['Protected Category'].items()}
distribution = df['Protected Category_encoded'].value_counts()
distribution.index = distribution.index.map(pc_mapping)

plt.figure(figsize=(4, 4))
plt.pie(distribution, labels=distribution.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of the Pr column')
plt.show()

"""####Correlation Matrix"""

corr_matrix = df.corr()
plt.figure(figsize=(16, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, linewidths=.5)
plt.show()

sensitive_features = ['Sex_encoded', 'Age Range_encoded', 'Citizenship_encoded', 'Residence_encoded', 'Protected Category_encoded']
for feature in sensitive_features:
    for i in range(len(list(df[feature].unique()))):
        total_elements = len(df[(df[feature] == i) & (df['STATUS'] == 1)]) #numero assunti
        total_age = len(df[df[feature] == i]) #totale
        percentage = (total_elements / total_age) * 100
        print(f"Percentage of elements where {feature} is {i} and STATUS is HIRED: {percentage:.2f}%")

"""##*Preprocessing*

##Algorithms
"""

sensitive_features.remove('Residence_encoded')

df = shuffle(df, random_state = random_seed)

X = df.drop(columns=['STATUS'])
y = df['STATUS']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_seed)

"""###SMOTE"""

smote = SMOTE(sampling_strategy='auto', random_state=random_seed)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

"""###Standardization & Normalization
Non sembrano necessarie in questo caso

###Reweighing
metrics are worse
"""

def reweight_trainset(X_train, y_train, sensitive_features, random_seed=None):
    if random_seed is not None:
      np.random.seed(random_seed)

    group_counts = X_train.groupby(sensitive_features).size()
    group_weights = 1 / group_counts
    group_weights = group_weights / group_weights.sum()

    sample_weights = X_train[sensitive_features].apply(tuple, axis=1).map(group_weights)
    sample_weights /= sample_weights.sum()

    reweighted_indices = np.random.choice(X_train.index, size = len(X_train), replace=True, p=sample_weights)
    X_train_reweighted = X_train.loc[reweighted_indices]
    y_train_reweighted = y_train.loc[reweighted_indices]

    return X_train_reweighted, y_train_reweighted

"""###Training"""

#X_train_final, y_train_final = reweight_trainset(X_train_resampled, y_train_resampled, sensitive_features, random_seed)
X_train_final = X_train_resampled
y_train_final = y_train_resampled

models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeClassifier(),
    'Naive Bayes': GaussianNB(),
    'XGBoost': XGBClassifier(random_state=random_seed),
    'KNN': KNeighborsClassifier(),
}

metrics = []
predictions = {}

for name, model in models.items():
  model.fit(X_train_final, y_train_final)
  y_pred = model.predict(X_test)

  if name in ['Linear Regression', 'XGBoost']:
    y_pred = (y_pred > 0.5).astype(int)

  predictions[name] = y_pred

  accuracy = round(accuracy_score(y_test, y_pred), 3)
  precision = round(precision_score(y_test, y_pred), 3)
  recall = round(recall_score(y_test, y_pred), 3)
  f1 = round(f1_score(y_test, y_pred),3)
  roc_auc = round(roc_auc_score(y_test, y_pred), 3)

  metrics.append({
      'Model': name,
      'Accuracy': accuracy,
      'Precision': precision,
      'Recall': recall,
      'F1-score': f1,
      'ROC AUC': roc_auc
  })

metrics = pd.DataFrame(metrics)
metrics.head()

predictions = pd.DataFrame(predictions)
predictions.head()

"""###Neural Networks"""

def create_model():
    model = Sequential()
    model.add(Input(shape=(X_train_final.shape[1],)))  # Layer di input

    # Primo layer con regolarizzazione L2
    model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.01)))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))  # Dropout con probabilità del 50%

    # Secondo layer con regolarizzazione L2
    model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.01)))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))  # Dropout con probabilità del 50%

    # Terzo layer con regolarizzazione L2
    model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.01)))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))  # Dropout con probabilità del 50%

    # Quarto layer con regolarizzazione L2
    model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.01)))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))  # Dropout con probabilità del 50%

    # Output layer
    model.add(Dense(1, activation='sigmoid'))

    # Compilazione del modello
    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
    return model

neural_models = []

for seed in range (85,92):
  np.random.seed(seed)
  tf.random.set_seed(seed)
  neural_models.append(create_model())

histories = []

for i, model in enumerate(neural_models):
  print(f"Fitting model {i+1}...")
  history = model.fit(X_train_final, y_train_final, epochs = 15, batch_size = 64, validation_split = 0.2)
  histories.append(history)
  print(f"Model {i+1} fitted.\n\n")

plt.plot(histories[0].history['accuracy'])
plt.plot(histories[0].history['val_accuracy'])
plt.title('Model 1 Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

plt.plot(histories[0].history['loss'])
plt.plot(histories[0].history['val_loss'])
plt.title('Model 1 Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

neural_predictions = []

for i, model in enumerate(neural_models):
  print(f"Predicting with model {i+1}...")
  y_pred = (model.predict(X_test) > 0.5).astype("int32")
  neural_predictions.append(y_pred)
  print(f"Predictions form model {i+1} stored.\n\n")

nn_metrics = []

for i, y_pred in enumerate(neural_predictions):
  accuracy = round(accuracy_score(y_test, y_pred), 3)
  precision = round(precision_score(y_test, y_pred), 3)
  recall = round(recall_score(y_test, y_pred), 3)
  f1 = round(f1_score(y_test, y_pred),3)
  roc_auc = round(roc_auc_score(y_test, y_pred), 3)

  nn_metrics.append({
      'Model': f"Neural Network {i+1}",
      'Accuracy': accuracy,
      'Precision': precision,
      'Recall': recall,
      'F1-score': f1,
      'ROC AUC': roc_auc
  })

nn_metrics = pd.DataFrame(nn_metrics)
nn_metrics

combined_metrics = pd.concat([metrics, nn_metrics], ignore_index=True)
combined_metrics

for i, model in enumerate(neural_models):
  models[f"Neural Network {i+1}"] = model

for i, prediction_list in enumerate(neural_predictions):
  predictions[f"Neural Network {i+1}"] = prediction_list.flatten()

"""#Fairness Metrics

##Demographic Parity
"""

non_sensitive_features = [feature for feature in df.columns if feature not in sensitive_features]

models_list = [model for model in models]

tolerance = 0.15
significance_level = 0.1

def calculate_demographic_parity(predictions, sensitive_attribute, name, significance_level, tolerance, activate_check=False):

    df = pd.DataFrame({
        'predictions': predictions,
        'sensitive_attribute': sensitive_attribute
    })

    # Proportion of positive predictions for each group
    positive_proportions = df.groupby('sensitive_attribute')['predictions'].mean()
    if positive_proportions.isna().any():
      print(f"Attenzione! Le seguenti categorie hanno valori NaN:\n{positive_proportions[positive_proportions.isna()]}")
    num_class = positive_proportions.shape[0]
    min_proportion = positive_proportions.min()
    max_proportion = positive_proportions.max()
    percentage_difference = (max_proportion - min_proportion)

    # Case for binary sensitive attribute
    if num_class == 2:

        if activate_check == True:
            print("===")
            print(name)
            print(positive_proportions)

        if percentage_difference <= tolerance:
            return 'T'
        else:
            return False

    # Case for multiclass sensitive attribute
    if num_class > 2:
        contingency_table = pd.crosstab(df['predictions'], df['sensitive_attribute'])
        chi2, p, dof, expected = chi2_contingency(contingency_table)

        if activate_check == True:
            print("===")
            print(name)
            print(positive_proportions)
            if (expected < 5).any():
                print(f"Sparse contigency for {name}")

        if p > significance_level:
            return 'T'
        else:
            return False

# Models behaviours over sensitive features
table = []

for model in models:
     temp = []
     for i in range(len(sensitive_features)):
        Boolean_Output = calculate_demographic_parity(predictions[model], X_test[sensitive_features[i]], sensitive_features[i], significance_level, tolerance, activate_check=True)
        temp.append(Boolean_Output)
     table.append(temp)

sf_df = pd.DataFrame(table, index = models_list, columns=sensitive_features)
sf_df.head(len(models_list))

"""##SHAP"""

def create_explanations(model, X, name):
  if name.startswith('Neural Network'):
    explainer = shap.GradientExplainer(model, X.values)
    shap_values = explainer.shap_values(X.values)[:1000].squeeze()
    return shap_values, X

  explainer = shap.Explainer(model, X)
  explanations = explainer(X)
  return explanations, X

def summaryPlot(model, X, lf, plot_type, plot_name):
    explanations, X = create_explanations(model, X, plot_name)

    fig, ax = plt.subplots()
    plt.title(f"{plot_name}")
    shap.summary_plot(explanations, X, lf, show=False, plot_size=None, plot_type=plot_type, max_display=len(lf), sort=True)
    plt.tight_layout()
    plt.show()
    plt.close()

tot_columns = list(X_test.columns)
summaryPlot(models[models_list[0]], X_test, tot_columns, plot_type='violin', plot_name='Linear Regression')
summaryPlot(models[models_list[3]], X_test, tot_columns, plot_type='violin', plot_name='XGBoost')

for i in range (5, 12):
  summaryPlot(models[models_list[i]], X_test, tot_columns, plot_type='violin', plot_name=models_list[i])

!python --version

