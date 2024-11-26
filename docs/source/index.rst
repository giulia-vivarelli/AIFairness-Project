Dataset Analysis for AKKODIS
============================

Overview
--------

The Akkodis Dataset consists of 40 columns and 21,277 entries. Each
candidate is identified by its ``ID`` and can appear in more than one
row, each one specific for an ``Event_type__val``.

Dataset Description
-------------------

Features
~~~~~~~~

- **ID**: unique identifier for the candidate
- **Candidate State**: status of the candidate’s application

  - ``Hired``: the candidate has been selected
  - ``Vivier``: the candidate will be taken in consideration for future
    opportunities
  - ``QM``: *Qualification Meeting* ??
  - ``In selection``: selection phase
  - ``First contact``: the candidate has been contacted from the company
    for the first time
  - ``Economic proposal``: the company has made a proposal to the
    candidate
  - ``Imported``: the candidate has been transfered from another DB ??

- **Age Range**: range of age for the candidate

  - ``< 20`` years
  - ``20 - 25`` years
  - ``26 - 30`` years
  - ``31 - 35`` years
  - ``36 - 40`` years
  - ``40 - 45`` years
  - ``> 45`` years

- **Residence**: current place of residence for the candidate
- **Sex**: gender identification (``Male|Female``)
- **Protected Category**: indicates if the candidate falls into a
  protected category

  - ``Article 1``
  - ``Article 18``
  - Not Specified

- **TAG**: keywords used by recruiter
- **Study Area**: Field of study or academic discipline
- **Study Title**: Academic degree or title obtained

  - ``Five-year degree``
  - ``Doctorate``
  - ``High school graduation``
  - ``Three-year degree``
  - ``master's degree``
  - ``Professional qualification``
  - ``Middle school diploma``

- **Years Experience**: number of years of professional experience

  - ``0``
  - ``0-1``
  - ``1-3``
  - ``3-5``
  - ``5-7``
  - ``7-10``
  - ``+10``

- **Sector**: industry or sector in which the candidate has experience
- **Last Role**: candidate’s most recent job role
- **Year of Insertion**: year when the candidate’s information was
  entered into the portal
- **Year of Recruitment**: year in which the candidate was hired
- **Recruitment Request**: represents the application request for a
  candidacy
- **Assumption Headquarters**: headquarters location associated with the
  hiring assumption
- **Job Family Hiring**: Job family or category for the hiring position
- **Job Title Hiring**: specific job title for the hiring position
- \**Event_type\__val*\*: It specifies the stage of the recruitment
  process for the candidate
- **Event_feedback**: feedback received from an event (``OK|KO``)
- **Linked_search_key**: keys indicate the number of searches conducted
  for a job position
- **Overall**: overall assessment, interview score

  - ``1 - Low`` or ``~ 1 - Low``
  - ``2 - Medium`` or ``~ 2 - Medium``
  - ``3 - High`` or ``~ 3 - High``
  - ``4 - Top`` or ``~ 4 - Top``

- **Job Description**: description of the job role
- **Candidate Profile**: ideal profile information for the candidate,
  requested by the company
- **Years Experience.1**: additional field for specifying years of
  experience requested
- **Minimum Ral** (Gross Annual Salary): minimum expected gross annual
  salary
- **Ral Maximum**: maximum expected gross annual salary
- **Study Level**: level of study requested for the job position, the
  values are equivalent to ``Study Title``
- **Study Area.1**: additional field for specifying the academic field
  of study requested
- **Akkodis headquarters**: headquarters location for Akkodis
- **Current Ral**: current or existing salary
- **Expected Ral**: expected salary
- **Technical Skills**: skills related to technical or specialized
  expertise from 1 to 4
- **Standing/Position**: standing or position within the organization
  from 1 to 4
- **Comunication**: communication skills from 1 to 4
- **Maturity**: level of maturity from 1 to 4
- **Dynamism**: level of Dynamism from 1 to 4
- **Mobility**: mobility from 1 to 4
- **English**: proficiency in the English language from 1 to 4

Possible Target Variables
~~~~~~~~~~~~~~~~~~~~~~~~~

Some possible target variables in this dataset could be: \*
**Suitability**: a new column that defines if a candidate is suitable
for the position, based on the information provided. \* **Possible
RAL**: a new column that predicts the adequate RAL for the candidate
profile.

.. code:: python

    #imports
    import pandas as pd
    from collections import Counter
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.preprocessing import LabelEncoder

.. code:: python

    dataset_path = 'Dataset_2.0_Akkodis.xlsx'
    
    df = pd.read_excel(dataset_path)

.. code:: python

    df.columns = df.columns.str.lstrip()
    df.columns = df.columns.str.title()

However the dataset contains very few samples with RAL values specified:

.. code:: python

    for col in df.columns:
      if 'Ral' in col:
        ral_null = df[col].isna().sum() / df.shape[0] * 100
        print(f'{ral_null:.2f}% of samples have no {col} specified')


.. parsed-literal::

    94.53% of samples have no Minimum Ral specified
    92.85% of samples have no Ral Maximum specified
    80.56% of samples have no Current Ral specified
    80.73% of samples have no Expected Ral specified


The **suitability** of a candidate could be obtained through
``Candidate State`` and ``Event_Feedback``. However the 2 columns don’t
seem to be always consistent as we can find samples with both ``Hired``
as *Candidate State* and ``KO`` as *Event_feedback*:

.. code:: python

    filtered_df = df[df['Event_Feedback'].str.contains('KO', na=False)]
    unique_values = filtered_df['Candidate State'].unique()
    
    print(df[df['Event_Feedback'].str.contains('KO', na=False)][['Candidate State', 'Event_Type__Val', 'Event_Feedback']])


.. parsed-literal::

             Candidate State        Event_Type__Val              Event_Feedback
    13                    QM  Qualification Meeting       KO (technical skills)
    87                 Hired    Technical interview     KO (opportunity closed)
    112                Hired    Technical interview  KO (proposed renunciation)
    122    Economic proposal      Economic proposal  KO (proposed renunciation)
    141         In selection           BM interview                KO (manager)
    ...                  ...                    ...                         ...
    21281       In selection           HR interview       KO (technical skills)
    21300  Economic proposal      Economic proposal  KO (proposed renunciation)
    21315       In selection           HR interview                KO (manager)
    21316       In selection           BM interview                KO (manager)
    21336       In selection           HR interview                KO (retired)
    
    [854 rows x 3 columns]


##Data Cleaning ###Duplicates

Each candidate has more than one row in the dataset, one for each
``Event_type__val``. We need to select the most recent one and remove
the other ones to guarantee consistency. We could assume the last row
for each ``ID`` to be the most recent one.

.. code:: python

    df_nodup = df.drop_duplicates(subset='Id', keep='last')

This however reduces drastically the number of samples in the dataset,
from 21 377 to 12 263 rows, removing the 43% of the whole dataset.

