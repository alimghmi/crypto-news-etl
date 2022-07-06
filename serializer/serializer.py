import time
import logger
import database
import pandas as pd


log = logger.get('serializer')


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
            log.warning('dataframe is empty')
            return False

        log.debug('dataframe ready to be loaded to database')
        return True

    def load(self):
        """Load validated dataframe to database 
        """        

        try:
            conn = database.SQLLite()
            conn.to_db(self.dataframe)
        except Exception as e:
            log.critical('error inserting data to database', exc_info=True)
            return False
        else:
            log.info('data inserted to database')

        try:
            filename = f'{int(time.time())}.csv'
            conn = database.Bucket()
            conn.to_bucket(filename, self.dataframe)
        except Exception as e:
            log.critical(f'error uploading {filename} to s3 bucket', exc_info=True)
            return False
        else:
            log.info(f'{filename} upladed to s3 bucket')
        
        return True

    def _sorted(self):
        """Sort list of dictioneries based on timestamp in decending order
        """        

        self.data = sorted(self.data, key=lambda x: x['timestamp'], reverse=False)
        log.debug('data sorted based on timestamp in ascending order')

    def _get_latest_date(self):
        """get most recent date in database from timestamp column 
        """     

        conn = database.SQLLite()
        df = conn.get_table()

        if not df.empty:
            log.debug('prior data found in database')
            return df.sort_values('timestamp', 
                ascending=False)['timestamp'].iloc[0]
        else:
            log.debug('no prior data available in database')
            return False

    def _filter_recent_news(self):
        """filter input data to contain news that's missing in database
        """   

        latest_date = self._get_latest_date()
        if not latest_date:
            log.debug('keeping all data without filtering')
            return 

        log.debug(f'rows count before filtering: {len(self.dataframe)}')
        log.debug(f'filtering input data by timestamp greater than {latest_date}')
        self.dataframe = self.dataframe[self.dataframe.timestamp > 
                latest_date].reset_index(drop=True)
        
        log.debug(f'rows count after filtering: {len(self.dataframe)}')
