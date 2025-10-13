from flask import Blueprint, request, jsonify
from extensions import db
from models import Event, Task
from datetime import datetime, timezone

api_bp = Blueprint('api', __name__)

def parse_datetime(date_string: str) -> datetime:
    """
    Parse datetime string and converts to UTC if needed, then returns a UTC datetime object.
    """

    dt = datetime.fromisoformat(date_string)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt



##################### Event Routes #####################
@api_bp.route('/events', methods=['GET'])
def get_events():
    """
    Get all events, optionally filtered by date range

    Query Parameters:
        start (str): ISO 8601 formatted start time to filter events (optional).
        end (str): ISO 8601 formatted end time to filter events (optional).

    Returns:
        Response: JSON array of events with HTTP status 200.
        Response: Error message with HTTP status 400 if date format is invalid or date range is invalid.
    """

    start = request.args.get('start')
    end = request.args.get('end')

    stmt = db.select(Event)
    start_dt = None
    end_dt = None

    try:
        if start:
            start_dt = parse_datetime(start)
            stmt = stmt.where(Event.end_time > start_dt)
        if end:
            end_dt = parse_datetime(end)
            stmt = stmt.where(Event.start_time < end_dt)
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDThh:mm:ss)'}), 400

    if start_dt and end_dt and end_dt < start_dt:
        return jsonify({'error': 'End time cannot be before start time'}), 400

    events = db.session.scalars(stmt.order_by(Event.start_time)).all()

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

        event = Event(
            title=title,
            description=data.get('description', None),
            start_time=start_time,
            end_time=end_time,
            location=data.get('location', None),
            all_day=data.get('all_day', False)
        )

        db.session.add(event)
        db.session.commit()

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
        title (str): Updated title of the event (optional); cannot be empty if provided.
        start_time (str): Updated ISO 8601 formatted start time of the event (optional); cannot be empty if provided.
        end_time (str): Updated ISO 8601 formatted end time of the event (optional); cannot be empty if provided.
        description (str): Updated description of the event (optional); if empty, sets to None.
        location (str): Updated location of the event (optional), cannot be empty if provided; if empty, sets to None.
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
        elif new_start_time and new_start_time > event.end_time:
            db.session.rollback()
            return jsonify({'error': 'Start time cannot be after existing end time'}), 400
        elif new_end_time and new_end_time < event.start_time:
            db.session.rollback()
            return jsonify({'error': 'End time cannot be before existing start time'}), 400

        if new_start_time:
            event.start_time = new_start_time
        if new_end_time:
            event.end_time = new_end_time

        if 'description' in data:
            description = data.get('description', '').strip()
            if description:
                event.description = description
            else:
                event.description = None

        if 'location' in data:
            location = data.get('location', '').strip()
            if location:
                event.location = location
            else:
                event.location = None

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



##################### Task Routes #####################
@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Get all tasks, optionally filtered by due date range

    Query Parameters:
        start_date (str): ISO 8601 formatted start date to filter tasks (optional).
        end_date (str): ISO 8601 formatted end date to filter tasks (optional).

    Returns:
        Response: JSON array of tasks with HTTP status 200.
        Response: Error message with HTTP status 400 if date format is invalid or date range is invalid.
    """


    start = request.args.get('start')
    end = request.args.get('end')

    stmt = db.select(Task)
    start_dt = None
    end_dt = None

    try:
        if start:
            start_dt = parse_datetime(start)
            stmt = stmt.where(Task.due_datetime >= start_dt)
        if end:
            end_dt = parse_datetime(end)
            stmt = stmt.where(Task.due_datetime <= end_dt)

    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDThh:mm:ss)'}), 400

    if start_dt and end_dt and end_dt < start_dt:
        return jsonify({'error': 'End date cannot be before start date'}), 400

    stmt = stmt.order_by(Task.due_datetime.nulls_last())

    tasks = db.session.scalars(stmt).all()

    return jsonify([task.to_dict() for task in tasks]), 200


@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Get a single task by ID

    Path Parameters:
        task_id (int): ID of the task to retrieve.

    Returns:
        Response: JSON object of the task with HTTP status 200.
        Response: Error message with HTTP status 404 if task not found.
        Response: Error message with HTTP status 500 for server errors.
    """

    task = db.get_or_404(Task, task_id)
    return jsonify(task.to_dict()), 200


