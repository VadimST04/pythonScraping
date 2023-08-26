# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class SQLitePipeline:
    def open_spider(self, spider):
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
        self.connection.close()

        df = pandas.DataFrame({
            'country': self.countries,
            'years': self.years,
            'population': self.populations,
        })
        df.to_csv('countries_population.csv', index_label='index')

    def process_item(self, item, spider):
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
