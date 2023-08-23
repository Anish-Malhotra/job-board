from graphene import Field, Int, List, ObjectType, String


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject) # expression is not evaluated until runtime
    applications = List(lambda: JobApplicationObject)
    
    @staticmethod
    def resolve_employer(root, info):
        return root.employer
    
    @staticmethod
    def resolve_applications(root, info):
        return root.applications
    
    
class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)
    
    @staticmethod
    def resolve_jobs(root, info):
        return root.jobs
    
    
class UserObject(ObjectType):
    id = Int()
    username = String()
    #password = String() -> left out to not expose
    email = String()
    role = String()
    applications = List(lambda: JobApplicationObject)
    
    @staticmethod
    def resolve_applications(root, info):
        return root.applications
    
    
class JobApplicationObject(ObjectType):
    id = Int()
    job_id = Int()
    user_id = Int()
    job = Field(lambda: JobObject)
    user = Field(lambda: UserObject)
    
    @staticmethod
    def resolve_job(root, info):
        return root.job
    
    @staticmethod
    def resolve_user(root, info):
        return root.user