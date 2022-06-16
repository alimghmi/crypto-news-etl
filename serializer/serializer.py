import database
import pandas as pd


class Serializer:
    """Serializer validate input data and save validated data to database
    """    

    def __init__(self, data):
        self.data = data

    def validate(self):
        """Main function to serialize input data

        Returns:
            Bool: 
                True for valid data  
                False for invalid data
        """      

        self._sorted()
        self.dataframe = pd.DataFrame(self.data)
        self.dataframe.dropna(inplace=True)
        self._filter_recent_news()

        if self.dataframe.empty:
            return False

        return True

    def load(self):
        """Load validated dataframe to database 
        """        

        try:
            conn = database.SQLLite()
            conn.to_db(self.dataframe)
            return self.dataframe
        except Exception as e:
            print('Err', e)
            return False

    def _sorted(self):
        """Sort list of dictioneries based on timestamp in decending order
        """        

        self.data = sorted(self.data, key=lambda x: x['timestamp'], reverse=False)

    def _get_latest_date(self):
        """get most recent date in database from timestamp column 
        """     

        conn = database.SQLLite()
        df = conn.get_table()

        if not df.empty:
            return df.sort_values('timestamp', 
                ascending=False)['timestamp'].iloc[0]
        else:
            return False

    def _filter_recent_news(self):
        """filter input data to contain news that's missing in database
        """   

        latest_date = self._get_latest_date()
        if not latest_date:
            return 

        self.dataframe = self.dataframe[self.dataframe.timestamp > 
                latest_date].reset_index(drop=True)