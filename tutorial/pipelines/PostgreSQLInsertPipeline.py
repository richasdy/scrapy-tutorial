import sys
import psycopg2
import logging

logging.basicConfig(
    level=logging.DEBUG,
    # format='%(asctime)s - %(filename)s - %(name)s - %(levelname)s - %(message)s'
    # format='%(asctime)s - %(module)s - %(name)s - %(levelname)s - %(message)s'
    format='%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger('tutorial.pipelines.PostgreSQLInsertPipeline')

class PostgreSQLInsertPipeline(object):
    def __init__(self):
        self.conn = psycopg2.connect(
            host='localhost', 
            database='scrapy_tutorial', 
            user='root', 
            password='toor'
            )
        self.cursor = self.conn.cursor()
        
        '''
        CREATE TABLE quote ( 
            id SERIAL, 
            author_bio TEXT, 
            author_birthday DATE, 
            author_bornlocation TEXT, 
            author_name VARCHAR(50), 
            quote_content TEXT, 
            PRIMARY KEY (id) 
            );
        '''

    def process_item(self, item, spider):    
        try:
            logger.debug('try insert data')
            sql = "INSERT INTO quote(author_bio, author_birthday, author_bornlocation, author_name, quote_content) VALUES (%s,%s,%s,%s,%s)"
            data = (item["author_bio"],item["author_birthday"],item["author_bornlocation"],item["author_name"],item["quote_content"])
            self.cursor.execute(sql,data)            
            self.conn.commit()            
        except psycopg2.DatabaseError as e:
            print ("Error %s",(e))
        return item