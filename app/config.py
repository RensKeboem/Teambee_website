"""
Configuration Management

Centralized configuration for the Teambee application.
"""

import os
import json
import logging
from typing import Dict, Optional


class Config:
    """
    Configuration class for managing application settings.
    
    This class centralizes all configuration management including
    environment variables, database settings, email configuration,
    and application-specific settings.
    """
    
    def __init__(self):
        """Initialize configuration with environment variables."""
        # Database Configuration
        self.DB_URL = os.getenv("DB_URL")
        self.TEST_DB_URL = os.getenv("TEST_DB_URL")
        
        # Email Configuration
        self.EMAIL_USER = os.getenv("EMAIL_USER")
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        self.FROM_EMAIL = os.getenv("FROM_EMAIL", self.EMAIL_USER)
        self.SMTP_SERVER = os.getenv("SMTP_SERVER")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT")) if os.getenv("SMTP_PORT") else None
        
        # Security Configuration
        self.SECRET_KEY = os.getenv("SECRET_KEY", "teambee-secret-key-change-in-production")
        
        # Server Configuration
        self.PORT = int(os.getenv("PORT", 8000))
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        self.RAILWAY_PUBLIC_DOMAIN = os.getenv("RAILWAY_PUBLIC_DOMAIN", "http://localhost:8000")
        
        # Application Configuration
        self.APP_VERSION = "1.0.0"
        self.SUPPORTED_LANGUAGES = ["nl", "en"]
        self.DEFAULT_LANGUAGE = "nl"
        
        # File Paths
        self.TRANSLATIONS_DIR = "translations"
        self.EMAIL_TEMPLATES_DIR = os.path.join("public", "email-templates")
        self.STATIC_DIR = "public"
        
        # Application Settings
        self.PASSWORD_MIN_LENGTH = 8
        self.RESET_TOKEN_EXPIRY_HOURS = 1
        self.REGISTRATION_TOKEN_EXPIRY_HOURS = 24
        self.MAX_FAILED_LOGIN_ATTEMPTS = 10
        self.ACCOUNT_LOCK_DURATION_MINUTES = 30
        
        # Logging Configuration
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration based on environment."""
        log_level = logging.DEBUG if self.ENVIRONMENT == "development" else logging.INFO
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
        
        # Suppress verbose debug logs even in development
        logging.getLogger("python_multipart").setLevel(logging.WARNING)
        logging.getLogger("python_multipart.multipart").setLevel(logging.WARNING)
        logging.getLogger("watchfiles").setLevel(logging.WARNING)
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"
    
    def get_db_url(self, use_test_db: bool = False) -> Optional[str]:
        """Get the appropriate database URL."""
        if use_test_db:
            return self.TEST_DB_URL
        return self.DB_URL
    
    def validate_email_config(self) -> bool:
        """Validate that email configuration is complete."""
        required_fields = [
            self.EMAIL_USER,
            self.EMAIL_PASSWORD,
            self.SMTP_SERVER,
            self.SMTP_PORT
        ]
        return all(field is not None for field in required_fields)
    
    def get_base_url(self) -> str:
        """Get the base URL for the application."""
        if self.is_production():
            return self.RAILWAY_PUBLIC_DOMAIN
        return f"http://{self.HOST}:{self.PORT}"
    
    def load_translations(self) -> Dict[str, Dict]:
        """Load translations from JSON files."""
        translations = {}
        
        for lang in self.SUPPORTED_LANGUAGES:
            file_path = os.path.join(self.TRANSLATIONS_DIR, f"{lang}.json")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    translations[lang] = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logging.warning(f"Error loading translations for {lang}: {e}")
                translations[lang] = {}
        
        return translations
    
    def get_static_file_path(self, relative_path: str) -> str:
        """Get the full path to a static file."""
        return os.path.join(self.STATIC_DIR, relative_path.lstrip("/"))
    
    def get_email_template_path(self, template_name: str, language: str = "en") -> str:
        """Get the path to an email template."""
        return os.path.join(
            self.EMAIL_TEMPLATES_DIR,
            template_name,
            f"{template_name}_{language}.html"
        )


# Global configuration instance
config = Config()


class LanguageMiddleware:
    """Middleware for language detection and setup."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = scope.get("request")
            if request:
                # Detect language from URL path
                path = request.url.path
                if path.startswith("/en"):
                    request.state.language = "en"
                else:
                    request.state.language = "nl"
        
        await self.app(scope, receive, send) 