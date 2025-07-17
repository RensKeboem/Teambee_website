"""
Login Section Component

Contains the login section component for the homepage.
"""

from fasthtml.common import *
from app.components.forms.login_form import LoginForm


class LoginSection:
    """Login section component."""
    
    def __init__(self, translations=None, versioned_url=None, current_lang="nl"):
        """Initialize the login section component."""
        self.translations = translations or {}
        self.versioned_url = versioned_url or (lambda x: x)
        self.current_lang = current_lang
    
    def get_text(self, section: str, key: str, default: str = "") -> str:
        """Get translated text for the given section and key."""
        try:
            return self.translations[self.current_lang][section][key]
        except (KeyError, AttributeError):
            # Fallback to Dutch if translation is missing
            try:
                return self.translations["nl"][section][key]
            except (KeyError, AttributeError):
                return default
    
    def render(self):
        """Render the login section."""
        # Get login translations for the current language
        login_translations = self.translations.get(self.current_lang, {}).get("login", {})
        login_form = LoginForm(login_translations, "main")
        
        return Section(
            Div(
                Div(
                    Div(
                        H2(
                            self.get_text("login", "title"),
                            id="login-heading",
                            cls="text-3xl font-bold italic text-[#3D2E7C] mb-2"
                        ),
                        P(
                            self.get_text("login", "subtitle"),
                            cls="text-gray-600"
                        ),
                        cls="text-center mb-8"
                    ),
                    
                    # Login form
                    login_form.render(),
                    
                    cls="max-w-md mx-auto"
                ),
                cls="container relative z-10"
            ),
            
            # Bottom honeycomb pattern
            Div(
                Img(
                    src=self.versioned_url("/static/assets/honeycomb-cropped.svg"),
                    alt="Honeycomb Pattern",
                    cls="w-[200%] h-[40vh] object-cover opacity-15 dark:opacity-10 pointer-events-none [transform:scaleY(-1)]",
                    loading="lazy"
                ),
                cls="absolute bottom-0 left-0 right-0 w-full h-[40vh] z-0"
            ),
            
            id="login",
            cls="pt-8 md:pt-12 pb-16 bg-white/90 backdrop-blur-sm relative"
        ) 