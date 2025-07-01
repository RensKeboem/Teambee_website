from fasthtml.common import *

class RegistrationForm:
    """Registration form component for new users."""
    
    def __init__(self):
        """Initialize the registration form component."""
        pass
    
    def render(self, club_name: str = "", pre_filled_email: str = ""):
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
                            value=pre_filled_email,
                            required=True,
                            pattern="^[A-Za-z0-9._%+\\-]+@[A-Za-z0-9.\\-]+\\.[A-Za-z]{2,}$",
                            autocomplete="email",
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
                            autocomplete="new-password",
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
                            autocomplete="new-password",
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
    
    def __init__(self, translations=None, language="nl"):
        """Initialize the password reset form component."""
        self.translations = translations or {}
        self.language = language
    
    def get_text(self, key: str, default: str = "") -> str:
        """Get translated text for the given key."""
        return self.translations.get(key, default)
    
    def render_request_form(self):
        """Render the password reset request form."""
        return Form(
            Div(
                H2(
                    self.get_text("request_title", "Reset Password"),
                    cls="text-3xl font-bold italic text-[#3D2E7C] mb-6"
                ),
                
                P(
                    self.get_text("request_subtitle", "Enter your email address and we'll send you a link to reset your password."),
                    cls="text-gray-600 mb-6"
                ),
                
                Div(
                    Label(self.get_text("email_label", "Email"), for_="email", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="email", id="email", name="email", placeholder=self.get_text("email_placeholder", "name@example.com"), 
                          required=True, aria_required="true",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        self.get_text("send_reset_link", "Send Reset Link"),
                        type="submit",
                        data_loading_text=self.get_text("sending", "Sending..."),
                        data_default_text=self.get_text("send_reset_link", "Send Reset Link"),
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                    ),
                    
                    Div(
                        A(self.get_text("back_to_login", "Back to Login"), href="/", 
                          cls="text-[#3D2E7C] hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded"),
                        cls="text-center text-sm text-gray-500 mt-3"
                    ),
                    cls="flex flex-col"
                ),
                
                cls="flex flex-col gap-6"
            ),
            method="post",
            action="/en/forgot-password" if self.language == "en" else "/forgot-password",
            cls="max-w-md mx-auto",
            role="form"
        )
    
    def render_reset_form(self):
        """Render the new password form."""
        return Form(
            Div(
                H2(
                    self.get_text("set_new_password_title", "Set New Password"),
                    cls="text-3xl font-bold italic text-[#3D2E7C] mb-6"
                ),
                
                # Error message container
                Div(
                    id="reset-error",
                    cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm w-full break-words"
                ),
                
                # Success message container
                Div(
                    id="reset-success",
                    cls="hidden mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm w-full break-words"
                ),
                
                # Hidden username field for accessibility
                Input(
                    type="text",
                    name="username",
                    autocomplete="username",
                    style="display: none;",
                    tabindex="-1",
                    aria_hidden="true"
                ),
                
                Div(
                    Label(self.get_text("new_password_label", "New Password"), for_="password", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="password", id="password", name="password", 
                          required=True, aria_required="true", minlength="8",
                          autocomplete="new-password",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    Div(self.get_text("password_min_length", "Password must be at least 8 characters long"), cls="text-xs text-gray-500 mt-1"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Label(self.get_text("confirm_password_label", "Confirm New Password"), for_="confirm_password", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="password", id="confirm_password", name="confirm_password", 
                          required=True, aria_required="true",
                          autocomplete="new-password",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    # Password mismatch error message
                    Div(
                        self.get_text("passwords_mismatch", "Passwords do not match"),
                        id="password-mismatch-error",
                        cls="hidden text-sm text-red-600 mt-1"
                    ),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        self.get_text("reset_password_button", "Reset Password"),
                        type="submit",
                        id="reset-password-submit-btn",
                        data_loading_text=self.get_text("resetting", "Resetting..."),
                        data_default_text=self.get_text("reset_password_button", "Reset Password"),
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed disabled:hover:bg-gray-400"
                    ),
                    cls="flex flex-col"
                ),
                
                cls="flex flex-col gap-6"
            ),
            id="reset-password-form",
            method="post",
            cls="w-full",
            role="form"
        )

class DashboardLayout:
    """Dashboard layout component."""
    
    def __init__(self, translations=None):
        """Initialize the dashboard layout."""
        self.translations = translations or {}
    
    def get_text(self, key: str, default: str = "") -> str:
        """Get translated text for the given key."""
        return self.translations.get(key, default)
    
    def render(self, user_info: dict, content: str = ""):
        """Render the dashboard layout."""
        return Html(
            Head(
                Title(self.get_text("title", "Teambee Dashboard")),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Link(rel="stylesheet", href="/static/app.css", type="text/css"),
                Link(rel="icon", href="/static/assets/Teambee icon.png", type="image/png"),
                Script(src="/static/js/user-dropdown.js"),
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
                            Span(f"{self.get_text('welcome', 'Welcome,')} {user_info.get('email', '')}", cls="text-gray-700 mr-4"),
                            
                            # User dropdown
                            Div(
                                Button(
                                    Img(src="/static/assets/user.svg", alt="User Menu", cls="w-5 h-5"),
                                    id="user-dropdown-button",
                                    aria_expanded="false",
                                    aria_haspopup="true",
                                    cls="inline-flex items-center justify-center w-8 h-8 rounded-lg text-gray-700 border border-gray-300 hover:bg-gray-100 hover:border-gray-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                                ),
                                
                                # Dropdown menu
                                Div(
                                    Button(
                                        self.get_text("update_password", "Update Password"),
                                        type="button",
                                        id="update-password-option",
                                        cls="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[#3D2E7C]"
                                    ),
                                    Button(
                                        self.get_text("invite_new_user", "Invite New User"),
                                        type="button",
                                        id="invite-user-option",
                                        cls="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[#3D2E7C]"
                                    ),
                                    Div(cls="border-t border-gray-100 my-1"),
                                    A(
                                        self.get_text("logout", "Logout"),
                                        href="/logout",
                                        cls="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-red-500"
                                    ),
                                    id="user-dropdown-menu",
                                    cls="hidden absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50",
                                    role="menu",
                                    aria_orientation="vertical"
                                ),
                                
                                cls="relative"
                            ),
                            
                            cls="flex items-center"
                        ),
                        cls="container flex h-16 items-center justify-between px-4"
                    ),
                    cls="bg-white border-b shadow-sm"
                ),
                
                # Main content
                Main(
                    Div(
                        H1(self.get_text("page_title", "Dashboard"), cls="text-3xl font-bold text-[#3D2E7C] mb-8"),
                        
                        # Dashboard content
                        Div(
                            Div(
                                H2(self.get_text("welcome_message", "Welcome to your Teambee Dashboard"), cls="text-xl font-semibold mb-4"),
                                P(self.get_text("welcome_subtitle", "Use the user menu in the top right to update your password or invite new users to your club."), 
                                  cls="text-gray-500"),
                                cls="bg-white p-6 rounded-lg shadow-sm border max-w-2xl mx-auto text-center"
                            ),
                            cls="grid gap-6"
                        ),
                        
                        cls="container mx-auto px-4 py-8"
                    ),
                    cls="flex-1 bg-gray-50"
                ),
                
                # Password Update Popup
                Div(
                    Div(
                        Div(
                            # Modal header
                            Div(
                                H2(self.get_text("update_password", "Update Password"), cls="text-2xl font-bold text-[#3D2E7C] mb-2"),
                                Button(
                                    Img(src="/static/assets/close.svg", alt="Close", cls="w-6 h-6 filter brightness-0"),
                                    id="close-password-popup",
                                    cls="text-gray-700 hover:text-gray-900 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                                ),
                                cls="flex justify-between items-center mb-6"
                            ),
                            
                            # Modal body
                            Div(
                                PasswordUpdateForm(self.translations).render(),
                                cls=""
                            ),
                            
                            cls="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-auto transform transition-all duration-300 ease-out scale-95 opacity-0"
                        ),
                        cls="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
                    ),
                    id="password-update-popup",
                    cls="hidden"
                ),
                
                # User Invite Popup
                Div(
                    Div(
                        Div(
                            # Modal header
                            Div(
                                H2(self.get_text("invite_new_user", "Invite New User"), cls="text-2xl font-bold text-[#3D2E7C] mb-2"),
                                Button(
                                    Img(src="/static/assets/close.svg", alt="Close", cls="w-6 h-6 filter brightness-0"),
                                    id="close-invite-popup",
                                    cls="text-gray-700 hover:text-gray-900 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                                ),
                                cls="flex justify-between items-center mb-6"
                            ),
                            
                            # Modal body
                            Div(
                                UserInviteForm(self.translations).render(),
                                cls=""
                            ),
                            
                            cls="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-auto transform transition-all duration-300 ease-out scale-95 opacity-0"
                        ),
                        cls="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
                    ),
                    id="user-invite-popup",
                    cls="hidden"
                ),
                
                                 cls="min-h-screen flex flex-col"
             )
         )

class AdminPanelLayout:
    """Admin panel layout component."""
    
    def __init__(self, versioned_url=None):
        """Initialize the admin panel layout."""
        self.versioned_url = versioned_url or (lambda x: x)
    
    def render(self, user_info: dict, content):
        """Render the admin panel layout."""
        return Html(
            Head(
                Title("Teambee Admin Panel"),
                Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                Link(rel="stylesheet", href=self.versioned_url("/static/app.css"), type="text/css"),
                Link(rel="icon", href=self.versioned_url("/static/assets/Teambee icon.png"), type="image/png"),
                Script(src=self.versioned_url("/static/js/shared-utils.js")),
                Script(src=self.versioned_url("/static/js/popup-dropdown.js")),
                Script(src=self.versioned_url("/static/js/admin-search.js")),
            ),
            Body(
                # Header
                Header(
                    Div(
                        Div(
                            Img(src=self.versioned_url("/static/assets/Teambee logo donker.png"), alt="Teambee Logo", cls="h-8 w-auto"),
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

class PasswordUpdateForm:
    """Password update form component."""
    
    def __init__(self, translations=None):
        """Initialize the password update form component."""
        self.translations = translations or {}
    
    def get_text(self, key: str, default: str = "") -> str:
        """Get translated text for the given key."""
        return self.translations.get(key, default)
    
    def render(self):
        """Render the password update form."""
        return Form(
            # Hidden username field for accessibility (password managers need this)
            Input(
                type="text",
                name="username",
                autocomplete="username",
                style="display: none;",
                tabindex="-1",
                aria_hidden="true"
            ),
            
            Div(
                # Error message container
                Div(
                    id="password-update-error",
                    cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
                ),
                
                # Success message container
                Div(
                    id="password-update-success",
                    cls="hidden mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm"
                ),
                
                Div(
                    Label(self.get_text("current_password", "Current Password"), for_="current_password", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="password", id="current_password", name="current_password", 
                          required=True, aria_required="true", autocomplete="current-password",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Label(self.get_text("new_password", "New Password"), for_="new_password", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="password", id="new_password", name="new_password", 
                          required=True, aria_required="true", minlength="8", autocomplete="new-password",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    Div(self.get_text("password_min_length", "Password must be at least 8 characters long"), cls="text-xs text-gray-500 mt-1"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Label(self.get_text("confirm_new_password", "Confirm New Password"), for_="confirm_new_password", cls="block text-sm font-medium text-gray-700 mb-1"),
                    Input(type="password", id="confirm_new_password", name="confirm_new_password", 
                          required=True, aria_required="true", autocomplete="new-password",
                          cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"),
                    cls="flex flex-col gap-2"
                ),
                
                Div(
                    Button(
                        self.get_text("update_password_button", "Update Password"),
                        type="submit",
                        id="password-update-btn",
                        data_updating_text=self.get_text("updating", "Updating..."),
                        data_default_text=self.get_text("update_password_button", "Update Password"),
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                    ),
                    cls="flex flex-col"
                ),
                
                cls="flex flex-col gap-4"
            ),
            id="password-update-form",
            method="post",
            action="/dashboard/update-password",
            cls="",
            role="form"
        )

class UserInviteForm:
    """User invite form component."""
    
    def __init__(self, translations=None):
        """Initialize the user invite form component."""
        self.translations = translations or {}
    
    def get_text(self, key: str, default: str = "") -> str:
        """Get translated text for the given key."""
        return self.translations.get(key, default)
    
    def render(self):
        """Render the user invite form."""
        return Div(
            Div(
                H3(
                    self.get_text("invite_subtitle", "Invite New User"),
                    cls="text-lg font-semibold text-[#3D2E7C] mb-4"
                ),
                
                # Error message container
                Div(
                    id="invite-error",
                    cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
                ),
                
                # Success message container
                Div(
                    id="invite-success",
                    cls="hidden mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm"
                ),
                
                Form(
                    P(
                        self.get_text("invite_subtitle", "Invite a new user to join your club by sending them a registration link."),
                        cls="text-gray-600 mb-4"
                ),
                
                Div(
                        Label(
                            self.get_text("email_address", "Email Address"),
                            for_="invite_email",
                            cls="block text-sm font-medium text-gray-700 mb-1"
                        ),
                        Input(
                            type="email",
                            id="invite_email",
                            name="invite_email",
                            placeholder=self.get_text("email_placeholder", "user@example.com"),
                            required=True,
                            cls="w-full px-3 py-2 border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                        ),
                        Div(
                            self.get_text("email_help", "Enter the email address of the person you want to invite"),
                            cls="text-xs text-gray-500 mt-1"
                        ),
                        cls="mb-4"
                    ),
                    
                    Button(
                        Span(self.get_text("send_invitation", "Send Invitation"), id="invite-button-text"),
                        Span(self.get_text("sending", "Sending..."), id="invite-button-loading", cls="hidden"),
                        type="submit",
                        id="invite-submit-btn",
                        cls="w-full bg-[#3D2E7C] hover:bg-[#3D2E7C]/90 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                    ),
                    
                    method="post",
                    action="/dashboard/invite-user",
                    id="invite-form"
                ),
                cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100"
            ),
            cls="max-w-md mx-auto"
        )

class AdminInviteForm:
    """Admin invite form component for sending registration links via email."""
    
    def __init__(self, versioned_url=None):
        """Initialize the admin invite form component."""
        self.versioned_url = versioned_url or (lambda x: x)
    
    def render(self):
        """Render the admin invite form popup."""
        return Div(
            # Modal backdrop
            Div(
                # Modal content
                Div(
                    # Modal header
                    Div(
                        H2(
                            "Send Registration Link",
                            cls="text-2xl font-bold text-[#3D2E7C] mb-2",
                            id="admin-invite-form-title"
                        ),
                        Button(
                            Img(
                                src=self.versioned_url("/static/assets/close.svg"),
                                alt="Close",
                                cls="w-6 h-6 filter brightness-0"
                            ),
                            id="close-admin-invite-popup",
                            cls="text-gray-700 hover:text-gray-900 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                        ),
                        cls="flex justify-between items-center mb-6"
                    ),
                    
                    # Modal body
                    Div(
                        P(
                            "Enter the email address where the registration link should be sent.",
                            cls="text-gray-600 mb-6",
                            id="admin-invite-form-subtitle"
                        ),
                        
                        # Error message container
                        Div(
                            id="admin-invite-error",
                            cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
                        ),
                        
                        # Success message container
                        Div(
                            id="admin-invite-success",
                            cls="hidden mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm"
                        ),
                        
                        # Form
                        Form(
                            # Hidden field for club_id
                            Input(type="hidden", id="admin_invite_club_id", name="club_id"),
                            
                            # Email field
                            Div(
                                Label(
                                    "Email Address",
                                    for_="admin_invite_email",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="email",
                                    id="admin_invite_email",
                                    name="email",
                                    placeholder="user@example.com",
                                    required=True,
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="mb-6"
                            ),
                            
                            # Submit button
                            Button(
                                Span("Send Registration Link", id="admin-invite-button-text"),
                                Span("Sending...", id="admin-invite-button-loading", cls="hidden"),
                                type="submit",
                                id="admin-invite-submit-btn",
                                disabled=True,
                                cls="w-full bg-gray-400 cursor-not-allowed disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                            ),
                            
                            method="post",
                            action="/admin/send-registration-link",
                            id="admin-invite-form"
                        ),
                        cls=""
                    ),
                    
                    cls="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-auto transform transition-all duration-300 ease-out scale-95 opacity-0"
                ),
                cls="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
            ),
            id="admin-invite-popup",
            cls="hidden"
        )


class ContactForm:
    """Contact form component for contact us and services inquiries."""
    
    def __init__(self, translations=None, versioned_url=None):
        """Initialize the contact form component."""
        self.translations = translations or {}
        self.versioned_url = versioned_url or (lambda x: x)
    
    def get_text(self, key: str, default: str = "") -> str:
        """Get translated text for the given key."""
        return self.translations.get(key, default)
    
    def render(self):
        """Render the contact form popup."""
        return Div(
            # Modal backdrop
            Div(
                # Modal content
                Div(
                    # Modal header
                    Div(
                        H2(
                            self.get_text("title", "Contact Us"),
                            cls="text-2xl font-bold text-[#3D2E7C] mb-2",
                            id="contact-form-title"
                        ),
                        Button(
                            Img(
                                src=self.versioned_url("/static/assets/close.svg"),
                                alt="Close",
                                cls="w-6 h-6 filter brightness-0"
                            ),
                            id="close-contact-popup",
                            cls="text-gray-700 hover:text-gray-900 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 rounded-lg"
                        ),
                        cls="flex justify-between items-center mb-6"
                    ),
                    
                    # Modal body
                    Div(
                        P(
                            self.get_text("subtitle", "Fill out the form below and we'll get back to you as soon as possible."),
                            cls="text-gray-600 mb-6",
                            id="contact-form-subtitle"
                        ),
                        
                        # Error message container
                        Div(
                            id="contact-error",
                            cls="hidden mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
                        ),
                        
                        # Success message container
                        Div(
                            id="contact-success",
                            cls="hidden mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm"
                        ),
                        
                        # Contact form
                        Form(
                            # Hidden field for form type
                            Input(
                                type="hidden",
                                id="form_type",
                                name="form_type",
                                value=""
                            ),
                            
                            # First name field
                            Div(
                                Label(
                                    self.get_text("first_name", "First Name"),
                                    for_="contact_first_name",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="text",
                                    id="contact_first_name",
                                    name="first_name",
                                    required=True,
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="mb-4"
                            ),
                            
                            # Last name field
                            Div(
                                Label(
                                    self.get_text("last_name", "Last Name"),
                                    for_="contact_last_name",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="text",
                                    id="contact_last_name",
                                    name="last_name",
                                    required=True,
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="mb-4"
                            ),
                            
                            # Club name field
                            Div(
                                Label(
                                    self.get_text("club_name", "Club Name"),
                                    for_="contact_club_name",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="text",
                                    id="contact_club_name",
                                    name="club_name",
                                    required=True,
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="mb-4"
                            ),
                            
                            # Email field
                            Div(
                                Label(
                                    self.get_text("email", "Email"),
                                    for_="contact_email",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="email",
                                    id="contact_email",
                                    name="email",
                                    required=True,
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="mb-4"
                            ),
                            
                            # Phone number field
                            Div(
                                Label(
                                    self.get_text("phone", "Phone Number"),
                                    for_="contact_phone",
                                    cls="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                Input(
                                    type="tel",
                                    id="contact_phone",
                                    name="phone",
                                    required=True,
                                    cls="w-full px-3 py-2 bg-[#F8F7FB] border border-gray-300 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:border-[#3D2E7C]"
                                ),
                                cls="mb-6"
                            ),
                            
                            # Submit button
                            Button(
                                Span(self.get_text("submit", "Send Message"), id="contact-button-text"),
                                Span(self.get_text("sending", "Sending..."), id="contact-button-loading", cls="hidden"),
                                type="submit",
                                id="contact-submit-btn",
                                disabled=True,
                                cls="w-full bg-gray-400 cursor-not-allowed disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-medium py-2 px-4 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2"
                            ),
                            
                            method="post",
                            action="/contact",
                            id="contact-form"
                        ),
                        cls=""
                    ),
                    
                    cls="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-auto transform transition-all duration-300 ease-out scale-95 opacity-0"
                ),
                cls="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
            ),
            id="contact-popup",
            cls="hidden"
        )