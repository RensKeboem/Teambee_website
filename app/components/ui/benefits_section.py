"""
Benefits Section Component

Contains the benefits section component for the homepage.
"""

from fasthtml.common import *


class BenefitsSection:
    """Benefits section component."""
    
    def __init__(self, translations=None, versioned_url=None, current_lang="nl"):
        """Initialize the benefits section component."""
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
        """Render the benefits section."""
        partners = [
            {"name": "TechnoGym", "logo": "TechnoGym", "url": "https://www.technogym.com/"},
            {"name": "Sportivity", "logo": "Sportivity", "url": "https://sportivity.nl/"},
            {"name": "Clickables", "logo": "Clickables", "url": "https://clickables.nl/"},
            {"name": "Unlock", "logo": "Unlock", "url": "https://unlock.nl/"}
        ]
        
        return Section(
            Div(
                Div(
                    H2(
                        self.get_text("benefits", "title"),
                        cls="text-3xl md:text-4xl font-bold italic text-[#3D2E7C] mb-4 animate-section-title"
                    ),
                    P(
                        self.get_text("benefits", "subtitle"),
                        cls="text-lg text-gray-600 max-w-2xl mx-auto animate-section-subtitle"
                    ),
                    cls="text-center mb-12"
                ),
                
                Div(
                    # Member Retention
                    Div(
                        Div(
                            self.get_text("benefits", "retention_percent"),
                            cls="text-4xl font-bold text-[#E8973A] mb-2"
                        ),
                        H3(
                            self.get_text("benefits", "retention_title"),
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            self.get_text("benefits", "retention_text"),
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100 animate-card"
                    ),
                    
                    # Member Referrals
                    Div(
                        Div(
                            self.get_text("benefits", "referral_times"),
                            cls="text-4xl font-bold text-[#E8973A] mb-2"
                        ),
                        H3(
                            self.get_text("benefits", "referral_title"),
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            self.get_text("benefits", "referral_text"),
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100 animate-card"
                    ),
                    
                    # Engagement Increase
                    Div(
                        Div(
                            self.get_text("benefits", "engagement_percent"),
                            cls="text-4xl font-bold text-[#E8973A] mb-2"
                        ),
                        H3(
                            self.get_text("benefits", "engagement_title"),
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            self.get_text("benefits", "engagement_text"),
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100 animate-card"
                    ),
                    
                    cls="grid md:grid-cols-3 gap-8 mb-16 animate-stagger-container"
                ),
                
                # Subtle line separator
                Div(
                    cls="border-t border-gray-100 w-full mb-8"
                ),
                
                # Partners section
                Div(
                    Div(
                        H3(
                            self.get_text("benefits", "partners"),
                            cls="text-lg font-medium text-gray-500 mb-8 animate-section-title"
                        ),
                        cls="text-center"
                    ),
                    
                    Div(
                        *[
                            Div(
                                A(
                                    Img(
                                        src=self.versioned_url(f"/static/assets/{partner['logo']}.png"),
                                        alt=partner["name"],
                                        cls="h-10 md:h-8 w-auto object-contain transition-all duration-300 hover:scale-110 hover:opacity-90"
                                    ),
                                    href=partner["url"],
                                    target="_blank",
                                    rel="noopener noreferrer",
                                    aria_label=f"Visit {partner['name']} website",
                                    cls="flex items-center justify-center p-4"
                                ),
                                cls="flex items-center justify-center animate-stagger-item"
                            )
                            for partner in partners
                        ],
                        cls="grid grid-cols-2 md:flex md:flex-nowrap justify-center items-center gap-4 md:gap-12 max-w-4xl mx-auto animate-stagger-container"
                    ),
                    
                    cls="container"
                ),
                
                cls="container"
            ),
            id="benefits",
            cls="pt-16 pb-8 bg-white/80 backdrop-blur-sm"
        ) 