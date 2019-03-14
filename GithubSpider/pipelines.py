# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import mysql.connector

class GithubspiderPipeline(object):
    def process_item(self, item, spider):
        if item.get('owner_name'):
            return item
        else:
            raise DropItem('Missing owner name in {}'.format(item))

class MySQLPipeline(object):
    def __init__(self):
        with open('secret.json', 'r') as jsonfile:
            self.mysql_conn_info = json.load(jsonfile)
            

    def open_spider(self, spider):
        self.db = mysql.connector.connect(**self.mysql_conn_info)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

    def process_item(self, item, spider):
        # Insert repo
        insert_repo = ("INSERT INTO repos "
               "(repo_name, owner_name, repo_url) "
               "VALUES (%s, %s, %s)")
        repo_data = (item['name'], item['owner_name'], item['repo_url'])
        self.cursor.execute(insert_repo, repo_data)
        repo_no = self.cursor.lastrowid

        # Insert tags
        query_tag = ("SELECT tag_no from tags "
            "WHERE tag_name=%s")
        insert_tag = ("INSERT INTO TAGS "
            "(tag_name) VALUES (%s)")
        insert_repo_tag = ("INSERT INTO repo_tag "
            "(repo_no, tag_no) VALUES (%s, %s)")
        for tag in item['tags']:
            self.cursor.execute(query_tag, (tag))
            (tag_no) = self.cursor.fetchone()
            if tag_no is None:
                self.cursor.execute(insert_tag, (tag))
                tag_no = self.cursor.lastrowid
            self.cursor.execute(insert_repo_tag, (repo_no, tag_no))



        return item