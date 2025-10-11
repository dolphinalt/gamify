from flask import Blueprint, request, jsonify
from extensions import db
from models import Event
from datetime import datetime

api_bp = Blueprint('api', __name__)

# Event Routes
@api_bp.route('/events', methods=['GET'])
def get_events():
    """
    Get all events, optionally filtered by date range

    Query Parameters:
        start_date (str): ISO 8601 formatted start date to filter events (optional).
        end_date (str): ISO 8601 formatted end date to filter events (optional).

    Returns:
        Response: JSON array of events with HTTP status 200.
    """

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    stmt = db.select(Event)

    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        stmt = stmt.where(Event.start_time >= start_dt)

    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        stmt = stmt.where(Event.end_time <= end_dt)

    stmt = stmt.order_by(Event.start_time)

    events = db.session.scalars(stmt).all()

    return jsonify([event.to_dict() for event in events]), 200


@api_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """
    Get a single event by ID

    Path Parameters:
        event_id (int): ID of the event to retrieve.

    Returns:
        Response: JSON object of the event with HTTP status 200.
        Response: Error message with HTTP status 404 if event not found.
    """

    event = db.get_or_404(Event, event_id)
    return jsonify(event.to_dict()), 200


@api_bp.route('/events', methods=['POST'])
def create_event():
    """
    Create a new event

    Request Body (JSON):
        title (str): Title of the event (required).
        description (str): Description of the event (optional).
        start_time (str): ISO 8601 formatted start time of the event (required).
        end_time (str): ISO 8601 formatted end time of the event (required).
        location (str): Location of the event (optional).
        all_day (bool): Whether the event lasts all day (optional, default: False).

    Returns:
        Response: JSON object of the created event with HTTP status 201.
        Response: Error message with HTTP status 400 if required fields are missing.
        Response: Error message with HTTP status 500 for server errors.
    """

    data = request.get_json()

    try:
        event = Event(
            title=data['title'],
            description=data.get('description'),
            start_time=datetime.fromisoformat(data['start_time'].replace('Z', '+00:00')),
            end_time=datetime.fromisoformat(data['end_time'].replace('Z', '+00:00')),
            location=data.get('location'),
            all_day=data.get('all_day', False)
        )

        db.session.add(event)
        db.session.commit()

        return jsonify(event.to_dict()), 201

    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """
    Update an existing event

    Path Parameters:
        event_id (int): ID of the event to update.

    Request Body (JSON):
        title (str): Updated title of the event (optional).
        description (str): Updated description of the event (optional).
        start_time (str): Updated ISO 8601 formatted start time of the event (optional).
        end_time (str): Updated ISO 8601 formatted end time of the event (optional).
        location (str): Updated location of the event (optional).
        all_day (bool): Updated all-day status of the event (optional).

    Returns:
        Response: JSON object of the updated event with HTTP status 200.
        Response: Error message with HTTP status 500 for server errors.
    """

    event = db.get_or_404(Event, event_id)
    data = request.get_json()

    try:
        if 'title' in data:
            event.title = data['title']
        if 'description' in data:
            event.description = data['description']
        if 'start_time' in data:
            event.start_time = datetime.fromisoformat(data['start_time'])
        if 'end_time' in data:
            event.end_time = datetime.fromisoformat(data['end_time'])
        if 'location' in data:
            event.location = data['location']
        if 'all_day' in data:
            event.all_day = data['all_day']

        db.session.commit()
        return jsonify(event.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """
    Delete an event

    Path Parameters:
        event_id (int): ID of the event to delete.

    Returns:
        Response: Success message with HTTP status 204 if deletion is successful.
        Response: Error message with HTTP status 500 for server errors.
    """

    event = db.get_or_404(Event, event_id)

    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully'}), 204

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500