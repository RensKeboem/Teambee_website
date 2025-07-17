# Teambee Website

A modern, responsive website for Teambee built with FastHTML and TailwindCSS. The website helps premium fitness clubs transform members into loyal ambassadors through personalized attention.

## Features

- 🏗️ **Modular Architecture** - Clean separation of concerns with organized packages
- 🎨 **Modern UI** - Responsive design with TailwindCSS and interactive elements
- 🔐 **User Authentication** - Complete auth system with registration, login, password reset
- 👥 **Admin Panel** - Club management and user administration
- 📊 **Dashboard** - User-specific dashboards with profile management
- 🌐 **Multi-language** - Dutch and English language support
- 📧 **Email Integration** - Contact forms and user notifications
- ⚡ **Performance** - Optimized with versioned static assets and middleware
- ♿ **Accessibility** - ARIA attributes and semantic HTML

## Prerequisites

- Python 3.7+
- Node.js and npm (for TailwindCSS)

## Quick Start

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Build TailwindCSS:**
   ```bash
   npm run build
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Open your browser:** Navigate to `http://localhost:8000`

## Development

For development with auto-reloading CSS:

1. **Start TailwindCSS watcher:**
   ```bash
   npm run dev
   ```

2. **In a separate terminal, run the app:**
   ```bash
   python run.py
   ```

The application will automatically reload when you make changes to Python files, and TailwindCSS will rebuild when you modify styles.

## Architecture

The codebase follows a clean, modular architecture with separation of concerns:

### 🏗️ Project Structure

```
Teambee/
├── 🚀 run.py                        # Application entry point
├── 🔧 main.py                       # FastHTML app setup and homepage
├── 
├── 📦 app/                          # Main application package
│   ├── 🔧 config.py                 # Configuration management
│   ├── 
│   ├── 🛠️  services/                 # Business logic layer
│   │   ├── auth_service.py          # Authentication & user management
│   │   ├── email_service.py         # Email sending functionality
│   │   └── session_service.py       # User session management
│   │
│   ├── 🗄️  models/                   # Data access layer
│   │   └── base.py                  # Database manager and connections
│   │
│   ├── 🌐 routes/                    # HTTP route handlers
│   │   ├── auth.py                  # Authentication routes
│   │   ├── public.py                # Public routes (homepage, contact)
│   │   ├── dashboard.py             # User dashboard routes
│   │   └── admin.py                 # Admin panel routes
│   │
│   ├── 🔌 middleware/                # Request/response processing
│   │   ├── security.py              # Security headers, HTTPS redirect
│   │   └── language.py              # Language detection and routing
│   │
│   ├── 🧩 components/               # Reusable UI components
│   │   ├── 📝 forms/                # Form components
│   │   │   ├── login_form.py        # Login form
│   │   │   ├── registration_form.py # User registration
│   │   │   ├── password_reset_form.py # Password reset
│   │   │   ├── password_update_form.py # Password change
│   │   │   ├── user_invite_form.py  # User invitation
│   │   │   ├── contact_form.py      # Contact us form
│   │   │   ├── club_form.py         # Club creation form
│   │   │   └── admin_invite_form.py # Admin user invitation
│   │   │
│   │   ├── 📄 layouts/              # Page layouts
│   │   │   ├── dashboard_layout.py  # User dashboard layout
│   │   │   └── admin_layout.py      # Admin panel layout
│   │   │
│   │   └── 🎨 ui/                   # UI section components
│   │       ├── hero_section.py      # Homepage hero section
│   │       ├── about_section.py     # About us section
│   │       ├── services_section.py  # Services section
│   │       ├── benefits_section.py  # Benefits section
│   │       ├── reviews_section.py   # Client reviews section
│   │       └── login_section.py     # Login form section
│   │
│   └── 🔧 utils/                    # Utility functions
│       └── helpers.py               # Common helper functions
│
├── 🎨 src/                          # TailwindCSS source
│   └── input.css                    # TailwindCSS input file
│
├── 🌐 public/                       # Static assets
│   ├── assets/                      # Images, SVGs, and media files
│   ├── js/                          # Client-side JavaScript
│   ├── data/                        # JSON data files
│   └── email-templates/             # HTML email templates
│
├── 🌍 translations/                 # Internationalization
│   ├── nl.json                      # Dutch translations
│   └── en.json                      # English translations
│
├── 🔧 Configuration Files
├── tailwind.config.js               # TailwindCSS configuration
├── package.json                     # Node.js dependencies and scripts
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
└── Procfile                         # Railway deployment configuration
```

### 🔄 Request Flow

1. **Middleware** processes requests (language detection, security headers)
2. **Routes** handle HTTP endpoints and delegate to services
3. **Services** contain business logic and data processing
4. **Models** handle database operations
5. **Components** render UI elements and forms

### 🎯 Key Design Principles

- **Single Responsibility** - Each module has one clear purpose
- **Dependency Injection** - Services are injected where needed
- **Separation of Concerns** - UI, business logic, and data are separated
- **Reusability** - Components can be used across different pages
- **Maintainability** - Clear structure makes debugging and updates easy

## Development Guidelines

### Adding New Features

1. **Routes** - Add new endpoints in appropriate route files
2. **Services** - Create services for business logic
3. **Components** - Build reusable UI components
4. **Translations** - Add text to translation files
5. **Tests** - Ensure functionality works as expected

### Code Organization

- Keep components small and focused
- Use services for complex business logic
- Follow the existing naming conventions
- Add proper docstrings and type hints
- Test new functionality thoroughly

## Deployment

The application is configured for Railway deployment with:
- `Procfile` for process management
- `railway.toml` for Railway configuration
- `Dockerfile` for containerized deployment
- Environment variables for configuration
---