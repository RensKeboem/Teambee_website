"""
Hero Section Component

Contains the hero section component for the homepage.
"""

from fasthtml.common import *


class HeroSection:
    """Hero section component for the homepage."""
    
    def __init__(self, translations=None, versioned_url=None, current_lang="nl"):
        """Initialize the hero section component."""
        self.translations = translations or {}
        self.versioned_url = versioned_url or (lambda x: x)
        self.current_lang = current_lang
    
    def get_text(self, section: str, key: str, default: str = "") -> str:
        """Get translated text for the given section and key."""
        try:
            return self.translations[self.current_lang][section][key]
        except (KeyError, AttributeError):
            # Fallback to default language (Dutch) if translation is missing
            try:
                return self.translations["nl"][section][key]
            except (KeyError, AttributeError):
                return default
    
    def render(self):
        """Render the hero section."""
        return Section(
            Div(
                Div(
                    Div(
                        H1(
                            self.get_text("home", "hero_title"),
                            cls="text-4xl md:text-5xl font-bold italic text-[#3D2E7C] leading-tight animate-section-title"
                        ),
                        P(
                            self.get_text("home", "hero_subtitle"),
                            cls="text-lg text-gray-600 max-w-md animate-section-subtitle"
                        ),
                        Div(
                            Button(
                                "Our services",
                                Span("→", cls="ml-2"),
                                cls="inline-flex h-10 items-center justify-center rounded-lg bg-[#3D2E7C] px-8 py-2 text-sm font-medium text-white shadow transition-all duration-300 ease-in-out hover:bg-[#3D2E7C]/90 hover:-translate-y-2 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 animate-card",
                                id="hero-services-button"
                            ),
                            cls="flex flex-col sm:flex-row gap-4"
                        ),
                        cls="space-y-6"
                    ),
                    Div(
                        Img(
                            src=self.versioned_url("/static/assets/Teambee icon.png"),
                            alt="Teambee Hero",
                            cls="w-full h-full object-contain animate-card",
                            loading="lazy"
                        ),
                        cls="relative h-[300px] md:h-[400px] hidden md:flex items-center justify-center"
                    ),
                    cls="grid gap-8 md:grid-cols-2 items-center"
                ),
                cls="container"
            ),
            cls="py-20 md:py-32"
        ) 