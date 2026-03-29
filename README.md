# 🎓 Hikmah AI

> Intelligent classical Islamic education assistant powered by AI, designed for Dars e Nizami students to deepen their understanding of traditional Islamic sciences.

## Overview

Hikmah AI is a comprehensive full-stack application that combines modern AI technology with classical Islamic knowledge. It provides students with intelligent analysis tools for classical Arabic texts, including morphological analysis (Sarf), grammatical analysis (Nahw), and rhetorical analysis (Balaghah). The platform features conversational AI chatbots, voice interaction, and personalized opportunity recommendations.

## 🌟 Key Features

### Text Analysis Lenses
- **FiveLens** - Multi-dimensional analysis of classical Arabic texts
- **Sarf (Morphology)** - Detailed word-form analysis and conjugation patterns
- **Nahw (Grammar)** - Grammatical structure and syntax analysis
- **Balaghah (Rhetoric)** - Classical Arabic rhetoric and eloquence analysis
- **Relevancy Bridge** - Intelligent chatbot with RAG (Retrieval Augmented Generation)

### Additional Features
- 🎤 **Voice Interaction** - Speech-to-text and text-to-speech capabilities
- 🔐 **Authentication** - Secure user authentication with Firebase and Clerk
- 💡 **Opportunity Explorer** - Personalized recommendations based on learning profile
- 🤖 **AI-Powered Chatbot** - Context-aware responses using LLMs (OpenAI/Groq)
- 📊 **Vector Search** - Advanced semantic search with Chroma vector database
- ⚡ **Real-time Updates** - Firestore integration for live data synchronization

## 📋 Tech Stack

### Frontend
- **Framework**: React 19 with Vite
- **Styling**: Tailwind CSS
- **State Management**: React Context & Hooks
- **Authentication**: Clerk & Firebase
- **HTTP Client**: Axios
- **Animations**: Framer Motion
- **Icons**: React Icons

### Backend
- **Framework**: FastAPI (Python)
- **LLM Integration**: OpenAI & Groq APIs
- **NLP**: PyArabic for Arabic language processing
- **Vector Database**: Chroma for semantic search
- **Database**: Google Cloud Firestore
- **Server**: Uvicorn with CORS middleware
- **Authentication**: Firebase Admin

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Deployment**: Vercel (Frontend), Cloud platforms (Backend)
- **Database**: Firestore, SQLite (Chroma)

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Docker & Docker Compose (optional)
- Firebase project credentials
- API keys for LLM services (OpenAI/Groq)

### Environment Setup

#### 1. Clone and Install Dependencies

```bash
# Frontend
cd frontend
npm install

# Backend
cd ../backend
pip install -r requirements.txt
```

#### 2. Configure Environment Variables

Create `.env` files in both frontend and backend directories:

**Backend** (`.env`):
```
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
FIREBASE_CREDENTIALS=path_to_firebase_json
DATABASE_URL=your_database_url
```

**Frontend** (`.env`):
```
VITE_FIREBASE_CONFIG=your_firebase_config
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_key
VITE_API_URL=http://localhost:8000
```

### Running Locally

#### Development Mode

```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173` and the backend at `http://localhost:8000`.

#### Using Docker Compose

```bash
docker-compose up --build
```

## 📁 Project Structure

```
Hikmah_AI/
├── frontend/                 # React Vite application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Application pages
│   │   ├── apis/            # API service clients
│   │   ├── firebase/        # Firebase configuration
│   │   └── styles/          # Global styles
│   └── package.json
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # FastAPI app initialization
│   │   ├── routes/         # API endpoints
│   │   │   ├── chat/       # Chat & RAG endpoints
│   │   │   ├── authentication_api.py
│   │   │   ├── classical_arabic_analyzer.py
│   │   │   ├── sarf_cag.py
│   │   │   ├── nahw_cag.py
│   │   │   ├── speech_services.py
│   │   │   └── opportunity_explorer.py
│   │   ├── models/         # Pydantic schemas
│   │   └── firebase_config.py
│   └── requirements.txt
│
├── ai_core/                 # AI models and preprocessing
│   ├── sarf_chatbot_streamlit.py
│   ├── balghah-chatbot.py
│   ├── nahw-chatbot.py
│   ├── vector_store.py     # Vector DB management
│   └── notebooks/          # Analysis notebooks
│
├── data_pipeline/          # Data processing pipeline
│   ├── Sarf_Cag.py
│   ├── Nahw_Cag.py
│   ├── pipeline_runner.py
│   └── data/
│
├── chunks/                 # Text chunks for RAG
├── docs/                   # Documentation & embeddings
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 🔌 API Endpoints

### Chat & Analysis
- `POST /chat/query` - Chat with RAG-powered bot
- `POST /analyze-arabic/analyze` - FiveLens text analysis
- `POST /sarf/analyze` - Sarf morphological analysis
- `POST /sarf/nahw` - Nahw grammatical analysis

### User & Auth
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/verify` - Token verification

### Other Services
- `POST /speech/transcribe` - Convert speech to text
- `POST /speech/synthesize` - Convert text to speech
- `GET /opportunities` - Get personalized opportunities

## 🔐 Authentication

The application uses dual authentication:
- **Firebase Authentication** - Primary auth system
- **Clerk** - Alternative auth provider with advanced features

## 📊 Data & Vector Search

The application uses:
- **Chroma Vector Database** - Semantic search on classical texts
- **Firebase Firestore** - Real-time user data & chat history
- **Text Embeddings** - Stored in `docs/embeddings/` for fast retrieval

## 🐳 Docker Deployment

### Build Docker Images

```bash
# Build all services
docker-compose build

# Run services
docker-compose up -d
```

### Production Deployment

Frontend is deployed on **Vercel** (see configured origins in backend):
- https://hikmah-ai-hui3.vercel.app
- https://hikmah-ai-s2ep.vercel.app
- https://hikmah-ai-nnjx.vercel.app

## 📦 Core Dependencies

### Frontend
- react@19.1.1
- vite@7.1.7
- tailwindcss@4.1.17
- axios@1.13.2
- firebase@12.6.0
- clerk@5.56.2

### Backend
- fastapi
- pyarabic (Arabic NLP)
- openai & groq (LLM APIs)
- firebase-admin
- chromadb (Vector DB)
- python-multipart

## 🛠️ Development

### Code Structure & Conventions

- **Frontend**: Components are located in `src/components/`, pages in `src/pages/`
- **Backend**: Routes follow REST principles, organized by feature
- **Naming**: Snake_case for Python files, camelCase for JavaScript/React

### Running Tests

```bash
# Add testing framework of choice
npm test          # Frontend
pytest            # Backend
```

## 📝 Contributing

To contribute to Hikmah AI:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

[Add your license here]

## 📧 Contact & Support

For questions or support, please reach out to the development team.

---

**Built with ❤️ for classical Islamic education.**
