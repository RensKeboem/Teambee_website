"""
Authentication Routes

Contains all authentication-related route handlers.
"""

from fasthtml.common import *
from starlette.responses import RedirectResponse
from app.components.forms.registration_form import RegistrationForm
from app.components.forms.password_reset_form import PasswordResetForm


class AuthRoutes:
    """Authentication route handlers."""
    
    def __init__(self, app_instance):
        """Initialize with reference to main app instance."""
        self.app = app_instance
        self.auth = app_instance.auth
        self.translations = app_instance.translations
    
    def setup_routes(self, rt):
        """Setup authentication routes."""
        
        @rt("/login", methods=["POST"])
        async def login_nl(request):
            """Handle Dutch login."""
            return await self.login_handler(request)
        
        @rt("/en/login", methods=["POST"])
        async def login_en(request):
            """Handle English login."""
            return await self.login_handler(request)
        
        @rt("/logout")
        async def logout(request):
            """Handle logout."""
            self.app.logout_user(request)
            # Determine redirect URL based on current language
            current_lang = getattr(request.state, 'language', 'nl')
            redirect_url = "/en" if current_lang == "en" else "/"
            return RedirectResponse(url=redirect_url, status_code=302)
        
        @rt("/register/{token}", methods=["GET", "POST"])
        async def registration_handler(request):
            """Handle user registration with token."""
            return await self.registration_handler(request)
        
        @rt("/forgot-password", methods=["GET", "POST"])
        async def forgot_password_nl(request):
            """Handle Dutch password reset."""
            return await self.forgot_password_shared_handler(request)
        
        @rt("/en/forgot-password", methods=["GET", "POST"])
        async def forgot_password_en(request):
            """Handle English password reset."""
            return await self.forgot_password_shared_handler(request)
        
        @rt("/reset-password/{token}", methods=["GET", "POST"])
        async def reset_password_handler(request):
            """Handle password reset with token."""
            return await self.reset_password_handler(request)
        
        @rt("/en/reset-password/{token}", methods=["GET", "POST"])
        async def reset_password_handler_en(request):
            """Handle English password reset with token."""
            return await self.reset_password_handler(request)
        
        @rt("/api/registration/{token}", methods=["GET"])
        async def get_registration_info(request):
            """Get registration info for a token (for AJAX requests)."""
            token = request.path_params.get("token")
            
            if not self.auth:
                return {"valid": False, "error": "Authentication service not available"}
            
            # Validate token
            club_id = self.auth.validate_registration_token(token)
            if not club_id:
                return {"valid": False, "error": "Invalid or expired token"}
            
            # Get club info
            club_info = self.app.auth.db.fetch_one(
                "SELECT name, language FROM clubs WHERE club_id = :club_id",
                {"club_id": club_id}
            )
            
            if not club_info:
                return {"valid": False, "error": "Club not found"}
            
            club_name, club_language = club_info
            
            return {
                "valid": True,
                "club_name": club_name,
                "club_language": club_language
            }
    
    async def login_handler(self, request):
        """Handle login form submission."""
        self.app.request = request  # Store request for translation context
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if not self.auth:
            if is_ajax:
                return {"success": False, "message": self.app.get_message("auth_not_available")}
            else:
                return RedirectResponse(url="/?error=auth_not_available", status_code=302)
        
        form = await request.form()
        email = form.get("email", "").strip()
        password = form.get("password", "")
        
        if not email or not password:
            if is_ajax:
                return {"success": False, "message": self.app.get_message("missing_credentials")}
            else:
                return RedirectResponse(url="/?error=missing_credentials", status_code=302)
        
        success, user_info, message = self.auth.authenticate_user(email, password)
        
        if success:
            self.app.login_user(request, user_info)
            
            # Determine redirect URL
            if user_info.get("club_id") is None:  # Admin user
                redirect_url = "/admin"
            else:  # Regular user
                current_lang = request.state.language
                redirect_url = "/en/dashboard" if current_lang == "en" else "/dashboard"
            
            if is_ajax:
                return {"success": True, "redirect_url": redirect_url}
            else:
                return RedirectResponse(url=redirect_url, status_code=302)
        else:
            if is_ajax:
                return {"success": False, "message": message}
            else:
                return RedirectResponse(url=f"/?error={message}", status_code=302)
    
    async def registration_handler(self, request):
        """Handle user registration with token."""
        self.app.request = request
        token = request.path_params.get("token")
        current_lang = request.state.language
        
        if not self.auth:
            return RedirectResponse(url=self.app.get_language_root_url(request), status_code=302)
        
        # Validate token
        club_id = self.auth.validate_registration_token(token)
        if not club_id:
            return RedirectResponse(url=f"{self.app.get_language_root_url(request)}?error=invalid_token", status_code=302)
        
        # Get club info
        club_info = self.app.auth.db.fetch_one(
            "SELECT name, language FROM clubs WHERE club_id = :club_id",
            {"club_id": club_id}
        )
        
        if not club_info:
            return RedirectResponse(url=f"{self.app.get_language_root_url(request)}?error=invalid_token", status_code=302)
        
        club_name, club_language = club_info
        
        if request.method == "POST":
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            form = await request.form()
            email = form.get("email", "").strip()
            password = form.get("password", "")
            confirm_password = form.get("confirm_password", "")
            
            # Validation
            if not email or not password:
                if is_ajax:
                    error_message = self.translations.get(current_lang, {}).get("messages", {}).get("missing_credentials", "Email and password are required")
                    return {"success": False, "message": error_message}
                return Title("Registration - Teambee"), RegistrationForm().render(club_name, email)
            
            if password != confirm_password:
                if is_ajax:
                    error_message = self.translations.get(current_lang, {}).get("messages", {}).get("passwords_no_match", "Passwords do not match")
                    return {"success": False, "message": error_message}
                return Title("Registration - Teambee"), RegistrationForm().render(club_name, email)
            
            if len(password) < 8:
                if is_ajax:
                    error_message = self.translations.get(current_lang, {}).get("messages", {}).get("password_too_short", "Password must be at least 8 characters long")
                    return {"success": False, "message": error_message}
                return Title("Registration - Teambee"), RegistrationForm().render(club_name, email)
            
            # Complete registration
            success, message = self.auth.complete_registration(token, email, password)
            
            if success:
                if is_ajax:
                    success_message = self.translations.get(current_lang, {}).get("messages", {}).get("registration_success", "Account created successfully! You can now log in.")
                    root_url = "/en" if current_lang == "en" else "/"
                    return {"success": True, "message": success_message, "redirect": root_url}
                else:
                    # Set success message and redirect to login
                    request.session["success_message"] = self.app.get_message("registration_success")
                    return RedirectResponse(url=self.app.get_language_root_url(request), status_code=302)
            else:
                if is_ajax:
                    return {"success": False, "message": message}
                return Title("Registration - Teambee"), RegistrationForm().render(club_name, email)
        
        # GET request - redirect to main page with registration token
        pre_filled_email = request.query_params.get("email", "")
        base_url = "/en" if current_lang == "en" else "/"
        redirect_url = f"{base_url}?registration_token={token}"
        if pre_filled_email:
            redirect_url += f"&email={pre_filled_email}"
        return RedirectResponse(url=redirect_url, status_code=302)
    
    async def forgot_password_shared_handler(self, request):
        """Handle password reset requests."""
        self.app.request = request
        current_lang = request.state.language
        
        password_reset_form = PasswordResetForm(
            self.translations.get(current_lang, {}).get("password_reset", {}),
            current_lang
        )
        
        if request.method == "POST":
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            if not self.auth:
                if is_ajax:
                    error_message = self.translations.get(current_lang, {}).get("messages", {}).get("auth_not_available", "Authentication service not available")
                    return {"success": False, "message": error_message}
                return Title("Reset Password - Teambee"), password_reset_form.render_request_form()
            
            form = await request.form()
            email = form.get("email", "").strip()
            
            if not email:
                if is_ajax:
                    error_message = self.translations.get(current_lang, {}).get("messages", {}).get("email_required", "Email address is required")
                    return {"success": False, "message": error_message}
            
            # Initiate password reset
            success, message = self.auth.initiate_password_reset(email, current_lang)
            
            if is_ajax:
                # Always show success message for security (even if email doesn't exist)
                return {"success": True, "message": self.app.get_message("password_reset_sent")}
            else:
                # Always show success message for security
                request.session["success_message"] = self.app.get_message("reset_email_sent")
                return RedirectResponse(url=self.app.get_language_root_url(request), status_code=302)
        
        # GET request
        return Title("Reset Password - Teambee"), password_reset_form.render_request_form()
    
    async def reset_password_handler(self, request):
        """Handle password reset with token."""
        self.app.request = request
        token = request.path_params.get("token")
        
        if not self.auth:
            return RedirectResponse(url="/", status_code=302)

        # Get current page language from request for AJAX responses
        current_page_lang = request.state.language
        
        # Get language from token for form rendering and redirects
        token_lang = self.auth.get_reset_token_language(token)
        
        # For GET requests, redirect to main page with token
        if request.method == "GET":
            base_url = "/en" if token_lang == "en" else "/"
            return RedirectResponse(url=f"{base_url}?reset_token={token}", status_code=302)
        
        password_reset_form = PasswordResetForm(
            self.translations.get(token_lang, {}).get("password_reset", {}),
            token_lang
        )
        
        if request.method == "POST":
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            form = await request.form()
            password = form.get("password", "")
            confirm_password = form.get("confirm_password", "")
            
            if not password or password != confirm_password:
                if is_ajax:
                    # Get error message in current page language
                    error_message = self.translations.get(current_page_lang, {}).get("messages", {}).get("passwords_no_match", "Passwords do not match or are empty")
                    return {"success": False, "message": error_message}
                return Title("Reset Password - Teambee"), password_reset_form.render_reset_form()
            
            success, message = self.auth.reset_password(token, password)
            
            if is_ajax:
                if success:
                    root_url = "/en" if current_page_lang == "en" else "/"
                    # Get success message in current page language
                    success_message = self.translations.get(current_page_lang, {}).get("messages", {}).get("password_reset_success", "Password reset successful! You can now log in with your new password.")
                    return {"success": True, "message": success_message, "redirect": root_url}
                else:
                    return {"success": False, "message": message}
            else:
                if success:
                    request.session["success_message"] = self.app.get_message("password_reset_success")
                    root_url = "/en" if token_lang == "en" else "/"
                    return RedirectResponse(url=root_url, status_code=302)
                else:
                    return Title("Reset Password - Teambee"), password_reset_form.render_reset_form()
        
        # GET request fallback (shouldn't reach here due to redirect above)
        base_url = "/en" if token_lang == "en" else "/"
        return RedirectResponse(url=f"{base_url}?reset_token={token}", status_code=302) 