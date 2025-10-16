# Recurring Events Documentation

This document explains how to use the recurring events feature in the Gamify API.

## Overview

The recurring events feature allows you to create events that repeat on a schedule (daily, weekly, monthly, or yearly). This is perfect for:
- Weekly lectures (e.g., every Tuesday and Thursday at 9:00 AM)
- Discussion sections (e.g., every Friday at 2:00 PM)
- Office hours (e.g., every Monday and Wednesday at 3:00 PM)
- Monthly meetings (e.g., first Monday of each month)

## How It Works

### Storage
- **Recurrence Rule**: A single rule defines the pattern (e.g., "every Tuesday and Thursday")
- **Base Event**: One event record stores the event details and links to the recurrence rule
- **Virtual Instances**: When you query events, the API automatically generates individual instances for the date range

### Advantages
- **Efficient storage**: One rule generates unlimited instances
- **Easy updates**: Modify the rule once, all future instances update automatically
- **Flexible queries**: Generate only the instances you need for a specific date range

## Creating Recurring Events

### API Endpoint
```
POST /api/events
```

### Basic Recurring Event
Create a lecture that occurs every Tuesday and Thursday at 9:00 AM until December 15, 2025:

```bash
curl -X POST http://localhost:5000/api/events ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"CSE 101 Lecture\",\"description\":\"Introduction to Computer Science\",\"start_time\":\"2025-10-14T09:00:00\",\"end_time\":\"2025-10-14T10:30:00\",\"location\":\"Room 101\",\"recurrence\":{\"freq\":\"WEEKLY\",\"interval\":1,\"byday\":\"TU,TH\",\"until\":\"2025-12-15T23:59:59\"}}"
```

### JSON Request Body
```json
{
  "title": "CSE 101 Lecture",
  "description": "Introduction to Computer Science",
  "start_time": "2025-10-14T09:00:00",
  "end_time": "2025-10-14T10:30:00",
  "location": "Room 101",
  "recurrence": {
    "freq": "WEEKLY",
    "interval": 1,
    "byday": "TU,TH",
    "until": "2025-12-15T23:59:59"
  }
}
```

## Recurrence Rule Parameters

### Required Fields
- **freq** (string): Frequency of recurrence
  - Values: `DAILY`, `WEEKLY`, `MONTHLY`, `YEARLY`
  - Example: `"freq": "WEEKLY"`

### Optional Fields

#### interval (integer)
Repeat every N periods. Default: 1
- Every 2 weeks: `"interval": 2`
- Every 3 days: `"interval": 3`

#### until (string, ISO 8601 datetime)
End date for the recurrence
- Example: `"until": "2025-12-31T23:59:59"`
- Cannot be used with `count`

#### count (integer)
Number of occurrences to generate
- Example: `"count": 10` (only 10 instances)
- Cannot be used with `until`

#### byday (string)
Days of the week (comma-separated)
- Values: `MO`, `TU`, `WE`, `TH`, `FR`, `SA`, `SU`
- Example: `"byday": "MO,WE,FR"` (Monday, Wednesday, Friday)
- Commonly used with `WEEKLY` frequency

#### bymonthday (string)
Days of the month (comma-separated)
- Values: 1-31
- Example: `"bymonthday": "1,15"` (1st and 15th of each month)
- Commonly used with `MONTHLY` frequency

#### bymonth (string)
Months of the year (comma-separated)
- Values: 1-12
- Example: `"bymonth": "1,6,12"` (January, June, December)
- Commonly used with `YEARLY` frequency

## Common Use Cases

### Weekly Lecture (Tuesday/Thursday)
```json
{
  "title": "Physics 101 Lecture",
  "start_time": "2025-10-14T09:00:00",
  "end_time": "2025-10-14T10:30:00",
  "location": "Science Building 201",
  "recurrence": {
    "freq": "WEEKLY",
    "byday": "TU,TH",
    "until": "2025-12-15T23:59:59"
  }
}
```

