# Flaks Music API

## Overview

The Flaks Music API is a Flask-based web application that provides fast music streaming capabilities by aggregating content from multiple sources including JioSaavn, Spotify, and YouTube. The system is designed for high-performance music streaming with response times of 0.3-0.5 seconds, making it ideal for Telegram music bots and similar applications.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python) with CORS enabled
- **Database**: MongoDB with PyMongo driver
- **Authentication**: Session-based admin authentication
- **API Management**: Custom API key system with rate limiting

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5.3.0
- **JavaScript**: Vanilla JS with async/await patterns
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Inter)

## Key Components

### 1. Application Core (`app.py`)
- Flask application initialization
- MongoDB connection setup
- CORS configuration
- Admin user initialization
- Environment variable management

### 2. Data Models (`models.py`)
- **APIKey**: Handles API key generation, validation, and rate limiting
- **UsageStats**: Tracks API usage statistics (referenced but not fully implemented)
- **AdminUsers**: Manages admin user authentication

### 3. Music Sources (`music_sources.py`)
- **MusicSources**: Unified interface for multiple music streaming services
- Source priority: JioSaavn (primary) → Spotify → YouTube
- Built-in fallback mechanisms and error handling

### 4. Routes (`routes.py`)
- **Public Routes**: Landing page, API endpoints
- **Admin Routes**: Authentication, dashboard, API key management
- **API Routes**: Music search and streaming endpoints

### 5. Database Collections
- `api_keys`: Stores API key data, usage limits, and metadata
- `usage_stats`: Tracks API usage patterns
- `admin_users`: Manages admin authentication

## Data Flow

1. **User Registration**: Admin creates API keys through dashboard
2. **Authentication**: API requests validated against MongoDB-stored keys
3. **Rate Limiting**: Daily request limits enforced per API key
4. **Music Search**: Query routed through multiple sources with fallback
5. **Response**: Direct audio stream URLs returned to client

## External Dependencies

### Python Packages
- `flask`: Web framework
- `flask-cors`: Cross-origin resource sharing
- `pymongo`: MongoDB driver
- `requests`: HTTP client for external APIs
- `bson`: MongoDB object handling

### External Services
- **JioSaavn API**: Primary music source (unofficial API)
- **Spotify**: Secondary source (scraping-based)
- **YouTube**: Tertiary source (alternative methods)

### Frontend Dependencies
- Bootstrap 5.3.0 (CDN)
- Font Awesome 6.4.0 (CDN)
- Google Fonts Inter (CDN)

## Deployment Strategy

### Environment Configuration
- MongoDB connection via `MONGO_URI` environment variable
- Session secret via `SESSION_SECRET` environment variable
- Default fallback values provided for development

### Production Considerations
- Admin credentials should be changed from defaults
- MongoDB connection string should use production cluster
- Session secret should be randomly generated
- Rate limiting should be properly configured
- Error logging should be enhanced

### Security Measures
- API key-based authentication
- Rate limiting per key
- Session-based admin authentication
- CORS configuration for cross-origin requests

## Changelog
- July 04, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.