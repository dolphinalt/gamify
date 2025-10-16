# Gamify Backend - Quick Start Guide

A Flask REST API with application factory pattern for managing events and tasks.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

The API will start at **http://localhost:5000**

## ✅ Verify It's Working

### Test the Root Endpoint
Open your browser or use curl:
```bash
curl http://localhost:5000/
```

Expected response:
```json
{
  "message": "Gamify API is running",
  "version": "1.0.0",
  "timestamp": "2025-10-15T12:00:00.000000+00:00",
  "docs": "/api/docs"
}
```

### Explore API Documentation
Visit **http://localhost:5000/api/docs** for interactive Swagger UI documentation.

### Test Creating an Event
```bash
curl -X POST http://localhost:5000/api/events ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Team Meeting\",\"start_time\":\"2025-10-15T10:00:00\",\"end_time\":\"2025-10-15T11:00:00\"}"
```

### Test Creating a Recurring Event
```bash
curl -X POST http://localhost:5000/api/events ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Weekly Standup\",\"start_time\":\"2025-10-15T09:00:00\",\"end_time\":\"2025-10-15T09:30:00\",\"recurrence\":{\"freq\":\"WEEKLY\",\"byday\":\"MO,WE,FR\",\"until\":\"2025-12-31T23:59:59\"}}"
```

### Get All Events
```bash
curl http://localhost:5000/api/events
```

### Get Events in a Date Range (expands recurring events)
```bash
curl "http://localhost:5000/api/events?start=2025-10-15T00:00:00&end=2025-10-20T23:59:59"
```

## 🏗️ Application Factory Pattern

This project uses the **Application Factory Pattern** for better modularity and testability.

### Project Structure
```
backend/
├── app.py              # Application factory & initialization
├── config.py           # Environment-based configuration
├── extensions.py       # Flask extensions (SQLAlchemy, CORS)
├── models.py           # Database models (Event, RecurrenceRule, Task)
├── routes.py           # API endpoints
├── requirements.txt    # Python dependencies
├── RECURRING_EVENTS.md # Recurring events documentation
└── instance/          # Database & instance files (auto-created)
```

### Key Benefits
✅ **Modular**: Clean separation of concerns  
✅ **Testable**: Easy to create test instances  
✅ **Configurable**: Environment-specific settings  
✅ **Scalable**: Simple to extend with new features  
✅ **Professional**: Follows Flask best practices  

## ⚙️ Configuration

The app uses environment-based configuration from `config.py`:

- **Development** (default): `DEBUG=True`, SQLite database
- **Production**: `DEBUG=False`, configurable database
- **Testing**: In-memory SQLite database

### Environment Variables

```bash
# Set environment (development/production/testing)
set FLASK_ENV=production

# Custom port (default: 5000)
set PORT=8000

# Secret key for sessions (REQUIRED in production!)
set SECRET_KEY=your-super-secret-key

# CORS allowed origins (comma-separated, default: http://localhost:3000)
set CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Database URL (production)
set DATABASE_URL=postgresql://user:pass@localhost/gamify
```

### Example: Run on Port 8080
```bash
set PORT=8080
python app.py
```

### Example: Production Mode
```bash
set FLASK_ENV=production
set SECRET_KEY=random-secure-key-here
set DATABASE_URL=postgresql://user:pass@host/db
python app.py
```

## 📚 API Endpoints

### Events
- `GET /api/events` - Get all events (with optional date filtering, auto-expands recurring events)
- `GET /api/events/<id>` - Get specific event
- `POST /api/events` - Create new event (supports recurrence)
- `PUT /api/events/<id>` - Update event (can add/update/remove recurrence)
- `DELETE /api/events/<id>` - Delete event

### Recurrence Rules
- `GET /api/recurrence-rules` - Get all recurrence rules
- `GET /api/recurrence-rules/<id>` - Get specific recurrence rule
- `DELETE /api/recurrence-rules/<id>` - Delete recurrence rule (cascades to events)

### Tasks
- `GET /api/tasks` - Get all tasks (with optional date filtering)
- `GET /api/tasks/<id>` - Get specific task
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task

**Full documentation with examples:** http://localhost:5000/api/docs

### Recurring Events Examples

**Create weekly lecture (every Tuesday and Thursday):**
```json
POST /api/events
{
  "title": "CS 101 Lecture",
  "start_time": "2025-10-15T09:00:00",
  "end_time": "2025-10-15T10:30:00",
  "recurrence": {
    "freq": "WEEKLY",
    "byday": "TU,TH",
    "until": "2025-12-15T23:59:59"
  }
}
```

**Create daily standup (10 occurrences):**
```json
POST /api/events
{
  "title": "Daily Standup",
  "start_time": "2025-10-15T09:00:00",
  "end_time": "2025-10-15T09:15:00",
  "recurrence": {
    "freq": "DAILY",
    "count": 10
  }
}
```

**Update event to add recurrence:**
```json
PUT /api/events/123
{
  "recurrence": {
    "freq": "WEEKLY",
    "byday": "MO,WE,FR"
  }
}
```

**Update event to remove recurrence:**
```json
PUT /api/events/123
{
  "recurrence": null
}
```

For more details, see [RECURRING_EVENTS.md](RECURRING_EVENTS.md)

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Check what's using port 5000
netstat -ano | findstr :5000

# Use a different port
set PORT=8080
python app.py
```

### Database Issues
```bash
# Delete database and start fresh
del instance\database.db
python app.py
```

### Import Errors
```bash
# Ensure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

### CORS Errors from Frontend
Make sure your frontend origin is in `CORS_ORIGINS`:
```bash
set CORS_ORIGINS=http://localhost:3000,http://localhost:5173
python app.py
```

## 🚢 Production Deployment

### Using Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
```

### Using Waitress (Windows)
```bash
pip install waitress
waitress-serve --port=5000 --call app:create_app
```

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Set strong `SECRET_KEY` (use secrets.token_hex(32))
- [ ] Configure production database (`DATABASE_URL`)
- [ ] Set proper `CORS_ORIGINS` (your frontend domain)
- [ ] Use WSGI server (gunicorn, waitress, uWSGI)
- [ ] Enable HTTPS
- [ ] Set up logging
- [ ] Configure firewall

## 🧪 Testing

Create test instances with different configurations:

```python
from app import create_app

# Test with in-memory database
test_app = create_app('testing')

with test_app.app_context():
    # Your test code here
    pass
```

## 📖 Additional Resources

- **Recurring Events Guide**: `backend/RECURRING_EVENTS.md` - Comprehensive recurring events documentation
- **Main README**: `backend/README.md` - Detailed architecture documentation
- **Swagger Docs**: http://localhost:5000/api/docs - Interactive API testing
- **Flask Docs**: https://flask.palletsprojects.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/

## 🆘 Need Help?

1. Check the **Swagger UI** for API examples: http://localhost:5000/api/docs
2. Review `backend/README.md` for architecture details
3. Check Flask logs in the terminal for error messages
