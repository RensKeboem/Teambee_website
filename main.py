from fasthtml.common import *
from app.components.forms.login_form import LoginForm
from app.components.forms.contact_form import ContactForm
from app.components.forms.password_reset_popup import PasswordResetPopup
from app.components.forms.registration_popup import RegistrationPopup
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.services.session_service import SessionService
from app.components.ui.hero_section import HeroSection
from app.components.ui.about_section import AboutSection
from app.components.ui.services_section import ServicesSection
from app.components.ui.benefits_section import BenefitsSection
from app.components.ui.reviews_section import ReviewsSection
from app.components.ui.login_section import LoginSection
from app.routes.auth import AuthRoutes
from app.routes.public import PublicRoutes
from app.routes.dashboard import DashboardRoutes
from app.routes.admin import AdminRoutes
from app.models.base import DatabaseManager
from app.config import config
from app.middleware.security import CustomHTTPSRedirectMiddleware, SecurityHeadersMiddleware
from app.middleware.language import LanguageMiddleware
from datetime import datetime
import os
import time
import json

from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware


class TeambeeApp:
    """Main application class for the Teambee website."""
    
    def __init__(self):
        """Initialize the Teambee application with TailwindCSS."""
        # Generate a global version string for cache busting
        self.version = str(int(time.time()))
        self.file_versions = {}
        
        # Load translations first
        self.translations = {}
        self.load_translations()
        
        # Initialize services
        try:
            self.auth = AuthService(DatabaseManager(), self.translations)
            self.email_service = EmailService()
        except Exception as e:
            print(f"Warning: Could not initialize services: {e}")
            self.auth = None
            self.email_service = None
        
        # Define middleware
        middleware = [
            Middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "teambee-secret-key-change-in-production")),
            Middleware(SecurityHeadersMiddleware),
            Middleware(LanguageMiddleware)
        ]
        
        # Only add HTTPS redirect in production
        if os.environ.get("ENVIRONMENT", "development") == "production":
            middleware.append(Middleware(CustomHTTPSRedirectMiddleware))
            
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
                # Stylesheets
                Link(rel="stylesheet", href=self.versioned_url("/static/app.css"), type="text/css"),
                Link(rel="icon", href=self.versioned_url("/static/assets/Teambee icon.png"), type="image/png"),
                # Scripts
                Script(src=self.versioned_url("/static/js/shared-utils.js")),
                Script(src=self.versioned_url("/static/js/ui-enhancements.js")),
                Script(src=self.versioned_url("/static/js/popup-dropdown.js")),
                Script(src=self.versioned_url("/static/js/form-handlers.js")),
                Script(src=self.versioned_url("/static/js/carousel.js")),
                Script(src=self.versioned_url("/static/js/success-stories.js")),
                Script(src=self.versioned_url("/static/js/password-reset-popup.js")),
                Script(src=self.versioned_url("/static/js/registration-popup.js")),
                Script(src=self.versioned_url("/static/js/auto-open-success-stories.js")),
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
    
    def get_message(self, key, default=""):
        """Get a translated message for the current language."""
        return self.get_text("messages", key, default)
    
    def get_language_root_url(self, request):
        """Get the root URL for the current language."""
        return "/en" if request.state.language == "en" else "/"
    
    def is_authenticated(self, request):
        """Check if user is authenticated."""
        return SessionService.is_authenticated(request)
    
    def get_current_user(self, request):
        """Get current user from session."""
        return SessionService.get_current_user(request)
    
    def login_user(self, request, user_info):
        """Log in user by storing info in session."""
        SessionService.login_user(request, user_info)
    
    def logout_user(self, request):
        """Log out user by clearing session."""
        SessionService.logout_user(request)
    
    def require_admin(self, request):
        """Check if user is authenticated and is admin."""
        return SessionService.require_admin(request, self.auth)
    
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

        # Initialize route handlers
        auth_routes = AuthRoutes(self)
        public_routes = PublicRoutes(self)
        dashboard_routes = DashboardRoutes(self)
        admin_routes = AdminRoutes(self)
        
        # Setup route groups
        auth_routes.setup_routes(rt)
        public_routes.setup_routes(rt)
        dashboard_routes.setup_routes(rt)
        admin_routes.setup_routes(rt)


        
        
        # Success stories direct link routes
        @rt("/success-stories")
        async def success_stories(request):
            """Render the home page with success stories panel automatically opened.
            
            This route works for both Dutch (/success-stories) and English (/en/success-stories) URLs.
            The LanguageMiddleware strips the /en prefix, so both URLs hit this single route.
            """
            self.request = request  # Store request for translation context
            
            # Check for success message in session and clear it
            success_message = request.session.pop("success_message", None)
            
            # Get the appropriate root URL for the current language
            target_url = self.get_language_root_url(request)
            
            homepage_content = self.create_homepage(
                success_message, 
                auto_open_success_stories=True, 
                target_url=target_url
            )
            
            return Title("Teambee"), homepage_content
    
    def send_contact_email(self, first_name, last_name, club_name, email, phone, identifier):
        """Send contact form email using EmailService."""
        if not self.email_service:
            return False, "Email service not available"
        
        return self.email_service.send_contact_email(
            first_name, last_name, club_name, email, phone, identifier
        )
    
    def create_homepage(self, success_message=None, auto_open_success_stories=False, target_url=None):
        """Create the Teambee homepage."""
        # Success message container (initially hidden)
        success_notification = Div(
            Div(
                Div(
                    Img(
                        src=self.versioned_url("/static/assets/check.svg"),
                        alt="Success",
                        cls="w-6 h-6 mr-3"
                    ),
                    Span(success_message or "", id="success-message-text"),
                                         Button(
                         Img(
                             src=self.versioned_url("/static/assets/close.svg"),
                             alt="Close",
                             cls="w-5 h-5 filter brightness-0"
                         ),
                         id="close-success-notification",
                         cls="ml-auto text-green-700 hover:text-green-900 transition-colors"
                     ),
                    cls="flex items-center bg-green-50 border border-green-200 rounded-lg p-4 shadow-sm"
                ),
                cls="container mx-auto px-4"
            ),
            cls="success-notification fixed top-20 left-0 right-0 z-40 animate-slide-down",
            style=f"display: {'block' if success_message else 'none'}",
            id="success-notification"
        ) if success_message else Div(id="success-notification", cls="success-notification fixed top-20 left-0 right-0 z-40 animate-slide-down", style="display: none")
        
        # Prepare container attributes
        container_attrs = {
            "cls": "flex min-h-screen flex-col relative"
        }
        
        # Add auto-open data attributes if needed
        if auto_open_success_stories and target_url:
            container_attrs["data-auto-open-success-stories"] = "true"
            container_attrs["data-target-url"] = target_url

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
            
            # Success notification
            success_notification,
            
            # Header
            self._create_header(),
            
            # Main content
            Main(
                # Hero Section
                HeroSection(self.translations, self.versioned_url, self.request.state.language).render(),
                
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
                AboutSection(self.translations, self.versioned_url, self.request.state.language).render(),
                
                # Services Section
                ServicesSection(self.translations, self.versioned_url, self.request.state.language).render(),
                
                # Benefits Section
                BenefitsSection(self.translations, self.versioned_url, self.request.state.language).render(),
                
                # Reviews Section
                ReviewsSection(self.translations, self.versioned_url, self.request.state.language).render(),
                
                # Login Section
                LoginSection(self.translations, self.versioned_url, self.request.state.language).render(),
                
                cls="flex-1 relative z-0",
                role="main",
                aria_label="Main content"
            ),
            
            # Footer
            self._create_footer(),
            
            # Login popup modal
            self._create_login_popup(),
            
            # Contact popup modal
            self._create_contact_popup(),
            
            # Password reset popup modal
            self._create_password_reset_popup(),
            
            # Registration popup modal
            self._create_registration_popup(),
            
            **container_attrs
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
                # Language selector dropdown and login button
                Div(
                    Div(
                        Button(
                            Span(current_lang.upper(), cls="mr-1"),
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
                        cls="relative"
                    ),
                    # Login button
                    Button(
                        self.get_text("login", "header_login"),
                        id="login-button",
                        cls="inline-flex h-9 items-center justify-center rounded-lg bg-[#94C46F] px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-[#94C46F]/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#94C46F] focus-visible:ring-offset-2 ml-3"
                    ),
                    cls="flex items-center"
                ),
                cls="container flex h-16 items-center justify-between"
            ),
            cls="fixed top-0 z-50 w-full bg-white/85 backdrop-blur-md supports-[backdrop-filter]:bg-white/65 border-b shadow-sm",
            role="banner"
        )
    

    
    
    
    def _create_login_popup(self):
        """Create the login popup modal."""
        # Get login translations for the current language
        login_translations = self.translations.get(self.request.state.language, {}).get("login", {})
        login_form = LoginForm(login_translations, "popup")
        
        return Div(
            # Modal backdrop
            Div(
                # Modal content
                Div(
                    # Modal header
                    Div(
                        H2(
                            self.get_text("login", "title"),
                            cls="text-2xl font-bold text-[#3D2E7C] mb-2"
                        ),
                        Button(
                            Img(
                                src=self.versioned_url("/static/assets/close.svg"),
                                alt="Close",
                                cls="w-6 h-6 filter brightness-0"
                            ),
                            id="close-login-popup",
                            cls="text-gray-700 hover:text-gray-900 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                        ),
                        cls="flex justify-between items-center mb-6"
                    ),
                    
                    # Modal body
                    Div(
                        P(
                            self.get_text("login", "subtitle"),
                            cls="text-gray-600 mb-6"
                        ),
                        
                        # Login form
                        login_form.render(),
                        cls=""
                    ),
                    
                    cls="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-auto transform transition-all duration-300 ease-out scale-95 opacity-0"
                ),
                cls="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
            ),
            id="login-popup",
            cls="hidden"
        )
    
    def _create_contact_popup(self):
        """Create the contact popup modal."""
        # Get contact translations for the current language
        contact_translations = self.translations.get(self.request.state.language, {}).get("contact", {})
        contact_form = ContactForm(contact_translations, self.versioned_url)
        
        return contact_form.render()
    
    def _create_password_reset_popup(self):
        """Create the password reset popup modal."""
        # Get password reset translations for the current language
        password_reset_translations = self.translations.get(self.request.state.language, {}).get("password_reset", {})
        password_reset_popup = PasswordResetPopup(password_reset_translations, self.versioned_url)
        
        return password_reset_popup.render()
    
    def _create_registration_popup(self):
        """Create the registration popup modal."""
        # Get registration translations for the current language
        registration_translations = self.translations.get(self.request.state.language, {}).get("registration", {})
        registration_popup = RegistrationPopup(registration_translations, self.versioned_url, self.request.state.language)
        
        return registration_popup.render()
    
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
                                    "info@teambee.fit",
                                    href="mailto:info@teambee.fit",
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
                                href="https://www.instagram.com/teamteambee/",
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
                                href="https://www.linkedin.com/company/teambee-fit",
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