@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task

    Request Body (JSON):
        title (str): Title of the task (required).
        description (str): Description of the task (required).
        location (str): Location of the task (optional).
        due_datetime (str): ISO 8601 formatted due date/time of the task (optional).
        link (str): Related link for the task (optional).

    Returns:
        Response: JSON object of the created task with HTTP status 201.
        Response: Error message with HTTP status 400 if required fields are missing.
        Response: Error message with HTTP status 500 for server errors.
    """

    data = request.get_json()

    try:
        title = data.get('title', '').strip()
        if not title:
            return jsonify({'error': 'Title cannot be empty'}), 400

        description = data.get('description', '').strip()
        if not description:
            return jsonify({'error': 'Description cannot be empty'}), 400

        due_datetime = None
        if 'due_datetime' in data and data['due_datetime']:
            try:
                due_datetime = parse_datetime(data['due_datetime'])
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDThh:mm:ss)'}), 400

        task = Task(
            title=title,
            description=description,
            location=data.get('location', None),
            due_datetime=due_datetime,
            link=data.get('link', None)
        )

        db.session.add(task)
        db.session.commit()

        return jsonify(task.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update an existing task

    Path Parameters:
        task_id (int): ID of the task to update.

    Request Body (JSON):
        title (str): Updated title of the task (optional); cannot be empty if provided.
        description (str): Updated description of the task (optional); cannot be empty if provided.
        location (str): Updated location of the task (optional); if empty, sets to None.
        due_datetime (str): Updated ISO 8601 formatted due date/time of the task (optional); if empty, sets to None.
        link (str): Updated link for the task (optional); if empty, sets to None.

    Returns:
        Response: JSON object of the updated task with HTTP status 200.
        Response: Error message with HTTP status 400 if:
            - Title is provided and empty
            - Date format is invalid
        Response: Error message with HTTP status 404 if task is not found.
        Response: Error message with HTTP status 500 for server errors.
    """

    task = db.get_or_404(Task, task_id)
    data = request.get_json()

    try:
        if 'title' in data:
            title = data.get('title', '').strip()
            if not title:
                db.session.rollback()
                return jsonify({'error': 'Title cannot be empty'}), 400
            task.title = title

        if 'description' in data:
            description = data.get('description', '').strip()
            if not description:
                db.session.rollback()
                return jsonify({'error': 'Description cannot be empty'}), 400
            task.description = description

        if 'location' in data:
            location = data.get('location', '').strip()
            if location:
                task.location = location
            else:
                task.location = None

        if 'due_datetime' in data:
            due_datetime = data.get('due_datetime', '').strip()
            if due_datetime:
                try:
                    task.due_datetime = parse_datetime(due_datetime)
                except ValueError:
                    db.session.rollback()
                    return jsonify({'error': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDThh:mm:ss)'}), 400
            else:
                task.due_datetime = None

        if 'link' in data:
            link = data.get('link', '').strip()
            if link:
                task.link = link
            else:
                task.link = None

        db.session.commit()
        return jsonify(task.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task

    Path Parameters:
        task_id (int): ID of the task to delete.

    Returns:
        Response: Empty response with HTTP status 204 if deletion is successful.
        Response: Error message with HTTP status 404 if task not found.
        Response: Error message with HTTP status 500 for server errors.
    """

    task = db.get_or_404(Task, task_id)

    try:
        db.session.delete(task)
        db.session.commit()
        return '', 204

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500