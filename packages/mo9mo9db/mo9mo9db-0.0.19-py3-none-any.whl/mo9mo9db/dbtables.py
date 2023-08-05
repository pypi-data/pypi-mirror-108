from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

from mo9mo9db.base_mixin import DBBaseMixin
from mo9mo9db.dbsession import get_db_engine

engine = get_db_engine()
Base = declarative_base()


class Studytimelogs(DBBaseMixin, Base):
    study_dt = Column(DateTime, unique=False)
    guild_id = Column(String(20), unique=False)
    member_id = Column(String(20), unique=False)
    voice_id = Column(String(20), unique=False)
    access = Column(String(10), unique=False)
    studytime_min = Column(Integer, unique=False)
    studytag_no = Column(String(10), unique=False)
    excluded_record = Column(Boolean)

    def __init__(self,
                 study_dt=None,
                 guild_id=None,
                 member_id=None,
                 voice_id=None,
                 access=None,
                 studytime_min=None,
                 studytag_no=None,
                 excluded_record=None):
        self.study_dt = study_dt
        self.guild_id = guild_id
        self.member_id = member_id
        self.access = access
        self.voice_id = voice_id
        self.studytime_min = studytime_min
        self.studytag_no = studytag_no
        self.excluded_record = excluded_record


class Studymembers(DBBaseMixin, Base):
    guild_id = Column(String(20), unique=False)
    member_id = Column(String(20), unique=True, primary_key=True)
    member_name = Column(String(50))
    joined_dt = Column(DateTime, unique=False)
    enrollment = Column(Boolean)

    def __init__(self,
                 guild_id=None,
                 member_id=None,
                 member_name=None,
                 joined_dt=None,
                 enrollment=None):
        self.guild_id = guild_id
        self.member_id = member_id
        self.member_name = member_name
        self.joined_dt = joined_dt
        self.enrollment = enrollment


class Times(DBBaseMixin, Base):
    guild_id = Column(String(20), unique=False)
    member_id = Column(String(20), unique=True)
    times_id = Column(String(20), unique=True)
    def __init__(self,
                 guild_id=None,
                 member_id=None,
                 times_id=None,):
        self.guild_id = guild_id
        self.member_id = member_id
        self.times_id = times_id


class Membersexperience(DBBaseMixin, Base):
    member_id = Column(String(20), unique=True)
    level = Column(Integer, unique=False)
    experience_studytime = Column(Integer, unique=False)

    def __init__(self,
                 member_id=None,
                 level=None,
                 experience_studytime=None):
        self.member_id = member_id
        self.level = level
        self.experience_studytime = experience_studytime


class Experiencevaluetable(DBBaseMixin, Base):
    levels = Column(Integer, unique=True)
    experience_min = Column(Integer, unique=False)
    experience_max = Column(Integer, unique=False)

    def __init__(self,
                 levels=None,
                 experience_min=None,
                 experience_max=None,):
        self.levels = levels
        self.experience_min = experience_min
        self.experience_max = experience_max


# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