.. code:: python

    print(f"{100 - df_nodup.shape[0]/df.shape[0]*100:.2f}% of the dataset were duplicates")


.. parsed-literal::

    42.63% of the dataset were duplicates


Unuseful Columns
~~~~~~~~~~~~~~~~

Some columns might be unuseful such as ``ID``, ``Year Of Insertion``,
``Linked_Search__Key`` …

.. code:: python

    columns_to_drop = ['Id', 'Last Role', 'Year Of Insertion',
                       'Assumption Headquarters', 'Linked_Search__Key',
                       'Akkodis Headquarters']

Some features are often not specified so filling with *default values*
might not be the right choice. A **threshold** could be set to select
the columns to drop. For example features specified in less than 40% of
the samples could be considered unuseful.

.. code:: python

    for col in df.columns:
      null_count = df[col].isna().sum() / df.shape[0]
      print(f'<{col}> null count: {null_count*100:.2f}%')
      if null_count > 0.6 and col != 'Event_Feedback' and col != 'Protected Category':
        columns_to_drop.append(col)


.. parsed-literal::

    <Id> null count: 0.00%
    <Candidate State> null count: 0.00%
    <Age Range> null count: 0.00%
    <Residence> null count: 0.01%
    <Sex> null count: 0.00%
    <Protected Category> null count: 99.60%
    <Tag> null count: 50.19%
    <Study Area> null count: 0.21%
    <Study Title> null count: 0.00%
    <Years Experience> null count: 0.00%
    <Sector> null count: 42.86%
    <Last Role> null count: 42.86%
    <Year Of Insertion> null count: 0.00%
    <Year Of Recruitment> null count: 88.82%
    <Recruitment Request> null count: 90.20%
    <Assumption Headquarters> null count: 88.86%
    <Job Family Hiring> null count: 88.86%
    <Job Title Hiring> null count: 88.86%
    <Event_Type__Val> null count: 7.44%
    <Event_Feedback> null count: 72.65%
    <Linked_Search__Key> null count: 70.41%
    <Overall> null count: 72.01%
    <Job Description> null count: 90.09%
    <Candidate Profile> null count: 90.22%
    <Years Experience.1> null count: 90.08%
    <Minimum Ral> null count: 94.53%
    <Ral Maximum> null count: 92.85%
    <Study Level> null count: 90.08%
    <Study Area.1> null count: 90.08%
    <Akkodis Headquarters> null count: 90.08%
    <Current Ral> null count: 80.56%
    <Expected Ral> null count: 80.73%
    <Technical Skills> null count: 72.14%
    <Standing/Position> null count: 72.05%
    <Comunication> null count: 72.08%
    <Maturity> null count: 72.10%
    <Dynamism> null count: 72.10%
    <Mobility> null count: 72.05%
    <English> null count: 72.19%


.. code:: python

    df = df_nodup.drop(columns=columns_to_drop)

.. code:: python

    print(f'The remaining columns are:\n')
    print(df.columns)


.. parsed-literal::

    The remaining columns are:
    
    Index(['Candidate State', 'Age Range', 'Residence', 'Sex',
           'Protected Category', 'Tag', 'Study Area', 'Study Title',
           'Years Experience', 'Sector', 'Event_Type__Val', 'Event_Feedback'],
          dtype='object')


NaNs Handling
~~~~~~~~~~~~~

There are still many columns left with no values specified.

.. code:: python

    print(f'Columns that contain NaN values:\n {df.columns[df.isnull().any()].tolist()}')


.. parsed-literal::

    Columns that contain NaN values:
     ['Residence', 'Protected Category', 'Tag', 'Study Area', 'Sector', 'Event_Type__Val', 'Event_Feedback']


In order to define *default values* we need to analyze each feature:

.. code:: python

    for col in df.columns[df.isnull().any()].tolist():
      print(f'{col} values: {df[col].unique()} \n')


.. parsed-literal::

    Residence values: ['TURIN » Turin ~ Piedmont' 'CONVERSANO » Bari ~ Puglia'
     'CASERTA » Caserta ~ Campania' ...
     'SAN FELICE A CANCELLO » Caserta ~ Campania'
     'PERDIFUMO » Salerno ~ Campania'
     'PALMANOVA » Udine ~ Friuli Venezia Giulia'] 
    
    Protected Category values: [nan 'Article 1' 'Article 18'] 
    
    Tag values: ['AUTOSAR, CAN, C, C++, MATLAB/SIMULINK, VECTOR/VENUS, VHDL, FPGA'
     '-, C, C++, DO178, LABVIEW, SOFTWARE DEVELOPMENT' 'PROCESS ENG.' ...
     '-, SOLIDWORKS, NX, CREO, INENTOR, GT POWER, AMESIM' 'SQL, UNIX'
     '-, ENVIRONMENTAL QUALITY, ENVIRONMENTAL MANAGER, ENVIRONMENTAL PROJECT ENGINEER, ISO 14001, ENVIRONMENTAL MANAGEMENT , ISO 14001, ENVIRONMENTAL MANAGEMENT, OFFSHORE'] 
    
    Study Area values: ['Automation/Mechatronics Engineering' 'computer engineering'
     'chemical engineering' 'Legal' 'Mechanical engineering'
     'Telecommunications Engineering' 'Economic - Statistics'
     'Materials Science and Engineering' 'Other scientific subjects'
     'Biomedical Engineering' 'electronic Engineering'
     'Information Engineering'
     'Aeronautical/Aerospace/Astronautics Engineering'
     'Energy and Nuclear Engineering' 'Informatics' 'Management Engineering'
     'Automotive Engineering' 'industrial engineering' 'Other' 'Surveyor'
     'Electrical Engineering' 'Scientific maturity' 'Chemist - Pharmaceutical'
     'Political-Social' 'Other humanities subjects' 'Geo-Biological'
     'Civil/Civil and Environmental Engineering' 'Psychology' 'Linguistics'
     'Agriculture and veterinary' 'Literary' 'Humanistic high school diploma'
     'Accounting' 'Communication Sciences' 'Safety Engineering' 'Architecture'
     'Mathematics' 'construction Engineering' 'Petroleum Engineering'
     'Naval Engineering' 'Artistic' nan
     'Mathematical-physical modeling for engineering'
     'Engineering for the environment and the territory' 'Medical'
     'Defense and Security' 'Physical education' 'Statistics'] 
    
    Sector values: ['Automotive' 'Aeronautics' 'Consulting' 'Telecom' 'Others' 'Space'
     'Life sciences' nan 'Railway' 'Defence' 'Naval'
     'Services and Information Systems' 'Energy' 'Machining - Heavy Industry'
     'Oil and Gas'] 
    
    Event_Type__Val values: ['BM interview' 'Candidate notification' 'Qualification Meeting'
     'Technical interview' 'HR interview' 'CV request' 'Contact note'
     'Inadequate CV' 'Economic proposal' 'Research association'
     'Sending SC to customer' nan 'Commercial note'] 
    
    Event_Feedback values: ['OK' nan 'KO (technical skills)' 'OK (waiting for departure)'
     'KO (proposed renunciation)' 'OK (live)' 'KO (mobility)' 'KO (manager)'
     'KO (retired)' 'OK (hired)' 'KO (seniority)' 'KO (ral)'
     'OK (other candidate)' 'KO (opportunity closed)' 'KO (lost availability)'
     'KO (language skills)'] 
    


