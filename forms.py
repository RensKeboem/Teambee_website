from fasthtml.common import *

class RegistrationForm:
    """Registration form component for new users."""
    
    def __init__(self):
        """Initialize the registration form component."""
        pass
    
    def render(self, club_name: str = ""):
        """Render the registration form with custom validation."""
        return Div(
            Form(
                Div(
                    H2(
                        f"Create Account for {club_name}" if club_name else "Create Account",
                        cls="text-3xl font-bold italic text-[#3D2E7C] mb-6"
                    ),
                    
                    # Email field with validation
                    Label(
                        Span("Email", cls="block text-sm font-medium text-gray-700 mb-1"),
                        Input(
                            type="email", 
                            id="email", 
                            name="email", 
                            placeholder=" ", 
                            required=True,
                            pattern="^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$",
                            cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C] peer invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500"
                        ),
                        Span(
                            "Please enter a valid email address",
                            cls="mt-1 hidden text-sm text-red-500 peer-[&:not(:placeholder-shown):not(:focus):invalid]:block"
                        ),
                        cls="flex flex-col gap-1 mb-4",
                        for_="email"
                    ),
                    
                    # Password field with validation
                    Label(
                        Span("Password", cls="block text-sm font-medium text-gray-700 mb-1"),
                        Input(
                            type="password", 
                            id="password", 
                            name="password", 
                            placeholder=" ", 
                            required=True,
                            pattern=".{8,}",
                            cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C] peer invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500"
                        ),
                        Span(
                            "Password must be at least 8 characters long",
                            cls="mt-1 hidden text-sm text-red-500 peer-[&:not(:placeholder-shown):not(:focus):invalid]:block"
                        ),
                        cls="flex flex-col gap-1 mb-4",
                        for_="password"
                    ),
                    
                    # Confirm Password field with validation
                    Label(
                        Span("Confirm Password", cls="block text-sm font-medium text-gray-700 mb-1"),
                        Input(
                            type="password", 
                            id="confirm_password", 
                            name="confirm_password", 
                            placeholder=" ", 
                            required=True,
                            cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C] peer"
                        ),
                        Span(
                            "Passwords do not match",
                            cls="mt-1 hidden text-sm text-red-500",
                            id="password-mismatch-error"
                        ),
                        cls="flex flex-col gap-1 mb-6",
                        for_="confirm_password"
                    ),
                    
                    # Submit button (disabled when form is invalid)
                    Div(
                        Button(
                            "Create Account",
                            type="submit",
                            cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 group-invalid:pointer-events-none group-invalid:opacity-30 transition-opacity"
                        ),
                        cls="flex flex-col"
                    ),
                    
                    cls="flex flex-col"
                ),
                method="post",
                cls="max-w-md mx-auto group",
                role="form",
                novalidate=True
            )
        )

