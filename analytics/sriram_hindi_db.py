from abc import ABC

from settings import *
from peewee import *
from playhouse.mysql_ext import MySQLConnectorDatabase, JSONField
from playhouse.shortcuts import ReconnectMixin

import sys, os

TABLE_NAME = "ShriramHindiEvents"


class ReconnectMySQLDatabase(ReconnectMixin, MySQLConnectorDatabase, ABC):
    pass


database = ReconnectMySQLDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database


class ShriramHindiEvents(BaseModel):
    id = BigAutoField()
    user_id = CharField(max_length=300, null=True)
    request_id = CharField(max_length=300, null=True)
    sender_id = CharField(max_length=300, null=True)
    event_type = CharField(max_length=100, null=True)
    event = JSONField(null=True)
    intent = CharField(max_length=100, null=True)
    intent_confidence = FloatField(null=True)
    entity = JSONField(null=True)
    action_name = CharField(max_length=100, null=True)
    action_confidence = FloatField(null=True)
    timestamp = TimestampField(utc=True, null=True)


# app = os.environ["PROJECT"]
#
# # app = 'prod'
# print("WORKING ENV:",app)

database.init(DATABASE, user=USER, password=PASSWORD, host=HOST)


# if app == 'prod':
#     database.init(DATABASE, user=USER, password=PASSWORD, host=HOST)
# else:
#     database.init(DATABASE, user='saarthi', password='bot_analytics', host='localhost')


def create_table():
    if database.connect(reuse_if_open=True):
        database.close()
        database.create_tables([eval(TABLE_NAME)])
        print('Table created %s ...' % (TABLE_NAME))
    else:
        print("cannot connect to DB %s ..." % (TABLE_NAME))
        sys.exit(0)


if __name__ == "__main__":
    create_table()
