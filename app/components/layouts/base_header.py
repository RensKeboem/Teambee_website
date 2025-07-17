"""
Base Header Component

Contains the standardized header component used across all pages.
"""

from fasthtml.common import *


class BaseHeader:
    """Base header component with standardized structure."""
    
    def __init__(self, versioned_url=None):
        """Initialize the base header."""
        self.versioned_url = versioned_url or (lambda x: x)
    
    def render(self, left_content, right_content):
        """Render the standardized header with custom left and right content.
        
        Args:
            left_content: Content for the left side (logo, title, etc.)
            right_content: Content for the right side (buttons, dropdowns, etc.)
        """
        return Header(
            Div(
                left_content,
                right_content,
                cls="container flex h-16 items-center justify-between"
            ),
            cls="fixed top-0 z-50 w-full bg-white/85 backdrop-blur-md supports-[backdrop-filter]:bg-white/65 border-b shadow-sm",
            role="banner"
        )
    
    def create_logo_link(self, href="/", title="Back to top"):
        """Create the standardized logo link."""
        return A(
            Img(
                src=self.versioned_url("/static/assets/Teambee logo donker.png"), 
                alt="Teambee Logo", 
                cls="h-8 sm:h-10 w-auto"
            ),
            href=href,
            title=title,
            aria_label="Back to top of page",
            cls="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
        )
    
    def create_language_dropdown(self, current_lang, alt_href, dropdown_id="language-dropdown"):
        """Create the standardized language dropdown."""
        return Div(
            Button(
                Span(current_lang.upper(), cls="mr-1"),
                Img(
                    src=self.versioned_url("/static/assets/dropdown-arrow.svg"),
                    alt="Language Dropdown",
                    cls="w-4 h-4"
                ),
                cls="flex items-center justify-center rounded-lg border border-gray-300 px-3 h-9 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-[#3D2E7C] focus:ring-offset-2",
                id=f"{dropdown_id}-button",
                type="button",
                aria_haspopup="true",
                aria_expanded="false"
            ),
            # Dropdown menu (initially hidden)
            Div(
                Div(
                    A(
                        "Nederlands",
                        href="/" if current_lang != "nl" else "#",
                        cls=f"block w-full px-4 py-2 text-left text-sm {'text-[#3D2E7C] font-semibold bg-gray-50' if current_lang == 'nl' else 'text-gray-700'} hover:bg-gray-100 hover:text-[#3D2E7C]",
                        hreflang="nl",
                        rel="alternate"
                    ),
                    cls="border-b border-gray-100"
                ),
                Div(
                    A(
                        "English",
                        href=alt_href if current_lang != "en" else "#",
                        cls=f"block w-full px-4 py-2 text-left text-sm {'text-[#3D2E7C] font-semibold bg-gray-50' if current_lang == 'en' else 'text-gray-700'} hover:bg-gray-100 hover:text-[#3D2E7C]",
                        hreflang="en",
                        rel="alternate"
                    ),
                    cls=""
                ),
                cls="hidden absolute right-0 z-10 mt-2 w-40 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none overflow-hidden",
                role="menu",
                aria_orientation="vertical",
                aria_labelledby=f"{dropdown_id}-button",
                id=f"{dropdown_id}-menu"
            ),
            cls="relative"
        ) 