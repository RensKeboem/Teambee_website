"""
User Invite Form Component

Contains the user invite form component for user dashboard.
"""

from fasthtml.common import *


class UserInviteForm:
    """User invite form component."""
    
    def __init__(self, translations=None, current_lang="nl"):
        """Initialize the user invite form component."""
        self.translations = translations or {}
        self.current_lang = current_lang
    
    def get_text(self, key: str, default: str = "") -> str:
        """Get translated text for the given key."""
        return self.translations.get(key, default)
    
    def render(self):
        """Render the user invite form."""
        # Set form action based on current language
        form_action = "/en/dashboard/invite-user" if self.current_lang == "en" else "/dashboard/invite-user"
        
        return Div(
            # Error message container
            Div(
                id="invite-error",
                cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
            ),
            
            # Success message container
            Div(
                id="invite-success",
                cls="hidden mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm"
            ),
            
            P(
                self.get_text("invite_subtitle", "Invite a new user to join your club by sending them a registration link."),
                cls="text-gray-600 mb-6"
            ),
            
            Form(
                Div(
                    Label(
                        self.get_text("email_address", "Email Address"),
                        for_="invite_email",
                        cls="block text-sm font-medium text-gray-700 mb-1"
                    ),
                    Input(
                        type="email",
                        id="invite_email",
                        name="invite_email",
                        placeholder=self.get_text("email_placeholder", "user@example.com"),
                        required=True,
                        aria_required="true",
                        cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                    ),
                    Div(
                        self.get_text("email_help", "Enter the email address of the person you want to invite"),
                        cls="text-xs text-gray-500 mt-1"
                    ),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        self.get_text("send_invitation", "Send Invitation"),
                        type="submit",
                        id="invite-submit-btn",
                        data_sending_text=self.get_text("sending", "Sending..."),
                        data_default_text=self.get_text("send_invitation", "Send Invitation"),
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                    ),
                    cls="flex flex-col"
                ),
                
                method="post",
                action=form_action,
                id="invite-form",
                cls="flex flex-col gap-4",
                role="form"
            ),
            cls=""
        ) 