### Daily Standup (Weekdays Only)
```json
{
  "title": "Daily Standup",
  "start_time": "2025-10-13T09:00:00",
  "end_time": "2025-10-13T09:15:00",
  "recurrence": {
    "freq": "WEEKLY",
    "byday": "MO,TU,WE,TH,FR",
    "count": 50
  }
}
```

### Monthly Team Meeting (First Monday)
```json
{
  "title": "Monthly Team Meeting",
  "start_time": "2025-11-03T14:00:00",
  "end_time": "2025-11-03T15:00:00",
  "recurrence": {
    "freq": "MONTHLY",
    "byday": "MO",
    "bymonthday": "1,2,3,4,5,6,7",
    "until": "2026-06-30T23:59:59"
  }
}
```
*Note: This approximates "first Monday" by specifying the first week of the month*

### Bi-Weekly Discussion Section
```json
{
  "title": "CSE 101 Discussion",
  "start_time": "2025-10-18T14:00:00",
  "end_time": "2025-10-18T15:00:00",
  "location": "Room 305",
  "recurrence": {
    "freq": "WEEKLY",
    "interval": 2,
    "byday": "FR",
    "until": "2025-12-15T23:59:59"
  }
}
```

### Every 10 Days
```json
{
  "title": "Progress Check-in",
  "start_time": "2025-10-15T10:00:00",
  "end_time": "2025-10-15T10:30:00",
  "recurrence": {
    "freq": "DAILY",
    "interval": 10,
    "count": 5
  }
}
```

## Retrieving Events

### Get Events with Date Range
When you query events with a date range, recurring events are automatically expanded into individual instances:

```bash
curl "http://localhost:5000/api/events?start=2025-10-13T00:00:00&end=2025-10-20T23:59:59"
```

### Response Format
Each instance includes:
- Original event details (title, description, location)
- Calculated start/end times for that specific occurrence
- `is_recurring_instance`: `true` for generated instances
- `recurrence_rule`: The full recurrence rule information

```json
[
  {
    "id": 1,
    "title": "CSE 101 Lecture",
    "start_time": "2025-10-14T09:00:00",
    "end_time": "2025-10-14T10:30:00",
    "location": "Room 101",
    "is_recurring_instance": true,
    "recurrence_rule": {
      "id": 1,
      "freq": "WEEKLY",
      "interval": 1,
      "byday": "TU,TH",
      "until": "2025-12-15T23:59:59"
    }
  },
  {
    "id": 1,
    "title": "CSE 101 Lecture",
    "start_time": "2025-10-16T09:00:00",
    "end_time": "2025-10-16T10:30:00",
    "location": "Room 101",
    "is_recurring_instance": true,
    "recurrence_rule": {
      "id": 1,
      "freq": "WEEKLY",
      "interval": 1,
      "byday": "TU,TH",
      "until": "2025-12-15T23:59:59"
    }
  }
]
```

### Disable Expansion
If you only want the base event (not expanded instances):

```bash
curl "http://localhost:5000/api/events?expand_recurring=false"
```

## Modifying Recurring Events

### Update All Future Instances
Simply update the base event or recurrence rule - all future instances will reflect the changes automatically.

```bash
curl -X PUT http://localhost:5000/api/events/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"location\":\"Room 202\"}"
```

### Delete All Instances
Delete the base event to remove all instances:

```bash
curl -X DELETE http://localhost:5000/api/events/1
```

## Recurrence Rule Management

### List All Recurrence Rules
```bash
curl http://localhost:5000/api/recurrence-rules
```

### Get Specific Rule
```bash
curl http://localhost:5000/api/recurrence-rules/1
```

### Delete Rule (and all associated events)
```bash
curl -X DELETE http://localhost:5000/api/recurrence-rules/1
```

## Best Practices

### 1. Always Specify an End Condition
Use either `until` or `count` to prevent infinite recurrence:

✅ **Good**: `"until": "2025-12-31T23:59:59"`
✅ **Good**: `"count": 20`
❌ **Avoid**: No end condition (can generate thousands of instances)

