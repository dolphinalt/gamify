from flask import Blueprint, request, jsonify
from extensions import db
from models import Event
from datetime import datetime, timezone

api_bp = Blueprint('api', __name__)

def parse_datetime(date_string: str) -> datetime:
    """
    Parse datetime string and converts to UTC if needed.
    If date_string does not contain timezone information, it is assumed to be in UTC.
    Returns datetime object with UTC timezone information.
    """

    dt = datetime.fromisoformat(date_string)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)

    return dt

# Event Routes
@api_bp.route('/events', methods=['GET'])
def get_events():
    """
    Get all events, optionally filtered by date range

    Query Parameters:
        start_time (str): ISO 8601 formatted start time to filter events (optional).
        end_time (str): ISO 8601 formatted end time to filter events (optional).

    Returns:
        Response: JSON array of events with HTTP status 200.
        Response: Error message with HTTP status 400 if date format is invalid or date range is invalid.
    """

    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    stmt = db.select(Event)
    start_tm = None
    end_tm = None

    try:
        if start_time:
            start_tm = parse_datetime(start_time)
            stmt = stmt.where(Event.start_time >= start_tm)
        if end_time:
            end_tm = parse_datetime(end_time)
            stmt = stmt.where(Event.end_time <= end_tm)

    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDThh:mm:ss)'}), 400

    if start_tm and end_tm and end_tm < start_tm:
        return jsonify({'error': 'End time cannot be before start time'}), 400

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
        Response: Error message with HTTP status 500 for server errors.
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
        title = data.get('title', '').strip()
        if not title:
            return jsonify({'error': 'Title cannot be empty'}), 400

        if 'start_time' not in data or not data['start_time']:
            return jsonify({'error': 'Start time is required'}), 400
        if 'end_time' not in data or not data['end_time']:
            return jsonify({'error': 'End time is required'}), 400

        try:
            start_time = parse_datetime(data['start_time'])
            end_time = parse_datetime(data['end_time'])
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDThh:mm:ss)'}), 400

        if end_time < start_time:
            return jsonify({'error': 'End time cannot be before start time'}), 400

        print(f'before creating event: start_time = {start_time}')

        event = Event(
            title=title,
            description=data.get('description'),
            start_time=start_time,
            end_time=end_time,
            location=data.get('location'),
            all_day=data.get('all_day', False)
        )

        db.session.add(event)
        db.session.commit()

        print(f'after creating event: start time = {event.add_utc(event.start_time)}')

        return jsonify(event.to_dict()), 201

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
        title (str): Updated title of the event (optional), cannot be empty of provided.
        description (str): Updated description of the event (optional).
        start_time (str): Updated ISO 8601 formatted start time of the event (optional).
        end_time (str): Updated ISO 8601 formatted end time of the event (optional).
        location (str): Updated location of the event (optional).
        all_day (bool): Updated all-day status of the event (optional).

    Returns:
        Response: JSON object of the updated event with HTTP status 200.
        Response: Error message with HTTP status 400 if:
            - Title is provided and empty
            - Date format is invalid
            - End time is before start time
            - New start time is after existing end time
            - New end time is before existing start time
            - all_day field is not a boolean
        Response: Error message with HTTP status 404 if event is not found.
        Response: Error message with HTTP status 500 for server errors.
    """

    event = db.get_or_404(Event, event_id)
    data = request.get_json()

    try:
        if 'title' in data:
            title = data.get('title', '').strip()
            if not title:
                db.session.rollback()
                return jsonify({'error': 'Title cannot be empty'}), 400
            event.title = title

        if 'description' in data:
            event.description = data['description']

        new_start_time = None
        new_end_time = None

        if 'start_time' in data:
            try:
                new_start_time = parse_datetime(data['start_time'])
            except ValueError:
                db.session.rollback()
                return jsonify({'error': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDThh:mm:ss)'}), 400

        if 'end_time' in data:
            try:
                new_end_time = parse_datetime(data['end_time'])
            except ValueError:
                db.session.rollback()
                return jsonify({'error': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDThh:mm:ss)'}), 400

        if new_start_time and new_end_time:
            if new_end_time < new_start_time:
                db.session.rollback()
                return jsonify({'error': 'End time cannot be before start time'}), 400
        elif new_start_time and new_start_time > event.add_utc(event.end_time):
            db.session.rollback()
            return jsonify({'error': 'Start time cannot be after existing end time'}), 400
        elif new_end_time and new_end_time < event.add_utc(event.start_time):
            db.session.rollback()
            return jsonify({'error': 'End time cannot be before existing start time'}), 400

        if new_start_time:
            event.start_time = new_start_time
        if new_end_time:
            event.end_time = new_end_time

        if 'location' in data:
            event.location = data['location']

        if 'all_day' in data:
            if not isinstance(data['all_day'], bool):
                db.session.rollback()
                return jsonify({'error': 'all_day must be a boolean'}), 400
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
        Response: Empty response with HTTP status 204 if deletion is successful.
        Response: Error message with HTTP status 404 if event not found.
        Response: Error message with HTTP status 500 for server errors.
    """

    event = db.get_or_404(Event, event_id)

    try:
        db.session.delete(event)
        db.session.commit()
        return '', 204

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500