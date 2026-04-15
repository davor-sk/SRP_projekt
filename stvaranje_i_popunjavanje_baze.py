# Imports
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, insert, inspect
from sqlalchemy.orm import sessionmaker, declarative_base

CSV_FILE_PATH = r"C:\Users\Davor\OneDrive\Radna površina\FAKS\3. godina\SRP\projekt\2_relational_model\processed\student_mental_health_PROCESSED.csv"

df = pd.read_csv(CSV_FILE_PATH, delimiter=',')
print(f"CSV size: {df.shape}")  # Print dataset size
print(df.head())  # Preview first few rows

Base = declarative_base()

# Definiranje sheme baze podataka


class Student(Base):
    __tablename__ = 'student'
    student_id            = Column(Integer, primary_key=True)
    age                   = Column(Integer, nullable=False)
    gender                = Column(String(10), nullable=False)
    course                = Column(String(50), nullable=False)
    year                  = Column(String(10), nullable=False)
    attendance_percentage = Column(Float, nullable=False)
    cgpa                  = Column(Float, nullable=False)

class AcademicProfile(Base):
    __tablename__ = 'academic_profile'
    id                      = Column(Integer, primary_key=True, autoincrement=True)
    student_fk              = Column(Integer, ForeignKey('student.student_id'))
    daily_study_hours       = Column(Float, nullable=False)
    screen_time_hours       = Column(Float, nullable=False)
    academic_pressure_score = Column(Integer, nullable=False)

class HealthProfile(Base):
    __tablename__ = 'health_profile'
    id                      = Column(Integer, primary_key=True, autoincrement=True)
    student_fk              = Column(Integer, ForeignKey('student.student_id'))
    daily_sleep_hours       = Column(Float, nullable=False)
    sleep_quality           = Column(String(20), nullable=False)
    physical_activity_hours = Column(Float, nullable=False)
    stress_level            = Column(String(20), nullable=False)
    anxiety_score           = Column(Integer, nullable=False)
    depression_score        = Column(Integer, nullable=False)

class WellbeingProfile(Base):
    __tablename__ = 'wellbeing_profile'
    id                     = Column(Integer, primary_key=True, autoincrement=True)
    student_fk             = Column(Integer, ForeignKey('student.student_id'))
    financial_stress_score = Column(Integer, nullable=False)
    social_support_score   = Column(Integer, nullable=False)
    internet_quality       = Column(String(20), nullable=False)
    burnout_level          = Column(String(20), nullable=False)


# Spajanje na bazu i stvaranje tablica
print("="*50)
print("KORAK 1: Spajam se na bazu...")
engine = create_engine("mysql+pymysql://root:root@localhost/student_mental_health")

print("KORAK 2: Brišem postojeće tablice...")
Base.metadata.drop_all(engine)

print("KORAK 3: Kreiram nove tablice...")
Base.metadata.create_all(engine)

print("KORAK 4: Tablice kreirane, provjera...")
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tablice u bazi NAKON kreiranja: {tables}")
print("="*50)

Session = sessionmaker(bind=engine)
session = Session()


# Punjenje tablica podacima


# 1. Student
print("Umetanje studenata...")
student_data = df[['student_id', 'age', 'gender', 'course', 'year',
                    'attendance_percentage', 'cgpa']].drop_duplicates(subset='student_id')
student_list = [{str(k): v for k, v in row.items()} for row in student_data.to_dict(orient="records")]
session.execute(insert(Student), student_list)
session.commit()
print(f"  -> {len(student_list)} studenata umetnuto")

# 2. AcademicProfile
print("Umetanje akademskih profila...")
academic_data = df[['student_id', 'daily_study_hours',
                     'screen_time_hours', 'academic_pressure_score']].copy()
academic_data = academic_data.rename(columns={'student_id': 'student_fk'})
academic_list = [{str(k): v for k, v in row.items()} for row in academic_data.to_dict(orient="records")]
session.execute(insert(AcademicProfile), academic_list)
session.commit()
print(f"  -> {len(academic_list)} akademskih profila umetnuto")

# 3. HealthProfile
print("Umetanje zdravstvenih profila...")
health_data = df[['student_id', 'daily_sleep_hours', 'sleep_quality',
                   'physical_activity_hours', 'stress_level',
                   'anxiety_score', 'depression_score']].copy()
health_data = health_data.rename(columns={'student_id': 'student_fk'})
health_list = [{str(k): v for k, v in row.items()} for row in health_data.to_dict(orient="records")]
session.execute(insert(HealthProfile), health_list)
session.commit()
print(f"  -> {len(health_list)} zdravstvenih profila umetnuto")

# 4. WellbeingProfile
print("Umetanje profila dobrobiti...")
wellbeing_data = df[['student_id', 'financial_stress_score',
                      'social_support_score', 'internet_quality', 'burnout_level']].copy()
wellbeing_data = wellbeing_data.rename(columns={'student_id': 'student_fk'})
wellbeing_list = [{str(k): v for k, v in row.items()} for row in wellbeing_data.to_dict(orient="records")]
session.execute(insert(WellbeingProfile), wellbeing_list)
session.commit()
print(f"  -> {len(wellbeing_list)} profila dobrobiti umetnuto")

session.close()
print("=" * 50)
print("Podaci uspješno uneseni u bazu!")