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
    ---
    tags:
      - Events
    parameters:
      - name: start
        in: query
        type: string
        required: false
        description: ISO 8601 formatted start time to filter events (e.g., 2025-10-13T00:00:00)
      - name: end
        in: query
        type: string
        required: false
        description: ISO 8601 formatted end time to filter events (e.g., 2025-10-14T23:59:59)
    responses:
      200:
        description: List of events
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              description:
                type: string
              start_time:
                type: string
                format: date-time
              end_time:
                type: string
                format: date-time
              location:
                type: string
              all_day:
                type: boolean
      400:
        description: Invalid date format or date range
        schema:
          type: object
          properties:
            error:
              type: string
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
    ---
    tags:
      - Events
    parameters:
      - name: event_id
        in: path
        type: integer
        required: true
        description: ID of the event to retrieve
    responses:
      200:
        description: Event details
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            description:
              type: string
            start_time:
              type: string
              format: date-time
            end_time:
              type: string
              format: date-time
            location:
              type: string
            all_day:
              type: boolean
      404:
        description: Event not found
    """

    event = db.get_or_404(Event, event_id)
    return jsonify(event.to_dict()), 200


@api_bp.route('/events', methods=['POST'])
def create_event():
    """
    Create a new event
    ---
    tags:
      - Events
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
            - start_time
            - end_time
          properties:
            title:
              type: string
              description: Title of the event
              example: "Team Meeting"
            description:
              type: string
              description: Description of the event
              example: "Weekly team sync"
            start_time:
              type: string
              format: date-time
              description: ISO 8601 formatted start time
              example: "2025-10-13T10:00:00"
            end_time:
              type: string
              format: date-time
              description: ISO 8601 formatted end time
              example: "2025-10-13T11:00:00"
            location:
              type: string
              description: Location of the event
              example: "Conference Room A"
            all_day:
              type: boolean
              description: Whether the event lasts all day
              default: false
    responses:
      201:
        description: Event created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            description:
              type: string
            start_time:
              type: string
              format: date-time
            end_time:
              type: string
              format: date-time
            location:
              type: string
            all_day:
              type: boolean
      400:
        description: Invalid input or validation error
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
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
    ---
    tags:
      - Events
    parameters:
      - name: event_id
        in: path
        type: integer
        required: true
        description: ID of the event to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: Updated title of the event
              example: "Team Meeting (Updated)"
            description:
              type: string
              description: Updated description of the event (empty string sets to None)
              example: "Weekly team sync - updated agenda"
            start_time:
              type: string
              format: date-time
              description: Updated ISO 8601 formatted start time
              example: "2025-10-13T14:00:00"
            end_time:
              type: string
              format: date-time
              description: Updated ISO 8601 formatted end time
              example: "2025-10-13T15:00:00"
            location:
              type: string
              description: Updated location (empty string sets to None)
              example: "Conference Room B"
            all_day:
              type: boolean
              description: Updated all-day status
    responses:
      200:
        description: Event updated successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            description:
              type: string
            start_time:
              type: string
              format: date-time
            end_time:
              type: string
              format: date-time
            location:
              type: string
            all_day:
              type: boolean
      400:
        description: Invalid input or validation error
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Event not found
      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
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
    ---
    tags:
      - Events
    parameters:
      - name: event_id
        in: path
        type: integer
        required: true
        description: ID of the event to delete
    responses:
      204:
        description: Event deleted successfully
      404:
        description: Event not found
      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
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
    ---
    tags:
      - Tasks
    parameters:
      - name: start
        in: query
        type: string
        required: false
        description: ISO 8601 formatted start date to filter tasks
      - name: end
        in: query
        type: string
        required: false
        description: ISO 8601 formatted end date to filter tasks
    responses:
      200:
        description: List of tasks
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              description:
                type: string
              due_datetime:
                type: string
                format: date-time
              completed:
                type: boolean
              priority:
                type: string
              category:
                type: string
      400:
        description: Invalid date format or date range
        schema:
          type: object
          properties:
            error:
              type: string
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
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID of the task to retrieve
    responses:
      200:
        description: Task details
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            description:
              type: string
            due_datetime:
              type: string
              format: date-time
            completed:
              type: boolean
            priority:
              type: string
            category:
              type: string
            location:
              type: string
            link:
              type: string
      404:
        description: Task not found
    """

    task = db.get_or_404(Task, task_id)
    return jsonify(task.to_dict()), 200


@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task
    ---
    tags:
      - Tasks
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
            - description
          properties:
            title:
              type: string
              description: Title of the task
              example: "Complete project proposal"
            description:
              type: string
              description: Description of the task
              example: "Finish the Q4 project proposal document"
            location:
              type: string
              description: Location of the task
              example: "Office"
            due_datetime:
              type: string
              format: date-time
              description: ISO 8601 formatted due date/time
              example: "2025-10-20T17:00:00"
            link:
              type: string
              description: Related link for the task
              example: "https://docs.example.com/proposal"
    responses:
      201:
        description: Task created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            description:
              type: string
            due_datetime:
              type: string
              format: date-time
            completed:
              type: boolean
            priority:
              type: string
            category:
              type: string
            location:
              type: string
            link:
              type: string
      400:
        description: Invalid input or validation error
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
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
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID of the task to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: Updated title of the task
              example: "Complete project proposal (Updated)"
            description:
              type: string
              description: Updated description of the task
              example: "Finish and submit the Q4 project proposal"
            location:
              type: string
              description: Updated location (empty string sets to None)
              example: "Home Office"
            due_datetime:
              type: string
              format: date-time
              description: Updated ISO 8601 formatted due date/time (empty string sets to None)
              example: "2025-10-21T17:00:00"
            link:
              type: string
              description: Updated link (empty string sets to None)
              example: "https://docs.example.com/updated-proposal"
    responses:
      200:
        description: Task updated successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            description:
              type: string
            due_datetime:
              type: string
              format: date-time
            completed:
              type: boolean
            priority:
              type: string
            category:
              type: string
            location:
              type: string
            link:
              type: string
      400:
        description: Invalid input or validation error
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Task not found
      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
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
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID of the task to delete
    responses:
      204:
        description: Task deleted successfully
      404:
        description: Task not found
      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
    """

    task = db.get_or_404(Task, task_id)

    try:
        db.session.delete(task)
        db.session.commit()
        return '', 204

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500