"""
Reviews Section Component

Contains the reviews section component for the homepage.
"""

from fasthtml.common import *
import json
import os


class ReviewsSection:
    """Reviews section component."""
    
    def __init__(self, translations=None, versioned_url=None, current_lang="nl"):
        """Initialize the reviews section component."""
        self.translations = translations or {}
        self.versioned_url = versioned_url or (lambda x: x)
        self.current_lang = current_lang
    
    def get_text(self, section: str, key: str, default: str = "") -> str:
        """Get translated text for the given section and key."""
        try:
            return self.translations[self.current_lang][section][key]
        except (KeyError, AttributeError):
            # Fallback to Dutch if translation is missing
            try:
                return self.translations["nl"][section][key]
            except (KeyError, AttributeError):
                return default
    
    def render(self):
        """Render the reviews section with client testimonials."""
        # Load reviews from JSON file
        reviews_path = os.path.join("public", "data", "reviews.json")
        try:
            with open(reviews_path, 'r') as f:
                reviews = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            reviews = []
        
        # Map of author names to their corresponding image files
        author_images = {
            "Marco & Patricia Kalfshoven": "doit_foto.jpeg",
            "Rick Sombroek": "rick_foto.jpg",
            "Jochem van der Linden": "xfit_foto.jpg",
            "Jasper Appeldoorn": "xfit_foto.jpg",
            "Jelle Notkamp": "EV_jelle.jpg"
        }
        
        # Generate review cards dynamically from the loaded data
        review_cards = []
        for i, review in enumerate(reviews):
            # Get the appropriate image for the author
            image_file = author_images.get(review["author"]["nl"], "profile-placeholder.svg")
            
            # Create the review card
            review_card = Div(
                Div(
                    Div(
                        Img(
                            src=self.versioned_url("/static/assets/quote.svg"),
                            alt="Quote",
                            cls="w-8 h-8 text-[#E8973A]"
                        ),
                        # Add translation label for English
                        Span(
                            "Translated from Dutch",
                            cls="text-xs text-gray-400 ml-2 italic" if self.current_lang == "en" else "hidden",
                        ),
                        cls="flex items-center mb-4"
                    ),
                    P(
                        review["quote"][self.current_lang],
                        cls="text-gray-600 mb-4 flex-grow"
                    ),
                    Div(
                        Div(
                            Img(
                                src=self.versioned_url(f"/static/assets/{image_file}"),
                                alt=review["author"][self.current_lang],
                                cls="w-10 h-10 rounded-full bg-gray-200 mr-3 object-cover"
                            ),
                            Div(
                                Div(
                                    review["author"][self.current_lang],
                                    cls="font-semibold text-[#1B1947]"
                                ),
                                Div(
                                    review["title"][self.current_lang],
                                    cls="text-sm text-gray-500"
                                ),
                            ),
                        ),
                        cls="flex items-center mt-3"
                    ),
                    cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100 h-full flex flex-col justify-between w-full animate-card"
                ),
                cls="slide w-full flex-shrink-0 px-4",
                id=f"review-{i}"  # Add unique ID for each review
            )
            review_cards.append(review_card)
        
        return Section(
            Div(
                Div(
                    H2(
                        self.get_text("reviews", "title"),
                        cls="text-3xl md:text-4xl font-bold italic text-[#3D2E7C] mb-4 animate-section-title"
                    ),
                    P(
                        self.get_text("reviews", "subtitle"),
                        cls="text-lg text-gray-600 max-w-2xl mx-auto animate-section-subtitle"
                    ),
                    cls="text-center mb-6"
                ),
                
                # Carousel implementation
                Div(
                    # Main slider container
                    Div(
                        # Wrapper for the slides
                        Div(
                            # Container for the slides
                            Div(
                                *review_cards,
                                id="slides",
                                cls="slides flex transition-transform duration-300 ease-out relative cursor-grab active:cursor-grabbing animate-stagger-container"
                            ),
                            cls="wrapper overflow-hidden relative w-full touch-pan-x"
                        ),
                        id="slider",
                        cls="slider relative w-full max-w-4xl mx-auto"
                    ),
                    
                    # Dots for navigation
                    Div(
                        id="review-dots",
                        cls="flex justify-center gap-2 mt-8"
                    ),
                    
                    # Success stories button
                    Div(
                        Button(
                            self.get_text("reviews", "success_stories"),
                            cls="inline-flex h-12 items-center justify-center rounded-lg bg-[#94C46F] px-8 py-2 text-base font-medium text-white shadow transition-all duration-300 ease-in-out hover:bg-[#94C46F]/90 hover:scale-105 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#94C46F] focus-visible:ring-offset-2 mt-8 animate-card",
                            id="show-success-stories"
                        ),
                        cls="text-center"
                    ),
                    
                    # Success stories panel (initially hidden)
                    Div(
                        Div(
                            # Header with close button that sticks to the top
                            Div(
                                Div(
                                    # Title on the left
                                    H3(
                                        self.get_text("reviews", "success_title"),
                                        cls="text-3xl md:text-4xl font-bold italic text-[#ffffff] mb-0"
                                    ),
                                    # Close button on the right
                                    Button(
                                        Img(
                                            src=self.versioned_url("/static/assets/close.svg"),
                                            alt="Close",
                                            cls="w-6 h-6"
                                        ),
                                        cls="text-white hover:text-gray-200 transition-colors",
                                        id="close-success-stories"
                                    ),
                                    cls="flex justify-between items-center w-full container mx-auto"
                                ),
                                cls="sticky top-0 bg-[#3D2E7C] pt-4 pb-4 z-20 w-full flex justify-center"
                            ),
                            
                            # Panel content
                            Div(
                                Div(
                                    # Success stories container with vertical scrolling
                                    cls="space-y-8"
                                ),
                                # Add extra padding at the bottom
                                cls="container mx-auto pt-4 pb-24"
                            ),
                            cls="bg-[#3D2E7C] h-screen w-full fixed top-16 right-0 transform translate-x-full transition-transform duration-500 ease-in-out z-[100] overflow-y-auto"
                        ),
                        id="success-stories-panel"
                    ),
                    
                    cls="relative"
                ),
                
                cls="container"
            ),
            id="reviews",
            cls="py-8 md:py-16 bg-gray-100"
        ) 