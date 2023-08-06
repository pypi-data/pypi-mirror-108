class CleanData:
    def __init__(self):
        ''' Init function for instantiation of objects'''
        return

    ''' # 1 --> Create function to count null values in a dataframe'''
    def null_count(df):
        num_nulls = df.isnull().sum().sum()
        print(df, '\n', '\n')
        return f'Number of NaN values =, {num_nulls}'

    ''' # 2 --> Create a train/test split function for a dataframe '''
    def train_test_split(df, frac):
        train = df.sample(frac=frac, random_state=200)
        test = df.drop(train.index)
        return train, test

    ''' # 3 --> Randomization function; randomizes all df cells + returns it'''
    def randomize(df, seed):
        # Shuffle rows
        df = df.sample(frac=1, random_state=seed)
        # Shuffle column values
        for col in df.columns:
            df[col] = np.random.RandomState(seed=seed).permutation(df[col])
        return df

    ''' # 4 --> Split addresses into three columns city/state/zip '''
    def addy_split(addy_series):
        address_df = pd.DataFrame({'address': addy_series})
        regex = r'(?P<City>[^,]+)\s*,\s*(?P<State>[^\s]+)\s+(?P<Zip>\S+)'
        df = address_df['address'].str.extract(regex)
        df[['drop', 'City']] = df['City'].str.split('\n', 1, expand=True)
        df = df.drop(columns='drop')
        return df

    ''' # 5 --> Return full state name or abbreviation '''
    # default is long-form to abbreviation, false = opposite
    def abbr_2_st(state_series, abbr_2_st=True):
        # Start with dictionary of abbr state keys and long state values
        state_dict = {
              'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas',
              'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California',
              'CO': 'Colorado', 'CT': 'Connecticut',
              'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida',
              'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa',
              'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas',
              'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts',
              'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan',
              'MN': 'Minnesota', 'MO': 'Missouri',
              'MP': 'Northern Mariana Islands',
              'MS': 'Mississippi', 'MT': 'Montana', 'NA': 'National',
              'NC': 'North Carolina', 'ND': 'North Dakota',
              'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
              'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York',
              'OH': 'Ohio', 'OK': 'Oklahoma',
              'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico',
              'RI': 'Rhode Island', 'UT': 'Utah', 'VA': 'Virginia',
              'SC': 'South Carolina', 'SD': 'South Dakota',
              'TN': 'Tennessee', 'TX': 'Texas', 'VT': 'Vermont',
              'VI': 'Virgin Islands', 'WY': 'Wyoming',
              'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia'
              }
        # If long-to-abbr. invert our dictionary so keys are long, values short
        if abbr_2_st:
            inv_state_dict = {v: k for k, v in state_dict.items()}
            state_list = []
            # Get abbr (value) for each state (key) in the inverted dict
            for state in state_series:
                state_list.append(inv_state_dict.get(state))
            return pd.Series(state_list)
        else:
            state_list = []
            for state in state_series:
                state_list.append(state_dict.get(state))
            return pd.Series(state_list)

    ''' # 6 --> Function takes list & df, creates new col in df of list '''
    def list_2_series(list_2_series, df):
        df['list'] = pd.Series(list_2_series)
        return df

    ''' # 7 --> 1.5*Interquartile range outlier detection/removal function '''
    def rm_outlier(df, col):
        IQR = df[col].quantile(0.75) - df[col].quantile(0.25)
        outlier = IQR * 1.5
        df = df[df[col] < outlier]
        return df

    ''' # 8 --> Function to Split MM/DD/YYYY into 3 separate columns '''
    def split_dates(date_series):
        df = pd.DataFrame(date_series, columns=['date'])
        df['Date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
        df['month'] = pd.to_datetime(df['Date']).dt.month
        df['day'] = pd.to_datetime(df['Date']).dt.day
        df['year'] = pd.to_datetime(df['Date']).dt.year
        df.drop(columns='date', inplace=True)
        df.set_index('Date', inplace=True)
        return df