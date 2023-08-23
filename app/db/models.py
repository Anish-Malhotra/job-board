from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Employer(Base):
    __tablename__ = "employers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    contact_email = Column(String(100))
    industry = Column(String(30))
    jobs = relationship("Job", back_populates="employer", lazy="joined")
    
    
class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30))
    description = Column(String(255))
    employer_id = Column(Integer, ForeignKey("employers.id"), nullable=False)
    employer = relationship("Employer", back_populates="jobs", lazy="joined")
    applications = relationship("JobApplication", back_populates="job", lazy="joined")
    
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30))
    hashed_password = Column(String(255))
    email = Column(String(100), unique=True)
    role = Column(String(30))
    applications = relationship("JobApplication", back_populates="user", lazy="joined")
    
    
class JobApplication(Base):
    __tablename__ = 'job_applications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    job = relationship("Job", back_populates="applications", lazy="joined")
    user = relationship("User", back_populates="applications", lazy="joined")