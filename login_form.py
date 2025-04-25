from fasthtml.common import *

class LoginForm:
    """Login form component for the Teambee application."""
    
    def __init__(self):
        """Initialize the login form component."""
        pass
    
    def render(self):
        """Render the login form."""
        return Form(
            Div(
                Div(
                    Label("Email", for_="email", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="email", id="email", name="email", placeholder="name@example.com", 
                          required=True, aria_required="true", aria_describedby="email-hint",
                          disabled=True, # To prevent auto-focus (since it is blured) 
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    Div(id="email-hint", cls="sr-only", text="Please enter your email address"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Div(
                        Label("Password", for_="password", cls="block text-sm font-medium text-gray-700"),
                        A("Forgot password?", href="#", aria_label="Reset your password",
                          cls="text-sm text-[#3D2E7C] hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded"),
                        cls="flex items-center justify-between mb-1"
                    ),
                    Input(type="password", id="password", name="password", 
                          required=True, aria_required="true", aria_describedby="password-hint",
                          disabled=True, # To prevent auto-focus (since it is blured) 
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    Div(id="password-hint", cls="sr-only", text="Please enter your password"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        "Login",
                        type="submit",
                        aria_label="Log in to your account",
                        disabled=True, # To prevent auto-focus (since it is blured) 
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                    ),
                    
                    Div(
                        "Don't have an account? ",
                        A("Contact us", href="mailto:info@teambee.nl", aria_label="Contact us to create a new account",
                          cls="text-[#3D2E7C] hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded"),
                        cls="text-center text-sm text-gray-500 mt-3"
                    ),
                    cls="flex flex-col"
                ),
                
                cls="flex flex-col gap-6"
            ),
            method="post",
            action="#",
            cls="flex flex-col gap-6",
            aria_labelledby="login-heading",
            role="form" 
        ) 