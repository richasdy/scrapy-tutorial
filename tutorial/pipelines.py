# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from tutorial.models import Quote, Author, Tag, db_connect, create_table
import logging
from scrapy.exporters import JsonLinesItemExporter

# https://stackoverflow.com/questions/41066481/how-to-set-crawler-parameter-from-scrapy-spider
class JsonLinesExporterPipeline(object):

    def __init__(self):
        # Storing output filename
        self.file_name = 'quotes.jl'
        # Creating a file handle and setting it to None
        self.file_handle = None


    def open_spider(self, spider):
        print('Custom export opened')

        # Opening file in binary-write mode
        file = open(self.file_name, 'wb')
        self.file_handle = file

        # Creating a FanItemExporter object and initiating export
        self.exporter = JsonLinesItemExporter(file)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        print('Custom Exporter closed')

        # Ending the export to file from FanItemExport object
        self.exporter.finish_exporting()

        # Closing the opened output file
        self.file_handle.close()
    
    def process_item(self, item, spider):
        # passing the item to FanItemExporter object for expoting to file
        self.exporter.export_item(item)
        return item


class DuplicatesSQLitePipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        logging.info("****DuplicatesPipeline: database connected****")

    def process_item(self, item, spider):
        session = self.Session()
        exist_quote = session.query(Quote).filter_by(quote_content = item["quote_content"]).first()
        if exist_quote is not None:  # the current quote exists
            raise DropItem("Duplicate item found: %s" % item["quote_content"])
            session.close()
        else:
            return item
            session.close()


class SaveQuotesSQLitePipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        logging.info("****SaveQuotePipeline: database connected****")


    def process_item(self, item, spider):

        """Save quotes in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        quote = Quote()
        author = Author()
        tag = Tag()
        author.name = item["author_name"]
        author.birthday = item["author_birthday"]
        author.bornlocation = item["author_bornlocation"]
        author.bio = item["author_bio"]
        quote.quote_content = item["quote_content"]

        # check whether the author exists
        exist_author = session.query(Author).filter_by(name = author.name).first()
        if exist_author is not None:  # the current author exists
            quote.author = exist_author
        else:
            quote.author = author

        # check whether the current quote has tags or not
        if "tags" in item:
            for tag_name in item["tags"]:
                tag = Tag(name=tag_name)
                # check whether the current tag already exists in the database
                exist_tag = session.query(Tag).filter_by(name = tag.name).first()
                if exist_tag is not None:  # the current tag exists
                    tag = exist_tag
                quote.tags.append(tag)

        try:
            session.add(quote)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
