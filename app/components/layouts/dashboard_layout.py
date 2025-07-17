"""
Dashboard Layout Component

Contains the dashboard layout component for user dashboard pages.
"""

from fasthtml.common import *
from app.components.forms.password_update_form import PasswordUpdateForm
from app.components.forms.user_invite_form import UserInviteForm
from app.components.layouts.base_header import BaseHeader


class DashboardLayout:
    """Dashboard layout component."""
    
    def __init__(self, translations=None, versioned_url=None, current_lang="nl"):
        """Initialize the dashboard layout."""
        self.translations = translations or {}
        self.versioned_url = versioned_url or (lambda x: x)
        self.current_lang = current_lang
    
    def get_text(self, key: str, default: str = "") -> str:
        """Get translated text for the given key."""
        return self.translations.get(key, default)
    
    def render(self, user_info: dict, content = None):
        """Render the dashboard layout."""
        # Determine language URLs
        if self.current_lang == "nl":
            alt_lang_url = "/en/dashboard"
            current_lang_display = "NL"
        else:
            alt_lang_url = "/dashboard"
            current_lang_display = "EN"
            
        # Create base header
        base_header = BaseHeader(self.versioned_url)
        
        return Html(
            Head(
                Title(self.get_text("title", "Teambee Dashboard")),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Link(rel="stylesheet", href=self.versioned_url("/static/app.css"), type="text/css"),
                Link(rel="icon", href=self.versioned_url("/static/assets/Teambee icon.png"), type="image/png"),
                Script(src=self.versioned_url("/static/js/shared-utils.js")),
                Script(src=self.versioned_url("/static/js/popup-dropdown.js")),
                Script(src=self.versioned_url("/static/js/user-dropdown.js")),
            ),
            Body(
                # Header using base header component
                base_header.render(
                    # Left content: Logo
                    Div(
                        base_header.create_logo_link(
                            f"/admin/view-club-dashboard/{user_info.get('club_id')}" if user_info.get("is_admin_viewing") else ("/dashboard" if self.current_lang == "nl" else "/en/dashboard"), 
                            "Dashboard"
                        ),
                        cls="flex items-center gap-2"
                    ),
                    # Right content: Language dropdown and user dropdown
                    Div(
                        # Language selector dropdown - need to fix href for dashboard
                        Div(
                            Button(
                                Span(current_lang_display, cls="mr-1"),
                                Img(
                                    src=self.versioned_url("/static/assets/dropdown-arrow.svg"),
                                    alt="Language Dropdown",
                                    cls="w-4 h-4"
                                ),
                                cls="flex items-center justify-center rounded-lg border border-gray-300 px-3 h-9 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-[#3D2E7C] focus:ring-offset-2",
                                id="language-dropdown-button",
                                type="button",
                                aria_haspopup="true",
                                aria_expanded="false"
                            ),
                            # Dropdown menu (initially hidden)
                            Div(
                                Div(
                                    A(
                                        "Nederlands",
                                        href=f"/admin/view-club-dashboard/{user_info.get('club_id')}?lang=nl" if user_info.get("is_admin_viewing") else ("/dashboard" if self.current_lang != "nl" else "#"),
                                        cls=f"block w-full px-4 py-2 text-left text-sm {'text-[#3D2E7C] font-semibold bg-gray-50' if self.current_lang == 'nl' else 'text-gray-700'} hover:bg-gray-100 hover:text-[#3D2E7C]",
                                        hreflang="nl",
                                        rel="alternate"
                                    ),
                                    cls="border-b border-gray-100"
                                ),
                                Div(
                                    A(
                                        "English",
                                        href=f"/admin/view-club-dashboard/{user_info.get('club_id')}?lang=en" if user_info.get("is_admin_viewing") else ("/en/dashboard" if self.current_lang != "en" else "#"),
                                        cls=f"block w-full px-4 py-2 text-left text-sm {'text-[#3D2E7C] font-semibold bg-gray-50' if self.current_lang == 'en' else 'text-gray-700'} hover:bg-gray-100 hover:text-[#3D2E7C]",
                                        hreflang="en",
                                        rel="alternate"
                                    ),
                                    cls=""
                                ),
                                cls="hidden absolute right-0 z-10 mt-2 w-40 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none overflow-hidden",
                                role="menu",
                                aria_orientation="vertical",
                                aria_labelledby="language-dropdown-button",
                                id="language-dropdown-menu"
                            ),
                            cls="relative mr-3"
                        ),
                        
                        # User dropdown (hidden when admin viewing)
                        Div(
                            Button(
                                Img(src=self.versioned_url("/static/assets/user.svg"), alt="User Menu", cls="w-5 h-5"),
                                id="user-dropdown-button",
                                aria_expanded="false",
                                aria_haspopup="true",
                                cls="inline-flex items-center justify-center w-9 h-9 rounded-lg text-gray-700 border border-gray-300 hover:bg-gray-100 hover:border-gray-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                            ),
                            
                            # Dropdown menu
                            Div(
                                # Only show user functions if not admin viewing
                                Button(
                                    self.get_text("update_password", "Update Password"),
                                    type="button",
                                    id="update-password-option",
                                    cls="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[#3D2E7C]"
                                ) if not user_info.get("is_admin_viewing") else "",
                                Button(
                                    self.get_text("invite_new_user", "Invite New User"),
                                    type="button",
                                    id="invite-user-option",
                                    cls="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[#3D2E7C]"
                                ) if not user_info.get("is_admin_viewing") else "",
                                Div(cls="border-t border-gray-100 my-1") if not user_info.get("is_admin_viewing") else "",
                                A(
                                    "← Back to Admin Panel" if user_info.get("is_admin_viewing") else self.get_text("logout", "Logout"),
                                    href="/admin/clubs" if user_info.get("is_admin_viewing") else "/logout",
                                    cls="block w-full text-left px-4 py-2 text-sm text-blue-600 hover:bg-blue-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-blue-500" if user_info.get("is_admin_viewing") else "block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-red-500"
                                ),
                                id="user-dropdown-menu",
                                cls="hidden absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50",
                                role="menu",
                                aria_orientation="vertical"
                            ),
                            
                            cls="relative"
                        ) if not user_info.get("is_admin_viewing") else A(
                            "← Back to Admin Panel",
                            href="/admin/clubs",
                            cls="inline-flex items-center justify-center px-3 h-9 rounded-lg text-sm font-medium text-blue-600 border border-blue-600 hover:bg-blue-600 hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2"
                        ),
                        
                        cls="flex items-center"
                    )
                ),
                
                # Main content
                Main(
                    Div(
                        # Admin notice (if provided as content)
                        content if content else "",
                        
                        H1(self.get_text("page_title", "Dashboard"), cls="text-3xl font-bold text-[#3D2E7C] mb-8"),
                        
                        # Dashboard content
                        Div(
                            Div(
                                H2(self.get_text("welcome_message", "Welcome to your Teambee Dashboard"), cls="text-xl font-semibold mb-4"),
                                P(self.get_text("welcome_subtitle", "Use the user menu in the top right to update your password or invite new users to your club.") if not user_info.get("is_admin_viewing") else self.get_text("admin_viewing_subtitle", "You are viewing this club's dashboard as an administrator."), 
                                  cls="text-gray-500"),
                                cls="bg-white p-6 rounded-lg shadow-sm border max-w-2xl mx-auto text-center"
                            ),
                            cls="grid gap-6"
                        ),
                        
                        cls="container mx-auto px-4 py-8"
                    ),
                    cls="flex-1 bg-gray-50 pt-16"
                ),
                
                # Password Update Popup (only show if not admin viewing)
                Div(
                    Div(
                        Div(
                            # Modal header
                            Div(
                                H2(self.get_text("update_password", "Update Password"), cls="text-2xl font-bold text-[#3D2E7C] mb-2"),
                                Button(
                                    Img(src=self.versioned_url("/static/assets/close.svg"), alt="Close", cls="w-6 h-6 filter brightness-0"),
                                    id="close-password-popup",
                                    cls="text-gray-700 hover:text-gray-900 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                                ),
                                cls="flex justify-between items-center mb-6"
                            ),
                            
                            # Modal body
                            Div(
                                PasswordUpdateForm(self.translations, self.current_lang).render(),
                                cls=""
                            ),
                            
                            cls="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-auto transform transition-all duration-300 ease-out scale-95 opacity-0"
                        ),
                        cls="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
                    ),
                    id="password-update-popup",
                    cls="hidden"
                ) if not user_info.get("is_admin_viewing") else "",
                
                # User Invite Popup (only show if not admin viewing)
                Div(
                    Div(
                        Div(
                            # Modal header
                            Div(
                                H2(self.get_text("invite_new_user", "Invite New User"), cls="text-2xl font-bold text-[#3D2E7C] mb-2"),
                                Button(
                                    Img(src=self.versioned_url("/static/assets/close.svg"), alt="Close", cls="w-6 h-6 filter brightness-0"),
                                    id="close-invite-popup",
                                    cls="text-gray-700 hover:text-gray-900 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                                ),
                                cls="flex justify-between items-center mb-6"
                            ),
                            
                            # Modal body
                            Div(
                                UserInviteForm(self.translations, self.current_lang).render(),
                                cls=""
                            ),
                            
                            cls="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-auto transform transition-all duration-300 ease-out scale-95 opacity-0"
                        ),
                        cls="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
                    ),
                    id="user-invite-popup",
                    cls="hidden"
                ) if not user_info.get("is_admin_viewing") else "",
                
                cls="min-h-screen flex flex-col"
            )
        ) 