### 2. Use Appropriate Date Ranges
When querying events, specify reasonable date ranges:

✅ **Good**: Query one week, month, or quarter at a time
❌ **Avoid**: Very large date ranges (e.g., 10 years) with recurring events

### 3. Match Frequency to Use Case
- **DAILY**: For habits, daily tasks
- **WEEKLY**: For classes, meetings with specific weekdays
- **MONTHLY**: For monthly reports, monthly meetings
- **YEARLY**: For anniversaries, annual reviews

### 4. Time Zones
All times are stored in UTC. Make sure to:
- Send times in ISO 8601 format
- Include timezone information or use UTC
- Frontend should convert to user's local timezone for display

## Integration with Task Scheduler

When the task scheduler queries events for a specific day:

1. **Query with specific date range**: Pass start and end times for that day
2. **Get expanded instances**: The API returns all event instances for that day, including recurring events
3. **Send to LLM**: Include these instances when generating the optimal schedule

Example:
```bash
# Get all events for October 15, 2025
curl "http://localhost:5000/api/events?start=2025-10-15T00:00:00&end=2025-10-15T23:59:59"
```

The response will include:
- One-time events scheduled for that day
- Instances of recurring events that fall on that day
- All with proper start/end times

## Technical Details

### Database Schema

**RecurrenceRule Table**:
- `id`: Primary key
- `freq`: Frequency (DAILY, WEEKLY, MONTHLY, YEARLY)
- `dtstart`: Start date for recurrence
- `interval`: Repeat every N periods
- `until`: End date (optional)
- `count`: Number of occurrences (optional)
- `byday`: Days of week (optional)
- `bymonthday`: Days of month (optional)
- `bymonth`: Months (optional)

**Event Table Updates**:
- `recurrence_rule_id`: Foreign key to RecurrenceRule (nullable)
- `recurrence_rule`: Relationship to RecurrenceRule

### Recurrence Generation
Uses the `python-dateutil` library's `rrule` implementation, which follows the iCalendar RFC 5545 standard.

### Performance Considerations
- Instances are generated on-demand (not stored in database)
- Generation is fast even for hundreds of instances
- Date range filtering happens before instance generation
- Consider pagination for very long-running recurring events

## Troubleshooting

### Problem: No instances returned
**Solution**: Check that the date range overlaps with the recurrence period
- Verify `start_time` of the base event
- Check `until` date of recurrence rule

### Problem: Wrong days of week
**Solution**: Ensure `byday` uses correct abbreviations
- Use: `MO, TU, WE, TH, FR, SA, SU`
- Not: `MON, TUES, M, T`, etc.

### Problem: Too many instances
**Solution**: Add an appropriate `until` or `count` limit

## Example: Complete Student Schedule Setup

```bash
# Add weekly lectures
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "CSE 101 Lecture",
    "start_time": "2025-10-14T09:00:00",
    "end_time": "2025-10-14T10:30:00",
    "location": "Room 101",
    "recurrence": {
      "freq": "WEEKLY",
      "byday": "TU,TH",
      "until": "2025-12-15T23:59:59"
    }
  }'

# Add weekly discussion section
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "CSE 101 Discussion",
    "start_time": "2025-10-17T14:00:00",
    "end_time": "2025-10-17T15:00:00",
    "location": "Room 305",
    "recurrence": {
      "freq": "WEEKLY",
      "byday": "FR",
      "until": "2025-12-15T23:59:59"
    }
  }'

# Add weekly office hours
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Professor Office Hours",
    "start_time": "2025-10-15T15:00:00",
    "end_time": "2025-10-15T16:00:00",
    "location": "Office 420",
    "recurrence": {
      "freq": "WEEKLY",
      "byday": "WE",
      "until": "2025-12-15T23:59:59"
    }
  }'

# Query all events for a specific week
curl "http://localhost:5000/api/events?start=2025-10-13T00:00:00&end=2025-10-20T23:59:59"
```

This will return all instances of recurring events plus any one-time events for that week.