Some default values could be:

.. code:: python

    df['Residence'] = df['Residence'].fillna('Not Specified')
    
    df['Protected Category'] = df['Protected Category'].fillna('No')
    
    df['Tag'] = df['Tag'].fillna('Not Specified')
    
    df['Study Area'] = df['Study Area'].fillna('Not Specified')
    
    df['Sector'] = df['Sector'].fillna('Not Specified')
    
    df['Event_Type__Val'] = df['Event_Type__Val'].fillna('Not Specified')
    
    df['Event_Feedback'] = df['Event_Feedback'].fillna('Not Specified')

Feature Mapping
~~~~~~~~~~~~~~~

Feature mapping can be used to simplify the values in the dataset.

Let’s analyze each feature:

**Candidate State**
^^^^^^^^^^^^^^^^^^^

.. code:: python

    candidate_state_counts = df['Candidate State'].value_counts()
    candidate_state_df = pd.DataFrame(candidate_state_counts.items(), columns=['Candidate State', 'Count'])
    candidate_state_df.plot(x='Candidate State', y='Count', kind='bar', legend=False)
    plt.title('Candidate State Counts')
    plt.ylabel('Frequency')




.. parsed-literal::

    Text(0, 0.5, 'Frequency')




.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_26_1.png


**Age Range**
^^^^^^^^^^^^^

.. code:: python

    custom_order = ['< 20 years', '20 - 25 years', '26 - 30 years',
                    '31 - 35 years', '36 - 40 years', '40 - 45 years', '> 45 years']
    df['Age Range'] = pd.Categorical(df['Age Range'], categories=custom_order, ordered=True)

.. code:: python

    age_range_counts = Counter(df['Age Range'].sort_values())
    age_range_df = pd.DataFrame(age_range_counts.items(), columns=['Age Range', 'Count'])
    age_range_df.plot(x='Age Range', y='Count', kind='bar', legend=False)
    plt.title('Age Range Counts')
    plt.ylabel('Frequency')




.. parsed-literal::

    Text(0, 0.5, 'Frequency')




.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_29_1.png


**Residence**
^^^^^^^^^^^^^

Mapping can be used to simplify this feature.

.. code:: python

    print(df['Residence'].unique())


.. parsed-literal::

    ['TURIN » Turin ~ Piedmont' 'CONVERSANO » Bari ~ Puglia'
     'CASERTA » Caserta ~ Campania' ...
     'SAN FELICE A CANCELLO » Caserta ~ Campania'
     'PERDIFUMO » Salerno ~ Campania'
     'PALMANOVA » Udine ~ Friuli Venezia Giulia']


.. code:: python

    residence_list = df['Residence'].unique()
    state_list = [s for s in residence_list if ('(STATE)' in s) or ('(OVERSEAS)' in s) or ('ETHIOPIA' in s) or ('SOUTH AFRICAN REPUBLIC' in s) or ('USSR' in s) or ('YUGOSLAVIA' in s)]
    state_list = [s.split(' » ')[0] for s in [s.split(' ~ ')[0] for s in state_list]]
    state_list = sorted(set(state_list))
    print(f"List of residence states of the candidates in the dataset:\n {state_list}")



.. parsed-literal::

    List of residence states of the candidates in the dataset:
     ['ALBANIA', 'ALGERIA', 'AUSTRIA', 'BELARUS', 'BELGIUM', 'BRAZIL', 'BULGARIA', 'CHILE', "CHINA PEOPLE'S REPUBLIC", 'COLOMBIA', 'CROATIA', 'CZECH REPUBLIC', 'EGYPT', 'ERITREA', 'FRANCE', 'GERMANY', 'GREAT BRITAIN-NORTHERN IRELAND', 'GREECE', 'GRENADA', 'HAITI', 'INDIA', 'INDONESIA', 'IRAN', 'ITALY', 'KUWAIT', 'LEBANON', 'LIBYA', 'LITHUANIA', 'MALAYSIA', 'MALTA', 'MEXICO', 'MONACO', 'MOROCCO', 'NETHERLANDS', 'NIGERIA', 'OMAN', 'PAKISTAN', 'PHILIPPINES', 'PORTUGAL', 'QATAR', 'REPUBLIC OF POLAND', 'ROMANIA', 'RUSSIAN FEDERATION', 'SAINT LUCIA', 'SAINT PIERRE ET MIQUELON (ISLANDS)', 'SAN MARINO', 'SERBIA AND MONTENEGRO', 'SINGAPORE', 'SLOVAKIA', 'SOUTH AFRICAN REPUBLIC', 'SPAIN', 'SRI LANKA', 'SWEDEN', 'SWITZERLAND', 'SYRIA', 'TONGA', 'TUNISIA', 'Türkiye', 'UKRAINE', 'UNITED ARAB EMIRATES', 'UNITED STATES OF AMERICA', 'USSR', 'UZBEKISTAN', 'VENEZUELA', 'YUGOSLAVIA']


.. code:: python

    italy_list = [s for s in residence_list if ('(STATE)' not in s) and ('(OVERSEAS)' not in s) and ('ETHIOPIA' not in s) and ('SOUTH AFRICAN REPUBLIC' not in s) and ('USSR' not in s) and ('YUGOSLAVIA' not in s)]
    italy_list = [s.split(' ~ ')[-1] for s in italy_list]
    italy_list = sorted(set(italy_list))
    print(f"List of residence italian regions of the candidates in the dataset:\n {italy_list}")


.. parsed-literal::

    List of residence italian regions of the candidates in the dataset:
     ['Abruzzo', 'Aosta Valley', 'Basilicata', 'Calabria', 'Campania', 'Emilia Romagna', 'Friuli Venezia Giulia', 'Lazio', 'Liguria', 'Lombardy', 'Marche', 'Molise', 'Not Specified', 'Piedmont', 'Puglia', 'Sardinia', 'Sicily', 'Trentino Alto Adige', 'Tuscany', 'Umbria', 'Veneto']


.. code:: python

    def map_residence(value):
        for region in italy_list:
            if region in value:
              return region
        for state in state_list:
            if state in value:
              return state
        return 'Not Specified'


The values in the ``Residence`` column could be replaced with either the
*italian region* or the *state*.

.. code:: python

    df['Residence'] = df['Residence'].apply(map_residence)
    df['Residence'] = df['Residence'].replace('Türkiye', 'TURKEY')
    df['Residence'] = df['Residence'].replace('USSR', 'RUSSIAN FEDERATION')

