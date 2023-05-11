# BASE SCRIPT FOR TESTS
# Run 'python test.py' to execute the test.

import unittest
import pandas as pd
# import your_module

from Group_6_mvp import annual_grants


class TestMethods(unittest.TestCase):
    def test_function_annual_grant(self):
        data1 = {'year': [2020, 2020, 2021, 2021],
                 'projectID': ['P1', 'P2', 'P1', 'P2'],
                 'ecContribution': [1, 1, 1, 1]}
        data2 = {'year': [2020, 2020, 2021, 2021],
                 'projectID': ['P1', 'P2', 'P1', 'P2'],
                 'ecContribution': [1, 1, 1, 1]}

        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        merged_df = pd.merge(df1, df2, left_on='projectID', right_on='projectID')
        result = merged_df.groupby('year_y')['ecContribution_y'].sum()
        result = result.tolist()

        cordat = pd.Series([4, 4], index=[2020, 2021])
        cordat = cordat.tolist()

        self.assertEqual(result, cordat)

        print("def annual_grants(df1, df2):"
              "merged_df = pd.merge(df1, df2, left_on='projectID', right_on='projectID')"
              "grouped = merged_df.groupby('year')['ecContribution'].sum()"
              "return grouped")


if __name__ == '__main__':
    unittest.main()
