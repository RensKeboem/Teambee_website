"""
Dashboard Routes Handler

Contains all dashboard-related route handlers.
"""

from fasthtml.common import *
from starlette.responses import RedirectResponse
from app.components.layouts.dashboard_layout import DashboardLayout


class DashboardRoutes:
    """Dashboard route handlers for authenticated users."""
    
    def __init__(self, app):
        """Initialize dashboard routes with app reference."""
        self.app = app
        
    def setup_routes(self, rt):
        """Set up dashboard routes."""
        
        @rt("/dashboard")
        async def dashboard(request):
            """Render the dashboard for authenticated users."""
            if not self.app.is_authenticated(request):
                return RedirectResponse(url="/", status_code=302)
            
            # Store request for translation context
            self.app.request = request
            
            user_info = self.app.get_current_user(request)
            
            # Use URL language (default is Dutch)
            current_lang = getattr(request.state, 'language', 'nl')
            
            # Get dashboard translations for the current language
            dashboard_translations = self.app.translations.get(current_lang, {}).get("dashboard", {})
            
            dashboard_layout = DashboardLayout(dashboard_translations, self.app.versioned_url, current_lang)
            return dashboard_layout.render(user_info)
        
        @rt("/en/dashboard")
        async def dashboard_en(request):
            """Render the dashboard for authenticated users in English."""
            if not self.app.is_authenticated(request):
                return RedirectResponse(url="/en", status_code=302)
            
            # Store request for translation context
            self.app.request = request
            
            user_info = self.app.get_current_user(request)
            
            # Use English language from URL
            current_lang = "en"
            
            # Get dashboard translations for English
            dashboard_translations = self.app.translations.get(current_lang, {}).get("dashboard", {})
            
            dashboard_layout = DashboardLayout(dashboard_translations, self.app.versioned_url, current_lang)
            return dashboard_layout.render(user_info)
        
        # Password update routes - shared handler
        async def password_update_handler(request):
            """Handle password update for authenticated users."""
            self.app.request = request  # Store request for translation context
            
            if not self.app.is_authenticated(request):
                return {"success": False, "message": self.app.get_message("authentication_required")}
            
            user_info = self.app.get_current_user(request)
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            if not self.app.auth:
                return {"success": False, "message": self.app.get_message("auth_service_unavailable")}
            
            form = await request.form()
            current_password = form.get("current_password", "")
            new_password = form.get("new_password", "")
            confirm_new_password = form.get("confirm_new_password", "")
            
            # Validate input
            if not all([current_password, new_password, confirm_new_password]):
                return {"success": False, "message": self.app.get_message("all_fields_required")}
            
            if new_password != confirm_new_password:
                return {"success": False, "message": self.app.get_message("passwords_no_match")}
            
            if len(new_password) < 8:
                return {"success": False, "message": self.app.get_message("password_too_short")}
            
            # Update password
            success, message = self.app.auth.update_user_password(
                user_info["user_id"], 
                current_password, 
                new_password
            )
            
            return {"success": success, "message": message}
        
        @rt("/dashboard/update-password", methods=["POST"])
        async def update_password(request):
            """Handle password update for authenticated users (Dutch)."""
            return await password_update_handler(request)
        
        @rt("/en/dashboard/update-password", methods=["POST"])
        async def update_password_en(request):
            """Handle password update for authenticated users (English)."""
            return await password_update_handler(request)
        
        # User invitation routes - shared handler
        async def invite_user_handler(request):
            """Handle user invitation for authenticated users."""
            self.app.request = request  # Store request for translation context
            
            if not self.app.is_authenticated(request):
                return {"success": False, "message": self.app.get_message("authentication_required")}
            
            user_info = self.app.get_current_user(request)
            
            # Only club users can invite (not admins)
            if not user_info.get("club_id"):
                return {"success": False, "message": self.app.get_message("only_club_users_invite")}
            
            if not self.app.auth:
                return {"success": False, "message": self.app.get_message("auth_service_unavailable")}
            
            form = await request.form()
            invite_email = form.get("invite_email", "").strip()
            
            # Validate input
            if not invite_email:
                return {"success": False, "message": self.app.get_message("email_required")}
            
            if "@" not in invite_email:
                return {"success": False, "message": self.app.get_message("valid_email_required")}
            
            # Send invitation
            success, message = self.app.auth.invite_user_to_club(
                user_info["club_id"],
                invite_email,
                user_info["email"]
            )
            
            return {"success": success, "message": message}
        
        @rt("/dashboard/invite-user", methods=["POST"])
        async def invite_user(request):
            """Handle user invitation for authenticated users (Dutch)."""
            return await invite_user_handler(request)
        
        @rt("/en/dashboard/invite-user", methods=["POST"])
        async def invite_user_en(request):
            """Handle user invitation for authenticated users (English)."""
            return await invite_user_handler(request) 