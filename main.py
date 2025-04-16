from fasthtml.common import *
from login_form import LoginForm
from datetime import datetime
import os
import time
import json
from starlette.staticfiles import StaticFiles
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses."""
    
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' https://unpkg.com https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        
        # Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # HSTS (HTTP Strict Transport Security)
        # Only in production environment to avoid issues in development
        if os.environ.get("ENVIRONMENT", "development") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
            
        return response

class LanguageMiddleware(BaseHTTPMiddleware):
    """Middleware to handle language routing and detection."""
    
    async def dispatch(self, request, call_next):
        # Get the path
        path = request.url.path
        
        # Determine language from path
        if path.startswith("/en"):
            request.state.language = "en"
            # Strip language prefix for internal routing if it's not just /en
            if path != "/en" and path != "/en/":
                request.scope["path"] = path[3:]
        else:
            request.state.language = "nl"
        
        response = await call_next(request)
        return response

class TeambeeApp:
    """Main application class for the Teambee website."""
    
    def __init__(self):
        """Initialize the Teambee application with TailwindCSS."""
        # Generate a global version string for cache busting
        self.version = str(int(time.time()))
        self.file_versions = {}
        
        # Define middleware
        middleware = [
            Middleware(SecurityHeadersMiddleware),
            Middleware(LanguageMiddleware)
        ]
        
        # Only add HTTPS redirect in production
        if os.environ.get("ENVIRONMENT", "development") == "production":
            middleware.append(Middleware(HTTPSRedirectMiddleware))
        
        # Load translations
        self.translations = {}
        self.load_translations()
            
        self.app = FastHTML(
            hdrs=[
                # Meta tags for SEO
                Meta(name="description", content="Teambee helps premium high-end fitness clubs transform members into loyal ambassadors through personalized attention at scale."),
                Meta(name="keywords", content="fitness clubs, member retention, loyalty, personalized experience, teambee"),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Meta(property="og:title", content="Teambee | Transform Members into Loyal Ambassadors"),
                Meta(property="og:description", content="Help your fitness club members become loyal ambassadors through personalized attention at scale."),
                Meta(property="og:type", content="website"),
                Meta(property="og:url", content="https://teambee.fit"),
                # Language-specific meta tags
                Link(rel="alternate", hreflang="nl", href="https://teambee.fit/"),
                Link(rel="alternate", hreflang="en", href="https://teambee.fit/en"),
                Link(rel="alternate", hreflang="x-default", href="https://teambee.fit/"),
                # Stylesheets and scripts
                Link(rel="stylesheet", href=self.versioned_url("/static/app.css"), type="text/css"),
                Link(rel="icon", href=self.versioned_url("/static/assets/Teambee icon.png"), type="image/png"),
                Script(src=self.versioned_url("/static/js/parallax.js")),
                Script(src=self.versioned_url("/static/js/success-stories.js")),
                Script(src=self.versioned_url("/static/js/carousel.js")),
                Script(src=self.versioned_url("/static/js/language-dropdown.js")),
                Script(src=self.versioned_url("/static/js/smooth-scroll.js")),
            ],
            middleware=middleware
        )
        
        # Setup routes first to ensure they take precedence over static files
        self.setup_routes()
        
        # Mount static files after routes are defined
        self.app.mount("/static", StaticFiles(directory="public"), name="static")
    
    def load_translations(self):
        """Load translations from JSON files."""
        translations_dir = os.path.join(os.path.dirname(__file__), "translations")
        for lang in ["nl", "en"]:
            file_path = os.path.join(translations_dir, f"{lang}.json")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.translations[lang] = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading translations for {lang}: {e}")
                self.translations[lang] = {}
    
    def get_text(self, section, key, default=""):
        """Get text in the current language."""
        current_request = getattr(self, 'request', None)
        if not current_request:
            return default
            
        lang = current_request.state.language
        try:
            return self.translations[lang][section][key]
        except (KeyError, AttributeError):
            # Fallback to default language (Dutch) if translation is missing
            try:
                return self.translations["nl"][section][key]
            except (KeyError, AttributeError):
                return default
    
    def versioned_url(self, path):
        """Add version parameter to URL for cache busting.
        
        For static files, the version is based on the file's modification time or hash.
        For non-file paths, the global version is used.
        """
        if path.startswith("/static/"):
            # Get file-specific version based on modification time or hash
            file_path = path.replace("/static/", "public/")
            
            # Check the cache first
            if file_path in self.file_versions:
                version = self.file_versions[file_path]
            else:
                try:
                    # Use last modification time for the file
                    if os.path.exists(file_path):
                        version = str(int(os.path.getmtime(file_path)))
                        self.file_versions[file_path] = version
                    else:
                        version = self.version
                except:
                    # Fallback to the global version
                    version = self.version
                    
            return f"{path}?v={version}"
        else:
            # For non-static paths, use the global version
            return f"{path}?v={self.version}"
    
    def setup_routes(self):
        """Set up the application routes."""
        rt = self.app.route
        
        @rt("/")
        async def home(request):
            """Render the home page in Dutch (default)."""
            self.request = request  # Store request for translation context
            return Title("Teambee"), self.create_homepage()
        
        @rt("/en")
        async def home_en(request):
            """Render the home page in English."""
            self.request = request  # Store request for translation context
            return Title("Teambee"), self.create_homepage()
        
        @rt("/en/")
        async def home_en_slash(request):
            """Redirect /en/ to /en."""
            return RedirectResponse(url="/en", status_code=301)
        
        # Add a route to detect browser language and redirect accordingly
        @rt("/detect-language")
        async def detect_language(request):
            """Detect browser language and redirect to appropriate version."""
            accept_language = request.headers.get("accept-language", "")
            browser_lang = accept_language.split(",")[0].split("-")[0] if accept_language else "en"
            
            # Default to English unless browser language is Dutch
            if browser_lang == "nl":
                return RedirectResponse(url="/", status_code=302)
            else:
                return RedirectResponse(url="/en", status_code=302)
    
    def create_homepage(self):
        """Create the Teambee homepage."""
        return Div(
            # Honeycomb pattern background
            Div(
                Img(
                    src=self.versioned_url("/static/assets/honeycomb-cropped.svg"),
                    alt="Honeycomb Pattern",
                    cls="fixed top-16 w-[200%] h-[40vh] object-cover opacity-15 dark:opacity-10 z-0 pointer-events-none parallax"
                ),
                cls="fixed top-0 left-0 right-0 w-full h-screen"
            ),
            
            # Header
            self._create_header(),
            
            # Main content
            Main(
                # Hero Section
                self._create_hero_section(),
                
                # Jumping arrow between hero and about sections
                Div(
                    Img(
                        src=self.versioned_url("/static/assets/arrow-sm-down.svg"),
                        alt="Scroll down",
                        cls="w-12 h-12 mx-auto mb-8 animate-bounce opacity-50"
                    ),
                    cls="text-center -mt-8"
                ),
                
                # About Section
                self._create_about_section(),
                
                # Services Section
                self._create_services_section(),
                
                # Benefits Section
                self._create_benefits_section(),
                
                # Reviews Section
                self._create_reviews_section(),
                
                # Login Section
                self._create_login_section(),
                
                cls="flex-1 relative z-0",
                role="main",
                aria_label="Main content"
            ),
            
            # Footer
            self._create_footer(),
            
            cls="flex min-h-screen flex-col relative"
        )
    
    def _create_header(self):
        """Create the header section."""
        # Determine the current language and alternate language URL
        current_lang = self.request.state.language
        current_path = self.request.url.path
        
        # Determine the alternate language URL
        if current_lang == "nl":
            alt_lang = "en"
            alt_path = "/en" + (current_path if current_path != "/" else "")
        else:
            alt_lang = "nl"
            alt_path = current_path[3:] if current_path.startswith("/en") else current_path
            if alt_path == "" or alt_path == "/":
                alt_path = "/"
        
        return Header(
            Div(
                Div(
                    A(
                        Img(src=self.versioned_url("/static/assets/Teambee logo donker.png"), alt="Teambee Logo", cls="h-8 sm:h-10 w-auto"),
                        href="/" if current_lang == "nl" else "/en",
                        title="Back to top",
                        aria_label="Back to top of page",
                        cls="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                    ),
                    cls="flex items-center gap-2"
                ),
                # Language selector dropdown
                Div(
                    Div(
                        # Dropdown button
                        Button(
                            Span(current_lang.upper(), cls="mr-1"),
                            Img(
                                src=self.versioned_url("/static/assets/dropdown-arrow.svg"),
                                alt="Language Dropdown",
                                cls="w-4 h-4"
                            ),
                            cls="flex items-center justify-center rounded-lg border border-gray-300 px-3 py-1 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-[#3D2E7C] focus:ring-offset-2",
                            id="language-dropdown-button",
                            type="button",
                            aria_haspopup="true",
                            aria_expanded="false"
                        ),
                        # A(
                        #     "Login",
                        #     href="#login",
                        #     cls="inline-flex h-9 items-center justify-center rounded-lg bg-[#94C46F] px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-[#94C46F]/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#94C46F] focus-visible:ring-offset-2"§
                        # ),
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
                                    href=alt_path if current_lang != "en" else "#",
                                    cls=f"block w-full px-4 py-2 text-left text-sm {'text-[#3D2E7C] font-semibold bg-gray-50' if current_lang == 'en' else 'text-gray-700'} hover:bg-gray-100 hover:text-[#3D2E7C]",
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
                        cls="relative ml-3"
                    ),
                    cls="flex items-center"
                ),
                cls="container flex h-16 items-center justify-between"
            ),
            cls="fixed top-0 z-50 w-full bg-white/85 backdrop-blur-md supports-[backdrop-filter]:bg-white/65 border-b shadow-sm",
            role="banner"
        )
    
    def _create_hero_section(self):
        """Create the hero section."""
        return Section(
            Div(
                Div(
                    Div(
                        H1(
                            self.get_text("home", "hero_title"),
                            cls="text-4xl md:text-5xl font-bold italic text-[#3D2E7C] leading-tight"
                        ),
                        P(
                            self.get_text("home", "hero_subtitle"),
                            cls="text-lg text-gray-600 max-w-md"
                        ),
                        Div(
                            A(
                                "Our services",
                                Span("→", cls="ml-2"),
                                cls="inline-flex h-10 items-center justify-center rounded-lg bg-[#3D2E7C] px-8 py-2 text-sm font-medium text-white shadow transition-all duration-300 ease-in-out hover:bg-[#3D2E7C]/90 hover:scale-105 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2",
                                data_scroll_to="services"
                            ),
                            # A(
                            #     "Login",
                            #     href="#login",
                            #     cls="inline-flex h-10 items-center justify-center rounded-lg border border-[#3D2E7C] px-8 py-2 text-sm font-medium text-[#3D2E7C] shadow-sm transition-colors hover:bg-[#3D2E7C]/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                            # ),
                            cls="flex flex-col sm:flex-row gap-4"
                        ),
                        cls="space-y-6"
                    ),
                    Div(
                        Img(
                            src=self.versioned_url("/static/assets/Teambee icon.png"),
                            alt="Teambee Hero",
                            cls="w-full h-full object-contain",
                            loading="lazy"
                        ),
                        cls="relative h-[300px] md:h-[400px] hidden md:flex items-center justify-center"
                    ),
                    cls="grid gap-8 md:grid-cols-2 items-center"
                ),
                cls="container"
            ),
            cls="py-20 md:py-32"
        )
    
    def _create_about_section(self):
        """Create the about section."""
        return Section(
            Div(
                Div(
                    H2(
                        self.get_text("about", "title"),
                        cls="text-3xl md:text-4xl font-bold italic text-[#3D2E7C] mb-4"
                    ),
                    P(
                        self.get_text("about", "subtitle"),
                        cls="text-lg text-gray-600 max-w-2xl mx-auto"
                    ),
                    cls="text-center mb-12"
                ),
                
                Div(
                    # Synergie card
                    Div(
                        Div(
                            Img(
                                src=self.versioned_url("/static/assets/users.svg"),
                                alt="Synergie Icon",
                                cls="w-6 h-6"
                            ),
                            cls="w-12 h-12 bg-[#E8973A]/20 rounded-full flex items-center justify-center mb-4"
                        ),
                        H3(
                            self.get_text("about", "teamwork_title"),
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            self.get_text("about", "teamwork_text"),
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm transform transition-all duration-300 hover:-translate-y-2 hover:shadow-md"
                    ),
                    
                    # Resultaatgericht card
                    Div(
                        Div(
                            Img(
                                src=self.versioned_url("/static/assets/target.svg"),
                                alt="Resultaatgericht Icon",
                                cls="w-6 h-6"
                            ),
                            cls="w-12 h-12 bg-[#3D2E7C]/20 rounded-full flex items-center justify-center mb-4"
                        ),
                        H3(
                            self.get_text("about", "results_title"),
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            self.get_text("about", "results_text"),
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm transform transition-all duration-300 hover:-translate-y-2 hover:shadow-md"
                    ),
                    
                    # Duurzaam card
                    Div(
                        Div(
                            Img(
                                src=self.versioned_url("/static/assets/sprout.svg"),
                                alt="Duurzaam Icon",
                                cls="w-6 h-6"
                            ),
                            cls="w-12 h-12 bg-[#94C46F]/20 rounded-full flex items-center justify-center mb-4"
                        ),
                        H3(
                            self.get_text("about", "sustainable_title"),
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            self.get_text("about", "sustainable_text"),
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm transform transition-all duration-300 hover:-translate-y-2 hover:shadow-md"
                    ),
                    
                    cls="grid md:grid-cols-3 gap-8"
                ),
                
                cls="container"
            ),
            id="about",
            cls="py-16 md:py-24"
        )
    
    def _create_services_section(self):
        """Create the services section."""
        return Section(
            Div(
                Div(
                    H2(
                        self.get_text("services", "title"),
                        cls="text-3xl md:text-4xl font-bold italic mb-4"
                    ),
                    P(
                        self.get_text("services", "subtitle"),
                        cls="text-lg text-white/80 max-w-2xl mx-auto"
                    ),
                    cls="text-center mb-12"
                ),
                
                Div(
                    # Implementation section
                    Div(
                        Div(
                            H3(
                                self.get_text("services", "implementation"),
                                cls="text-xl font-semibold text-[#ffffff] mb-2"
                            ),
                            Ul(
                                self._create_check_list_item(self.get_text("services", "strategy")),
                                self._create_check_list_item(self.get_text("services", "design")),
                                self._create_check_list_item(self.get_text("services", "implementation_detail")),
                                self._create_check_list_item(self.get_text("services", "education")),
                                self._create_check_list_item(self.get_text("services", "data_support")),
                                cls="space-y-3"
                            ),
                            cls="bg-[#1B1947] p-6 rounded-lg"
                        ),
                        cls="flex flex-col"
                    ),
                    
                    # Call-to-action button
                    Div(
                        A(
                            self.get_text("services", "cta"),
                            cls="inline-flex h-12 items-center justify-center rounded-lg bg-[#94C46F] px-8 py-2 text-base font-medium text-white shadow transition-all duration-300 ease-in-out hover:bg-[#94C46F]/90 hover:scale-105 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#94C46F] focus-visible:ring-offset-2 mt-8",
                            data_scroll_to="contact"
                        ),
                        cls="text-center"
                    ),
                    
                    cls="grid gap-8"
                ),
                
                cls="container"
            ),
            id="services",
            cls="py-8 md:py-16 bg-[#3D2E7C] text-white"
        )
    
    def _create_check_list_item(self, text):
        """Create a check list item with an orange check icon."""
        return Li(
            Img(
                src=self.versioned_url("/static/assets/check.svg"),
                alt="Check",
                cls="h-6 w-6 mr-2 mt-0.5"
            ),
            Span(text),
            cls="flex items-start"
        )
    
    def _create_benefits_section(self):
        """Create the benefits section."""
        partners = [
            {"name": "TechnoGym", "logo": "TechnoGym", "url": "https://www.technogym.com/"},
            {"name": "Sportivity", "logo": "Sportivity", "url": "https://sportivity.nl/"},
            {"name": "Clickables", "logo": "Clickables", "url": "https://clickables.nl/"},
            {"name": "Unlock", "logo": "Unlock", "url": "https://unlock.nl/"}
        ]
        
        return Section(
            Div(
                Div(
                    H2(
                        self.get_text("benefits", "title"),
                        cls="text-3xl md:text-4xl font-bold italic text-[#3D2E7C] mb-4"
                    ),
                    P(
                        self.get_text("benefits", "subtitle"),
                        cls="text-lg text-gray-600 max-w-2xl mx-auto"
                    ),
                    cls="text-center mb-12"
                ),
                
                Div(
                    # Member Retention
                    Div(
                        Div(
                            self.get_text("benefits", "retention_percent"),
                            cls="text-4xl font-bold text-[#E8973A] mb-2"
                        ),
                        H3(
                            self.get_text("benefits", "retention_title"),
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            self.get_text("benefits", "retention_text"),
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100"
                    ),
                    
                    # Member Referrals
                    Div(
                        Div(
                            self.get_text("benefits", "referral_times"),
                            cls="text-4xl font-bold text-[#E8973A] mb-2"
                        ),
                        H3(
                            self.get_text("benefits", "referral_title"),
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            self.get_text("benefits", "referral_text"),
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100"
                    ),
                    
                    # Engagement Increase
                    Div(
                        Div(
                            self.get_text("benefits", "engagement_percent"),
                            cls="text-4xl font-bold text-[#E8973A] mb-2"
                        ),
                        H3(
                            self.get_text("benefits", "engagement_title"),
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            self.get_text("benefits", "engagement_text"),
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100"
                    ),
                    
                    cls="grid md:grid-cols-3 gap-8 mb-16"
                ),
                
                # Subtle line separator
                Div(
                    cls="border-t border-gray-100 w-full mb-8"
                ),
                
                # Partners section
                Div(
                    Div(
                        H3(
                            self.get_text("benefits", "partners"),
                            cls="text-lg font-medium text-gray-500 mb-8"
                        ),
                        cls="text-center"
                    ),
                    
                    Div(
                        *[
                            Div(
                                A(
                                    Img(
                                        src=self.versioned_url(f"/static/assets/{partner['logo']}.png"),
                                        alt=partner["name"],
                                        cls="h-10 md:h-8 w-auto object-contain transition-all duration-300 hover:scale-110 hover:opacity-90"
                                    ),
                                    href=partner["url"],
                                    target="_blank",
                                    rel="noopener noreferrer",
                                    aria_label=f"Visit {partner['name']} website",
                                    cls="flex items-center justify-center p-4"
                                ),
                                cls="flex items-center justify-center"
                            )
                            for partner in partners
                        ],
                        cls="grid grid-cols-2 md:flex md:flex-nowrap justify-center items-center gap-4 md:gap-12 max-w-4xl mx-auto"
                    ),
                    
                    cls="container"
                ),
                
                cls="container"
            ),
            id="benefits",
            cls="pt-16 pb-8 bg-white/80 backdrop-blur-sm"
        )
    
    def _create_reviews_section(self):
        """Create the reviews section with client testimonials."""
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
            "Jasper Appeldoorn": "xfit_foto.jpg"
        }
        
        # Generate review cards dynamically from the loaded data
        review_cards = []
        for i, review in enumerate(reviews):
            # Get the appropriate image for the author
            image_file = author_images.get(review["author"], "profile-placeholder.svg")
            
            # Create the review card
            review_card = Div(
                Div(
                    Img(
                        src=self.versioned_url("/static/assets/quote.svg"),
                        alt="Quote",
                        cls="w-8 h-8 text-[#E8973A]"
                    ),
                    P(
                        review["quote"],
                        cls="text-gray-600 mb-4 flex-grow"
                    ),
                    Div(
                        Div(
                            Img(
                                src=self.versioned_url(f"/static/assets/{image_file}"),
                                alt=review["author"],
                                cls="w-10 h-10 rounded-full bg-gray-200 mr-3 object-cover"
                            ),
                            Div(
                                Div(
                                    review["author"],
                                    cls="font-semibold text-[#1B1947]"
                                ),
                                Div(
                                    review["title"],
                                    cls="text-sm text-gray-500"
                                ),
                            ),
                        ),
                        cls="flex items-center mt-3"
                    ),
                    cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100 h-full flex flex-col justify-between w-full"
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
                        cls="text-3xl md:text-4xl font-bold italic text-[#3D2E7C] mb-4"
                    ),
                    P(
                        self.get_text("reviews", "subtitle"),
                        cls="text-lg text-gray-600 max-w-2xl mx-auto"
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
                                cls="slides flex transition-transform duration-300 ease-out relative cursor-grab active:cursor-grabbing"
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
                            cls="inline-flex h-12 items-center justify-center rounded-lg bg-[#94C46F] px-8 py-2 text-base font-medium text-white shadow transition-all duration-300 ease-in-out hover:bg-[#94C46F]/90 hover:scale-105 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#94C46F] focus-visible:ring-offset-2 mt-8",
                            id="show-success-stories"
                        ),
                        cls="text-center"
                    ),
                    
                    # Success stories panel (initially hidden)
                    Div(
                        Div(
                            # Header with close button that sticks to the top
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
                                cls="sticky top-0 bg-[#3D2E7C] pt-4 pb-4 z-20 flex justify-between items-center px-4 md:px-8"
                            ),
                            
                            # Panel content
                            Div(
                                Div(
                                    # Success stories container with vertical scrolling
                                    cls="space-y-8"
                                ),
                                # Add extra padding at the bottom
                                cls="max-w-7xl mx-auto px-4 pt-4 pb-24"
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
    
    def _create_login_section(self):
        """Create the login section."""
        login_form = LoginForm()
        
        return Section(
            Div(
                Div(
                    Div(
                        H2(
                            self.get_text("login", "title"),
                            id="login-heading",
                            cls="text-3xl font-bold italic text-[#3D2E7C] mb-2"
                        ),
                        P(
                            self.get_text("login", "subtitle"),
                            cls="text-gray-600"
                        ),
                        cls="text-center mb-8"
                    ),
                    
                    # Wrapper with relative positioning
                    Div(
                        # Login form
                        login_form.render(),
                        
                        # Overlay with improved styling, extended beyond form edges
                        Div(
                            Div(
                                H3(
                                    self.get_text("login", "coming_soon"),
                                    cls="text-2xl font-bold text-white mb-2"
                                ),
                                P(
                                    self.get_text("login", "coming_soon_text"),
                                    cls="text-white/90"
                                ),
                                cls="text-center p-8 bg-[#3D2E7C] rounded-lg shadow-lg w-full max-w-sm"
                            ),
                            cls="absolute -inset-8 flex items-center justify-center z-10 bg-white/50 backdrop-blur-sm rounded-2xl"
                        ),
                        
                        cls="relative"
                    ),
                    
                    cls="max-w-md mx-auto"
                ),
                cls="container relative z-10"
            ),
            
            # Bottom honeycomb pattern
            Div(
                Img(
                    src=self.versioned_url("/static/assets/honeycomb-cropped.svg"),
                    alt="Honeycomb Pattern",
                    cls="w-[200%] h-[40vh] object-cover opacity-15 dark:opacity-10 pointer-events-none [transform:scaleY(-1)]",
                    loading="lazy"
                ),
                cls="absolute bottom-0 left-0 right-0 w-full h-[40vh] z-0"
            ),
            
            id="login",
            cls="pt-8 md:pt-12 pb-16 bg-white/90 backdrop-blur-sm relative"
        )
    
    def _create_footer(self):
        """Create the footer section."""
        return Footer(
            Div(
                Div(
                    Div(
                        Div(
                            Img(
                                src=self.versioned_url("/static/assets/Teambee logo wit.png"),
                                alt="Teambee Logo",
                                cls="h-8 w-auto"
                            ),
                            cls="mb-4"
                        ),
                        P(
                            self.get_text("footer", "description"),
                            cls="text-white/70 text-sm"
                        ),
                        cls=""
                    ),
                    
                    Div(
                        H3(
                            self.get_text("footer", "contact"),
                            cls="font-semibold text-lg mb-4"
                        ),
                        Ul(
                            Li(
                                A(
                                    "info@teambee.nl",
                                    href="mailto:info@teambee.nl",
                                    cls="text-white/70 hover:text-white transition-colors"
                                ),
                                cls=""
                            ),
                            Li(
                                A(
                                    "+31 (6) 24 52 79 37", 
                                    href="tel:+31624527937",
                                    cls="text-white/70 hover:text-white transition-colors"
                                ),
                                cls=""
                            ),
                            Li(
                                A(
                                    "Hellingbaan 424, Amsterdam", 
                                    href="https://www.google.com/maps/search/?api=1&query=Hellingbaan+424+Amsterdam",
                                    target="_blank",
                                    rel="noopener noreferrer",
                                    cls="text-white/70 hover:text-white transition-colors"
                                ),
                                cls=""
                            ),
                            cls="space-y-2"
                        ),
                        cls="md:text-right contact-info"
                    ),
                    
                    cls="grid gap-8 md:grid-cols-2"
                ),
                
                Div(
                    Div(
                        P(
                            f"© {datetime.now().year} Teambee. " + self.get_text("footer", "rights_reserved"),
                            cls=""
                        ),
                        cls="text-white/50 text-sm"
                    ),
                    
                    Div(
                        Div(
                            A(
                                Img(
                                    src=self.versioned_url("/static/assets/instagram-167-svgrepo-com.svg"),
                                    alt="Instagram",
                                    cls="w-6 h-6"
                                ),
                                href="https://www.instagram.com/keboemmastersinretention/",
                                target="_blank",
                                rel="noopener noreferrer",
                                aria_label="Follow us on Instagram",
                                cls="hover:opacity-75 transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-[#1B1947] rounded-lg"
                            ),
                            cls="px-3 transform transition-transform duration-300"
                        ),
                        Div(
                            A(
                                Img(
                                    src=self.versioned_url("/static/assets/linkedin-svgrepo-com.svg"),
                                    alt="LinkedIn",
                                    cls="w-6 h-6"
                                ),
                                href="https://linkedin.com/company/keboem",
                                target="_blank",
                                rel="noopener noreferrer",
                                aria_label="Connect with us on LinkedIn",
                                cls="hover:opacity-75 transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-[#1B1947] rounded-lg"
                            ),
                            cls="px-3 transform transition-transform duration-300"
                        ),
                        Div(
                            A(
                                Img(
                                    src=self.versioned_url("/static/assets/facebook-svgrepo-com.svg"),
                                    alt="Facebook",
                                    cls="w-6 h-6"
                                ),
                                href="https://www.facebook.com/keboem",
                                target="_blank",
                                rel="noopener noreferrer",
                                aria_label="Visit our Facebook page",
                                cls="hover:opacity-75 transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-[#1B1947] rounded-lg"
                            ),
                            cls="px-3 transform transition-transform duration-300"
                        ),
                        cls="flex items-center justify-end"
                    ),
                    
                    cls="border-t border-white/10 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center gap-6"
                ),
                
                cls="container"
            ),
            cls="bg-[#1B1947] text-white py-12 relative z-0",
            role="contentinfo",
            id="contact"
        )
    
    def get_app(self):
        """Return the FastHTML app instance."""
        return self.app


# Initialize the Teambee application
teambee = TeambeeApp()

# Expose the app at the module level for FastHTML to find
app = teambee.get_app()

if __name__ == "__main__":
    # Start the FastHTML server
    serve(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))