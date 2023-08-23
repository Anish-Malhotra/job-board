from graphene import Field, Int, Mutation, String
from graphql import GraphQLError

from app.db.database import Session
from app.db.models import Job, JobApplication, User
from app.gql.types import JobApplicationObject, UserObject
from app.utils import authd_user_same_as, generate_token, get_authenticated_user, hash_password, verify_password


class LoginUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)
        
    token = String()
    
    @staticmethod
    def mutate(root, info, email, password):
        with Session() as session:
            user = session.query(User).filter(User.email == email).first()
            
            if not user:
                raise GraphQLError('A user by that email does not exist')
            
            verify_password(user.hashed_password, password)
            
            token = generate_token(user.email, user.role)
            return LoginUser(token=token)
        
        
class AddUser(Mutation):
    class Arguments:
        email = String(required=True)
        username = String(required=True)
        password = String(required=True)
        role = String(required=True)
        
    user = Field(lambda: UserObject)
    
    @staticmethod
    def mutate(root, info, email, username, password, role):
        current_user = get_authenticated_user(info.context)
        with Session as session:
            existing_user = session.query(User).filter(User.email == email).first()
            
            if existing_user is not None:
                raise GraphQLError('User with that email already exists')
            if role == 'admin':
                if current_user.role != 'admin':
                    raise GraphQLError('Admins can only be registered by admins')
            
            hashed_password = hash_password(password)
            
            user = User(
                email=email,
                username=username,
                hashed_password=hashed_password,
                role=role,
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
            return AddUser(user=user)
        
        
class ApplyToJob(Mutation):
    class Arguments:
        user_id = Int(required=True)
        job_id = Int(required=True)
        
    job_application = Field(lambda: JobApplicationObject)
    
    @authd_user_same_as
    def mutate(root, info, user_id, job_id):
        with Session() as session:
            job = session.query(Job).filter(Job.id == job_id).first()
            if job is None:
                raise GraphQLError(f"Job {job_id} does not exist")
            
            existing_application = session.query(JobApplication).filter(
                JobApplication.job_id == job_id,
                JobApplication.user_id == user_id
            ).first()
            
            if existing_application:
                raise GraphQLError(f"User has already applied to job {job_id}")
            
            application = JobApplication(
                user_id=user_id, job_id=job_id,
            )
            
            session.add(application)
            session.commit()
            session.refresh(application)
            return ApplyToJob(job_application=application)