from databank import mongoupload
from api import api
from databank import helpers

def add_data():
    '''Gets all data into db
        Returns none
    '''

    mongoupload.mongoadd_prots()
    mongoupload.mongoadd_speakers()
    mongoupload.mongoadd_partys()

#api.start_api()

mongoupload.get_imageurl(speakers=)
