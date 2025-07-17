"""
Password Update Form Component

Contains the password update form component for user dashboard.
"""

from fasthtml.common import *


class PasswordUpdateForm:
    """Password update form component."""
    
    def __init__(self, translations=None, current_lang="nl"):
        """Initialize the password update form component."""
        self.translations = translations or {}
        self.current_lang = current_lang
    
    def get_text(self, key: str, default: str = "") -> str:
        """Get translated text for the given key."""
        return self.translations.get(key, default)
    
    def render(self):
        """Render the password update form."""
        # Set form action based on current language
        form_action = "/en/dashboard/update-password" if self.current_lang == "en" else "/dashboard/update-password"
        
        return Form(
            # Hidden username field for accessibility (password managers need this)
            Input(
                type="text",
                name="username",
                autocomplete="username",
                style="display: none;",
                tabindex="-1",
                aria_hidden="true"
            ),
            
            Div(
                # Error message container
                Div(
                    id="password-update-error",
                    cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
                ),
                
                # Success message container
                Div(
                    id="password-update-success",
                    cls="hidden mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm"
                ),
                
                Div(
                    Label(self.get_text("current_password", "Current Password"), for_="current_password", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="password", id="current_password", name="current_password", 
                          required=True, aria_required="true", autocomplete="current-password",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Label(self.get_text("new_password", "New Password"), for_="new_password", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="password", id="new_password", name="new_password", 
                          required=True, aria_required="true", minlength="8", autocomplete="new-password",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    Div(self.get_text("password_min_length", "Password must be at least 8 characters long"), cls="text-xs text-gray-500 mt-1"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Label(self.get_text("confirm_new_password", "Confirm New Password"), for_="confirm_new_password", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="password", id="confirm_new_password", name="confirm_new_password", 
                          required=True, aria_required="true", autocomplete="new-password",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        self.get_text("update_password_button", "Update Password"),
                        type="submit",
                        id="password-update-btn",
                        data_updating_text=self.get_text("updating", "Updating..."),
                        data_default_text=self.get_text("update_password_button", "Update Password"),
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                    ),
                    cls="flex flex-col"
                ),
                
                cls="flex flex-col gap-4"
            ),
            id="password-update-form",
            method="post",
            action=form_action,
            cls="",
            role="form"
        ) 