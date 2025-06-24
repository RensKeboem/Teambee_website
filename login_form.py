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
                               cls="text-sm text-[#3D2E7C] hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded bg-transparent border-none p-0 cursor-pointer"),
                        cls="flex items-center justify-between mb-1"
                    ),
                    Input(type="password", id=self.get_id("password"), name="password", 
                          required=True, aria_required="true", aria_describedby=self.get_id("password-hint"),
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    Div(id=self.get_id("password-hint"), cls="sr-only", text="Please enter your password"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        Span(self.get_text("login_button", "Login"), id=self.get_id("login-button-text")),
                        Span(self.get_text("logging_in", "Logging in..."), id=self.get_id("login-button-loading"), cls="hidden"),
                        type="submit",
                        id=self.get_id("login-submit-btn"),
                        aria_label="Log in to your account",
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                    ),
                    
                    Div(
                        self.get_text("no_account", "Don't have an account?") + " ",
                        A(self.get_text("contact_us", "Contact us"), href="mailto:info@teambee.fit", aria_label="Contact us to create a new account",
                          cls="text-[#3D2E7C] hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded"),
                        cls="text-center text-sm text-gray-500 mt-3"
                    ),
                    cls="flex flex-col"
                ),
                
                cls="flex flex-col gap-6"
            ),
            id=self.get_id("login-form"),
            method="post",
            cls="flex flex-col gap-6",
            aria_labelledby="login-heading",
            role="form" 
        ) 