To better define *residence* 3 new columns could be added:
``Residence State``, ``Residence Italian Region``,
``European Residence``. This kind of information needs to be protected
but should also be taken in consideration in order to ensure *Fairness*.

.. code:: python

    df['Residence State'] = df['Residence'].apply(lambda x: x if x in state_list else 'ITALY')

.. code:: python

    distrib_it = [len(df[df['Residence State'] == 'ITALY']),
                    df.shape[0]-len(df[df['Residence State'] == 'ITALY'])]
    labels = ['Italian Residence', 'Non-Italian Residence']
    plt.pie(distrib_it, labels=labels, autopct='%1.1f%%')
    plt.title('Italian vs Non-Italian Residence Distribution')
    plt.show()



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_39_0.png


.. code:: python

    res_state_counts = Counter(df[df['Residence State'] != 'ITALY']['Residence State'])
    res_state_df = pd.DataFrame(res_state_counts.items(), columns=['Residence State', 'Count'])
    res_state_df = res_state_df.sort_values(by='Count', ascending=False)
    res_state_df.head(20).plot(x='Residence State', y='Count', kind='bar', legend=False)
    plt.title('Top 20 Residence States (other than Italy)')
    plt.ylabel('Frequency')
    plt.show()



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_40_0.png


.. code:: python

    df['Residence Italian Region'] = df['Residence'].apply(lambda x: x if x in italy_list else 'Not in ITALY')

.. code:: python

    df.loc[
        (df['Residence State'] == 'ITALY') & (df['Residence Italian Region'] == 'Not in ITALY'),
        'Residence Italian Region'
    ] = 'Not Specified'

.. code:: python

    it_reg_counts = Counter(df['Residence Italian Region'])
    it_reg_df = pd.DataFrame(it_reg_counts.items(), columns=['Residence Italian Region', 'Count'])
    it_reg_df = it_reg_df.sort_values(by='Count', ascending=False)
    it_reg_df.head(20).plot(x='Residence Italian Region', y='Count', kind='bar', legend=False)
    plt.title('Top 20 Residence Italian Regions')
    plt.ylabel('Frequency')
    plt.show()



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_43_0.png


.. code:: python

    european_countries = [
        'ALBANIA', 'AUSTRIA', 'BELARUS', 'BELGIUM', 'BULGARIA', 'CROATIA', 'CZECH REPUBLIC',
        'FRANCE', 'GERMANY', 'GREAT BRITAIN-NORTHERN IRELAND', 'GREECE', 'ITALY', 'LATVIA',
        'LITHUANIA', 'LUXEMBOURG', 'MALTA', 'MOLDOVA', 'MONACO', 'MONTENEGRO', 'NETHERLANDS',
        'NORWAY', 'POLAND', 'PORTUGAL', 'ROMANIA', 'RUSSIA', 'SAN MARINO', 'SERBIA', 'SLOVAKIA',
        'SLOVENIA', 'SPAIN', 'SWEDEN', 'SWITZERLAND', 'UKRAINE'
    ]
    df['European Residence'] = df['Residence State'].apply(lambda x: 'Yes' if x in european_countries else 'No')

.. code:: python

    eu_distrib = Counter(df['European Residence'])
    eu_distrib_df = pd.DataFrame(eu_distrib.items(), columns=['European Residence', 'Count'])
    
    labels = eu_distrib_df['European Residence']
    labels.replace({'Yes': 'European', 'No': 'Non-European'}, inplace=True)
    sizes = eu_distrib_df['Count']
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('European Residence Distribution')
    plt.show()



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_45_0.png


The ``Residence`` column could then be removed.

.. code:: python

    df = df.drop(columns=['Residence'])

**Sex**
^^^^^^^

The dataset is unbalanced with respect to the Sex feature, with 76.8%
male candidates and 23.2% female candidates.

.. code:: python

    sex_distrib = Counter(df['Sex'])
    sex_distrib_df = pd.DataFrame(sex_distrib.items(), columns=['Sex', 'Count'])
    
    labels = sex_distrib_df['Sex']
    sizes = sex_distrib_df['Count']
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)




.. parsed-literal::

    ([<matplotlib.patches.Wedge at 0x7c7b4c4fd6f0>,
      <matplotlib.patches.Wedge at 0x7c7b4c4fd600>],
     [Text(0.15654062369121927, -1.0888044053613875, 'Male'),
      Text(-0.15654057272060573, 1.0888044126895817, 'Female')],
     [Text(0.08538579474066504, -0.5938933120153022, '76.8%'),
      Text(-0.0853857669385122, 0.5938933160124991, '23.2%')])




.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_49_1.png


**Protected Category**
^^^^^^^^^^^^^^^^^^^^^^

Mapping can be applied to simplify this feature and discriminate between
candidates that are part of a protected category and candidates who are
not.

.. code:: python

    df['Protected Category'] = df['Protected Category'].replace('Article 18', 'Yes')
    df['Protected Category'] = df['Protected Category'].replace('Article 1', 'Yes')

The dataset is highly unbalanced with respect to this feature, with only
0.4% candidates from protected categories.

.. code:: python

    pr_cat_distrib = Counter(df['Protected Category'])
    pr_cat_distrib_df = pd.DataFrame(pr_cat_distrib.items(), columns=['Protected Category', 'Count'])
    
    labels = pr_cat_distrib_df['Protected Category']
    labels.replace({'No': 'No Protected Category', 'Yes': 'Protected Category'}, inplace=True)
    sizes = pr_cat_distrib_df['Count']
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)




.. parsed-literal::

    ([<matplotlib.patches.Wedge at 0x7c7b4c49ac80>,
      <matplotlib.patches.Wedge at 0x7c7b4c49af50>],
     [Text(0.8346254005063664, -0.7165196723256019, 'No Protected Category'),
      Text(-0.8346254188500342, 0.7165196509583008, 'Protected Category')],
     [Text(0.45525021845801794, -0.39082891217760096, '99.6%'),
      Text(-0.4552502284636549, 0.3908289005227095, '0.4%')])




.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_53_1.png


**Tag**
^^^^^^^

This feature is highly irregular and will need processing in order to be
useful. Some mapping could be applied to clean the data:

.. code:: python

    df['Tag'] = df['Tag'].replace('-', 'Not Specified')
    df['Tag'] = df['Tag'].replace('.', 'Not Specified')
    df['Tag'] = df['Tag'].replace('X', 'Not Specified')

.. code:: python

    print(df['Tag'].unique())


.. parsed-literal::

    ['AUTOSAR, CAN, C, C++, MATLAB/SIMULINK, VECTOR/VENUS, VHDL, FPGA'
     '-, C, C++, DO178, LABVIEW, SOFTWARE DEVELOPMENT' 'PROCESS ENG.' ...
     '-, SOLIDWORKS, NX, CREO, INENTOR, GT POWER, AMESIM' 'SQL, UNIX'
     '-, ENVIRONMENTAL QUALITY, ENVIRONMENTAL MANAGER, ENVIRONMENTAL PROJECT ENGINEER, ISO 14001, ENVIRONMENTAL MANAGEMENT , ISO 14001, ENVIRONMENTAL MANAGEMENT, OFFSHORE']


