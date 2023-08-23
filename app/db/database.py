from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.data import employers_data, jobs_data, users_data, applications_data
from app.db.models import Base, Employer, Job, User, JobApplication
from app.config.settings import DB_URL


engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)


def prepare_database():
    from app.utils import hash_password
    
    Base.metadata.drop_all(engine) # drop all tables from declarative Base
    Base.metadata.create_all(engine) # create all tables from declarative Base
    
    session = Session()
    
    for employer in employers_data:
        emp = Employer(**employer)
        session.add(emp)

    for job in jobs_data:
        session.add(Job(**job))
        
    for user in users_data:
        user['hashed_password'] = hash_password(user['password'])
        del user['password']
        session.add(User(**user))
        
    for app in applications_data:
        session.add(JobApplication(**app))
        
    session.commit()
    session.close()