from requirements import *


class PreProcess:
    """
    Class is used to perform cleaning based on inputs.
    """

    def __init__(self, dataframe=None):
        self.df = dataframe

    def visualize_missing_values(self):
        df = self.df
        missing_values = df.isnull().sum()
        missing_values_perc = 100 * df.isnull().sum() / len(df)
        types = df.dtypes
        types.replace({"object": "str"}, inplace=True)
        missing_values_table = pd.concat([missing_values, missing_values_perc, types], axis=1)
        renamed_table_columns = missing_values_table.rename(columns={0: "Missing Values",
                                                                     1: "% of Total Values",
                                                                     2: "Type"})
        renamed_table_columns = renamed_table_columns.sort_values("% of Total Values", ascending=False).round(1)
        plt.figure(figsize=(13, 6))
        sns.set(style="whitegrid", color_codes=True)
        sns.barplot(x=renamed_table_columns.index, y=renamed_table_columns["% of Total Values"],
                    data=renamed_table_columns)
        plt.xticks(rotation=90)
        plt.title("Percent of Missing Values")
        plt.show()
        return renamed_table_columns

    def alt_visualize_missing_values(self):
        """
        Uses Seaborn
        :return:
        """

        sns.heatmap(self.df.isnull(), yticklabels=False, cbar=False, cmap="Blues")
        return self.df.isnull()

    def correlation_matrix(self):
        """
        for map, utility is given to two types, can be expanded upon at a later date.
        :param map:
        :return:
        """
        df = self.df
        plt.figure(figsize=(8, 8))
        sns.heatmap(df.corr(), annot=False, cmap='BuPu')
        plt.show()
        return df.corr()

    def categorical_to_numeric(self):
        df = self.df
        for col in df[df.select_dtypes(exclude=['int64', 'float64']).columns].columns.tolist():
            value = df[col].unique()
            for count, str_in_col in enumerate(value):
                if str(str_in_col).lower() == 'nan':
                    count = None
                df[col] = df[col].replace(str_in_col, count)

        return df

    def cleaning_dataframe(self, thresh_hold=.5, method='SI', mode='mean', state_or_neighbors=2):
        """
        SimpleImputer is univariate, taking only a single feature into account.
        IterativeImputer takes a multivariate approach, or uses multiple features.
        KNNImputer takes a multivariate approach, or uses multiple features.
        This will try and make predictions for the missing values depending on
        which columns are passed to the imputation method.
        ATTENTION: CAN ONLY FIND NUMERICAL INPUTS - NOT FOR QUALITATIVE DATA
        :param state_or_neighbors:
        :param thresh_hold:
        :param method:
        :param mode:
        :return:
        """
        if method == 'SI':
            impute_data = SimpleImputer(missing_values=np.nan, strategy=mode, verbose=0)
        elif method == 'II':
            impute_data = IterativeImputer()
        else:
            impute_data = KNNImputer(n_neighbors=state_or_neighbors)
        df = self.df
        for column in df:
            if df[column].isnull().sum() / len(df) >= thresh_hold:
                df.drop(columns=column, axis=1)
            else:
                impute_df = impute_data.fit_transform(df.select_dtypes(exclude=['str', 'obj']))

        return df

    def train_dataset(self, column_name, tSize=.6, rStates=5):
        """
        Takes in class information, currently dataframe.
        column_name is the column you want to predict.
        tSize is the test_size for train_test_split function.
        rStates is the number of random states for train_test_split function.
        :param column_name:
        :param tSize:
        :param rStates:
        :return:
        """
        df = self.df
        X_train, X_test, y_train, y_test = train_test_split(df.iloc[:-1], df.iloc[-1], test_size=tSize, random_state=rStates)

        return X_train, X_test, y_train, y_test
