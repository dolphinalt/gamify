from flask import Blueprint, request, jsonify
from extensions import db
from models import Event, Task, RecurrenceRule
from datetime import datetime, timezone, timedelta
from sqlalchemy import or_, and_

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
    Get all events, optionally filtered by date range.
    Expands recurring events into individual instances within the date range.
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
      - name: expand_recurring
        in: query
        type: boolean
        required: false
        default: true
        description: Whether to expand recurring events into instances (default true)
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
              is_recurring_instance:
                type: boolean
              recurrence_rule:
                type: object
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
    expand_recurring = request.args.get('expand_recurring', 'true').lower() != 'false'

    stmt = db.select(Event)
    start_dt = None
    end_dt = None

    try:
        if start:
            start_dt = parse_datetime(start)
        if end:
            end_dt = parse_datetime(end)
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDThh:mm:ss)'}), 400

    if start_dt and end_dt and end_dt < start_dt:
        return jsonify({'error': 'End time cannot be before start time'}), 400

    # Apply date filters at database level
    # For recurring events, we need to include them even if their original
    # start/end times are outside the range, because they might have instances within the range

    if start_dt and end_dt:
        # Both start and end provided: non-recurring events must overlap the range
        stmt = stmt.where(
            or_(
                Event.recurrence_rule_id.isnot(None),  # Include all recurring events
                and_(
                    Event.end_time >= start_dt,  # Non-recurring event overlaps range
                    Event.start_time < end_dt
                )
            )
        )
    elif start_dt:
        # Only start provided: non-recurring events must end after start
        stmt = stmt.where(
            or_(
                Event.recurrence_rule_id.isnot(None),  # Include all recurring events
                Event.end_time >= start_dt
            )
        )
    elif end_dt:
        # Only end provided: non-recurring events must start before end
        stmt = stmt.where(
            or_(
                Event.recurrence_rule_id.isnot(None),  # Include all recurring events
                Event.start_time < end_dt
            )
        )

    # Get filtered events
    all_events = db.session.scalars(stmt.order_by(Event.start_time)).all()

    result_events = []

    for event in all_events:
        if event.recurrence_rule and expand_recurring:
            # Generate recurring instances
            if not start_dt or not end_dt:
                # If no date range specified, use a default range
                # Show occurrences from now until 1 year from now
                range_start = start_dt or datetime.now(timezone.utc)
                range_end = end_dt or (range_start + timedelta(days=365))
            else:
                range_start = start_dt
                range_end = end_dt

            # Generate occurrence dates
            occurrences = event.recurrence_rule.generate_occurrences(range_start, range_end)

            # Calculate event duration
            event_duration = event.end_time - event.start_time

            # Create instance for each occurrence
            for occurrence_start in occurrences:
                occurrence_end = occurrence_start + event_duration

                # Filter recurring instances by the requested date range
                if start_dt and occurrence_end < start_dt:
                    continue
                if end_dt and occurrence_start >= end_dt:
                    continue

                # Create a virtual event instance
                instance = {
                    'id': event.id,  # Keep original event ID
                    'created_at': event.created_at.isoformat(),
                    'updated_at': event.updated_at.isoformat(),
                    'title': event.title,
                    'start_time': occurrence_start.isoformat(),
                    'end_time': occurrence_end.isoformat(),
                    'description': event.description,
                    'location': event.location,
                    'all_day': event.all_day,
                    'is_recurring_instance': True,
                    'recurrence_rule': event.recurrence_rule.to_dict()
                }
                result_events.append(instance)
        else:
            # Non-recurring event (already filtered by database query)
            event_dict = event.to_dict()
            event_dict['is_recurring_instance'] = False
            result_events.append(event_dict)

    # Sort by start time
    result_events.sort(key=lambda x: x['start_time'])

    return jsonify(result_events), 200


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
    Create a new event, optionally with recurrence
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
            recurrence:
              type: object
              description: Recurrence rule for the event
              properties:
                freq:
                  type: string
                  enum: ['DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']
                  description: Frequency of recurrence
                  example: "WEEKLY"
                interval:
                  type: integer
                  description: Repeat every N periods
                  default: 1
                  example: 1
                until:
                  type: string
                  format: date-time
                  description: End date for recurrence
                  example: "2025-12-31T23:59:59"
                count:
                  type: integer
                  description: Number of occurrences
                  example: 10
                byday:
                  type: string
                  description: Days of week (MO,TU,WE,TH,FR,SA,SU)
                  example: "TU,TH"
                bymonthday:
                  type: string
                  description: Days of month (1-31)
                  example: "1,15"
                bymonth:
                  type: string
                  description: Months (1-12)
                  example: "1,6,12"
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
            recurrence_rule:
              type: object
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

        # Handle recurrence if provided
        recurrence_rule = None
        if 'recurrence' in data and data['recurrence']:
            recurrence_data = data['recurrence']

            # Validate frequency
            freq = recurrence_data.get('freq', '').upper()
            if freq not in ['DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']:
                return jsonify({'error': 'Invalid frequency. Must be DAILY, WEEKLY, MONTHLY, or YEARLY'}), 400

            # Parse until date if provided
            until = None
            if 'until' in recurrence_data and recurrence_data['until']:
                try:
                    until = parse_datetime(recurrence_data['until'])
                except ValueError:
                    return jsonify({'error': 'Invalid until date format'}), 400

            # Validate count and until (only one should be provided)
            count = recurrence_data.get('count')
            if count and until:
                return jsonify({'error': 'Cannot specify both count and until'}), 400

            recurrence_rule = RecurrenceRule(
                freq=freq,
                dtstart=start_time,
                interval=recurrence_data.get('interval', 1),
                until=until,
                count=count,
                byday=recurrence_data.get('byday'),
                bymonthday=recurrence_data.get('bymonthday'),
                bymonth=recurrence_data.get('bymonth')
            )

        event = Event(
            title=title,
            description=data.get('description', None),
            start_time=start_time,
            end_time=end_time,
            location=data.get('location', None),
            all_day=data.get('all_day', False),
            recurrence_rule=recurrence_rule
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
    Update an existing event and optionally its recurrence rule
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
            recurrence:
              type: object
              description: Updated recurrence rule (null to remove recurrence)
              properties:
                freq:
                  type: string
                  enum: ['DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']
                interval:
                  type: integer
                until:
                  type: string
                  format: date-time
                count:
                  type: integer
                byday:
                  type: string
                bymonthday:
                  type: string
                bymonth:
                  type: string
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
            recurrence_rule:
              type: object
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

        # Handle recurrence rule updates
        if 'recurrence' in data:
            recurrence_data = data['recurrence']

            if recurrence_data is None:
                # Remove recurrence (convert to one-time event)
                if event.recurrence_rule:
                    old_rule = event.recurrence_rule
                    event.recurrence_rule = None
                    event.recurrence_rule_id = None
                    db.session.delete(old_rule)
            else:
                # Update or create recurrence rule
                freq = recurrence_data.get('freq', '').upper()
                if freq not in ['DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']:
                    db.session.rollback()
                    return jsonify({'error': 'Invalid frequency. Must be DAILY, WEEKLY, MONTHLY, or YEARLY'}), 400

                # Parse until date if provided
                until = None
                if 'until' in recurrence_data and recurrence_data['until']:
                    try:
                        until = parse_datetime(recurrence_data['until'])
                    except ValueError:
                        db.session.rollback()
                        return jsonify({'error': 'Invalid until date format'}), 400

                # Validate count and until (only one should be provided)
                count = recurrence_data.get('count')
                if count and until:
                    db.session.rollback()
                    return jsonify({'error': 'Cannot specify both count and until'}), 400

                # Use updated start_time if provided, otherwise keep existing
                dtstart = new_start_time if new_start_time else event.start_time

                if event.recurrence_rule:
                    # Update existing rule
                    event.recurrence_rule.freq = freq
                    event.recurrence_rule.dtstart = dtstart
                    event.recurrence_rule.interval = recurrence_data.get('interval', 1)
                    event.recurrence_rule.until = until
                    event.recurrence_rule.count = count
                    event.recurrence_rule.byday = recurrence_data.get('byday')
                    event.recurrence_rule.bymonthday = recurrence_data.get('bymonthday')
                    event.recurrence_rule.bymonth = recurrence_data.get('bymonth')
                else:
                    # Create new rule
                    new_rule = RecurrenceRule(
                        freq=freq,
                        dtstart=dtstart,
                        interval=recurrence_data.get('interval', 1),
                        until=until,
                        count=count,
                        byday=recurrence_data.get('byday'),
                        bymonthday=recurrence_data.get('bymonthday'),
                        bymonth=recurrence_data.get('bymonth')
                    )
                    event.recurrence_rule = new_rule

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



##################### Recurrence Rule Routes #####################
@api_bp.route('/recurrence-rules', methods=['GET'])
def get_recurrence_rules():
    """
    Get all recurrence rules
    ---
    tags:
      - Recurrence Rules
    responses:
      200:
        description: List of recurrence rules
        schema:
          type: array
          items:
            type: object
    """

    stmt = db.select(RecurrenceRule)
    rules = db.session.scalars(stmt).all()
    return jsonify([rule.to_dict() for rule in rules]), 200


@api_bp.route('/recurrence-rules/<int:rule_id>', methods=['GET'])
def get_recurrence_rule(rule_id):
    """
    Get a single recurrence rule by ID
    ---
    tags:
      - Recurrence Rules
    parameters:
      - name: rule_id
        in: path
        type: integer
        required: true
        description: ID of the recurrence rule
    responses:
      200:
        description: Recurrence rule details
      404:
        description: Recurrence rule not found
    """

    rule = db.get_or_404(RecurrenceRule, rule_id)
    return jsonify(rule.to_dict()), 200


@api_bp.route('/recurrence-rules/<int:rule_id>', methods=['DELETE'])
def delete_recurrence_rule(rule_id):
    """
    Delete a recurrence rule (will also delete associated events due to cascade)
    ---
    tags:
      - Recurrence Rules
    parameters:
      - name: rule_id
        in: path
        type: integer
        required: true
        description: ID of the recurrence rule to delete
    responses:
      204:
        description: Recurrence rule deleted successfully
      404:
        description: Recurrence rule not found
      500:
        description: Server error
    """

    rule = db.get_or_404(RecurrenceRule, rule_id)

    try:
        db.session.delete(rule)
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