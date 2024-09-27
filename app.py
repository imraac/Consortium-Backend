from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Registration, ContactDetail, Consortium

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Change this to your preferred database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Create an API endpoint for registration
@app.route('/api/registration', methods=['POST'])
def register_agency():
    data = request.get_json()

    # Validate incoming data
    if not all(key in data for key in (
        'agencyName', 'acronym', 'description', 'missionStatement', 
        'website', 'isNGO', 'yearsOperational', 'reasonToJoin', 
        'participatesInConsortium', 'understandsPrinciples')):
        return jsonify({'error': 'Missing data'}), 400

    # Create a new registration instance
    registration = Registration(
        agency_name=data['agencyName'],
        acronym=data.get('acronym'),  # Optional
        description=data['description'],
        mission_statement=data['missionStatement'],
        website=data['website'],
        is_ngo=data['isNGO'],
        years_operational=data['yearsOperational'],
        reason_to_join=data['reasonToJoin'],
        participates_in_consortium=data['participatesInConsortium'],
        understands_principles=data['understandsPrinciples'],
    )

    # Add to the session and commit
    db.session.add(registration)
    db.session.commit()

    return jsonify({'message': 'Registration successful!', 'id': registration.id}), 201

@app.route('/api/contact-details', methods=['POST'])
def save_contact_details():
    data = request.get_json()

    # Validate incoming data
    if not all(key in data for key in ('founders', 'boardDirectors', 'keyStaffs')):
        return jsonify({'error': 'Missing data'}), 400

    # Save Founders
    for founder in data['founders']:
        new_contact = ContactDetail(
            name=founder['name'],
            contact=founder['contact'],
            clan=founder['clan'],
            role='founder'
        )
        db.session.add(new_contact)

    # Save Board Directors
    for director in data['boardDirectors']:
        new_contact = ContactDetail(
            name=director['name'],
            contact=director['contact'],
            clan=director['clan'],
            role='director'
        )
        db.session.add(new_contact)

    # Save Key Staffs
    for staff in data['keyStaffs']:
        new_contact = ContactDetail(
            name=staff['name'],
            contact=staff['contact'],
            clan=staff['clan'],
            role='staff'
        )
        db.session.add(new_contact)

    # Commit all the changes to the database
    db.session.commit()

    return jsonify({'message': 'Contact details saved successfully!'}), 201


@app.route('/api/consortium', methods=['POST'])
def save_consortium():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Create a new consortium instance
    new_consortium = Consortium(
        active_year=data.get('activeYear'),
        partner_ngos=data.get('partnerNGOs'),
        international_staff=data.get('internationalStaff'),
        national_staff=data.get('nationalStaff'),
        program_plans=data.get('programPlans'),
        main_donors=data.get('mainDonors'),
        annual_budget=data.get('annualBudget'),
        membership_type=data.get('membershipType')
    )

    try:
        db.session.add(new_consortium)  # Add to the session
        db.session.commit()  # Commit the transaction
        return jsonify({"message": "Data saved successfully!", "data": data}), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 400

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
