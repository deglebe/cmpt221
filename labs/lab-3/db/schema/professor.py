"""professor.py: create a table named professors in the marist database"""
from db.server import db

class Professor(db.Model):
    __tablename__ = 'Professors'
    ProfessorID = db.Column(db.Integer,primary_key=True, autoincrement=True)
    ProfessorFN = db.Column(db.String(40))
    ProfessorLN = db.Column(db.String(40))
    ProfessorEmail = db.Column(db.String(40))

    # create relationship with courses table. assoc table name = ProfessorCourse
    course = db.relationship('Courses', secondary = 'ProfessorCourse', back_populates = 'Professors')

    def __init__(self, first_name, last_name, email):
        self.ProfessorFN = first_name
        self.ProfessorLN = last_name
        self.ProfessorEmail = email

    def __repr__(self):
        return f"""
            PROFESSOR ID:   {self.ProfessorID}
            PROFESSOR NAME: {self.ProfessorFN} {self.ProfessorLN},
            EMAIL:          {self.ProfessorEmail}
        """
    
    def __repr__(self):
        return self.__repr__()
