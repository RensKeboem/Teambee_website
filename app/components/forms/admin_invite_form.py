"""
Admin Invite Form Component

Contains the admin invite form component for sending registration links via email.
"""

from fasthtml.common import *


class AdminInviteForm:
    """Admin invite form component for sending registration links via email."""
    
    def __init__(self, versioned_url=None):
        """Initialize the admin invite form component."""
        self.versioned_url = versioned_url or (lambda x: x)
    
    def render(self):
        """Render the admin invite form popup."""
        return Div(
            # Modal backdrop
            Div(
                # Modal content
                Div(
                    # Modal header
                    Div(
                        H2(
                            "Send Registration Link",
                            cls="text-2xl font-bold text-[#3D2E7C] mb-2",
                            id="admin-invite-form-title"
                        ),
                        Button(
                            Img(
                                src=self.versioned_url("/static/assets/close.svg"),
                                alt="Close",
                                cls="w-6 h-6 filter brightness-0"
                            ),
                            id="close-admin-invite-popup",
                            cls="text-gray-700 hover:text-gray-900 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                        ),
                        cls="flex justify-between items-center mb-6"
                    ),
                    
                    # Modal body
                    Div(
                        P(
                            "Enter the email address where the registration link should be sent.",
                            cls="text-gray-600 mb-6",
                            id="admin-invite-form-subtitle"
                        ),
                        
                        # Error message container
                        Div(
                            id="admin-invite-error",
                            cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
                        ),
                        
                        # Success message container
                        Div(
                            id="admin-invite-success",
                            cls="hidden mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm"
                        ),
                        
                        # Form
                        Form(
                            # Hidden field for club_id
                            Input(type="hidden", id="admin_invite_club_id", name="club_id"),
                            
                            # Email field
                            Div(
                                Label(
                                    "Email Address",
                                    for_="admin_invite_email",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="email",
                                    id="admin_invite_email",
                                    name="email",
                                    placeholder="user@example.com",
                                    required=True,
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="mb-6"
                            ),
                            
                            # Submit button
                            Button(
                                Span("Send Registration Link", id="admin-invite-button-text"),
                                Span("Sending...", id="admin-invite-button-loading", cls="hidden"),
                                type="submit",
                                id="admin-invite-submit-btn",
                                disabled=True,
                                cls="w-full bg-gray-400 cursor-not-allowed disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                            ),
                            
                            method="post",
                            action="/admin/send-registration-link",
                            id="admin-invite-form"
                        ),
                        cls=""
                    ),
                    
                    cls="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-auto transform transition-all duration-300 ease-out scale-95 opacity-0"
                ),
                cls="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
            ),
            id="admin-invite-popup",
            cls="hidden"
        ) 