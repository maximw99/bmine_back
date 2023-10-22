from databank import mongoupload


def add_data():
    '''Gets all data into db
        Returns none
    '''

    mongoupload.mongoadd_prots()
    mongoupload.mongoadd_speakers()
    mongoupload.mongoadd_partys()

