"""
Contact Form Component

Contains the contact form component for contact us and services inquiries.
"""

from fasthtml.common import *


class ContactForm:
    """Contact form component for contact us and services inquiries."""
    
    def __init__(self, translations=None, versioned_url=None):
        """Initialize the contact form component."""
        self.translations = translations or {}
        self.versioned_url = versioned_url or (lambda x: x)
    
    def get_text(self, key: str, default: str = "") -> str:
        """Get translated text for the given key."""
        return self.translations.get(key, default)
    
    def render(self):
        """Render the contact form popup."""
        return Div(
            # Modal backdrop
            Div(
                # Modal content
                Div(
                    # Modal header
                    Div(
                        H2(
                            self.get_text("title", "Contact Us"),
                            cls="text-2xl font-bold text-[#3D2E7C] mb-2",
                            id="contact-form-title"
                        ),
                        Button(
                            Img(
                                src=self.versioned_url("/static/assets/close.svg"),
                                alt="Close",
                                cls="w-6 h-6 filter brightness-0"
                            ),
                            id="close-contact-popup",
                            cls="text-gray-700 hover:text-gray-900 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                        ),
                        cls="flex justify-between items-center mb-6"
                    ),
                    
                    # Modal body
                    Div(
                        P(
                            self.get_text("subtitle", "Fill out the form below and we'll get back to you as soon as possible."),
                            cls="text-gray-600 mb-6",
                            id="contact-form-subtitle"
                        ),
                        
                        # Error message container
                        Div(
                            id="contact-error",
                            cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
                        ),
                        
                        # Success message container
                        Div(
                            id="contact-success",
                            cls="hidden mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm"
                        ),
                        
                        # Contact form
                        Form(
                            # Hidden field for form type
                            Input(
                                type="hidden",
                                id="form_type",
                                name="form_type",
                                value=""
                            ),
                            
                            # First name field
                            Div(
                                Label(
                                    self.get_text("first_name", "First Name"),
                                    for_="contact_first_name",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="text",
                                    id="contact_first_name",
                                    name="first_name",
                                    required=True,
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="mb-4"
                            ),
                            
                            # Last name field
                            Div(
                                Label(
                                    self.get_text("last_name", "Last Name"),
                                    for_="contact_last_name",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="text",
                                    id="contact_last_name",
                                    name="last_name",
                                    required=True,
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="mb-4"
                            ),
                            
                            # Club name field
                            Div(
                                Label(
                                    self.get_text("club_name", "Club Name"),
                                    for_="contact_club_name",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="text",
                                    id="contact_club_name",
                                    name="club_name",
                                    required=True,
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="mb-4"
                            ),
                            
                            # Email field
                            Div(
                                Label(
                                    self.get_text("email", "Email"),
                                    for_="contact_email",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="email",
                                    id="contact_email",
                                    name="email",
                                    required=True,
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="mb-4"
                            ),
                            
                            # Phone number field
                            Div(
                                Label(
                                    self.get_text("phone", "Phone Number"),
                                    for_="contact_phone",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="tel",
                                    id="contact_phone",
                                    name="phone",
                                    required=True,
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="mb-6"
                            ),
                            
                            # Submit button
                            Button(
                                Span(self.get_text("submit", "Send Message"), id="contact-button-text"),
                                Span(self.get_text("sending", "Sending..."), id="contact-button-loading", cls="hidden"),
                                type="submit",
                                id="contact-submit-btn",
                                disabled=True,
                                cls="w-full bg-gray-400 cursor-not-allowed disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                            ),
                            
                            method="post",
                            action="/contact",
                            id="contact-form"
                        ),
                        cls=""
                    ),
                    
                    cls="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-auto transform transition-all duration-300 ease-out scale-95 opacity-0"
                ),
                cls="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
            ),
            id="contact-popup",
            cls="hidden"
        ) 