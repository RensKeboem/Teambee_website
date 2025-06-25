from fasthtml.common import *
from login_form import LoginForm
from auth import AuthManager
from forms import RegistrationForm, PasswordResetForm, DashboardLayout, AdminPanelLayout, ClubForm, ContactForm
from database_manager import DatabaseManager
from datetime import datetime
import os
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from starlette.staticfiles import StaticFiles
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

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
        
        # Initialize authentication manager
        try:
            self.auth = AuthManager(DatabaseManager())
        except Exception as e:
            print(f"Warning: Could not initialize authentication: {e}")
            self.auth = None
        
        # Define middleware
        middleware = [
            Middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "teambee-secret-key-change-in-production")),
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
                # Stylesheets
                Link(rel="stylesheet", href=self.versioned_url("/static/app.css"), type="text/css"),
                Link(rel="icon", href=self.versioned_url("/static/assets/Teambee icon.png"), type="image/png"),
                # Scripts
                Script(src=self.versioned_url("/static/js/ui-enhancements.js")),
                Script(src=self.versioned_url("/static/js/popup-dropdown.js")),
                Script(src=self.versioned_url("/static/js/form-handlers.js")),
                Script(src=self.versioned_url("/static/js/carousel.js")),
                Script(src=self.versioned_url("/static/js/success-stories.js")),
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
    
    def is_authenticated(self, request):
        """Check if user is authenticated."""
        return request.session.get("user_id") is not None
    
    def get_current_user(self, request):
        """Get current user from session."""
        user_id = request.session.get("user_id")
        if not user_id:
            return None
        
        return {
            "user_id": user_id,
            "club_id": request.session.get("club_id"),
            "email": request.session.get("email"),
            "club_name": request.session.get("club_name")
        }
    
    def login_user(self, request, user_info):
        """Log in user by storing info in session."""
        request.session["user_id"] = user_info["user_id"]
        request.session["club_id"] = user_info["club_id"]
        request.session["email"] = user_info["email"]
        request.session["club_name"] = user_info["club_name"]
    
    def logout_user(self, request):
        """Log out user by clearing session."""
        request.session.clear()
    
    def require_admin(self, request):
        """Check if user is authenticated and is admin."""
        if not self.is_authenticated(request):
            return False
        user_info = self.get_current_user(request)
        return self.auth and self.auth.is_admin(user_info)
    
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
        
        # Authentication routes
        @rt("/login", methods=["POST"])
        async def login(request):
            """Handle login form submission."""
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            if not self.auth:
                if is_ajax:
                    return {"success": False, "message": "Authentication service is currently unavailable"}
                else:
                    return RedirectResponse(url="/?error=auth_not_available", status_code=302)
            
            form = await request.form()
            email = form.get("email", "").strip()
            password = form.get("password", "")
            
            if not email or not password:
                if is_ajax:
                    return {"success": False, "message": "Please enter both email and password"}
                else:
                    return RedirectResponse(url="/?error=missing_credentials", status_code=302)
            
            success, user_info, message = self.auth.authenticate_user(email, password)
            
            if success:
                self.login_user(request, user_info)
                # Redirect to admin panel if user is admin, otherwise to dashboard
                redirect_url = "/admin" if self.auth.is_admin(user_info) else "/dashboard"
                
                if is_ajax:
                    return {"success": True, "redirect_url": redirect_url}
                else:
                    return RedirectResponse(url=redirect_url, status_code=302)
            else:
                # Convert error codes to user-friendly messages
                error_messages = {
                    "Invalid email or password": "Invalid email or password. Please try again.",
                    "missing_credentials": "Please enter both email and password",
                    "auth_not_available": "Authentication service is currently unavailable"
                }
                
                # Check if message contains account lock information
                if "Account is locked until" in message:
                    user_message = "Your account has been temporarily locked due to multiple failed login attempts. Please try again later."
                else:
                    user_message = error_messages.get(message, "Login failed. Please try again.")
                
                if is_ajax:
                    return {"success": False, "message": user_message}
                else:
                    return RedirectResponse(url=f"/?error={message}", status_code=302)
        
        @rt("/logout")
        async def logout(request):
            """Handle user logout."""
            self.logout_user(request)
            return RedirectResponse(url="/", status_code=302)
        
        @rt("/dashboard")
        async def dashboard(request):
            """Render the dashboard for authenticated users."""
            if not self.is_authenticated(request):
                return RedirectResponse(url="/", status_code=302)
            
            user_info = self.get_current_user(request)
            
            # Get user's language preference from their club or default to Dutch
            user_lang = "nl"  # Default language
            if user_info.get("club_id") and self.auth:
                clubs_df = self.auth.get_clubs()
                if clubs_df is not None and not clubs_df.empty:
                    club_row = clubs_df[clubs_df['club_id'] == user_info["club_id"]]
                    if not club_row.empty:
                        user_lang = club_row.iloc[0]['language']
            
            # Get dashboard translations for the user's language
            dashboard_translations = self.translations.get(user_lang, {}).get("dashboard", {})
            
            dashboard_layout = DashboardLayout(dashboard_translations)
            return dashboard_layout.render(user_info)
        
        @rt("/dashboard/update-password", methods=["POST"])
        async def update_password(request):
            """Handle password update for authenticated users."""
            if not self.is_authenticated(request):
                return {"success": False, "message": "Authentication required"}
            
            user_info = self.get_current_user(request)
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            if not self.auth:
                return {"success": False, "message": "Authentication service unavailable"}
            
            form = await request.form()
            current_password = form.get("current_password", "")
            new_password = form.get("new_password", "")
            confirm_new_password = form.get("confirm_new_password", "")
            
            # Validate input
            if not all([current_password, new_password, confirm_new_password]):
                return {"success": False, "message": "All fields are required"}
            
            if new_password != confirm_new_password:
                return {"success": False, "message": "New passwords do not match"}
            
            if len(new_password) < 8:
                return {"success": False, "message": "New password must be at least 8 characters long"}
            
            # Update password
            success, message = self.auth.update_user_password(
                user_info["user_id"], 
                current_password, 
                new_password
            )
            
            return {"success": success, "message": message}
        
        @rt("/dashboard/invite-user", methods=["POST"])
        async def invite_user(request):
            """Handle user invitation for authenticated users."""
            if not self.is_authenticated(request):
                return {"success": False, "message": "Authentication required"}
            
            user_info = self.get_current_user(request)
            
            # Only club users can invite (not admins)
            if not user_info.get("club_id"):
                return {"success": False, "message": "Only club users can invite new users"}
            
            if not self.auth:
                return {"success": False, "message": "Authentication service unavailable"}
            
            form = await request.form()
            invite_email = form.get("invite_email", "").strip()
            
            # Validate input
            if not invite_email:
                return {"success": False, "message": "Email address is required"}
            
            if "@" not in invite_email:
                return {"success": False, "message": "Please enter a valid email address"}
            
            # Send invitation
            success, message = self.auth.invite_user_to_club(
                user_info["club_id"],
                invite_email,
                user_info["email"]
            )
            
            return {"success": success, "message": message}
        
        @rt("/register/{token}", methods=["GET", "POST"])
        async def registration_handler(request):
            """Handle both GET and POST for user registration."""
            if not self.auth:
                return RedirectResponse(url="/?error=auth_not_available", status_code=302)
            
            token = request.path_params["token"]
            
            if request.method == "GET":
                # Show registration form
                club_id = self.auth.validate_registration_token(token)
                
                if not club_id:
                    return Title("Invalid Registration Link"), Div(
                        Div(
                            H1("Invalid or Expired Registration Link", cls="text-3xl font-bold text-red-600 mb-4"),
                            P("This registration link is invalid or has expired.", cls="text-gray-600 mb-4"),
                            A("Go to Home", href="/", cls="text-[#3D2E7C] hover:underline"),
                            cls="text-center"
                        ),
                        cls="min-h-screen flex items-center justify-center bg-gray-50"
                    )
                
                # Get club name
                clubs_df = self.auth.get_clubs()
                club_name = ""
                if clubs_df is not None and not clubs_df.empty:
                    club_row = clubs_df[clubs_df['club_id'] == club_id]
                    if not club_row.empty:
                        club_name = club_row.iloc[0]['name']
                
                # Check for pre-filled email from invitation
                pre_filled_email = request.query_params.get("email", "")
                
                registration_form = RegistrationForm()
                return Title("Create Account"), Html(
                    Head(
                        Title("Create Account"),
                        Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                        Link(rel="stylesheet", href=self.versioned_url("/static/app.css"), type="text/css"),
                        Link(rel="icon", href=self.versioned_url("/static/assets/Teambee icon.png"), type="image/png"),
                        Script(src=self.versioned_url("/static/js/form-handlers.js"))
                    ),
                    Body(
                        Div(
                            registration_form.render(club_name, pre_filled_email),
                            cls="min-h-screen flex items-center justify-center bg-gray-50 py-12"
                        )
                    )
                )
            
            elif request.method == "POST":
                # Handle user registration
                form = await request.form()
                email = form.get("email", "").strip()
                password = form.get("password", "")
                confirm_password = form.get("confirm_password", "")
                
                # Client-side validation prevents invalid submissions
                
                success, message = self.auth.complete_registration(token, email, password)
                
                if success:
                    return RedirectResponse(url="/?success=registration_complete", status_code=302)
                else:
                    # Show error page for database/server errors
                    return Title("Registration Error"), Div(
                        Div(
                            H1("Registration Error", cls="text-3xl font-bold text-red-600 mb-4"),
                            P(f"Registration failed: {message}", cls="text-gray-600 mb-4"),
                            A("Go Back", href=f"/register/{token}", cls="text-[#3D2E7C] hover:underline"),
                            cls="text-center"
                        ),
                        cls="min-h-screen flex items-center justify-center bg-gray-50"
                    )
        
        @rt("/forgot-password", methods=["GET", "POST"])
        async def forgot_password_handler(request):
            """Handle both GET and POST for forgot password."""
            if request.method == "GET":
                # Show forgot password form
                # Get current language from request state or URL
                current_lang = getattr(request.state, 'language', 'nl')
                password_reset_translations = self.translations.get(current_lang, {}).get("password_reset", {})
                
                reset_form = PasswordResetForm(password_reset_translations, current_lang)
                return Title(password_reset_translations.get("title", "Reset Password")), Div(
                    reset_form.render_request_form(),
                    cls="min-h-screen flex items-center justify-center bg-gray-50 py-12"
                )
            
            elif request.method == "POST":
                # Handle forgot password request
                is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
                
                if not self.auth:
                    if is_ajax:
                        return {"success": False, "message": "Authentication service is currently unavailable"}
                    else:
                        return RedirectResponse(url="/?error=auth_not_available", status_code=302)
                
                form = await request.form()
                email = form.get("email", "").strip()
                
                # Get current language from request state
                current_lang = getattr(request.state, 'language', 'nl')
                
                if not email:
                    if is_ajax:
                        return {"success": False, "message": "Please enter your email address"}
                    else:
                        return RedirectResponse(url="/forgot-password?error=missing_email", status_code=302)
                
                success, message = self.auth.initiate_password_reset(email, current_lang)
                
                if is_ajax:
                    if success:
                        return {"success": True, "message": "Password reset link has been sent to your email address if it exists in our system."}
                    else:
                        # For security, always show success message to prevent email enumeration
                        return {"success": True, "message": "Password reset link has been sent to your email address if it exists in our system."}
                else:
                    if success:
                        return RedirectResponse(url="/?success=reset_email_sent", status_code=302)
                    else:
                        return RedirectResponse(url="/forgot-password?error=reset_failed", status_code=302)
        
        @rt("/reset-password/{token}", methods=["GET", "POST"])
        async def reset_password_handler(request):
            """Handle both GET and POST for password reset."""
            if not self.auth:
                return RedirectResponse(url="/?error=auth_not_available", status_code=302)
            
            token = request.path_params["token"]
            
            if request.method == "GET":
                # Show password reset form
                # Get the language for this reset token
                reset_language = self.auth.get_reset_token_language(token)
                password_reset_translations = self.translations.get(reset_language, {}).get("password_reset", {})
                
                # Validate token
                reset_data = self.auth.db.fetch_one(
                    "SELECT user_id, expires_at, used_at FROM password_resets WHERE token = :token",
                    {"token": token}
                )
                
                if not reset_data or reset_data[2] or datetime.now() > reset_data[1]:  # used_at or expired
                    return Title(password_reset_translations.get("invalid_expired_title", "Invalid Reset Link")), Div(
                        Div(
                            H1(password_reset_translations.get("invalid_expired_title", "Invalid or Expired Reset Link"), cls="text-3xl font-bold text-red-600 mb-4"),
                            P(password_reset_translations.get("invalid_expired_message", "This password reset link is invalid or has expired."), cls="text-gray-600 mb-4"),
                            A(password_reset_translations.get("request_new_link", "Request New Reset Link"), href="/forgot-password", cls="text-[#3D2E7C] hover:underline"),
                            cls="text-center"
                        ),
                        cls="min-h-screen flex items-center justify-center bg-gray-50"
                    )
                
                reset_form = PasswordResetForm(password_reset_translations, reset_language)
                return Html(
                    Head(
                        Title(password_reset_translations.get("title", "Reset Password")),
                        Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                        Link(rel="stylesheet", href=self.versioned_url("/static/app.css"), type="text/css"),
                        Link(rel="icon", href=self.versioned_url("/static/assets/Teambee icon.png"), type="image/png"),
                        Script(src=self.versioned_url("/static/js/form-handlers.js")),
                    ),
                    Body(
                        Div(
                            Div(
                                reset_form.render_reset_form(),
                                cls="w-full max-w-md"
                            ),
                            cls="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4"
                        )
                    )
                )
            
            elif request.method == "POST":
                # Handle password reset
                is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
                
                form = await request.form()
                password = form.get("password", "")
                confirm_password = form.get("confirm_password", "")
                
                # Validate input
                if not password or not confirm_password:
                    error_message = "Both password fields are required"
                    if is_ajax:
                        return {"success": False, "message": error_message}
                    else:
                        return RedirectResponse(url=f"/reset-password/{token}?error=missing_fields", status_code=302)
                
                if password != confirm_password:
                    error_message = "Passwords do not match"
                    if is_ajax:
                        return {"success": False, "message": error_message}
                    else:
                        return RedirectResponse(url=f"/reset-password/{token}?error=passwords_dont_match", status_code=302)
                
                if len(password) < 8:
                    error_message = "Password must be at least 8 characters long"
                    if is_ajax:
                        return {"success": False, "message": error_message}
                    else:
                        return RedirectResponse(url=f"/reset-password/{token}?error=password_too_short", status_code=302)
                
                # Try to reset password
                success, message = self.auth.reset_password(token, password)
                
                if is_ajax:
                    if success:
                        return {"success": True, "message": "Password reset successfully! You can now log in with your new password.", "redirect": "/"}
                    else:
                        return {"success": False, "message": message}
                else:
                    if success:
                        return RedirectResponse(url="/?success=password_reset", status_code=302)
                    else:
                        return RedirectResponse(url=f"/reset-password/{token}?error={message}", status_code=302)
        
        # Admin panel routes
        @rt("/admin")
        async def admin_redirect(request):
            """Redirect to admin users page."""
            if not self.require_admin(request):
                return RedirectResponse(url="/", status_code=302)
            
            return RedirectResponse(url="/admin/users", status_code=302)
        
        @rt("/admin/users")
        async def admin_users(request):
            """Admin users page."""
            if not self.require_admin(request):
                return RedirectResponse(url="/", status_code=302)
            
            user_info = self.get_current_user(request)
            admin_layout = AdminPanelLayout(self.versioned_url)
            
            # Get all users
            users_df = self.auth.get_all_users()
            
            if users_df is None or users_df.empty:
                user_rows = [Tr(Td("No users found", colspan="7", cls="text-center text-gray-500 py-4"))]
            else:
                user_rows = []
                for _, user in users_df.iterrows():
                    user_rows.append(
                        Tr(
                            Td(str(user['user_id']), cls="px-4 py-2 text-sm"),
                            Td(user['email'], cls="px-4 py-2 text-sm"),
                            Td(user['user_type'], cls="px-4 py-2 text-sm"),
                            Td(user['club_name'] if user['club_name'] else 'N/A', cls="px-4 py-2 text-sm"),
                            Td(str(user['last_login']) if user['last_login'] else 'Never', cls="px-4 py-2 text-sm text-gray-500"),
                            Td(str(user['created_at']), cls="px-4 py-2 text-sm text-gray-500"),
                            Td(
                                Form(
                                    Button(
                                        Img(
                                            src=self.versioned_url("/static/assets/trash.svg"),
                                            alt="Delete",
                                            cls="w-4 h-4"
                                        ),
                                        type="submit",
                                        cls="p-1 text-red-600 hover:text-red-800 hover:bg-red-100 rounded transition-colors",
                                        onclick="return confirm('Are you sure you want to delete this user? This action cannot be undone.')"
                                    ),
                                    method="post",
                                    action=f"/admin/delete-user/{user['user_id']}"
                                ),
                                cls="px-4 py-2 text-sm"
                            ),
                            cls="border-b hover:bg-gray-50 user-row"
                        )
                    )
            
            content = Div(
                Div(
                    H1("All Users", cls="text-3xl font-bold text-[#3D2E7C] mb-4"),
                    
                    # Search bar
                    Div(
                        Input(
                            type="text",
                            id="user-search",
                            placeholder="Search by email...",
                            cls="w-full max-w-md px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#3D2E7C] focus:border-[#3D2E7C]"
                        ),
                        cls="mb-6"
                    ),
                    
                    Div(
                        Table(
                            Thead(
                                Tr(
                                    Th("ID", cls="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Email", cls="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Type", cls="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Club", cls="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Last Login", cls="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Created", cls="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Actions", cls="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    cls="bg-gray-50"
                                )
                            ),
                            Tbody(*user_rows, id="users-tbody"),
                            cls="min-w-full divide-y divide-gray-200"
                        ),
                        
                        # No results message (initially hidden)
                        Div(
                            P("No users found matching your search.", cls="text-center text-gray-500 py-8"),
                            id="no-users-found",
                            cls="hidden bg-white shadow-sm rounded-lg p-4"
                        ),
                        
                        # Pagination container
                        Div(id="users-pagination-container"),
                        
                        cls="bg-white shadow-sm rounded-lg overflow-hidden"
                    ),

                    
                    cls="container mx-auto px-4"
                ),
            )
            
            return admin_layout.render(user_info, content)
        
        @rt("/admin/clubs")
        async def admin_clubs(request):
            """Admin clubs page."""
            if not self.require_admin(request):
                return RedirectResponse(url="/", status_code=302)
            
            user_info = self.get_current_user(request)
            admin_layout = AdminPanelLayout(self.versioned_url)
            
            # Get all clubs
            clubs_df = self.auth.get_clubs()
            
            if clubs_df is None or clubs_df.empty:
                club_rows = [Tr(Td("No clubs found", colspan="6", cls="text-center text-gray-500 py-8"))]
            else:
                club_rows = []
                for _, club in clubs_df.iterrows():
                    club_rows.append(
                        Tr(
                            Td(str(club['club_id']), cls="px-4 py-3 text-sm"),
                            Td(club['name'], cls="px-4 py-3 text-sm font-medium"),
                            Td(club['system_prefix'], cls="px-4 py-3 text-sm"),
                            Td(club['language'].upper(), cls="px-4 py-3 text-sm"),
                            Td(str(club['created_at']), cls="px-4 py-3 text-sm text-gray-500"),
                            Td(
                                A("Generate Link", href=f"/admin/generate-link/{club['club_id']}", 
                                  cls="text-[#3D2E7C] hover:underline text-sm"),
                                cls="px-4 py-3 text-sm"
                            ),
                            cls="border-b hover:bg-gray-50 club-row"
                        )
                    )
            
            content = Div(
                Div(
                    H1("All Clubs", cls="text-3xl font-bold text-[#3D2E7C] mb-4"),
                    
                    # Action bar with search and create button
                    Div(
                        Input(
                            type="text",
                            id="club-search",
                            placeholder="Search by club name...",
                            cls="flex-1 max-w-md px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#3D2E7C] focus:border-[#3D2E7C]"
                        ),
                        A("Create New Club", href="/admin/create-club", 
                          cls="inline-flex items-center px-4 py-2 bg-[#3D2E7C] text-white rounded-lg hover:bg-[#3D2E7C]/90"),
                        cls="flex justify-between items-center gap-4 mb-6"
                    ),
                    
                    Div(
                        Table(
                            Thead(
                                Tr(
                                    Th("ID", cls="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Name", cls="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("System Prefix", cls="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Language", cls="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Created", cls="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Actions", cls="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    cls="bg-gray-50"
                                )
                            ),
                            Tbody(*club_rows, id="clubs-tbody"),
                            cls="min-w-full divide-y divide-gray-200"
                        ),
                        
                        # No results message (initially hidden)
                        Div(
                            P("No clubs found matching your search.", cls="text-center text-gray-500 py-8"),
                            id="no-clubs-found",
                            cls="hidden bg-white shadow-sm rounded-lg p-4"
                        ),
                        
                        # Pagination container
                        Div(id="clubs-pagination-container"),
                        
                        cls="bg-white shadow-sm rounded-lg overflow-hidden"
                    ),

                    
                    cls="container mx-auto px-4"
                ),
            )
            
            return admin_layout.render(user_info, content)
        
        @rt("/admin/create-club", methods=["GET", "POST"])
        async def admin_create_club_handler(request):
            """Handle both GET and POST for club creation."""
            if not self.require_admin(request):
                return RedirectResponse(url="/", status_code=302)
            
            if request.method == "GET":
                # Show the form
                user_info = self.get_current_user(request)
                admin_layout = AdminPanelLayout(self.versioned_url)
                club_form = ClubForm(self.versioned_url)
                
                content = Div(
                    Div(
                        club_form.render(),
                        cls="container mx-auto px-4"
                    ),
                )
                
                return admin_layout.render(user_info, content)
            
            elif request.method == "POST":
                # Handle form submission
                if not self.auth:
                    return RedirectResponse(url="/admin/create-club?error=auth_not_available", status_code=302)
                
                try:
                    form = await request.form()
                    name = form.get("name", "").strip()
                    system_prefix = form.get("system_prefix", "").strip()
                    language = form.get("language", "").strip()
                    
                    if not all([name, system_prefix, language]):
                        return RedirectResponse(url="/admin/create-club?error=missing_fields", status_code=302)
                    
                    # Create club
                    success, message, club_id = self.auth.create_club(name, system_prefix, language)
                    
                    if success and club_id:
                        # Generate registration token for the new club
                        token = self.auth.create_registration_token(club_id)
                        
                        if token:
                            registration_link = f"{os.getenv('BASE_URL', 'http://localhost:8000')}/register/{token}"
                            
                            user_info = self.get_current_user(request)
                            admin_layout = AdminPanelLayout(self.versioned_url)
                            
                            content = Div(
                                Div(
                                    H1("Club Created Successfully!", cls="text-3xl font-bold text-green-600 mb-6"),
                                    
                                    Div(
                                        H3("Club Details:", cls="text-lg font-semibold mb-4"),
                                        P(f"Name: {name}", cls="mb-2"),
                                        P(f"System Prefix: {system_prefix}", cls="mb-2"),
                                        P(f"Language: {language.upper()}", cls="mb-2"),
                                        P(f"Club ID: {club_id}", cls="mb-6"),
                                        
                                        H3("Registration Link:", cls="text-lg font-semibold mb-4"),
                                        Code(registration_link, cls="block p-4 bg-gray-100 rounded mb-4 break-all text-sm"),
                                        P("Share this link with the club administrator to create their account.", cls="text-sm text-gray-600 mb-6"),
                                        
                                        Div(
                                            A("Create Another Club", href="/admin/create-club", 
                                              cls="inline-flex items-center px-4 py-2 bg-[#3D2E7C] text-white rounded-lg hover:bg-[#3D2E7C]/90 mr-4"),
                                            A("View All Clubs", href="/admin/clubs", 
                                              cls="inline-flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"),
                                            cls="flex gap-4"
                                        ),
                                        
                                        cls="bg-white p-6 rounded-lg shadow-sm border"
                                    ),
                                    
                                    cls="container mx-auto px-4"
                                ),
                            )
                            
                            return admin_layout.render(user_info, content)
                        else:
                            return RedirectResponse(url="/admin/create-club?error=token_creation_failed", status_code=302)
                    else:
                        return RedirectResponse(url=f"/admin/create-club?error={message}", status_code=302)
                    
                except Exception as e:
                    return RedirectResponse(url="/admin/create-club?error=unexpected_error", status_code=302)
        
        @rt("/admin/generate-link/{club_id}")
        async def admin_generate_link(request):
            """Generate registration link for existing club."""
            if not self.require_admin(request):
                return RedirectResponse(url="/", status_code=302)
            
            club_id = int(request.path_params["club_id"])
            
            if not self.auth:
                return RedirectResponse(url="/admin/clubs?error=auth_not_available", status_code=302)
            
            token = self.auth.create_registration_token(club_id)
            
            if token:
                registration_link = f"{os.getenv('BASE_URL', 'http://localhost:8000')}/register/{token}"
                
                user_info = self.get_current_user(request)
                admin_layout = AdminPanelLayout(self.versioned_url)
                
                content = Div(
                    Div(
                        H1("Registration Link Generated", cls="text-3xl font-bold text-green-600 mb-6"),
                        
                        Div(
                            H3("Registration Link:", cls="text-lg font-semibold mb-4"),
                            Code(registration_link, cls="block p-4 bg-gray-100 rounded mb-4 break-all text-sm"),
                            P("Share this link with the club administrator to create their account.", cls="text-sm text-gray-600 mb-6"),
                            
                            A("Back to Clubs", href="/admin/clubs", 
                              cls="inline-flex items-center px-4 py-2 bg-[#3D2E7C] text-white rounded-lg hover:bg-[#3D2E7C]/90"),
                            
                            cls="bg-white p-6 rounded-lg shadow-sm border"
                        ),
                        
                        cls="container mx-auto px-4"
                    )
                )
                
                return admin_layout.render(user_info, content)
            else:
                return RedirectResponse(url="/admin/clubs?error=token_creation_failed", status_code=302)
        
        @rt("/admin/delete-user/{user_id}", methods=["POST"])
        async def admin_delete_user(request):
            """Delete a user."""
            if not self.require_admin(request):
                return RedirectResponse(url="/", status_code=302)
            
            user_id = int(request.path_params["user_id"])
            
            if not self.auth:
                return RedirectResponse(url="/admin/users?error=auth_not_available", status_code=302)
            
            # Prevent admin from deleting themselves
            current_user = self.get_current_user(request)
            if current_user and current_user["user_id"] == user_id:
                return RedirectResponse(url="/admin/users?error=cannot_delete_self", status_code=302)
            
            success, message = self.auth.delete_user(user_id)
            
            if success:
                return RedirectResponse(url="/admin/users?success=user_deleted", status_code=302)
            else:
                return RedirectResponse(url=f"/admin/users?error={message}", status_code=302)
        
        # Contact form route
        @rt("/contact", methods=["POST"])
        async def contact_handler(request):
            """Handle contact form submissions."""
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            # Get current language for translations
            self.request = request
            current_lang = request.state.language
            
            try:
                form = await request.form()
                first_name = form.get("first_name", "").strip()
                last_name = form.get("last_name", "").strip()
                club_name = form.get("club_name", "").strip()
                email = form.get("email", "").strip()
                phone = form.get("phone", "").strip()
                form_type = form.get("form_type", "").strip()
                
                # Validate required fields
                if not all([first_name, last_name, club_name, email, phone]):
                    error_msg = self.get_text("contact", "all_fields_required") or "All fields are required"
                    if is_ajax:
                        return {"success": False, "message": error_msg}
                    else:
                        return RedirectResponse(url="/?error=missing_fields", status_code=302)
                
                # Validate email format
                if "@" not in email or "." not in email:
                    error_msg = self.get_text("contact", "invalid_email") or "Please enter a valid email address"
                    if is_ajax:
                        return {"success": False, "message": error_msg}
                    else:
                        return RedirectResponse(url="/?error=invalid_email", status_code=302)
                
                # Determine form type identifier
                identifier = "CRM" if form_type == "services" else "Ongoing"
                
                # Send email
                success, message = self.send_contact_email(
                    first_name, last_name, club_name, email, phone, identifier
                )
                
                if is_ajax:
                    if success:
                        success_msg = self.get_text("contact", "success_message") or "Thank you for your message! We'll get back to you soon."
                        return {"success": True, "message": success_msg}
                    else:
                        error_msg = self.get_text("contact", "error_message") or "Sorry, there was an error sending your message. Please try again."
                        return {"success": False, "message": error_msg}
                else:
                    if success:
                        return RedirectResponse(url="/?success=contact_sent", status_code=302)
                    else:
                        return RedirectResponse(url="/?error=contact_failed", status_code=302)
                
            except Exception as e:
                print(f"Contact form error: {e}")
                error_msg = self.get_text("contact", "error_message") or "Sorry, there was an error sending your message. Please try again."
                if is_ajax:
                    return {"success": False, "message": error_msg}
                else:
                    return RedirectResponse(url="/?error=contact_failed", status_code=302)
    
    def send_contact_email(self, first_name, last_name, club_name, email, phone, identifier):
        """Send contact form email to info@teambee.fit."""
        try:
            # Use the same email configuration as auth system
            email_user = os.getenv("EMAIL_USER")
            email_password = os.getenv("EMAIL_PASSWORD")
            from_email = os.getenv("FROM_EMAIL", email_user)
            smtp_server = os.getenv("SMTP_SERVER")
            smtp_port = int(os.getenv("SMTP_PORT"))
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = "info@teambee.fit"
            msg['Subject'] = f"New Contact Form Submission - {identifier}"
            
            # Email body
            body = f"""
New contact form submission:

Name: {first_name} {last_name}
Club: {club_name}
Email: {email}
Phone: {phone}
Type: {identifier}

---
This message was sent from the Teambee website contact form.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_user, email_password)
                server.send_message(msg)
            
            return True, "Email sent successfully"
            
        except Exception as e:
            print(f"Email sending error: {e}")
            return False, f"Failed to send email: {str(e)}"
    
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
            
            # Login popup modal
            self._create_login_popup(),
            
            # Contact popup modal
            self._create_contact_popup(),
            
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
    
    def _create_hero_section(self):
        """Create the hero section."""
        return Section(
            Div(
                Div(
                    Div(
                        H1(
                            self.get_text("home", "hero_title"),
                            cls="text-4xl md:text-5xl font-bold italic text-[#3D2E7C] leading-tight animate-section-title"
                        ),
                        P(
                            self.get_text("home", "hero_subtitle"),
                            cls="text-lg text-gray-600 max-w-md animate-section-subtitle"
                        ),
                        Div(
                            Button(
                                "Our services",
                                Span("→", cls="ml-2"),
                                cls="inline-flex h-10 items-center justify-center rounded-lg bg-[#3D2E7C] px-8 py-2 text-sm font-medium text-white shadow transition-all duration-300 ease-in-out hover:bg-[#3D2E7C]/90 hover:-translate-y-2 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#3D2E7C] focus-visible:ring-offset-2 animate-card",
                                id="hero-services-button"
                            ),
                            cls="flex flex-col sm:flex-row gap-4"
                        ),
                        cls="space-y-6"
                    ),
                    Div(
                        Img(
                            src=self.versioned_url("/static/assets/Teambee icon.png"),
                            alt="Teambee Hero",
                            cls="w-full h-full object-contain animate-card",
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
                        cls="bg-white p-6 rounded-lg shadow-sm transform transition-shadow duration-300 hover:shadow-md hover:shadow-gray-300"
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
                        cls="bg-white p-6 rounded-lg shadow-sm transform transition-shadow duration-300 hover:shadow-md hover:shadow-gray-300"
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
                        cls="bg-white p-6 rounded-lg shadow-sm transform transition-shadow duration-300 hover:shadow-md hover:shadow-gray-300"
                    ),
                    
                    cls="grid md:grid-cols-3 gap-8 animate-stagger-container"
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
                        cls="text-3xl md:text-4xl font-bold italic mb-4 animate-section-title"
                    ),
                    cls="text-center mb-12"
                ),
                
                Div(
                    # Implementation section
                    Div(
                        Div(
                            # Header section
                            Div(
                                H3(
                                    self.get_text("services", "implementation"),
                                    cls="text-xl font-semibold text-[#ffffff] mb-2"
                                ),
                                P(
                                    self.get_text("services", "subtitle"),
                                    cls="text-sm text-white/80 animate-section-subtitle mb-4"
                                ),
                                # Separator line
                                Div(
                                    cls="w-50 h-0.5 bg-white/30 mb-6"
                                ),
                                cls=""
                            ),
                            
                            # Content section
                            Div(
                                Ul(
                                    self._create_check_list_item(self.get_text("services", "strategy")),
                                    self._create_check_list_item(self.get_text("services", "design")),
                                    self._create_check_list_item(self.get_text("services", "implementation_detail")),
                                    self._create_check_list_item(self.get_text("services", "education")),
                                    self._create_check_list_item(self.get_text("services", "data_support")),
                                    cls="space-y-3"
                                ),
                                cls="flex-grow"
                            ),
                            
                            # Button container
                            Div(
                                Button(
                                    self.get_text("services", "cta"),
                                    cls="inline-flex h-12 items-center justify-center rounded-lg bg-[#94C46F] px-8 py-2 text-base font-medium text-white shadow transition-all duration-300 ease-in-out hover:bg-[#94C46F]/90 hover:scale-105 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#94C46F] focus-visible:ring-offset-2 animate-card",
                                    id="services-cta-button",
                                    data_form_type="services"
                                ),
                                cls="text-center mt-4"
                            ),
                            cls="bg-[#1B1947] p-6 rounded-lg min-h-[570px] animate-card flex flex-col justify-between"
                        ),
                        cls="flex flex-col"
                    ),
                    
                    # Data Support section
                    Div(
                        Div(
                            # Header section
                            Div(
                                H3(
                                    self.get_text("services", "data_support_title"),
                                    cls="text-xl font-semibold text-[#ffffff] mb-2"
                                ),
                                P(
                                    self.get_text("services", "data_support_subtitle"),
                                    cls="text-sm text-white/80 animate-section-subtitle mb-4"
                                ),
                                # Separator line
                                Div(
                                    cls="w-50 h-0.5 bg-white/30 mb-6"
                                ),
                                cls=""
                            ),
                            
                            # Content section
                            Div(
                                Ul(
                                    self._create_check_list_item(self.get_text("services", "data_support_inzicht")),
                                    self._create_check_list_item(self.get_text("services", "data_support_actie")),
                                    self._create_check_list_item(self.get_text("services", "data_support_retentie")),
                                    self._create_check_list_item(self.get_text("services", "data_support_team")),
                                    self._create_check_list_item(self.get_text("services", "data_support_groei")),
                                    cls="space-y-3"
                                ),
                                cls="flex-grow"
                            ),
                            
                            # Button container
                            Div(
                                Button(
                                    self.get_text("services", "view_report"),
                                    cls="inline-flex h-12 items-center justify-center rounded-lg bg-[#94C46F] px-8 py-2 text-base font-medium text-white shadow transition-all duration-300 ease-in-out hover:bg-[#94C46F]/90 hover:scale-105 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#94C46F] focus-visible:ring-offset-2 animate-card",
                                    data_form_type="services"
                                ),
                                cls="text-center mt-4"
                            ),
                            cls="bg-[#1B1947] p-6 rounded-lg min-h-[570px] animate-card flex flex-col justify-between"
                        ),
                        cls="flex flex-col"
                    ),
                    cls="grid md:grid-cols-2 gap-8 animate-stagger-container"
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
            cls="flex items-start animate-stagger-item"
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
                        cls="text-3xl md:text-4xl font-bold italic text-[#3D2E7C] mb-4 animate-section-title"
                    ),
                    P(
                        self.get_text("benefits", "subtitle"),
                        cls="text-lg text-gray-600 max-w-2xl mx-auto animate-section-subtitle"
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
                        cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100 animate-card"
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
                        cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100 animate-card"
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
                        cls="bg-white p-6 rounded-lg shadow-sm border border-gray-100 animate-card"
                    ),
                    
                    cls="grid md:grid-cols-3 gap-8 mb-16 animate-stagger-container"
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
                            cls="text-lg font-medium text-gray-500 mb-8 animate-section-title"
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
                                cls="flex items-center justify-center animate-stagger-item"
                            )
                            for partner in partners
                        ],
                        cls="grid grid-cols-2 md:flex md:flex-nowrap justify-center items-center gap-4 md:gap-12 max-w-4xl mx-auto animate-stagger-container"
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
            "Jasper Appeldoorn": "xfit_foto.jpg",
            "Jelle Notkamp": "EV_jelle.jpg"
        }
        
        # Get current language
        current_lang = self.request.state.language
        
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
                            cls="text-xs text-gray-400 ml-2 italic" if current_lang == "en" else "hidden",
                        ),
                        cls="flex items-center mb-4"
                    ),
                    P(
                        review["quote"][current_lang],
                        cls="text-gray-600 mb-4 flex-grow"
                    ),
                    Div(
                        Div(
                            Img(
                                src=self.versioned_url(f"/static/assets/{image_file}"),
                                alt=review["author"][current_lang],
                                cls="w-10 h-10 rounded-full bg-gray-200 mr-3 object-cover"
                            ),
                            Div(
                                Div(
                                    review["author"][current_lang],
                                    cls="font-semibold text-[#1B1947]"
                                ),
                                Div(
                                    review["title"][current_lang],
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
    
    def _create_login_section(self):
        """Create the login section."""
        # Get login translations for the current language
        login_translations = self.translations.get(self.request.state.language, {}).get("login", {})
        login_form = LoginForm(login_translations, "main")
        
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
                    
                    # Login form
                    login_form.render(),
                    
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