.. code:: python

    all_keywords = df['Tag'].str.split(', ').explode()
    keyword_counts = Counter(all_keywords)
    
    keyword_df = pd.DataFrame(keyword_counts.items(), columns=['Keyword', 'Count'])
    keyword_df.drop(keyword_df[keyword_df['Keyword'] == 'Not Specified'].index, inplace=True)
    keyword_df.drop(keyword_df[keyword_df['Keyword'] == '.'].index, inplace=True)
    keyword_df.drop(keyword_df[keyword_df['Keyword'] == '-'].index, inplace=True)
    keyword_df.drop(keyword_df[keyword_df['Keyword'] == 'X'].index, inplace=True)
    keyword_df = keyword_df.sort_values(by='Count', ascending=False)
    
    keyword_df.head(10)




.. raw:: html

    
      <div id="df-bd8a1fd4-1e0a-4f0e-8d99-6f986c91353a" class="colab-df-container">
        <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Keyword</th>
          <th>Count</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>20</th>
          <td>MATLAB</td>
          <td>576</td>
        </tr>
        <tr>
          <th>3</th>
          <td>C++</td>
          <td>312</td>
        </tr>
        <tr>
          <th>2</th>
          <td>C</td>
          <td>305</td>
        </tr>
        <tr>
          <th>21</th>
          <td>SIMULINK</td>
          <td>305</td>
        </tr>
        <tr>
          <th>107</th>
          <td>SOLIDWORKS</td>
          <td>299</td>
        </tr>
        <tr>
          <th>35</th>
          <td>PYTHON</td>
          <td>275</td>
        </tr>
        <tr>
          <th>137</th>
          <td>EXCEL</td>
          <td>177</td>
        </tr>
        <tr>
          <th>52</th>
          <td>JAVA</td>
          <td>176</td>
        </tr>
        <tr>
          <th>136</th>
          <td>OFFICE</td>
          <td>143</td>
        </tr>
        <tr>
          <th>205</th>
          <td>AUTOCAD</td>
          <td>129</td>
        </tr>
      </tbody>
    </table>
    </div>
        <div class="colab-df-buttons">
    
      <div class="colab-df-container">
        <button class="colab-df-convert" onclick="convertToInteractive('df-bd8a1fd4-1e0a-4f0e-8d99-6f986c91353a')"
                title="Convert this dataframe to an interactive table."
                style="display:none;">
    
      <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
        <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
      </svg>
        </button>
    
      <style>
        .colab-df-container {
          display:flex;
          gap: 12px;
        }
    
        .colab-df-convert {
          background-color: #E8F0FE;
          border: none;
          border-radius: 50%;
          cursor: pointer;
          display: none;
          fill: #1967D2;
          height: 32px;
          padding: 0 0 0 0;
          width: 32px;
        }
    
        .colab-df-convert:hover {
          background-color: #E2EBFA;
          box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
          fill: #174EA6;
        }
    
        .colab-df-buttons div {
          margin-bottom: 4px;
        }
    
        [theme=dark] .colab-df-convert {
          background-color: #3B4455;
          fill: #D2E3FC;
        }
    
        [theme=dark] .colab-df-convert:hover {
          background-color: #434B5C;
          box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
          filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
          fill: #FFFFFF;
        }
      </style>
    
        <script>
          const buttonEl =
            document.querySelector('#df-bd8a1fd4-1e0a-4f0e-8d99-6f986c91353a button.colab-df-convert');
          buttonEl.style.display =
            google.colab.kernel.accessAllowed ? 'block' : 'none';
    
          async function convertToInteractive(key) {
            const element = document.querySelector('#df-bd8a1fd4-1e0a-4f0e-8d99-6f986c91353a');
            const dataTable =
              await google.colab.kernel.invokeFunction('convertToInteractive',
                                                        [key], {});
            if (!dataTable) return;
    
            const docLinkHtml = 'Like what you see? Visit the ' +
              '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
              + ' to learn more about interactive tables.';
            element.innerHTML = '';
            dataTable['output_type'] = 'display_data';
            await google.colab.output.renderOutput(dataTable, element);
            const docLink = document.createElement('div');
            docLink.innerHTML = docLinkHtml;
            element.appendChild(docLink);
          }
        </script>
      </div>
    
    
    <div id="df-97debbdd-03eb-4501-8acc-0302ce8791cf">
      <button class="colab-df-quickchart" onclick="quickchart('df-97debbdd-03eb-4501-8acc-0302ce8791cf')"
                title="Suggest charts"
                style="display:none;">
    
    <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
         width="24px">
        <g>
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
        </g>
    </svg>
      </button>
    
    <style>
      .colab-df-quickchart {
          --bg-color: #E8F0FE;
          --fill-color: #1967D2;
          --hover-bg-color: #E2EBFA;
          --hover-fill-color: #174EA6;
          --disabled-fill-color: #AAA;
          --disabled-bg-color: #DDD;
      }
    
      [theme=dark] .colab-df-quickchart {
          --bg-color: #3B4455;
          --fill-color: #D2E3FC;
          --hover-bg-color: #434B5C;
          --hover-fill-color: #FFFFFF;
          --disabled-bg-color: #3B4455;
          --disabled-fill-color: #666;
      }
    
      .colab-df-quickchart {
        background-color: var(--bg-color);
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        fill: var(--fill-color);
        height: 32px;
        padding: 0;
        width: 32px;
      }
    
      .colab-df-quickchart:hover {
        background-color: var(--hover-bg-color);
        box-shadow: 0 1px 2px rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15);
        fill: var(--button-hover-fill-color);
      }
    
      .colab-df-quickchart-complete:disabled,
      .colab-df-quickchart-complete:disabled:hover {
        background-color: var(--disabled-bg-color);
        fill: var(--disabled-fill-color);
        box-shadow: none;
      }
    
      .colab-df-spinner {
        border: 2px solid var(--fill-color);
        border-color: transparent;
        border-bottom-color: var(--fill-color);
        animation:
          spin 1s steps(1) infinite;
      }
    
      @keyframes spin {
        0% {
          border-color: transparent;
          border-bottom-color: var(--fill-color);
          border-left-color: var(--fill-color);
        }
        20% {
          border-color: transparent;
          border-left-color: var(--fill-color);
          border-top-color: var(--fill-color);
        }
        30% {
          border-color: transparent;
          border-left-color: var(--fill-color);
          border-top-color: var(--fill-color);
          border-right-color: var(--fill-color);
        }
        40% {
          border-color: transparent;
          border-right-color: var(--fill-color);
          border-top-color: var(--fill-color);
        }
        60% {
          border-color: transparent;
          border-right-color: var(--fill-color);
        }
        80% {
          border-color: transparent;
          border-right-color: var(--fill-color);
          border-bottom-color: var(--fill-color);
        }
        90% {
          border-color: transparent;
          border-bottom-color: var(--fill-color);
        }
      }
    </style>
    
      <script>
        async function quickchart(key) {
          const quickchartButtonEl =
            document.querySelector('#' + key + ' button');
          quickchartButtonEl.disabled = true;  // To prevent multiple clicks.
          quickchartButtonEl.classList.add('colab-df-spinner');
          try {
            const charts = await google.colab.kernel.invokeFunction(
                'suggestCharts', [key], {});
          } catch (error) {
            console.error('Error during call to suggestCharts:', error);
          }
          quickchartButtonEl.classList.remove('colab-df-spinner');
          quickchartButtonEl.classList.add('colab-df-quickchart-complete');
        }
        (() => {
          let quickchartButtonEl =
            document.querySelector('#df-97debbdd-03eb-4501-8acc-0302ce8791cf button');
          quickchartButtonEl.style.display =
            google.colab.kernel.accessAllowed ? 'block' : 'none';
        })();
      </script>
    </div>
    
        </div>
      </div>




