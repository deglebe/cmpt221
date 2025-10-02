"""orm.py: sqlalchemy orm used to manage the Professors table"""
from db.server import get_session
from db.schema import Professor

"""Lab 4 - Part 2:
- Insert 3 records into the Professors table
- Update 1 record in the Professors table
- Delete 1 record in the Professors table
"""

def get_all_professors():
    """Select all records from the Professors table using SQLAlchemy ORM."""
    session = get_session()
    try:
        # get all entries in the Professors table
        professors = session.query(Professor).all()
        return professors
    
    finally:
        session.close()

def insert_professors():
    """Insert 3 records into the Professors table using SQLAlchemy ORM."""
    session = get_session()
    try:
        professor1 = Professor(FirstName="Donald", LastName="Schwartz", Email="donald.schwartz@marist.edu")
        professor2 = Professor(FirstName="Sandhya", LastName="Aneja", Email="sandhya.aneja@marist.edu")
        professor3 = Professor(FirstName="Heidemarie", LastName="Mueller", Email="heidemarie.mueller@marist.edu")

        session.add_all([professor1, professor2, professor3])
        # "save" the changes
        session.commit()

    except Exception as e:
        session.rollback()
        print("Error inserting professors:", e)

    finally:
        session.close()

def update_professor():
    """Update one record in the Professors table using SQLAlchemy ORM."""
    session = get_session()
    try:
        professor = session.query(Professor).filter(Professor.ProfessorID == 2).scalar_one_or_none()

        if professor:
            professor.FirstName = "Bowu"
            # "save" the changes
            session.commit()
        else:
            print(f"no professor found with that id")
    
    except Exception as e:
        session.rollback()
        print("Error updating professor:", e)
        
    finally:
        session.close()

def delete_professor():
    """Delete one record in the Professors table using SQLAlchemy ORM."""
    session = get_session()
    try:
        professor = session.query(Professor).filter(Professor.ProfessorID == 3).scalar_one_or_none()

        if professor:
            session.delete(professor)
            # "save" the changes
            session.commit()
        else:
            print(f"no professor found with that id")

    except Exception as e:
        session.rollback()
        print("Error updating professor:", e)

    finally:
        session.close()

