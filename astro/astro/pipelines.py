# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class AstroPipeline(object):
    def process_item(self, item, spider):
        return item

class MySqlPipeline(object):
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME')
        host = spider.settings.get('MYSQL_DB_HOST')
        port = spider.settings.get('MYSQL_PORY')
        user = spider.settings.get('MYSQL_USER')
        password = spider.settings.get('MYSQL_PASSWORD')
        # Database Connecting
        self.connection = pymysql.connect(
            host = host,
            user = user,
            password= password,
            db = db,
            cursorclass= pymysql.cursors.DictCursor
        )

    def close_spider(self, spider):
        self.connection.close()

    old_data_from_sql = []
    def filter_repeat_data(self, item):
        # Getting Old Data from DB
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM astro"
            cursor.execute(sql)
            for row in cursor:
                self.old_data_from_sql.append(row['astro_name'])
        
        if item['astro_name'] not in self.old_data_from_sql:
            self.insert_to_mysql(item)

    def process_item(self, item, spider):
        self.filter_repeat_data(item)
        return item

    def insert_to_mysql(self, item):
        values = (
            item['date'],
            item['astro_name'],
            item['title_all_score'],
            item['title_love_score'],
            item['title_work_score'],
            item['title_money_score'],
            item['title_all_desc'],
            item['title_love_desc'],
            item['title_work_desc'],
            item['title_money_desc']
        )
        with self.connection.cursor() as cursor:
            sql = 'INSERT INTO `astro` (`date`, `astro_name`, `title_all_score`, \
            `title_all_desc`, `title_love_score`, `title_love_desc`, \
            `title_work_score`, `title_work_desc`, `title_money_score`, `title_money_desc`) VALUES \
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, values)
            self.connection.commit()