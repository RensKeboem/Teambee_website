"""
Club Form Component

Contains the club creation form component for admin panel.
"""

from fasthtml.common import *


class ClubForm:
    """Club creation form component."""
    
    def __init__(self, versioned_url=None):
        """Initialize the club form component."""
        self.versioned_url = versioned_url or (lambda x: x)
    
    def render(self):
        """Render the club creation form."""
        return Form(
            Div(
                H2(
                    "Create New Club",
                    cls="text-3xl font-bold italic text-[#3D2E7C] mb-6"
                ),
                
                # Error message container
                Div(
                    id="club-error",
                    cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
                ),
                
                # Success message container
                Div(
                    id="club-success",
                    cls="hidden mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm"
                ),
                
                Div(
                    Label("Club Name", for_="name", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="text", id="name", name="name", placeholder="Enter club name", 
                          required=True, aria_required="true",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Label("System Prefix", for_="system_prefix", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="text", id="system_prefix", name="system_prefix", placeholder="e.g., CLUB_001", 
                          required=True, aria_required="true",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    Div("Unique identifier for the club's system", cls="text-xs text-gray-500 mt-1"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Label("Language", for_="language", cls="block text-sm font-medium text-gray-700 mb-1"),
                    
                    # Hidden input for form submission
                    Input(type="hidden", id="language", name="language", value="nl", required=True),
                    
                    # Custom dropdown
                    Div(
                        Button(
                            Span("Dutch", id="language-display", cls="mr-2"),
                            Img(
                                src=self.versioned_url("/static/assets/dropdown-arrow.svg"),
                                alt="Language Dropdown",
                                cls="w-4 h-4"
                            ),
                            cls="flex items-center justify-between w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C] text-left",
                            id="club-language-dropdown-button",
                            type="button",
                            aria_haspopup="true",
                            aria_expanded="false"
                        ),
                        # Dropdown menu (initially hidden)
                        Div(
                            Div(
                                Button(
                                    "Dutch",
                                    type="button",
                                    data_value="nl",
                                    cls="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 hover:text-[#3D2E7C] language-option",
                                ),
                                cls="border-b border-gray-100"
                            ),
                            Div(
                                Button(
                                    "English",
                                    type="button", 
                                    data_value="en",
                                    cls="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 hover:text-[#3D2E7C] language-option",
                                ),
                                cls=""
                            ),
                            cls="hidden absolute left-0 z-10 mt-2 w-full origin-top-left rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none overflow-hidden",
                            role="menu",
                            aria_orientation="vertical",
                            aria_labelledby="club-language-dropdown-button",
                            id="club-language-dropdown-menu"
                        ),
                        cls="relative"
                    ),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        "Create Club",
                        type="submit",
                        id="club-submit-btn",
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-3 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed"
                    ),
                    cls="flex flex-col"
                ),
                
                cls="flex flex-col gap-6"
            ),
            method="post",
            cls="max-w-md mx-auto",
            role="form"
        ) 