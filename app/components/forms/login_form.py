"""
Login Form Component

Contains the login form component for the Teambee application.
"""

from fasthtml.common import *


class LoginForm:
    """Login form component for the Teambee application."""
    
    def __init__(self, translations=None, prefix=""):
        """Initialize the login form component."""
        self.translations = translations or {}
        self.prefix = prefix + "-" if prefix else ""
    
    def get_text(self, key, default=""):
        """Get translated text for login form."""
        return self.translations.get(key, default)
    
    def get_id(self, base_id):
        """Get prefixed ID for form elements."""
        return f"{self.prefix}{base_id}"
    
    def render(self):
        """Render the login form."""
        return Form(
            # Error message container
            Div(
                id=self.get_id("login-error"),
                cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
            ),
            
            # Success/info message container
            Div(
                id=self.get_id("login-info"),
                cls="hidden mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-blue-700 text-sm"
            ),
            
            Div(
                Div(
                    Label(self.get_text("email_label", "Email"), for_=self.get_id("email"), cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="email", id=self.get_id("email"), name="email", placeholder=self.get_text("email_placeholder", "name@example.com"), 
                          required=True, aria_required="true", aria_describedby=self.get_id("email-hint"),
                          autocomplete="username",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    Div(id=self.get_id("email-hint"), cls="sr-only", text="Please enter your email address"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Div(
                        Label(self.get_text("password", "Password"), for_=self.get_id("password"), cls="block text-sm font-medium text-gray-700"),
                        Button(self.get_text("forgot_password", "Forgot password?"), 
                               type="button", id=self.get_id("forgot-password-btn"), aria_label="Reset your password",
                               tabindex="-1",
                               cls="text-sm text-[#3D2E7C] hover:text-[#2A1F5C] transition-colors cursor-pointer bg-transparent border-none p-0 underline"),
                        cls="flex justify-between items-center mb-1"
                    ),
                    Input(type="password", id=self.get_id("password"), name="password", placeholder=self.get_text("password_placeholder", "Enter your password"), 
                          required=True, aria_required="true", aria_describedby=self.get_id("password-hint"),
                          autocomplete="current-password",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    Div(id=self.get_id("password-hint"), cls="sr-only", text="Please enter your password"),
                    cls="flex flex-col gap-2"
                ),
                
                cls="flex flex-col gap-4 mb-6"
            ),
            
            Button(
                Div(
                    Span(self.get_text("login_button", "Log In"), id=self.get_id("login-button-text")),
                    Div(
                        Div(cls="animate-spin rounded-full h-4 w-4 border-b-2 border-white"),
                        id=self.get_id("login-button-loading"),
                        cls="hidden"
                    ),
                    cls="flex items-center justify-center gap-2"
                ),
                type="submit", 
                id=self.get_id("login-submit-btn"),
                cls="w-full bg-[#3D2E7C] text-white py-2 px-4 rounded-lg hover:bg-[#2A1F5C] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            ),
            
            id=self.get_id("login-form"),
            method="post",
            action="/login",  # Will be updated by JavaScript based on language
            cls="space-y-4",
            novalidate=True
        ) 