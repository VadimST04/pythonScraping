# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class SQLitePipeline:
    """
    This pipeline is designed to store country population data, including country name, year, and population,
    into SQLite database and into CSV file.
    """

    def open_spider(self, spider):
        """
        Open the spider and set up the database connection and lists to store data for CSV file.
        Also create table in database if it does not exist there.
        :param spider: The spider instances.
        :return: None
        """
        self.connection = sqlite3.connect('countries_population.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS population(
                country TEXT,
                year TEXT,
                population TEXT
            )
        ''')
        self.connection.commit()

        self.countries = []
        self.years = []
        self.populations = []

    def close_spider(self, spider):
        """
        Close the spider and finalize the database connection.
        Also add data to DataFrame and then to CSV file.
        :param spider: The spider instances.
        :return: None
        """
        self.connection.close()

        df = pandas.DataFrame({
            'country': self.countries,
            'years': self.years,
            'population': self.populations,
        })
        df.to_csv('countries_population.csv', index_label='index')

    def process_item(self, item, spider):
        """
        Store the scraped data in the database and add data to the appropriate list.
        :param item: The scraped items.
        :param spider: The spider instances.
        :return: None
        """
        self.cursor.execute('''
            INSERT INTO population (country, year, population) VALUES(?,?,?)
        ''', (
            item.get('country'),
            item.get('year'),
            item.get('population'),
        ))
        self.connection.commit()

        self.countries.append(item.get('country'))
        self.years.append(item.get('year'))
        self.populations.append(item.get('population'), )
        return item
