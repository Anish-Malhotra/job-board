from graphene import Field, Int, List, ObjectType
from sqlalchemy.orm import joinedload

from app.db.database import Session
from app.db.models import Employer, Job, JobApplication, User
from app.gql.types import EmployerObject, JobApplicationObject, JobObject, UserObject


class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject, id=Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id=Int(required=True))
    users = List(UserObject)
    applications = List(JobApplicationObject)
    
    @staticmethod
    def resolve_jobs(root, info):
        with Session() as session:
            return session.query(Job).all()
        
    @staticmethod
    def resolve_job(root, info, id):
        with Session() as session:
            return session.query(Job).filter(Job.id == id).first()
    
    @staticmethod
    def resolve_employers(root, info):
        with Session() as session:
            return session.query(Employer).all()
        
    @staticmethod
    def resolve_employer(root, info, id):
        with Session() as session:
            return session.query(Employer).filter(Employer.id == id).first()
        
    @staticmethod
    def resolve_users(root, info):
        with Session() as session:
            return session.query(User).all()
        
    @staticmethod
    def resolve_applications(root, info):
        with Session() as session:
            return session.query(JobApplication).all()
