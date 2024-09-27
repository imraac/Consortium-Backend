# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agency_name = db.Column(db.String(255), nullable=False)
    acronym = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=False)
    mission_statement = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(255), nullable=False)
    is_ngo = db.Column(db.Boolean, default=False)
    years_operational = db.Column(db.Integer, nullable=False)
    reason_to_join = db.Column(db.Text, nullable=False)
    participates_in_consortium = db.Column(db.Boolean, default=False)
    understands_principles = db.Column(db.Boolean, default=False)


class ContactDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    clan = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'founder', 'director', or 'staff'

    def __repr__(self):
        return f'<ContactDetail {self.name}, {self.role}>'
    
class Consortium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active_year = db.Column(db.String(4), nullable=False)  # Store as string to handle years
    partner_ngos = db.Column(db.Text, nullable=False)  # Store as text for longer entries
    international_staff = db.Column(db.Integer, nullable=False)
    national_staff = db.Column(db.Integer, nullable=False)
    program_plans = db.Column(db.Text, nullable=False)
    main_donors = db.Column(db.Text, nullable=False)
    annual_budget = db.Column(db.String(20), nullable=False)  # Consider budget as string for formatting
    membership_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Consortium {self.active_year}>'

