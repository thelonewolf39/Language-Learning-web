# Language Learning Web - Spanish Edition

A self-hosted language learning platform for learning Spanish, built with Vue.js and FastAPI.

## Features

- **5 Complete Lessons** covering:
  - Basic Greetings
  - Numbers 1-20
  - Common Foods
  - Colors
  - Family Members

- **Interactive Learning**:
  - Vocabulary cards with pronunciations
  - Practice quizzes with instant feedback
  - Score tracking for each lesson

- **User System**:
  - User registration and authentication
  - Progress tracking (coming soon)

- **Fully Dockerized**: Easy deployment with Docker Compose

## Quick Start with Docker

### Prerequisites
- Docker
- Docker Compose

### Running the Application

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Language-Learning-web
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. Stop the application:
```bash
docker-compose down
```

### Rebuilding After Changes

If you make changes to the code:
```bash
docker-compose up -d --build
```

## Development Setup (Without Docker)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

## Project Structure

```
Language-Learning-web/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── models.py        # Database models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── crud.py          # Database operations
│   │   └── lessons.json     # Lesson content
│   ├── data/
│   │   └── users.db         # SQLite database
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .dockerignore
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── MainPage.vue      # Main landing page
│   │   │   ├── LessonCard.vue    # Lesson preview card
│   │   │   └── LessonView.vue    # Interactive lesson view
│   │   ├── App.vue
│   │   └── main.js
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── .dockerignore
└── docker-compose.yml
```

## API Endpoints

- `POST /api/v1/users/register` - Register new user
- `GET /api/v1/lessons` - Get all available lessons

## Technology Stack

### Backend
- FastAPI - Modern Python web framework
- SQLAlchemy - SQL toolkit and ORM
- Passlib with Argon2 - Password hashing
- SQLite - Database

### Frontend
- Vue 3 - Progressive JavaScript framework
- Vite - Fast build tool
- Axios - HTTP client
- Tailwind CSS - Utility-first CSS

### Deployment
- Docker - Containerization
- Docker Compose - Multi-container orchestration
- Nginx - Web server for frontend

## Environment Variables

### Backend
- `DATABASE_URL` - Database connection string (default: sqlite:///./data/users.db)

### Frontend
- `VITE_API_URL` - Backend API URL (default: http://127.0.0.1:8000)

## Lesson Structure

Each lesson includes:
- **Title & Description** - Overview of the lesson
- **Difficulty Level** - Beginner, intermediate, or advanced
- **Vocabulary** - Spanish words with English translations and pronunciations
- **Exercises** - Multiple-choice quizzes to test knowledge

## Future Enhancements

- [ ] User authentication with JWT tokens
- [ ] Progress tracking for completed lessons
- [ ] Spaced repetition algorithm for vocabulary review
- [ ] Audio pronunciations
- [ ] More advanced lessons (intermediate and advanced levels)
- [ ] Writing exercises
- [ ] Conversation practice scenarios
- [ ] Leaderboard and achievements

## Contributing

Feel free to submit issues and pull requests to improve the platform!

## License

This project is for educational purposes.