class PasswordResetForm:
    """Password reset form component."""
    
    def __init__(self):
        """Initialize the password reset form component."""
        pass
    
    def render_request_form(self):
        """Render the password reset request form."""
        return Form(
            Div(
                H2(
                    "Reset Password",
                    cls="text-3xl font-bold italic text-[#3D2E7C] mb-6"
                ),
                
                P(
                    "Enter your email address and we'll send you a link to reset your password.",
                    cls="text-gray-600 mb-6"
                ),
                
                Div(
                    Label("Email", for_="email", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="email", id="email", name="email", placeholder="name@example.com", 
                          required=True, aria_required="true",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        "Send Reset Link",
                        type="submit",
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                    ),
                    
                    Div(
                        A("Back to Login", href="/", 
                          cls="text-[#3D2E7C] hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded"),
                        cls="text-center text-sm text-gray-500 mt-3"
                    ),
                    cls="flex flex-col"
                ),
                
                cls="flex flex-col gap-6"
            ),
            method="post",
            cls="max-w-md mx-auto",
            role="form"
        )
    
    def render_reset_form(self):
        """Render the new password form."""
        return Form(
            Div(
                H2(
                    "Set New Password",
                    cls="text-3xl font-bold italic text-[#3D2E7C] mb-6"
                ),
                
                Div(
                    Label("New Password", for_="password", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="password", id="password", name="password", 
                          required=True, aria_required="true", minlength="8",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    Div("Password must be at least 8 characters long", cls="text-xs text-gray-500 mt-1"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Label("Confirm New Password", for_="confirm_password", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="password", id="confirm_password", name="confirm_password", 
                          required=True, aria_required="true",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        "Reset Password",
                        type="submit",
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                    ),
                    cls="flex flex-col"
                ),
                
                cls="flex flex-col gap-6"
            ),
            method="post",
            cls="max-w-md mx-auto",
            role="form"
        )

class DashboardLayout:
    """Dashboard layout component."""
    
    def __init__(self):
        """Initialize the dashboard layout."""
        pass
    
    def render(self, user_info: dict, content: str = ""):
        """Render the dashboard layout."""
        return Html(
            Head(
                Title("Teambee Dashboard"),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Link(rel="stylesheet", href="/static/app.css", type="text/css"),
                Link(rel="icon", href="/static/assets/Teambee icon.png", type="image/png"),
            ),
            Body(
                # Header
                Header(
                    Div(
                        Div(
                            Img(src="/static/assets/Teambee logo donker.png", alt="Teambee Logo", cls="h-8 w-auto"),
                            cls="flex items-center"
                        ),
                        Div(
                            Span(f"Welcome, {user_info.get('email', '')}", cls="text-gray-700 mr-4"),
                            Span(f"Club: {user_info.get('club_name', '')}", cls="text-gray-500 mr-4"),
                            A("Logout", href="/logout", 
                              cls="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium"),
                            cls="flex items-center"
                        ),
                        cls="container flex h-16 items-center justify-between px-4"
                    ),
                    cls="bg-white border-b shadow-sm"
                ),
                
                # Main content
                Main(
                    Div(
                        H1("Dashboard", cls="text-3xl font-bold text-[#3D2E7C] mb-8"),
                        
                        # Dashboard content placeholder
                        Div(
                            Div(
                                H2("Welcome to your Teambee Dashboard", cls="text-xl font-semibold mb-4"),
                                P("This is where you'll be able to access your club's analytics and reports.", 
                                  cls="text-gray-600 mb-4"),
                                P("Dashboard functionality will be implemented here.", 
                                  cls="text-gray-500"),
                                cls="bg-white p-6 rounded-lg shadow-sm border"
                            ),
                            cls="grid gap-6"
                        ),
                        
                        cls="container mx-auto px-4 py-8"
                    ),
                    cls="flex-1 bg-gray-50"
                ),
                                 cls="min-h-screen flex flex-col"
             )
         )

class AdminPanelLayout:
    """Admin panel layout component."""
    
    def __init__(self):
        """Initialize the admin panel layout."""
        pass
    
    def render(self, user_info: dict, content):
        """Render the admin panel layout."""
        return Html(
            Head(
                Title("Teambee Admin Panel"),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Link(rel="stylesheet", href="/static/app.css", type="text/css"),
                Link(rel="icon", href="/static/assets/Teambee icon.png", type="image/png"),
            ),
            Body(
                # Header
                Header(
                    Div(
                        Div(
                            Img(src="/static/assets/Teambee logo donker.png", alt="Teambee Logo", cls="h-8 w-auto"),
                            Span("Admin Panel", cls="ml-4 text-lg font-semibold text-[#3D2E7C]"),
                            cls="flex items-center"
                        ),
                        Div(
                            Span(f"Welcome, {user_info.get('email', '')}", cls="text-gray-700 mr-4"),
                            A("Logout", href="/logout", 
                              cls="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium"),
                            cls="flex items-center"
                        ),
                        cls="container flex h-16 items-center justify-between px-4"
                    ),
                    cls="bg-white border-b shadow-sm"
                ),
                
                # Navigation
                Nav(
                    Div(
                        A("Dashboard", href="/admin", 
                          cls="px-4 py-2 text-sm font-medium text-[#3D2E7C] hover:bg-gray-100 rounded-lg"),
                        A("Users", href="/admin/users", 
                          cls="px-4 py-2 text-sm font-medium text-[#3D2E7C] hover:bg-gray-100 rounded-lg"),
                        A("Clubs", href="/admin/clubs", 
                          cls="px-4 py-2 text-sm font-medium text-[#3D2E7C] hover:bg-gray-100 rounded-lg"),
                        A("Create Club", href="/admin/create-club", 
                          cls="px-4 py-2 text-sm font-medium bg-[#3D2E7C] text-white hover:bg-[#3D2E7C]/90 rounded-lg"),
                        cls="container flex gap-2 px-4 py-3"
                    ),
                    cls="bg-gray-50 border-b"
                ),
                
                # Main content
                Main(
                    content,
                    cls="flex-1 bg-gray-50 py-8"
                ),
                cls="min-h-screen flex flex-col"
            )
        )

class ClubForm:
    """Club creation form component."""
    
    def __init__(self):
        """Initialize the club form component."""
        pass
    
    def render(self):
        """Render the club creation form."""
        return Form(
            Div(
                H2(
                    "Create New Club",
                    cls="text-3xl font-bold italic text-[#3D2E7C] mb-6"
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
                    Select(
                        Option("Dutch", value="nl"),
                        Option("English", value="en"),
                        name="language", required=True,
                        cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                    ),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        "Create Club & Generate Registration Link",
                        type="submit",
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-3 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                    ),
                    cls="flex flex-col"
                ),
                
                cls="flex flex-col gap-6"
            ),
            method="post",
            cls="max-w-md mx-auto",
            role="form"
        ) 