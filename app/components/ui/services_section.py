"""
Services Section Component

Contains the services section component for the homepage.
"""

from fasthtml.common import *


class ServicesSection:
    """Services section component."""
    
    def __init__(self, translations=None, versioned_url=None, current_lang="nl"):
        """Initialize the services section component."""
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
    
    def _create_check_list_item(self, text):
        """Create a check list item with an orange check icon."""
        return Li(
            Img(
                src=self.versioned_url("/static/assets/check.svg"),
                alt="Check",
                cls="h-6 w-6 mr-2 mt-0.5"
            ),
            Span(text),
            cls="flex items-start animate-stagger-item"
        )
    
    def render(self):
        """Render the services section."""
        return Section(
            Div(
                Div(
                    H2(
                        self.get_text("services", "title"),
                        cls="text-3xl md:text-4xl font-bold italic mb-4 animate-section-title"
                    ),
                    cls="text-center mb-12"
                ),
                
                Div(
                    # Implementation section
                    Div(
                        Div(
                            # Header section
                            Div(
                                H3(
                                    self.get_text("services", "implementation"),
                                    cls="text-xl font-semibold text-[#ffffff] mb-2"
                                ),
                                P(
                                    self.get_text("services", "subtitle"),
                                    cls="text-sm text-white/80 animate-section-subtitle mb-4"
                                ),
                                # Separator line
                                Div(
                                    cls="w-50 h-0.5 bg-white/30 mb-6"
                                ),
                                cls=""
                            ),
                            
                            # Content section
                            Div(
                                Ul(
                                    self._create_check_list_item(self.get_text("services", "strategy")),
                                    self._create_check_list_item(self.get_text("services", "design")),
                                    self._create_check_list_item(self.get_text("services", "implementation_detail")),
                                    self._create_check_list_item(self.get_text("services", "education")),
                                    self._create_check_list_item(self.get_text("services", "data_support")),
                                    cls="space-y-3"
                                ),
                                cls="flex-grow"
                            ),
                            
                            # Button container
                            Div(
                                Button(
                                    self.get_text("services", "cta"),
                                    cls="inline-flex h-12 items-center justify-center rounded-lg bg-[#94C46F] px-8 py-2 text-base font-medium text-white shadow transition-all duration-300 ease-in-out hover:bg-[#94C46F]/90 hover:scale-105 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#94C46F] focus-visible:ring-offset-2 animate-card",
                                    id="services-cta-button",
                                    data_form_type="services"
                                ),
                                cls="text-center mt-4"
                            ),
                            cls="bg-[#1B1947] p-6 rounded-lg min-h-[570px] animate-card flex flex-col justify-between"
                        ),
                        cls="flex flex-col"
                    ),
                    
                    # Data Support section
                    Div(
                        Div(
                            # Header section
                            Div(
                                H3(
                                    self.get_text("services", "data_support_title"),
                                    cls="text-xl font-semibold text-[#ffffff] mb-2"
                                ),
                                P(
                                    self.get_text("services", "data_support_subtitle"),
                                    cls="text-sm text-white/80 animate-section-subtitle mb-4"
                                ),
                                # Separator line
                                Div(
                                    cls="w-50 h-0.5 bg-white/30 mb-6"
                                ),
                                cls=""
                            ),
                            
                            # Content section
                            Div(
                                Ul(
                                    self._create_check_list_item(self.get_text("services", "data_support_inzicht")),
                                    self._create_check_list_item(self.get_text("services", "data_support_actie")),
                                    self._create_check_list_item(self.get_text("services", "data_support_retentie")),
                                    self._create_check_list_item(self.get_text("services", "data_support_team")),
                                    self._create_check_list_item(self.get_text("services", "data_support_groei")),
                                    cls="space-y-3"
                                ),
                                cls="flex-grow"
                            ),
                            
                            # Button container
                            Div(
                                Button(
                                    self.get_text("services", "view_report"),
                                    cls="inline-flex h-12 items-center justify-center rounded-lg bg-[#94C46F] px-8 py-2 text-base font-medium text-white shadow transition-all duration-300 ease-in-out hover:bg-[#94C46F]/90 hover:scale-105 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#94C46F] focus-visible:ring-offset-2 animate-card",
                                    data_form_type="services"
                                ),
                                cls="text-center mt-4"
                            ),
                            cls="bg-[#1B1947] p-6 rounded-lg min-h-[570px] animate-card flex flex-col justify-between"
                        ),
                        cls="flex flex-col"
                    ),
                    cls="grid md:grid-cols-2 gap-8 animate-stagger-container"
                ),
                
                cls="container"
            ),
            id="services",
            cls="py-8 md:py-16 bg-[#3D2E7C] text-white"
        ) 