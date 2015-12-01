import datetime
import uuid

from peewee import SqliteDatabase, Model, CharField, BooleanField, IntegerField

from server.config import conf
from server.utils import logger
from server.hmsexceptions import UserNotExistException



# create a peewee database instance -- our models will use this database to
# persist information
database = SqliteDatabase('hms.sqlite3')


class BaseModel(Model):
    class Meta:
        database = database


class DoctorModel(BaseModel):
    """
    {
            'firstname':'',
            'lastname':'',
            'qualification':'',
            'profession': 'xxx',
            'experience':'',
            'gender':'',
            'schedule':'',

    }
    """
    uid = CharField(unique=True)
    firstname = CharField(max_length=100)
    lastname = CharField(max_length=100)
    email = CharField()
    qualification = CharField(max_length=100)
    profession = CharField(max_length=100)
    experience = IntegerField()
    gender = CharField(max_length=10)

    class Meta:
        order_by = ('lastname',)

    def __str__(self):
        return self.uid

    @classmethod
    def create_by_dict(cls, post_data):
        return DoctorModel.create(
            uid=str(uuid.uuid4()),
            firstname=post_data.get('firstname'),
            lastname=post_data.get('lastname'),
            email=post_data.get('email', 'no'),
            qualification=post_data.get('qualification', 'q'),
            profession=post_data.get('profession', 'p'),
            # need a better solution
            experience=int(post_data.get('experience', '0')),
            gender=post_data.get('gender', 'm'),
            )

    @classmethod
    def get_dict(cls, uid):
        logger.debug('in DoctorModel.get_dict ')
        user_dict = {}
        try:
            user = DoctorModel.get(DoctorModel.uid==uid)

        except Exception as ex:
            logger.debug('in DoctorModel.get_dict exception, ', ex)
            raise UserNotExistException()
        else:
            user_dict['firstname'] = user.firstname
            user_dict['lastname'] = user.lastname
            user_dict['email'] = user.email
            user_dict['qualification'] = user.qualification
            user_dict['profession'] = user.profession
            user_dict['experience'] = str(user.experience)
            user_dict['gender'] = user.gender
            logger.debug('after ger user: %s' % uid)
            return user_dict


def create_tables():
    database.connect()
    database.create_tables([DoctorModel], safe=True)
    # database.create_tables([DoctorModel])


if __name__ == '__main__':
    create_tables()
