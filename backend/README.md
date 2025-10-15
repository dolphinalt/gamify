# Gamify Backend

A Flask-based REST API for managing events and tasks in a gamified calendar application.

## Project Structure

```
backend/
├── app.py              # Application factory and initialization
├── config.py           # Configuration management for different environments
├── extensions.py       # Flask extensions initialization
├── models.py           # SQLAlchemy database models
├── routes.py           # API route definitions
├── requirements.txt    # Python dependencies
└── instance/          # Instance-specific files (database, etc.)
    └── database.db    # SQLite database (auto-generated)
```

## Architecture

This project follows the **Application Factory Pattern**, which provides:

- **Modularity**: Clear separation of concerns across different modules
- **Testability**: Easy to create multiple app instances with different configurations
- **Scalability**: Simple to add new features and extensions
- **Flexibility**: Support for multiple environments (development, production, testing)

### Key Components

#### `app.py` - Application Factory
- `create_app(config_name)`: Main factory function that creates and configures the Flask app
- `initialize_extensions(app)`: Initializes all Flask extensions (database, CORS, Swagger)
- `register_blueprints(app)`: Registers API blueprints
- `register_error_handlers(app)`: Sets up custom error handlers

#### `config.py` - Configuration Management
- `Config`: Base configuration class with default settings
- `DevelopmentConfig`: Development environment settings
- `ProductionConfig`: Production environment settings
- `TestingConfig`: Testing environment settings

#### `extensions.py` - Extensions
- Centralizes initialization of Flask extensions (SQLAlchemy, CORS)
- Extensions are created without app binding and initialized later in the factory

#### `models.py` - Database Models
- `Event`: Calendar events with start/end times, locations, descriptions
- `Task`: Tasks with due dates, descriptions, and links
- Hybrid properties for proper timezone handling (UTC storage)

#### `routes.py` - API Routes
- `/api/events`: CRUD operations for events
- `/api/tasks`: CRUD operations for tasks
- Full Swagger documentation for all endpoints

## Configuration

### Environment Variables

- `FLASK_ENV`: Set the environment (`development`, `production`, `testing`)
- `PORT`: Port number for the server (defaults to `5000`)
- `SECRET_KEY`: Secret key for sessions (REQUIRED in production)
- `DATABASE_URL`: Database URL (for production, defaults to SQLite)
- `CORS_ORIGINS`: Comma-separated list of allowed CORS origins (defaults to `http://localhost:3000`)

### Example

```bash
# Development (default)
python app.py

# Development on custom port
set PORT=8080
python app.py

# Production
set FLASK_ENV=production
set PORT=5000
set SECRET_KEY=your-secret-key
set DATABASE_URL=postgresql://user:pass@localhost/dbname
set CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
python app.py
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:5000/api/docs`
- API Spec (JSON): `http://localhost:5000/apispec.json`

## Features

### Events API
- Create, read, update, and delete calendar events
- Filter events by date range
- Support for all-day events
- Automatic timezone handling (UTC)

### Tasks API
- Create, read, update, and delete tasks
- Optional due dates
- Support for locations and external links
- Filter tasks by due date range

### Additional Features
- **CORS Support**: Configured for frontend integration
- **Error Handling**: Consistent error responses across all endpoints
- **Input Validation**: Comprehensive validation for all inputs
- **Swagger Documentation**: Interactive API documentation
- **Timezone Handling**: Proper UTC storage and conversion

## Development

### Adding New Routes

1. Define the route in `routes.py` using the `api_bp` blueprint
2. Add Swagger documentation to the route
3. The route will be automatically registered under `/api/`

### Adding New Models

1. Create the model in `models.py` extending `Base`
2. Add a `to_dict()` method for JSON serialization
3. Run the app to auto-create tables

### Adding New Extensions

1. Add the extension to `extensions.py`
2. Initialize it in the `initialize_extensions()` function in `app.py`

## Testing

Create test instances with different configurations:

```python
from app import create_app

# Create a test app
app = create_app('testing')

with app.app_context():
    # Your test code here
    pass
```

## Database

The application uses SQLite by default for simplicity. The database file is created automatically in the `instance/` directory.

For production, configure a proper database (PostgreSQL, MySQL, etc.) using the `DATABASE_URL` environment variable.

## License

See the LICENSE file in the project root.
