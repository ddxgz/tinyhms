import datetime
import uuid

from peewee import (SqliteDatabase, Model, CharField, BooleanField, IntegerField,
    TextField, ForeignKeyField, CompositeKey, MySQLDatabase)

from tinyhms.config import conf
from tinyhms.utils import logger
from tinyhms.hmsexceptions import UserNotExistException



# create a peewee database instance -- our models will use this database to
# persist information
# if conf.db_type == 'sqlite3':
#     database = SqliteDatabase('{}.sqlite3'.format(conf.db_filename))
# elif conf.db_type == 'mysql':
#     logger.error('MySQL support is not implemented yet!')


def point_db(config):
    if config.db_type == 'sqlite3':
        # print('using sqlite ')
        database = SqliteDatabase('{}.sqlite3'.format(config.db_filename))
    elif config.db_type == 'mysql':
        database = MySQLDatabase('mysql', host='192.168.59.200',
            user="root",passwd="root")
    return database


def create_tables(config, create_initdata=False):
    database = point_db(config)
    database.connect()
    database.create_tables([DoctorModel, PatientModel, ObjectModel,
        PrescriptionModel, CommentModel, DischargeModel, LoginModel], safe=True)
    if create_initdata:
        LoginModel.create(
            username='admin',
            password='admin',
            role='admin'
            )
    return database
    # database.create_tables([DoctorModel])


database = point_db(conf)


class BaseModel(Model):
    class Meta:
        database = database


