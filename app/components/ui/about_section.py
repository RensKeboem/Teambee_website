"""
About Section Component

Contains the about section component for the homepage.
"""

from fasthtml.common import *


class AboutSection:
    """About section component."""
    
    def __init__(self, translations=None, versioned_url=None, current_lang="nl"):
        """Initialize the about section component."""
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
        """Render the about section."""
        return Section(
            Div(
                Div(
                    H2(
                        self.get_text("about", "title"),
                        cls="text-3xl md:text-4xl font-bold italic text-[#3D2E7C] mb-4"
                    ),
                    P(
                        self.get_text("about", "subtitle"),
                        cls="text-lg text-gray-600 max-w-2xl mx-auto"
                    ),
                    cls="text-center mb-12"
                ),
                
                Div(
                    # Synergie card
                    Div(
                        Div(
                            Img(
                                src=self.versioned_url("/static/assets/users.svg"),
                                alt="Synergie Icon",
                                cls="w-6 h-6"
                            ),
                            cls="w-12 h-12 bg-[#E8973A]/20 rounded-full flex items-center justify-center mb-4"
                        ),
                        H3(
                            self.get_text("about", "teamwork_title"),
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            self.get_text("about", "teamwork_text"),
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm transform transition-shadow duration-300 hover:shadow-md hover:shadow-gray-300"
                    ),
                    
                    # Resultaatgericht card
                    Div(
                        Div(
                            Img(
                                src=self.versioned_url("/static/assets/target.svg"),
                                alt="Resultaatgericht Icon",
                                cls="w-6 h-6"
                            ),
                            cls="w-12 h-12 bg-[#3D2E7C]/20 rounded-full flex items-center justify-center mb-4"
                        ),
                        H3(
                            self.get_text("about", "results_title"),
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            self.get_text("about", "results_text"),
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm transform transition-shadow duration-300 hover:shadow-md hover:shadow-gray-300"
                    ),
                    
                    # Duurzaam card
                    Div(
                        Div(
                            Img(
                                src=self.versioned_url("/static/assets/sprout.svg"),
                                alt="Duurzaam Icon",
                                cls="w-6 h-6"
                            ),
                            cls="w-12 h-12 bg-[#94C46F]/20 rounded-full flex items-center justify-center mb-4"
                        ),
                        H3(
                            self.get_text("about", "sustainable_title"),
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            self.get_text("about", "sustainable_text"),
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm transform transition-shadow duration-300 hover:shadow-md hover:shadow-gray-300"
                    ),
                    
                    cls="grid md:grid-cols-3 gap-8 animate-stagger-container"
                ),
                
                cls="container"
            ),
            id="about",
            cls="py-16 md:py-24"
        ) 