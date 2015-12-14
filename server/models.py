import datetime
import uuid

from peewee import SqliteDatabase, Model, CharField, BooleanField, IntegerField, \
    TextField

from server.config import conf
from server.utils import logger
from server.hmsexceptions import UserNotExistException



# create a peewee database instance -- our models will use this database to
# persist information
# if conf.db_type == 'sqlite3':
#     database = SqliteDatabase('{}.sqlite3'.format(conf.db_filename))
# elif conf.db_type == 'mysql':
#     logger.error('MySQL support is not implemented yet!')


def point_db(config):
    if config.db_type == 'sqlite3':
        database = SqliteDatabase('{}.sqlite3'.format(config.db_filename))
    elif config.db_type == 'mysql':
        logger.error('MySQL support is not implemented yet!')
    return database

def create_tables(config):
    database = point_db(config)
    database.connect()
    database.create_tables([DoctorModel, PatientModel], safe=True)
    return database
    # database.create_tables([DoctorModel])


database = point_db(conf)


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
    # uid = CharField(unique=True)
    email = CharField(max_length=100, unique=True)
    firstname = CharField(max_length=100)
    lastname = CharField(max_length=100)
    qualification = CharField(max_length=100)
    profession = CharField(max_length=100)
    experience = IntegerField()
    gender = CharField(max_length=10)

    class Meta:
        order_by = ('lastname',)

    def __str__(self):
        return self.email

    @classmethod
    def create_by_dict(cls, post_data):
        return DoctorModel.create(
            # uid=str(uuid.uuid4()),
            firstname=post_data.get('firstname'),
            lastname=post_data.get('lastname'),
            email=post_data.get('email'),
            qualification=post_data.get('qualification', 'q'),
            profession=post_data.get('profession', 'p'),
            # need a better solution
            experience=int(post_data.get('experience', '0')),
            gender=post_data.get('gender', 'm'),
            )

    @classmethod
    def get_dict(cls, email):
        logger.debug('in DoctorModel.get_dict ')
        user_dict = {}
        try:
            user = DoctorModel.get(DoctorModel.email==email)

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
            logger.debug('after ger user: %s' % email)
            return user_dict

    @classmethod
    def update_by_dict(cls, email, post_data):
        user = DoctorModel.get(DoctorModel.email==email)
        with database.atomic():
            q = DoctorModel.update(
                firstname=post_data.get('firstname', user.firstname),
                lastname=post_data.get('lastname', user.lastname),
                qualification=post_data.get('qualification', user.qualification),
                profession=post_data.get('profession', user.profession),
                experience=int(post_data.get('experience', user.experience)),
                gender=post_data.get('gender', user.gender),
                ).where(DoctorModel.email==email)
            q.execute()


class PatientModel(BaseModel):
    """
    {
        'first_name':'',
        'last_name':'',
        'birthdate':'',
        'mobile_phone','',
        'email':'',
        'address':'',
        'gender':'',
        'height':'',
        'weight':'',
        'blood_group':'',
        'occupation':'',
        'marriage':'',
        'reference':'',
        'doctor_in_charge':'',
        'allergy':[],
        'accompanied_by':'',
    }
    """
    # uid = CharField(unique=True)
    email = CharField(max_length=100, unique=True)
    firstname = CharField(max_length=100)
    lastname = CharField(max_length=100)
    # email = CharField()
    birthdate = CharField()
    address = CharField()
    mobile_phone = CharField()
    gender = CharField()
    height = IntegerField()
    weight = IntegerField()
    blood_group = CharField()
    occupation = CharField()
    marriage = CharField()
    reference = CharField(max_length=100)
    doctor_in_charge = CharField()
    allergy = CharField()
    accompanied_by = CharField()

    class Meta:
        order_by = ('lastname',)

    def __str__(self):
        return self.email

    @classmethod
    def create_by_dict(cls, post_data):
        return PatientModel.create(
            # uid = str(uuid.uuid4()),
            firstname = post_data.get('firstname'),
            lastname = post_data.get('lastname'),
            birthdate = post_data.get('birthdate', '2015'),
            email = post_data.get('email', 'no'),
            address = post_data.get('address', 'add'),
            mobile_phone = post_data.get('mobile_phone', 138),
            blood_group = post_data.get('blood_group', 'a'),
            gender = post_data.get('gender', 'm'),
            height = post_data.get('height', 170),
            weight = post_data.get('weight', 180),
            occupation = post_data.get('occupation', '111'),
            marriage = post_data.get('marriage', 'y'),
            reference = post_data.get('reference', '1'),
            doctor_in_charge = post_data.get('doctor_in_charge', '1'),
            allergy = post_data.get('allergy', '1'),
            accompanied_by = post_data.get('accompanied_by', '1'),
            )

    @classmethod
    def get_dict(cls, email):
        logger.debug('in PatientModel.get_dict ')
        user_dict = {}
        try:
            user = PatientModel.get(PatientModel.email==email)

        except Exception as ex:
            logger.debug('in PatientModel.get_dict exception, ', ex)
            raise UserNotExistException()
        else:
            user_dict['firstname'] = user.firstname
            user_dict['lastname'] = user.lastname
            user_dict['email'] = user.email
            user_dict['birthdate'] = user.birthdate
            user_dict['address'] = user.address
            user_dict['mobile_phone'] = user.mobile_phone
            user_dict['gender'] = user.gender
            user_dict['height'] = user.height
            user_dict['weight'] = user.weight
            user_dict['occupation'] = user.occupation
            user_dict['marriage'] = user.marriage
            user_dict['reference'] = user.reference
            user_dict['doctor_in_charge'] = user.doctor_in_charge
            user_dict['allergy'] = user.allergy
            user_dict['accompanied_by'] = user.accompanied_by
            logger.debug('after ger user: %s' % email)
            return user_dict


    @classmethod
    def update_by_dict(cls, email, post_data):
        user = PatientModel.get(PatientModel.email==email)
        with database.atomic():
            q = PatientModel.update(
                firstname=post_data.get('firstname', user.firstname),
                lastname=post_data.get('lastname', user.lastname),
                gender=post_data.get('gender', user.gender),
                birthdate = post_data.get('birthdate', user.birthdate),
                address = post_data.get('address', user.address),
                mobile_phone = post_data.get('mobile_phone', user.mobile_phone),
                blood_group = post_data.get('blood_group', user.blood_group),
                height = int(post_data.get('height', user.height)),
                weight = int(post_data.get('weight', user.weight)),
                occupation = post_data.get('occupation', user.occupation),
                marriage = post_data.get('marriage', user.marriage),
                reference = post_data.get('reference', user.reference),
                doctor_in_charge = post_data.get('doctor_in_charge', user.doctor_in_charge),
                allergy = post_data.get('allergy', user.allergy),
                accompanied_by = post_data.get('accompanied_by', user.accompanied_by),
                ).where(PatientModel.email==email)
            q.execute()


class ObjectModel(BaseModel):
    """

    """
    patient = models.ForeignKey(PatientModel)

    objid = CharField(unique=True)
    description = TextField()
    datetime = CharField(max_length=100)

    class Meta:
        order_by = ('objid',)

    def __str__(self):
        return self.patient + '/' + self.objid


if __name__ == '__main__':
    create_tables(conf)
