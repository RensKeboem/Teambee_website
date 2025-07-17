"""
Registration Popup Component

Contains the registration popup component for the main page.
"""

from fasthtml.common import *


class RegistrationPopup:
    """Registration popup component."""
    
    def __init__(self, translations=None, versioned_url=None, language="nl"):
        """Initialize the registration popup component."""
        self.translations = translations or {}
        self.versioned_url = versioned_url or (lambda x: x)
        self.language = language
    
    def get_text(self, key: str, default: str = "") -> str:
        """Get translated text for the given key."""
        return self.translations.get(key, default)
    
    def render(self):
        """Render the registration popup."""
        return Div(
            # Modal backdrop
            Div(
                # Modal content
                Div(
                    # Modal header
                    Div(
                        H2(
                            self.get_text("create_account_title", "Create Your Account"),
                            cls="text-2xl font-bold text-[#3D2E7C] mb-2"
                        ),
                        Button(
                            Img(
                                src=self.versioned_url("/static/assets/close.svg"),
                                alt="Close",
                                cls="w-6 h-6 filter brightness-0"
                            ),
                            id="close-registration-popup",
                            cls="text-gray-700 hover:text-gray-900 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                        ),
                        cls="flex justify-between items-center mb-6"
                    ),
                    
                    # Modal body
                    Div(
                        P(
                            id="registration-club-subtitle",
                            cls="text-gray-600 mb-6"
                        ),
                        
                        # Error message container
                        Div(
                            id="registration-popup-error",
                            cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm w-full break-words"
                        ),
                        
                        # Success message container
                        Div(
                            id="registration-popup-success",
                            cls="hidden mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm w-full break-words"
                        ),
                        
                        # Registration form
                        Form(
                            # Hidden token field
                            Input(
                                type="hidden",
                                id="registration-token",
                                name="token"
                            ),
                            
                            # Email field
                            Div(
                                Label(
                                    self.get_text("email_label", "Email"),
                                    for_="registration-email",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="email",
                                    id="registration-email",
                                    name="email",
                                    required=True,
                                    aria_required="true",
                                    autocomplete="email",
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="flex flex-col gap-2 mb-4"
                            ),
                            
                            # Password field
                            Div(
                                Label(
                                    self.get_text("password_label", "Password"),
                                    for_="registration-password",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="password",
                                    id="registration-password",
                                    name="password",
                                    required=True,
                                    aria_required="true",
                                    autocomplete="new-password",
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                Div(
                                    self.get_text("password_requirement", "Password must be at least 8 characters long"),
                                    cls="text-xs text-gray-500 mt-1"
                                ),
                                cls="flex flex-col gap-2 mb-4"
                            ),
                            
                            # Confirm Password field
                            Div(
                                Label(
                                    self.get_text("confirm_password_label", "Confirm Password"),
                                    for_="registration-confirm-password",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="password",
                                    id="registration-confirm-password",
                                    name="confirm_password",
                                    required=True,
                                    aria_required="true",
                                    autocomplete="new-password",
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                # Password mismatch error message
                                Div(
                                    self.get_text("passwords_mismatch", "Passwords do not match"),
                                    id="registration-password-mismatch-error",
                                    cls="hidden text-sm text-red-600 mt-1"
                                ),
                                cls="flex flex-col gap-2 mb-6"
                            ),
                            
                            Button(
                                self.get_text("create_account_button", "Create Account"),
                                type="submit",
                                id="registration-submit-btn",
                                data_loading_text=self.get_text("creating_account", "Creating Account..."),
                                data_default_text=self.get_text("create_account_button", "Create Account"),
                                cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed disabled:hover:bg-gray-400"
                            ),
                            
                            id="registration-form",
                            method="post",
                            cls="flex flex-col",
                            role="form"
                        ),
                        cls=""
                    ),
                    
                    cls="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-auto transform transition-all duration-300 ease-out scale-95 opacity-0"
                ),
                cls="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
            ),
            id="registration-popup",
            cls="hidden"
        ) 