.. code:: python

    keyword_df.head(20).plot(x='Keyword', y='Count', kind='bar', legend=False)
    plt.title('Top 20 keywords used by recruiters')
    plt.ylabel('Frequency')
    plt.xlabel('Keyword')
    plt.show()




.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_58_0.png


**Study Area**
^^^^^^^^^^^^^^

.. code:: python

    print(f"There are {len(df['Study Area'].unique())} different <Study Area> values:\n {df['Study Area'].unique()} \n")


.. parsed-literal::

    There are 48 different <Study Area> values:
     ['Automation/Mechatronics Engineering' 'computer engineering'
     'chemical engineering' 'Legal' 'Mechanical engineering'
     'Telecommunications Engineering' 'Economic - Statistics'
     'Materials Science and Engineering' 'Other scientific subjects'
     'Biomedical Engineering' 'electronic Engineering'
     'Information Engineering'
     'Aeronautical/Aerospace/Astronautics Engineering'
     'Energy and Nuclear Engineering' 'Informatics' 'Management Engineering'
     'Automotive Engineering' 'industrial engineering' 'Other' 'Surveyor'
     'Electrical Engineering' 'Scientific maturity' 'Chemist - Pharmaceutical'
     'Political-Social' 'Other humanities subjects' 'Geo-Biological'
     'Civil/Civil and Environmental Engineering' 'Psychology' 'Linguistics'
     'Agriculture and veterinary' 'Literary' 'Humanistic high school diploma'
     'Accounting' 'Communication Sciences' 'Safety Engineering' 'Architecture'
     'Mathematics' 'construction Engineering' 'Petroleum Engineering'
     'Naval Engineering' 'Artistic' 'Not Specified'
     'Mathematical-physical modeling for engineering'
     'Engineering for the environment and the territory' 'Medical'
     'Defense and Security' 'Physical education' 'Statistics'] 
    


.. code:: python

    study_areas_counts = Counter(df['Study Area'])
    
    study_areas_counts_df = pd.DataFrame(study_areas_counts.items(), columns=['Study Area', 'Count'])
    study_areas_counts_df = study_areas_counts_df.sort_values(by='Count', ascending=False)
    
    study_areas_counts_df.head(10)