class DoctorModel(BaseModel):
    """
    {
            'first_name':'',
            'last_name':'',
            'qualification':'',
            'profession': 'xxx',
            'experience':'',
            'gender':'',
            'schedule':'',

    }
    """
    # uid = CharField(unique=True)
    email = CharField(max_length=100, unique=True)
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    qualification = CharField(max_length=100)
    profession = CharField(max_length=100)
    birth = CharField(max_length=100)
    experience = IntegerField()
    gender = CharField(max_length=10)
    patients = TextField()

    class Meta:
        order_by = ('last_name',)

    def __str__(self):
        return self.email

    @classmethod
    def create_by_dict(cls, post_data):
        return DoctorModel.create(
            # uid=str(uuid.uuid4()),
            first_name=post_data.get('first_name'),
            last_name=post_data.get('last_name'),
            # change after dev
            email=post_data.get('email', '{}@doctor.hms.com'.format(
                post_data.get('first_name')+post_data.get('last_name'))),
            qualification=post_data.get('qualification', 'q'),
            profession=post_data.get('profession', 'p'),
            birth=post_data.get('birth', ''),
            # need a better solution
            experience=int(post_data.get('experience', '0')),
            gender=post_data.get('gender', 'm'),
            patients=post_data.get('patients', '')
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
            user_dict['first_name'] = user.first_name
            user_dict['last_name'] = user.last_name
            user_dict['email'] = user.email
            user_dict['qualification'] = user.qualification
            user_dict['profession'] = user.profession
            user_dict['birth'] = user.birth
            user_dict['experience'] = str(user.experience)
            user_dict['gender'] = user.gender
            user_dict['patients'] = user.patients
            logger.debug('after ger user: %s' % email)
            return user_dict

    @classmethod
    def update_by_dict(cls, email, post_data):
        user = DoctorModel.get(DoctorModel.email==email)
        with database.atomic():
            q = DoctorModel.update(
                first_name=post_data.get('first_name', user.first_name),
                last_name=post_data.get('last_name', user.last_name),
                qualification=post_data.get('qualification', user.qualification),
                profession=post_data.get('profession', user.profession),
                birth=post_data.get('birth', user.birth),
                experience=int(post_data.get('experience', user.experience)),
                gender=post_data.get('gender', user.gender),
                patients=post_data.get('patients', user.patients),
                ).where(DoctorModel.email==email)
            q.execute()


class PatientModel(BaseModel):
    # uid = CharField(unique=True)
    email = CharField(max_length=100, unique=True)
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    # email = CharField()
    birthdate = CharField()
    address = CharField()
    mobile_phone = CharField()
    gender = CharField()
    # height = IntegerField()
    # weight = IntegerField()
    height = CharField()
    weight = CharField()
    blood_group = CharField()
    occupation = CharField()
    marriage = CharField()
    reference = CharField(max_length=100)
    doctor_in_charge = CharField()
    allergy = CharField()
    accompanied_by = CharField()
    billing = CharField(max_length=30)

    class Meta:
        order_by = ('last_name',)

    def __str__(self):
        return self.email

    @classmethod
    def create_by_dict(cls, post_data):
        return PatientModel.create(
            # uid = str(uuid.uuid4()),
            first_name = post_data.get('first_name'),
            last_name = post_data.get('last_name'),
            birthdate = post_data.get('birthdate', '2015'),
            # email = post_data.get('email', 'no'),
            email=post_data.get('email', '{}@patient.hms.com'.format(
                post_data.get('first_name')+post_data.get('last_name'))),
            address = post_data.get('address', 'add'),
            mobile_phone = post_data.get('mobile_phone', '138'),
            blood_group = post_data.get('blood_group', 'a'),
            gender = post_data.get('gender', 'm'),
            height = post_data.get('height', '170'),
            weight = post_data.get('weight', '180'),
            occupation = post_data.get('occupation', '111'),
            marriage = post_data.get('marriage', 'y'),
            reference = post_data.get('reference', '1'),
            doctor_in_charge = post_data.get('doctor_in_charge', '1'),
            allergy = post_data.get('allergy', '1'),
            accompanied_by = post_data.get('accompanied_by', '1'),
            billing = post_data.get('billing', 'cash'),
            )

    @classmethod
    def get_dict(cls, email):
        logger.debug('in PatientModel.get_dict:{} '.format(email))
        user_dict = {}
        try:
            user = PatientModel.get(PatientModel.email==email)

        except Exception as ex:
            logger.debug('in PatientModel.get_dict exception, ', ex)
            raise UserNotExistException()
        else:
            user_dict['first_name'] = user.first_name
            user_dict['last_name'] = user.last_name
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
            user_dict['billing'] = user.billing
            logger.debug('after ger user: %s' % email)
            return user_dict


    @classmethod
    def update_by_dict(cls, email, post_data):
        user = PatientModel.get(PatientModel.email==email)
        with database.atomic():
            q = PatientModel.update(
                first_name=post_data.get('first_name', user.first_name),
                last_name=post_data.get('last_name', user.last_name),
                gender=post_data.get('gender', user.gender),
                birthdate = post_data.get('birthdate', user.birthdate),
                address = post_data.get('address', user.address),
                mobile_phone = post_data.get('mobile_phone', user.mobile_phone),
                blood_group = post_data.get('blood_group', user.blood_group),
                # height = int(post_data.get('height', user.height)),
                # weight = int(post_data.get('weight', user.weight)),
                height = post_data.get('height', user.height),
                weight = post_data.get('weight', user.weight),
                occupation = post_data.get('occupation', user.occupation),
                marriage = post_data.get('marriage', user.marriage),
                reference = post_data.get('reference', user.reference),
                doctor_in_charge = post_data.get('doctor_in_charge', user.doctor_in_charge),
                allergy = post_data.get('allergy', user.allergy),
                accompanied_by = post_data.get('accompanied_by', user.accompanied_by),
                billing = post_data.get('billing', user.billing),
                ).where(PatientModel.email==email)
            q.execute()


class ObjectModel(BaseModel):
    """

    """
    patient = ForeignKeyField(PatientModel)

    objid = CharField(unique=True)
    objname = CharField(max_length=100)
    description = TextField()
    datetime = CharField(max_length=100)

    class Meta:
        order_by = ('objid',)

    def __str__(self):
        return str(self.patient) + '/' + str(self.objid)

    @classmethod
    def create_by_dict(cls, patientid, post_data):
        user = PatientModel.get(PatientModel.email==patientid)
        logger.debug(type(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        return ObjectModel.create(
            # uid=str(uuid.uuid4()),
            patient=user,
            objid=patientid + '-' + post_data.get('objname')+ '-' + \
                post_data.get('datetime', datetime.datetime.now().strftime('%Y%m%d%H%M%S')),
            objname=post_data.get('objname'),
            description=post_data.get('description', 'p'),
            datetime=post_data.get('datetime', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            )


class PrescriptionModel(BaseModel):
    """

    """
    patient = ForeignKeyField(PatientModel)
    drug_id = CharField(unique=True)
    datetime = CharField(max_length=100)
    drug_name = CharField(max_length=100)
    after_meal = CharField(max_length=10)
    amount = IntegerField()
    dosage_per_day = IntegerField()
    response_doctor = CharField(max_length=200)
    description = TextField()

    class Meta:
        order_by = ('drug_id',)

    def __str__(self):
        return str(self.drug_id)

    @classmethod
    def create_by_dict(cls, patientid, doctorid, post_data):
        user = PatientModel.get(PatientModel.email==patientid)
        logger.debug(type(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        return PrescriptionModel.create(
            # uid=str(uuid.uuid4()),
            patient=user,
            response_doctor=doctorid,
            drug_id=patientid + '-' + post_data.get('drug_name')+ '-' + \
                post_data.get('datetime', datetime.datetime.now().strftime('%Y%m%d%H%M%S')),
            datetime=post_data.get('datetime', datetime.datetime.now().strftime('%Y%m%d%H%M%S')),
            drug_name=post_data.get('drug_name'),
            after_meal=post_data.get('after_meal'),
            amount=post_data.get('amount'),
            dosage_per_day=post_data.get('dosage_per_day'),
            description=post_data.get('description', ''),
            )


class CommentModel(BaseModel):
    """

    """
    patient = ForeignKeyField(PatientModel)
    comment_id = CharField(unique=True)
    datetime = CharField(max_length=100)
    comment = TextField()
    response_doctor = CharField(max_length=200)

    class Meta:
        order_by = ('comment_id',)

    def __str__(self):
        return str(self.comment_id)

    @classmethod
    def create_by_dict(cls, patientid, doctorid, post_data):
        user = PatientModel.get(PatientModel.email==patientid)
        logger.debug(type(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        return CommentModel.create(
            # uid=str(uuid.uuid4()),
            patient=user,
            response_doctor=doctorid,
            comment_id=patientid + '-' + doctorid + '-' + \
                post_data.get('datetime', datetime.datetime.now().strftime('%Y%m%d%H%M%S')),
            datetime=post_data.get('datetime', datetime.datetime.now().strftime('%Y%m%d%H%M%S')),
            comment=post_data.get('comment'),
            )


class DischargeModel(BaseModel):
    """

    """
    patient = ForeignKeyField(PatientModel)
    discharge_id = CharField(unique=True)
    datetime = CharField(max_length=100)
    room = CharField(max_length=100)
    bed = CharField(max_length=100)
    indate = CharField(max_length=100)
    outdate = CharField(max_length=100)
    response_doctor = CharField(max_length=200)
    description = TextField()

    class Meta:
        order_by = ('discharge_id',)

    def __str__(self):
        return str(self.discharge_id)

    @classmethod
    def create_by_dict(cls, patientid, doctorid, post_data):
        user = PatientModel.get(PatientModel.email==patientid)
        logger.debug(type(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        return DischargeModel.create(
            # uid=str(uuid.uuid4()),
            patient=user,
            response_doctor=doctorid,
            discharge_id=patientid + '-' + doctorid + '-' + \
                post_data.get('indate', datetime.datetime.now().strftime('%Y%m%d%H%M%S')),
            datetime=post_data.get('datetime', datetime.datetime.now().strftime('%Y%m%d%H%M%S')),
            indate=post_data.get('indate', datetime.datetime.now().strftime('%Y%m%d')),
            room=post_data.get('room', 'not assigned'),
            bed=post_data.get('bed', 'not assigned'),
            outdate=post_data.get('outdate', 'not yet'),
            description=post_data.get('description', 'no description'),
            )

    @classmethod
    def update_by_dict(cls, patientid, doctorid, indate, post_data):
        discharge = DischargeModel.get(DischargeModel.discharge_id==patientid + '-' + doctorid + '-' + \
            indate)
        with database.atomic():
            q = DischargeModel.update(
                indate=discharge.indate,
                outdate=post_data.get('outdate', ''),
                response_doctor=post_data.get('response_doctor', discharge.response_doctor),
                room = post_data.get('room', discharge.room),
                bed = post_data.get('bed', discharge.bed),
                description = post_data.get('description', discharge.description),

                datetime=post_data.get('datetime', datetime.datetime.now().strftime('%Y%m%d%H%M%S')),
                ).where(DischargeModel.discharge_id==patientid + '-' + doctorid + '-' + \
                    indate)
            q.execute()


class LoginModel(BaseModel):
    """

    """

    username = CharField(max_length=100, unique=True)
    password = CharField(max_length=100)
    role = CharField(max_length=100)

    # class Meta:
    #     primary_key = CompositeKey('username', 'role')
    def __str__(self):
        return str(self.username)

    @classmethod
    def create_by_dict(cls, role, post_data):
        logger.debug('str(uuid.uuid4().hex[0:6]:{}'.format(str(uuid.uuid4().hex[0:6])))

        return LoginModel.create(

            # change after dev
            username=post_data.get('email', '{}@{}.hms.com'.format(
                post_data.get('first_name')+post_data.get('last_name'), role)),
            role=role,
            password=post_data.get('last_name') + str(uuid.uuid4().hex[0:6])
            )

    # @classmethod
    # def get_dict(cls, email):
    #     logger.debug('in DoctorModel.get_dict ')
    #     user_dict = {}
    #     try:
    #         user = DoctorModel.get(DoctorModel.email==email)
    #
    #     except Exception as ex:
    #         logger.debug('in DoctorModel.get_dict exception, ', ex)
    #         raise UserNotExistException()
    #     else:
    #         user_dict['first_name'] = user.first_name
    #         user_dict['last_name'] = user.last_name
    #         user_dict['email'] = user.email
    #         user_dict['qualification'] = user.qualification
    #         user_dict['profession'] = user.profession
    #         user_dict['birth'] = user.birth
    #         user_dict['experience'] = str(user.experience)
    #         user_dict['gender'] = user.gender
    #         user_dict['patients'] = user.patients
    #         logger.debug('after ger user: %s' % email)
    #         return user_dict

    # @classmethod
    # def update_by_dict(cls, email, post_data):
    #     user = DoctorModel.get(DoctorModel.email==email)
    #     with database.atomic():
    #         q = DoctorModel.update(
    #             first_name=post_data.get('first_name', user.first_name),
    #             last_name=post_data.get('last_name', user.last_name),
    #             qualification=post_data.get('qualification', user.qualification),
    #             profession=post_data.get('profession', user.profession),
    #             birth=post_data.get('birth', user.birth),
    #             experience=int(post_data.get('experience', user.experience)),
    #             gender=post_data.get('gender', user.gender),
    #             patients=post_data.get('patients', user.patients),
    #             ).where(DoctorModel.email==email)
    #         q.execute()


if __name__ == '__main__':
    create_tables(conf)
