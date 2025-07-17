"""
Registration Form Component

Contains the registration form component for new users.
"""

from fasthtml.common import *


class RegistrationForm:
    """Registration form component for new users."""
    
    def __init__(self):
        """Initialize the registration form component."""
        pass
    
    def render(self, club_name: str = "", pre_filled_email: str = ""):
        """Render the registration form with custom validation."""
        return Div(
            Form(
                Div(
                    H2(
                        f"Create Account for {club_name}" if club_name else "Create Account",
                        cls="text-3xl font-bold italic text-[#3D2E7C] mb-6"
                    ),
                    
                    # Email field with validation
                    Label(
                        Span("Email", cls="block text-sm font-medium text-gray-700 mb-1"),
                        Input(
                            type="email", 
                            id="email", 
                            name="email", 
                            placeholder=" ", 
                            value=pre_filled_email,
                            required=True,
                            pattern="^[A-Za-z0-9._%+\\-]+@[A-Za-z0-9.\\-]+\\.[A-Za-z]{2,}$",
                            autocomplete="email",
                            cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C] peer invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500"
                        ),
                        Span(
                            "Please enter a valid email address",
                            cls="mt-1 hidden text-sm text-red-500 peer-[&:not(:placeholder-shown):not(:focus):invalid]:block"
                        ),
                        cls="flex flex-col gap-1 mb-4",
                        for_="email"
                    ),
                    
                    # Password field with validation
                    Label(
                        Span("Password", cls="block text-sm font-medium text-gray-700 mb-1"),
                        Input(
                            type="password", 
                            id="password", 
                            name="password", 
                            placeholder=" ", 
                            required=True,
                            pattern=".{8,}",
                            autocomplete="new-password",
                            cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C] peer invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500"
                        ),
                        Span(
                            "Password must be at least 8 characters long",
                            cls="mt-1 hidden text-sm text-red-500 peer-[&:not(:placeholder-shown):not(:focus):invalid]:block"
                        ),
                        cls="flex flex-col gap-1 mb-4",
                        for_="password"
                    ),
                    
                    # Confirm Password field with validation
                    Label(
                        Span("Confirm Password", cls="block text-sm font-medium text-gray-700 mb-1"),
                        Input(
                            type="password", 
                            id="confirm_password", 
                            name="confirm_password", 
                            placeholder=" ", 
                            required=True,
                            autocomplete="new-password",
                            cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C] peer"
                        ),
                        Span(
                            "Passwords do not match",
                            cls="mt-1 hidden text-sm text-red-500",
                            id="password-mismatch-error"
                        ),
                        cls="flex flex-col gap-1 mb-6",
                        for_="confirm_password"
                    ),
                    
                    # Submit button (disabled when form is invalid)
                    Div(
                        Button(
                            "Create Account",
                            type="submit",
                            cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 group-invalid:pointer-events-none group-invalid:opacity-30 transition-opacity"
                        ),
                        cls="flex flex-col"
                    ),
                    
                    cls="flex flex-col"
                ),
                method="post",
                cls="max-w-md mx-auto group",
                role="form",
                novalidate=True
            ),
            cls="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8"
        ) 