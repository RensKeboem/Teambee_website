"""
Password Reset Form Component

Contains the password reset form component.
"""

from fasthtml.common import *


class PasswordResetForm:
    """Password reset form component."""
    
    def __init__(self, translations=None, language="nl"):
        """Initialize the password reset form component."""
        self.translations = translations or {}
        self.language = language
    
    def get_text(self, key: str, default: str = "") -> str:
        """Get translated text for the given key."""
        return self.translations.get(key, default)
    
    def render_request_form(self):
        """Render the password reset request form."""
        return Form(
            Div(
                H2(
                    self.get_text("request_title", "Reset Password"),
                    cls="text-3xl font-bold italic text-[#3D2E7C] mb-6"
                ),
                
                P(
                    self.get_text("request_subtitle", "Enter your email address and we'll send you a link to reset your password."),
                    cls="text-gray-600 mb-6"
                ),
                
                Div(
                    Label(self.get_text("email_label", "Email"), for_="email", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="email", id="email", name="email", placeholder=self.get_text("email_placeholder", "name@example.com"), 
                          required=True, aria_required="true",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        self.get_text("send_reset_link", "Send Reset Link"),
                        type="submit",
                        data_loading_text=self.get_text("sending", "Sending..."),
                        data_default_text=self.get_text("send_reset_link", "Send Reset Link"),
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                    ),
                    
                    Div(
                        A(self.get_text("back_to_login", "Back to Login"), href="/", 
                          cls="text-[#3D2E7C] hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded"),
                        cls="text-center text-sm text-gray-500 mt-3"
                    ),
                    cls="flex flex-col"
                ),
                
                cls="flex flex-col gap-6"
            ),
            method="post",
            action="/en/forgot-password" if self.language == "en" else "/forgot-password",
            cls="max-w-md mx-auto",
            role="form"
        )
    
    def render_reset_form(self):
        """Render the new password form."""
        return Form(
            Div(
                H2(
                    self.get_text("set_new_password_title", "Set New Password"),
                    cls="text-3xl font-bold italic text-[#3D2E7C] mb-6"
                ),
                
                # Error message container
                Div(
                    id="reset-error",
                    cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm w-full break-words"
                ),
                
                # Success message container
                Div(
                    id="reset-success",
                    cls="hidden mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm w-full break-words"
                ),
                
                # Hidden username field for accessibility
                Input(
                    type="text",
                    name="username",
                    autocomplete="username",
                    style="display: none;",
                    tabindex="-1",
                    aria_hidden="true"
                ),
                
                Div(
                    Label(self.get_text("new_password_label", "New Password"), for_="password", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="password", id="password", name="password", 
                          required=True, aria_required="true", minlength="8",
                          autocomplete="new-password",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    Div(self.get_text("password_min_length", "Password must be at least 8 characters long"), cls="text-xs text-gray-500 mt-1"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Label(self.get_text("confirm_password_label", "Confirm New Password"), for_="confirm_password", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="password", id="confirm_password", name="confirm_password", 
                          required=True, aria_required="true",
                          autocomplete="new-password",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    # Password mismatch error message
                    Div(
                        self.get_text("passwords_mismatch", "Passwords do not match"),
                        id="password-mismatch-error",
                        cls="hidden text-sm text-red-600 mt-1"
                    ),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        self.get_text("reset_password_button", "Reset Password"),
                        type="submit",
                        id="reset-password-submit-btn",
                        data_loading_text=self.get_text("resetting", "Resetting..."),
                        data_default_text=self.get_text("reset_password_button", "Reset Password"),
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed disabled:hover:bg-gray-400"
                    ),
                    cls="flex flex-col"
                ),
                
                cls="flex flex-col gap-6"
            ),
            id="reset-password-form",
            method="post",
            cls="w-full",
            role="form"
        ) 