.. raw:: html

    
      <div id="df-50451c5a-7fa2-4bc3-b478-14bd3e40f299" class="colab-df-container">
        <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Study Area</th>
          <th>Count</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>4</th>
          <td>Mechanical engineering</td>
          <td>2235</td>
        </tr>
        <tr>
          <th>1</th>
          <td>computer engineering</td>
          <td>1344</td>
        </tr>
        <tr>
          <th>12</th>
          <td>Aeronautical/Aerospace/Astronautics Engineering</td>
          <td>951</td>
        </tr>
        <tr>
          <th>9</th>
          <td>Biomedical Engineering</td>
          <td>924</td>
        </tr>
        <tr>
          <th>17</th>
          <td>industrial engineering</td>
          <td>901</td>
        </tr>
        <tr>
          <th>15</th>
          <td>Management Engineering</td>
          <td>798</td>
        </tr>
        <tr>
          <th>10</th>
          <td>electronic Engineering</td>
          <td>685</td>
        </tr>
        <tr>
          <th>18</th>
          <td>Other</td>
          <td>567</td>
        </tr>
        <tr>
          <th>11</th>
          <td>Information Engineering</td>
          <td>485</td>
        </tr>
        <tr>
          <th>0</th>
          <td>Automation/Mechatronics Engineering</td>
          <td>430</td>
        </tr>
      </tbody>
    </table>
    </div>
        <div class="colab-df-buttons">
    
      <div class="colab-df-container">
        <button class="colab-df-convert" onclick="convertToInteractive('df-50451c5a-7fa2-4bc3-b478-14bd3e40f299')"
                title="Convert this dataframe to an interactive table."
                style="display:none;">
    
      <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
        <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
      </svg>
        </button>
    
      <style>
        .colab-df-container {
          display:flex;
          gap: 12px;
        }
    
        .colab-df-convert {
          background-color: #E8F0FE;
          border: none;
          border-radius: 50%;
          cursor: pointer;
          display: none;
          fill: #1967D2;
          height: 32px;
          padding: 0 0 0 0;
          width: 32px;
        }
    
        .colab-df-convert:hover {
          background-color: #E2EBFA;
          box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
          fill: #174EA6;
        }
    
        .colab-df-buttons div {
          margin-bottom: 4px;
        }
    
        [theme=dark] .colab-df-convert {
          background-color: #3B4455;
          fill: #D2E3FC;
        }
    
        [theme=dark] .colab-df-convert:hover {
          background-color: #434B5C;
          box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
          filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
          fill: #FFFFFF;
        }
      </style>
    
        <script>
          const buttonEl =
            document.querySelector('#df-50451c5a-7fa2-4bc3-b478-14bd3e40f299 button.colab-df-convert');
          buttonEl.style.display =
            google.colab.kernel.accessAllowed ? 'block' : 'none';
    
          async function convertToInteractive(key) {
            const element = document.querySelector('#df-50451c5a-7fa2-4bc3-b478-14bd3e40f299');
            const dataTable =
              await google.colab.kernel.invokeFunction('convertToInteractive',
                                                        [key], {});
            if (!dataTable) return;
    
            const docLinkHtml = 'Like what you see? Visit the ' +
              '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
              + ' to learn more about interactive tables.';
            element.innerHTML = '';
            dataTable['output_type'] = 'display_data';
            await google.colab.output.renderOutput(dataTable, element);
            const docLink = document.createElement('div');
            docLink.innerHTML = docLinkHtml;
            element.appendChild(docLink);
          }
        </script>
      </div>
    
    
    <div id="df-c0461018-c5c1-402e-a14d-f64706eaf7a3">
      <button class="colab-df-quickchart" onclick="quickchart('df-c0461018-c5c1-402e-a14d-f64706eaf7a3')"
                title="Suggest charts"
                style="display:none;">
    
    <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
         width="24px">
        <g>
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
        </g>
    </svg>
      </button>
    
    <style>
      .colab-df-quickchart {
          --bg-color: #E8F0FE;
          --fill-color: #1967D2;
          --hover-bg-color: #E2EBFA;
          --hover-fill-color: #174EA6;
          --disabled-fill-color: #AAA;
          --disabled-bg-color: #DDD;
      }
    
      [theme=dark] .colab-df-quickchart {
          --bg-color: #3B4455;
          --fill-color: #D2E3FC;
          --hover-bg-color: #434B5C;
          --hover-fill-color: #FFFFFF;
          --disabled-bg-color: #3B4455;
          --disabled-fill-color: #666;
      }
    
      .colab-df-quickchart {
        background-color: var(--bg-color);
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        fill: var(--fill-color);
        height: 32px;
        padding: 0;
        width: 32px;
      }
    
      .colab-df-quickchart:hover {
        background-color: var(--hover-bg-color);
        box-shadow: 0 1px 2px rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15);
        fill: var(--button-hover-fill-color);
      }
    
      .colab-df-quickchart-complete:disabled,
      .colab-df-quickchart-complete:disabled:hover {
        background-color: var(--disabled-bg-color);
        fill: var(--disabled-fill-color);
        box-shadow: none;
      }
    
      .colab-df-spinner {
        border: 2px solid var(--fill-color);
        border-color: transparent;
        border-bottom-color: var(--fill-color);
        animation:
          spin 1s steps(1) infinite;
      }
    
      @keyframes spin {
        0% {
          border-color: transparent;
          border-bottom-color: var(--fill-color);
          border-left-color: var(--fill-color);
        }
        20% {
          border-color: transparent;
          border-left-color: var(--fill-color);
          border-top-color: var(--fill-color);
        }
        30% {
          border-color: transparent;
          border-left-color: var(--fill-color);
          border-top-color: var(--fill-color);
          border-right-color: var(--fill-color);
        }
        40% {
          border-color: transparent;
          border-right-color: var(--fill-color);
          border-top-color: var(--fill-color);
        }
        60% {
          border-color: transparent;
          border-right-color: var(--fill-color);
        }
        80% {
          border-color: transparent;
          border-right-color: var(--fill-color);
          border-bottom-color: var(--fill-color);
        }
        90% {
          border-color: transparent;
          border-bottom-color: var(--fill-color);
        }
      }
    </style>
    
      <script>
        async function quickchart(key) {
          const quickchartButtonEl =
            document.querySelector('#' + key + ' button');
          quickchartButtonEl.disabled = true;  // To prevent multiple clicks.
          quickchartButtonEl.classList.add('colab-df-spinner');
          try {
            const charts = await google.colab.kernel.invokeFunction(
                'suggestCharts', [key], {});
          } catch (error) {
            console.error('Error during call to suggestCharts:', error);
          }
          quickchartButtonEl.classList.remove('colab-df-spinner');
          quickchartButtonEl.classList.add('colab-df-quickchart-complete');
        }
        (() => {
          let quickchartButtonEl =
            document.querySelector('#df-c0461018-c5c1-402e-a14d-f64706eaf7a3 button');
          quickchartButtonEl.style.display =
            google.colab.kernel.accessAllowed ? 'block' : 'none';
        })();
      </script>
    </div>
    
        </div>
      </div>




.. code:: python

    study_areas_counts_df.head(20).plot(x='Study Area', y='Count', kind='bar', legend=False)
    plt.title('Top 20 Study Areas')
    plt.ylabel('Frequency')
    plt.xlabel('Study Area')
    plt.show()



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_62_0.png


**Study Title**
^^^^^^^^^^^^^^^

.. code:: python

    print(f"There are {len(df['Study Title'].unique())} different <Study Title> values:\n {df['Study Title'].unique()} \n")


.. parsed-literal::

    There are 7 different <Study Title> values:
     ['Five-year degree' 'Doctorate' 'High school graduation'
     'Three-year degree' "master's degree" 'Middle school diploma'
     'Professional qualification'] 
    


.. code:: python

    study_title_distrib = df['Study Title'].value_counts()
    study_title_df = pd.DataFrame(study_title_distrib.items(), columns=['Study Title', 'Count'])
    study_title_df.plot(x='Study Title', y='Count', kind='bar', legend=False)
    plt.title('Study Title Distribution')
    plt.ylabel('Frequency')
    plt.xlabel('Study Title')
    plt.show()



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_65_0.png


**Years Experience**
^^^^^^^^^^^^^^^^^^^^

.. code:: python

    print(f"There are {len(df['Years Experience'].unique())} different <Years Experience> categories:\n {df['Years Experience'].unique()} \n")


.. parsed-literal::

    There are 7 different <Years Experience> categories:
     ['[1-3]' '[7-10]' '[3-5]' '[5-7]' '[+10]' '[0]' '[0-1]'] 
    


.. code:: python

    custom_order = ['[0]', '[0-1]', '[1-3]', '[3-5]', '[5-7]', '[7-10]', '[+10]']
    df['Years Experience'] = pd.Categorical(df['Years Experience'], categories=custom_order, ordered=True)
    
    years_exp_counts = Counter(df['Years Experience'].sort_values())
    years_exp_df = pd.DataFrame(years_exp_counts.items(), columns=['Years Experience', 'Count'])
    years_exp_df.plot(x='Years Experience', y='Count', kind='bar', legend=False)
    plt.title('Years Experience Distribution')
    plt.ylabel('Frequency')




.. parsed-literal::

    Text(0, 0.5, 'Frequency')




.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_68_1.png


**Sector**
^^^^^^^^^^

This feature doesn’t seem relevant as its most frequent values are “*Not
Specified*” and “*Others*”.

.. code:: python

    sector_counts = Counter(df['Sector'])
    sector_df = pd.DataFrame(sector_counts.items(), columns=['Sector', 'Count'])
    sector_df = sector_df.sort_values(by='Count', ascending=False)
    sector_df.plot(x='Sector', y='Count', kind='bar', legend=False)
    plt.title('Sector Distribution')
    plt.ylabel('Frequency')
    plt.show()



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_70_0.png


\**Event_type\__val*\*
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    print(f"There are {len(df['Event_Type__Val'].unique())} different values for <Event_Type__Val:\n {df['Event_Type__Val'].unique()}")


.. parsed-literal::

    There are 13 different values for <Event_Type__Val:
     ['BM interview' 'Candidate notification' 'Qualification Meeting'
     'Technical interview' 'HR interview' 'CV request' 'Contact note'
     'Inadequate CV' 'Economic proposal' 'Research association'
     'Sending SC to customer' 'Not Specified' 'Commercial note']


