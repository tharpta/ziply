# Ziply - FastAPI Web Application

A zipcode-based social platform built with FastAPI and SQLAlchemy. Users create posts called zips that are only visible within their own zipcode!

## Local Development

1. Activate virtual environment:
```bash
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

## Production Deployment

### Option 1: Railway (Recommended)

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect and deploy your FastAPI app
6. Your app will be live at `https://your-app-name.railway.app`

### Option 2: Render

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new "Web Service"
4. Connect your GitHub repo
5. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Option 3: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Push: `git push heroku main`

### Environment Variables

For production, set these environment variables:
- `DATABASE_URL`: PostgreSQL connection string (optional, defaults to SQLite)

## Features

- Location-based posts using IP geolocation
- SQLite database (local) / PostgreSQL (production)
- Responsive web interface
- Real-time zipcode detection
