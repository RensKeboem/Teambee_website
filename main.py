from fasthtml.common import *
from login_form import LoginForm
from datetime import datetime
import os
import time
from starlette.staticfiles import StaticFiles
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses."""
    
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
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

class TeambeeApp:
    """Main application class for the Teambee website."""
    
    def __init__(self):
        """Initialize the Teambee application with TailwindCSS."""
        # Generate a global version string for cache busting
        self.version = str(int(time.time()))
        self.file_versions = {}
        
        # Define middleware
        middleware = [
            Middleware(SecurityHeadersMiddleware)
        ]
        
        # Only add HTTPS redirect in production
        if os.environ.get("ENVIRONMENT", "development") == "production":
            middleware.append(Middleware(HTTPSRedirectMiddleware))
            
        self.app = FastHTML(
            hdrs=[
                # Meta tags for SEO
                Meta(name="description", content="Teambee helps premium high-end fitness clubs transform members into loyal ambassadors through personalized attention at scale."),
                Meta(name="keywords", content="fitness clubs, member retention, loyalty, personalized experience, teambee"),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Meta(property="og:title", content="Teambee | Transform Members into Loyal Ambassadors"),
                Meta(property="og:description", content="Help your fitness club members become loyal ambassadors through personalized attention at scale."),
                Meta(property="og:type", content="website"),
                Meta(property="og:url", content="https://teambee.com"),
                # Stylesheets and scripts
                Link(rel="stylesheet", href=self.versioned_url("/static/app.css"), type="text/css"),
                Link(rel="icon", href=self.versioned_url("/static/assets/Teambee icon.png"), type="image/png"),
                Script(src=self.versioned_url("/static/js/parallax.js"))
            ],
            middleware=middleware
        )
        
        # Setup routes first to ensure they take precedence over static files
        self.setup_routes()
        
        # Mount static files after routes are defined
        self.app.mount("/static", StaticFiles(directory="public"), name="static")
        
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
        def home():
            """Render the home page."""
            return self.create_homepage()
    
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
                
                # About Section
                self._create_about_section(),
                
                # Services Section
                self._create_services_section(),
                
                # Benefits Section
                self._create_benefits_section(),
                
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
        return Header(
            Div(
                Div(
                    A(
                        Img(src=self.versioned_url("/static/assets/Teambee logo donker.png"), alt="Teambee Logo", cls="h-10 w-auto"),
                        href="#",
                        title="Back to top",
                        aria_label="Back to top of page",
                        cls="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                    ),
                    cls="flex items-center gap-2"
                ),
                # A(
                #     "Login",
                #     href="#login",
                #     cls="inline-flex h-9 items-center justify-center rounded-lg bg-[#94C46F] px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-[#94C46F]/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#94C46F] focus-visible:ring-offset-2"
                Div(
                    "Login Coming Soon",
                    cls="inline-flex h-9 items-center justify-center rounded-lg bg-gray-400 px-4 py-2 text-sm font-medium text-white shadow transition-colors cursor-not-allowed"
                ),
                cls="container flex h-16 items-center justify-between"
            ),
            cls="sticky top-0 z-50 w-full bg-white/85 backdrop-blur-md supports-[backdrop-filter]:bg-white/65 border-b shadow-sm",
            role="banner"
        )
    
    def _create_hero_section(self):
        """Create the hero section."""
        return Section(
            Div(
                Div(
                    Div(
                        H1(
                            "We beat the short with the long term",
                            cls="text-4xl md:text-5xl font-bold italic text-[#3D2E7C] leading-tight"
                        ),
                        P(
                            "Teambee helpt premium health- en wellnesscentra leden te transformeren tot loyale ambassadeurs via MyWellness CRM, met gepersonaliseerde aandacht en op maat gemaakte customer journeys voor duurzame groei.",
                            cls="text-lg text-gray-600 max-w-md"
                        ),
                        Div(
                            A(
                                "Our services",
                                Span("→", cls="ml-2"),
                                href="#services",
                                cls="inline-flex h-10 items-center justify-center rounded-lg bg-[#3D2E7C] px-8 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-[#3D2E7C]/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                            ),
                            # A(
                            #     "Login",
                            #     href="#login",
                            #     cls="inline-flex h-10 items-center justify-center rounded-lg border border-[#3D2E7C] px-8 py-2 text-sm font-medium text-[#3D2E7C] shadow-sm transition-colors hover:bg-[#3D2E7C]/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                            # ),
                            # cls="flex flex-col sm:flex-row gap-4"
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
                        "Let's win together!",
                        cls="text-3xl md:text-4xl font-bold italic text-[#3D2E7C] mb-4"
                    ),
                    P(
                        "Teamwork is onze kracht. Met data en gepersonaliseerde aandacht creëren we synergie tussen health- en wellnesscentra en hun leden voor duurzame groei.",
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
                            "Teamwork makes the dream work",
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            "Bij Teambee draait alles om samenwerking. We verbinden clubs en leden met op maat gemaakte oplossingen, wat leidt tot wederzijds succes en langdurige relaties.",
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
                            "Resultaten die er toe doen",
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            "Onze focus ligt op meetbare resultaten: hogere ledenretentie, tevreden leden en een stijgende omzet voor clubs.",
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
                            "Duurzame groei, langdurig succes",
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            "We bouwen duurzame relaties die zorgen voor stabiele groei en langdurig succes voor clubs.",
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
                        "Happy, healthy members mean sustainable growth",
                        cls="text-3xl md:text-4xl font-bold italic mb-4"
                    ),
                    P(
                        "Onze bewezen 5-stappen aanpak zorgt voor strategische, datagedreven groei voor jouw fitnessclub:",
                        cls="text-lg text-white/80 max-w-2xl mx-auto"
                    ),
                    cls="text-center mb-12"
                ),
                
                Div(
                    Div(
                        H3(
                            "CRM-implementatie (3 maanden)",
                            cls="text-xl font-semibold text-[#ffffff] mb-2"
                        ),
                        Ul(
                            self._create_check_list_item("Strategie – Samen ontwikkelen we een gepersonaliseerde aanpak die perfect past bij jouw club en leden."),
                            self._create_check_list_item("Design – We ontwerpen Customer Journeys die leden écht raken en langdurig betrokken houden."),
                            self._create_check_list_item("Implementatie – Naadloze integratie met MyWellness CRM en geautomatiseerde workflows voor maximale efficiëntie."),
                            self._create_check_list_item("Educatie – Training en begeleiding van jouw team op locatie voor een succesvolle uitvoering van de strategie."),
                            self._create_check_list_item("Data support – Doorlopende monitoring en optimalisatie van de resultaten voor constante groei."),
                            cls="space-y-3"
                        ),
                        cls="bg-[#1B1947] p-6 rounded-lg"
                    ),
                    
                    cls="grid md:grid-cols-1 gap-8"
                ),
                
                cls="container"
            ),
            id="services",
            cls="py-16 md:py-24 bg-[#3D2E7C] text-white"
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
        return Section(
            Div(
                Div(
                    H2(
                        "The best-scored goal is the goal we achieve",
                        cls="text-3xl md:text-4xl font-bold italic text-[#3D2E7C] mb-4"
                    ),
                    P(
                        "Ontdek hoe Teambee de ledenervaring transformeert en duurzame groei stimuleert.",
                        cls="text-lg text-gray-600 max-w-2xl mx-auto"
                    ),
                    cls="text-center mb-12"
                ),
                
                Div(
                    # Member Retention
                    Div(
                        Div(
                            "73%",
                            cls="text-4xl font-bold text-[#E8973A] mb-2"
                        ),
                        H3(
                            "Gemiddelde retentie",
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            "Gemiddeld zien onze klanten een ledenretentie van 73%, ver boven de industrienormen.",
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100"
                    ),
                    
                    # Member Referrals
                    Div(
                        Div(
                            "3.8x",
                            cls="text-4xl font-bold text-[#E8973A] mb-2"
                        ),
                        H3(
                            "Meer member referrals",
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            "Leden worden ambassadeurs, die 3.8x meer aanbevelingen genereren dan traditionele marketing.",
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100"
                    ),
                    
                    # Engagement Increase
                    Div(
                        Div(
                            "68%",
                            cls="text-4xl font-bold text-[#E8973A] mb-2"
                        ),
                        H3(
                            "Hogere engagement",
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            "Leden tonen 68% meer betrokkenheid met gepersonaliseerde journeys en aandacht.",
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100"
                    ),
                    
                    cls="grid md:grid-cols-3 gap-8"
                ),
                
                cls="container"
            ),
            id="benefits",
            cls="py-16 md:py-24 bg-white/80 backdrop-blur-sm"
        )
    
    def _create_login_section(self):
        """Create the login section."""
        login_form = LoginForm()
        
        return Section(
            Div(
                Div(
                    Div(
                        H2(
                            "Login to your dashboard",
                            id="login-heading",
                            cls="text-3xl font-bold italic text-[#3D2E7C] mb-2"
                        ),
                        P(
                            "Krijg toegang tot je persoonlijke Teambee dashboard om inzicht te krijgen in jouw clubprestaties",
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
                                    "Coming Soon!",
                                    cls="text-2xl font-bold text-white mb-2"
                                ),
                                P(
                                    "We zijn momenteel bezig aan deze functie. Coming soon!",
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
            cls="pt-16 md:pt-24 pb-16 bg-white/90 backdrop-blur-sm relative"
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
                            "Teambee helpt fitnessclubs wereldwijd leden te binden en duurzame groei te realiseren met slimme technologie en persoonlijke aanpak.",
                            cls="text-white/70 text-sm"
                        ),
                        cls=""
                    ),
                    
                    Div(
                        H3(
                            "Contact",
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
                                    "+31 (0)20 123 4567", 
                                    href="tel:+31201234567",
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
                        cls="md:text-right"
                    ),
                    
                    cls="grid gap-8 md:grid-cols-2"
                ),
                
                Div(
                    Div(
                        P(
                            f"© {datetime.now().year} Teambee. All rights reserved.",
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
            cls="bg-[#1B1947] text-white py-12 relative z-10",
            role="contentinfo"
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