.. code:: python

    etv_distrib = Counter(df['Event_Type__Val'])
    etv_distrib_df = pd.DataFrame(etv_distrib.items(), columns=['Event_Type__Val', 'Count'])
    etv_distrib_df = etv_distrib_df.sort_values(by='Count', ascending=False)
    etv_distrib_df.plot(x='Event_Type__Val', y='Count', kind='bar', legend=False)
    plt.title('Event Type Distribution')
    plt.ylabel('Frequency')
    plt.show()



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_73_0.png


The most frequent type of **event** is the “*CV Request*”, meaning that
Akkodis has not yet received anything from that candidate. This could
mean that for this kind of candidates there’s no way to determine
whether they are eligible or not for the position.

.. code:: python

    cv_req_counts = df[df['Event_Type__Val'] == 'CV request']['Candidate State'].value_counts()
    cv_req_df = pd.DataFrame(cv_req_counts.items(), columns=['Candidate State', 'Count'])
    cv_req_df.plot(x='Candidate State', y='Count', kind='bar', legend=False)
    plt.title('Candidate State for CV request')
    plt.ylabel('Frequency')
    plt.show()



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_75_0.png


**Event_feedback**
^^^^^^^^^^^^^^^^^^

This feature could be simplified with mapping, reducing the number of
possible values from 16 to 3:

.. code:: python

    print(f"There are {len(df['Event_Feedback'].unique())} possible values for <Event_Feedback>:\n {df['Event_Feedback'].unique()}")


.. parsed-literal::

    There are 16 possible values for <Event_Feedback>:
     ['OK' 'Not Specified' 'KO (technical skills)' 'OK (waiting for departure)'
     'KO (proposed renunciation)' 'OK (live)' 'KO (mobility)' 'KO (manager)'
     'KO (retired)' 'OK (hired)' 'KO (seniority)' 'KO (ral)'
     'OK (other candidate)' 'KO (opportunity closed)' 'KO (lost availability)'
     'KO (language skills)']


.. code:: python

    df['Event_Feedback'] = df['Event_Feedback'].apply(lambda x: 'OK' if 'OK' in x else x)
    df['Event_Feedback'] = df['Event_Feedback'].apply(lambda x: 'KO' if 'KO' in x else x)

.. code:: python

    print(f"After mapping there are now {len(df['Event_Feedback'].unique())} possible values for <Event_Feedback>:\n {df['Event_Feedback'].unique()}")


.. parsed-literal::

    After mapping there are now 3 possible values for <Event_Feedback>:
     ['OK' 'Not Specified' 'KO']


.. code:: python

    ok_ko_distrib = df['Event_Feedback'].value_counts()
    ok_ko_distrib_df = pd.DataFrame(ok_ko_distrib.items(), columns=['Event_Feedback', 'Count'])
    
    ok_ko_distrib = ok_ko_distrib_df['Count']
    labels = ok_ko_distrib_df['Event_Feedback']
    
    plt.pie(ok_ko_distrib, labels=labels, autopct='%1.1f%%')
    plt.title('Event Feedback Distribution')
    plt.show()



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_80_0.png


Data Visualization
------------------

**Sex and Candidate State**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    pivot = df.pivot_table(index='Sex', columns='Candidate State', aggfunc='size', fill_value=0)
    
    pivot.plot(kind='bar', figsize=(10, 6))
    plt.title('Candidate State by Sex')
    plt.ylabel('Count')
    plt.xlabel('Sex')
    plt.legend(title='Candidate State', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()




.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_82_0.png


.. code:: python

    pivot_percentage = pivot.div(pivot.sum(axis=1), axis=0)
    
    pivot_percentage.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title('Candidate State by Sex (Normalized)')
    plt.ylabel('Proportion')
    plt.xlabel('Sex')
    plt.legend(title='Candidate State', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()




.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_83_0.png


**Protected Category and Candidate State**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    pivot = df.pivot_table(index='Protected Category', columns='Candidate State', aggfunc='size', fill_value=0)
    pivot_percentage = pivot.div(pivot.sum(axis=1), axis=0)
    
    pivot_percentage.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title('Candidate State by Protected Category (Normalized)')
    plt.ylabel('Proportion')
    plt.xlabel('Protected Category')
    plt.legend(title='Candidate State', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_85_0.png


**Age Range and Candidate State**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    plt.figure(figsize=(12, 6))
    sns.histplot(
        data= df,
        x='Age Range',
        hue='Candidate State',
        multiple='stack',
        palette='Set2',
        shrink=0.8
    )
    plt.title("Distribution of Age Ranges by Candidate State", fontsize=14)
    plt.xlabel("Age Range", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='Candidate State', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
    
    
    plt.figure(figsize=(12, 6))
    sns.boxplot(
        data=df,
        x='Candidate State',
        y=df['Age Range'].map(lambda x: int(x.split('-')[0]) if '-' in x else (19 if '<' in x else 46)),
        palette='Set3'
    )
    plt.title("Candidate State by Age Range (Numerical Approximation)", fontsize=14)
    plt.xlabel("Candidate State", fontsize=12)
    plt.ylabel("Age Range (Approximate Numerical Value)", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



.. parsed-literal::

    WARNING:matplotlib.legend:No artists with labels found to put in legend.  Note that artists whose label start with an underscore are ignored when legend() is called with no argument.



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_87_1.png


.. parsed-literal::

    <ipython-input-77-b2f861d90bfc>:20: FutureWarning: 
    
    Passing `palette` without assigning `hue` is deprecated and will be removed in v0.14.0. Assign the `x` variable to `hue` and set `legend=False` for the same effect.
    
      sns.boxplot(



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_87_3.png


**Correlation**
^^^^^^^^^^^^^^^

.. code:: python

    print(df.columns)


.. parsed-literal::

    Index(['Candidate State', 'Age Range', 'Sex', 'Protected Category', 'Tag',
           'Study Area', 'Study Title', 'Years Experience', 'Sector',
           'Event_Type__Val', 'Event_Feedback', 'Residence State',
           'Residence Italian Region', 'European Residence'],
          dtype='object')


.. code:: python

    df_encoded = df.copy()
    
    age_mapping = {
        '< 20 years': 1,
        '20 - 25 years': 2,
        '26 - 30 years': 3,
        '31 - 35 years': 4,
        '36 - 40 years': 5,
        '40 - 45 years': 6,
        '> 45 years': 7
    }
    
    df_encoded['Age Range'] = df_encoded['Age Range'].map(age_mapping)
    
    le = LabelEncoder()
    
    for col in df_encoded.columns:
        if col != 'Age Range':
            df_encoded[col] = le.fit_transform(df_encoded[col])
    
    correlation_matrix = df_encoded.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f")
    plt.title('Correlation Matrix')
    plt.show()



.. image:: Akkodis_Dataset_Analysis_files/Akkodis_Dataset_Analysis_90_0.png

