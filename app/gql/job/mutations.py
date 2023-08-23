from graphene import Boolean, Field, Int, Mutation, String

from app.db.database import Session
from app.db.models import Job
from app.gql.types import JobObject
from app.utils import admin_user


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)
        
    job = Field(lambda: JobObject)
    
    @admin_user
    def mutate(root, info, title, description, employer_id):
        with Session() as session:
            job = Job(
                title=title,
                description=description,
                employer_id=employer_id,
            )
            session.add(job)
            session.commit()
            session.refresh(job)
            return AddJob(job=job)
        
        
class UpdateJob(Mutation):
    class Arguments:
        id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()
        
    job = Field(lambda: JobObject)
    
    @admin_user
    def mutate(root, info, id, title=None, description=None, employer_id=None):
        with Session() as session:
            job = session.query(Job).filter(Job.id == id).first()
            #job = session.query(Job).options(joinedload(Job.employer)).filter(Job.id == id).first()
            if not job:
                raise Exception("Job not found")
            
            if title:
                job.title = title
            if description:
                job.description = description
            if employer_id:
                job.employer_id = employer_id
            
            session.commit()
            session.refresh(job)
            return UpdateJob(job=job)
        
        
class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)
        
    success = Boolean() # we just want to report the status of the deletion
    
    @admin_user
    def mutate(root, info, id):
        with Session() as session:
            job = session.query(Job).filter(Job.id == id).first()
            
            if not job:
                raise Exception("Job not found")
            
            session.delete(job)
            session.commit()
            return DeleteJob(success=True)