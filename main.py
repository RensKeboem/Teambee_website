from fasthtml.common import *
from login_form import LoginForm
from datetime import datetime
import os

class TeambeeApp:
    """Main application class for the Teambee website."""
    
    def __init__(self):
        """Initialize the Teambee application with TailwindCSS."""
        self.app = FastHTML(
            title="Teambee | Transform Members into Loyal Ambassadors",
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
                Link(rel="stylesheet", href="app.css", type="text/css"),
                Link(rel="icon", href="/assets/Teambee icon.png", type="image/png"),
                Script(src="js/parallax.js")
            ]
        )
        self.setup_routes()
        
    def setup_routes(self):
        """Set up the application routes."""
        rt = self.app.route
        
        @rt("/{fname:path}.{ext:static}")
        def static_files(fname: str, ext: str):
            """Serve static files from the public directory."""
            return FileResponse(f'public/{fname}.{ext}')
        
        @rt('/assets/{fname:path}.{ext:static}')
        def asset_files(fname: str, ext: str):
            """Serve asset files from the public/assets directory."""
            return FileResponse(f'public/assets/{fname}.{ext}')
        
        @rt('/')
        def home():
            """Render the home page."""
            return self.create_homepage()
    
    def create_homepage(self):
        """Create the Teambee homepage."""
        return Div(
            # Honeycomb pattern background
            Div(
                Img(
                    src="/assets/honeycomb-cropped.svg",
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
                        Img(src="/assets/Teambee logo donker.svg", alt="Teambee Logo", cls="h-10 w-auto"),
                        href="#",
                        title="Back to top",
                        aria_label="Back to top of page",
                        cls="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                    ),
                    cls="flex items-center gap-2"
                ),
                A(
                    "Login",
                    href="#login",
                    cls="inline-flex h-9 items-center justify-center rounded-lg bg-[#94C46F] px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-[#94C46F]/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#94C46F] focus-visible:ring-offset-2"
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
                            "Teambee helps premium high-end fitness clubs transform members into loyal ambassadors through personalized attention at scale.",
                            cls="text-lg text-gray-600 max-w-md"
                        ),
                        Div(
                            A(
                                "Our Services",
                                Span("→", cls="ml-2"),
                                href="#services",
                                cls="inline-flex h-10 items-center justify-center rounded-lg bg-[#3D2E7C] px-8 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-[#3D2E7C]/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                            ),
                            A(
                                "Login",
                                href="#login",
                                cls="inline-flex h-10 items-center justify-center rounded-lg border border-[#3D2E7C] px-8 py-2 text-sm font-medium text-[#3D2E7C] shadow-sm transition-colors hover:bg-[#3D2E7C]/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                            ),
                            cls="flex flex-col sm:flex-row gap-4"
                        ),
                        cls="space-y-6"
                    ),
                    Div(
                        Img(
                            src="/assets/Teambee icon.png",
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
                        "We create synergy between fitness clubs and their members through data-driven, personalized attention at scale.",
                        cls="text-lg text-gray-600 max-w-2xl mx-auto"
                    ),
                    cls="text-center mb-12"
                ),
                
                Div(
                    # Synergie card
                    Div(
                        Div(
                            Img(
                                src="/assets/users.svg",
                                alt="Synergie Icon",
                                cls="w-6 h-6"
                            ),
                            cls="w-12 h-12 bg-[#E8973A]/20 rounded-full flex items-center justify-center mb-4"
                        ),
                        H3(
                            "Synergie",
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            "We believe in the power of teamwork. Creating synergy between fitness clubs and their members.",
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm transform transition-all duration-300 hover:-translate-y-2 hover:shadow-md"
                    ),
                    
                    # Resultaatgericht card
                    Div(
                        Div(
                            Img(
                                src="/assets/target.svg",
                                alt="Resultaatgericht Icon",
                                cls="w-6 h-6"
                            ),
                            cls="w-12 h-12 bg-[#3D2E7C]/20 rounded-full flex items-center justify-center mb-4"
                        ),
                        H3(
                            "Resultaatgericht",
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            "We focus on measurable results: higher retention, satisfied members, and increased sales.",
                            cls="text-gray-600"
                        ),
                        cls="bg-white p-6 rounded-lg shadow-sm transform transition-all duration-300 hover:-translate-y-2 hover:shadow-md"
                    ),
                    
                    # Duurzaam card
                    Div(
                        Div(
                            Img(
                                src="/assets/sprout.svg",
                                alt="Duurzaam Icon",
                                cls="w-6 h-6"
                            ),
                            cls="w-12 h-12 bg-[#94C46F]/20 rounded-full flex items-center justify-center mb-4"
                        ),
                        H3(
                            "Duurzaam",
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            "We always focus on long-term relationships and sustainable growth for fitness clubs and their members.",
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
                        "Our services help premium fitness clubs create exceptional member experiences.",
                        cls="text-lg text-white/80 max-w-2xl mx-auto"
                    ),
                    cls="text-center mb-12"
                ),
                
                Div(
                    # Personalized Member Journeys
                    Div(
                        H3(
                            "Personalized Member Journeys",
                            cls="text-xl font-semibold mb-4"
                        ),
                        Ul(
                            self._create_check_list_item("Custom onboarding experiences for new members"),
                            self._create_check_list_item("Automated check-ins and progress tracking"),
                            self._create_check_list_item("Personalized workout recommendations"),
                            self._create_check_list_item("Milestone celebrations and rewards"),
                            cls="space-y-3"
                        ),
                        cls="bg-[#1B1947] p-6 rounded-lg"
                    ),
                    
                    # Data-Driven Retention Strategies
                    Div(
                        H3(
                            "Data-Driven Retention Strategies",
                            cls="text-xl font-semibold mb-4"
                        ),
                        Ul(
                            self._create_check_list_item("Member engagement analytics"),
                            self._create_check_list_item("Predictive churn modeling"),
                            self._create_check_list_item("Targeted re-engagement campaigns"),
                            self._create_check_list_item("Performance benchmarking"),
                            cls="space-y-3"
                        ),
                        cls="bg-[#1B1947] p-6 rounded-lg"
                    ),
                    
                    cls="grid md:grid-cols-2 gap-8"
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
                src="/assets/check.svg",
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
                        "See how Teambee transforms member experiences and drives sustainable growth.",
                        cls="text-lg text-gray-600 max-w-2xl mx-auto"
                    ),
                    cls="text-center mb-12"
                ),
                
                Div(
                    # Member Retention
                    Div(
                        Div(
                            "92%",
                            cls="text-4xl font-bold text-[#E8973A] mb-2"
                        ),
                        H3(
                            "Member Retention",
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            "Our clients see an average 92% annual member retention rate, well above industry standards.",
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
                            "Member Referrals",
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            "Members become ambassadors, generating 3.8x more referrals than traditional marketing.",
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
                            "Engagement Increase",
                            cls="text-xl font-semibold text-[#1B1947] mb-2"
                        ),
                        P(
                            "Members show 68% higher engagement with personalized journeys and attention.",
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
                            "Access your personalized Teambee dashboard to manage your club's member journeys.",
                            cls="text-gray-600"
                        ),
                        cls="text-center mb-8"
                    ),
                    
                    login_form.render(),
                    
                    cls="max-w-md mx-auto"
                ),
                cls="container relative z-10"
            ),
            
            # Bottom honeycomb pattern
            Div(
                Img(
                    src="/assets/honeycomb-cropped.svg",
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
                                src="/assets/Teambee logo wit.svg",
                                alt="Teambee Logo",
                                cls="h-8 w-auto"
                            ),
                            cls="mb-4"
                        ),
                        P(
                            "Teambee helps premium high-end clubs transform members into loyal ambassadors.",
                            cls="text-white/70 text-sm"
                        ),
                        Div(
                            Div(
                                A(
                                    Img(
                                        src="/assets/instagram-167-svgrepo-com.svg",
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
                                        src="/assets/linkedin-svgrepo-com.svg",
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
                                        src="/assets/facebook-svgrepo-com.svg",
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
                            cls="mt-8 flex items-center"
                        ),
                        cls=""
                    ),
                    
                    Div(
                        H3(
                            "Contact",
                            cls="font-semibold text-lg mb-4"
                        ),
                        Ul(
                            Li("info@teambee.com", cls="text-white/70"),
                            Li("+31 (0)20 123 4567", cls="text-white/70"),
                            Li("Amsterdam, The Netherlands", cls="text-white/70"),
                            cls="space-y-2"
                        ),
                        cls="md:text-right"
                    ),
                    
                    cls="grid gap-8 md:grid-cols-2"
                ),
                
                Div(
                    P(
                        f"© {datetime.now().year} Teambee. All rights reserved.",
                        cls=""
                    ),
                    cls="border-t border-white/10 mt-8 pt-8 text-center text-white/50 text-sm"
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