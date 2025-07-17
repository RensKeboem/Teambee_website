"""
Admin Panel Layout Component

Contains the admin panel layout component for admin pages.
"""

from fasthtml.common import *
from app.components.layouts.base_header import BaseHeader


class AdminPanelLayout:
    """Admin panel layout component."""
    
    def __init__(self, versioned_url=None):
        """Initialize the admin panel layout."""
        self.versioned_url = versioned_url or (lambda x: x)
    
    def render(self, user_info: dict, content):
        """Render the admin panel layout."""
        # Create base header
        base_header = BaseHeader(self.versioned_url)
        
        return Html(
            Head(
                Title("Teambee Admin Panel"),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Link(rel="stylesheet", href=self.versioned_url("/static/app.css"), type="text/css"),
                Link(rel="icon", href=self.versioned_url("/static/assets/Teambee icon.png"), type="image/png"),
                Script(src="https://unpkg.com/htmx.org@1.9.10"),
                Script(src=self.versioned_url("/static/js/shared-utils.js")),
                Script(src=self.versioned_url("/static/js/popup-dropdown.js")),
                Script(src=self.versioned_url("/static/js/admin-search.js")),
                Script(src=self.versioned_url("/static/js/club-form.js")),
            ),
            Body(
                # Header using base header component
                base_header.render(
                    # Left content: Logo + Admin Panel text
                    Div(
                        base_header.create_logo_link("/admin/users", "Admin Panel"),
                        Span("Admin Panel", cls="ml-4 text-lg font-semibold text-[#3D2E7C]"),
                        cls="flex items-center gap-2"
                    ),
                    # Right content: Logout
                    Div(
                        A("Logout", href="/logout", 
                          cls="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium"),
                        cls="flex items-center"
                    )
                ),
                
                # Navigation
                Nav(
                    Div(
                        A("Users", href="/admin/users", 
                          cls="px-4 py-2 text-sm font-medium text-[#3D2E7C] hover:bg-gray-100 rounded-lg"),
                        A("Clubs", href="/admin/clubs", 
                          cls="px-4 py-2 text-sm font-medium text-[#3D2E7C] hover:bg-gray-100 rounded-lg"),
                        A("Create Club", href="/admin/create-club", 
                          cls="px-4 py-2 text-sm font-medium bg-[#3D2E7C] text-white hover:bg-[#3D2E7C]/90 rounded-lg"),
                        cls="container flex gap-2 px-4 py-3"
                    ),
                    cls="bg-gray-50 border-b mt-16"
                ),
                
                # Main content
                Main(
                    content,
                    cls="flex-1 bg-gray-50 py-8"
                ),
                
                # Delete Confirmation Popup
                Div(
                    # Modal backdrop
                    Div(
                        # Modal content
                        Div(
                            # Modal header
                            Div(
                                H2(
                                    "Confirm Delete",
                                    cls="text-2xl font-bold text-red-600 mb-2"
                                ),
                                Button(
                                    Img(
                                        src=self.versioned_url("/static/assets/close.svg"),
                                        alt="Close",
                                        cls="w-6 h-6 filter brightness-0"
                                    ),
                                    id="close-delete-popup",
                                    cls="text-gray-700 hover:text-gray-900 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-600 focus-visible:ring-offset-2 rounded-lg"
                                ),
                                cls="flex justify-between items-center mb-6"
                            ),
                            
                            # Modal body
                            Div(
                                P(
                                    "Are you sure you want to delete this user? This action cannot be undone.",
                                    cls="text-gray-700 mb-6"
                                ),
                                Div(
                                    "Email: ",
                                    Span(id="delete-user-email", cls="font-semibold"),
                                    cls="text-sm text-gray-600 mb-6"
                                ),
                                
                                # Action buttons
                                Div(
                                    Button(
                                        "Cancel",
                                        id="cancel-delete-btn",
                                        cls="px-4 py-2 text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-lg font-medium mr-3 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-500 focus-visible:ring-offset-2"
                                    ),
                                    Button(
                                        "Delete User",
                                        id="confirm-delete-btn",
                                        cls="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-600 focus-visible:ring-offset-2"
                                    ),
                                    cls="flex justify-end"
                                ),
                                cls=""
                            ),
                            
                            cls="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-auto transform transition-all duration-300 ease-out scale-95 opacity-0"
                        ),
                        cls="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
                    ),
                    id="delete-confirmation-popup",
                    cls="hidden"
                ),
                
                cls="min-h-screen flex flex-col"
            )
        ) 