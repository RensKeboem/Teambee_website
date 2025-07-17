"""
Public Routes

Contains public-facing route handlers like homepage, contact, etc.
"""

from fasthtml.common import *
from starlette.responses import RedirectResponse, PlainTextResponse


class PublicRoutes:
    """Public route handlers."""
    
    def __init__(self, app_instance):
        """Initialize with reference to main app instance."""
        self.app = app_instance
    
    def setup_routes(self, rt):
        """Setup public routes."""
        
        @rt("/health")
        async def health(request):
            """Health check endpoint."""
            return PlainTextResponse("OK", status_code=200)

        @rt("/")
        async def home(request):
            """Render the home page in Dutch (default)."""
            self.app.request = request  # Store request for translation context
            # Check for success message in session and clear it
            success_message = request.session.pop("success_message", None)
            return Title("Teambee"), self.app.create_homepage(success_message)
        
        @rt("/en")
        async def home_en(request):
            """Render the home page in English."""
            self.app.request = request  # Store request for translation context
            # Check for success message in session and clear it
            success_message = request.session.pop("success_message", None)
            return Title("Teambee"), self.app.create_homepage(success_message)
        
        @rt("/en/")
        async def home_en_slash(request):
            """Redirect /en/ to /en."""
            return RedirectResponse(url="/en", status_code=301)
        
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
        
        @rt("/contact", methods=["POST"])
        async def contact_nl(request):
            """Handle Dutch contact form."""
            return await self.contact_form_handler(request)
        
        @rt("/en/contact", methods=["POST"])
        async def contact_en(request):
            """Handle English contact form."""
            return await self.contact_form_handler(request)
        
        @rt("/success-stories")
        async def success_stories(request):
            """Handle success stories direct access."""
            self.app.request = request
            return Title("Success Stories - Teambee"), self.app.create_homepage(
                auto_open_success_stories=True, 
                target_url="/success-stories"
            )
    
    async def contact_form_handler(self, request):
        """Handle contact form submissions."""
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # Get current language for translations
        self.app.request = request
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
                error_msg = self.app.get_text("contact", "all_fields_required") or "All fields are required"
                if is_ajax:
                    return {"success": False, "message": error_msg}
                else:
                    return RedirectResponse(url="/?error=missing_fields", status_code=302)
            
            # Validate email format
            if "@" not in email or "." not in email:
                error_msg = self.app.get_text("contact", "invalid_email") or "Please enter a valid email address"
                if is_ajax:
                    return {"success": False, "message": error_msg}
                else:
                    return RedirectResponse(url="/?error=invalid_email", status_code=302)
            
            # Determine form type identifier
            identifier = "CRM" if form_type == "services" else "Ongoing"
            
            # Send email notification
            success = self.app.send_contact_email(
                first_name, last_name, club_name, email, phone, identifier
            )
            
            if success:
                success_msg = self.app.get_text("contact", "message_sent") or "Thank you! Your message has been sent successfully."
                if is_ajax:
                    return {"success": True, "message": success_msg}
                else:
                    request.session["success_message"] = success_msg
                    redirect_url = "/en" if current_lang == "en" else "/"
                    return RedirectResponse(url=redirect_url, status_code=302)
            else:
                error_msg = self.app.get_text("contact", "send_error") or "Sorry, there was an error sending your message. Please try again."
                if is_ajax:
                    return {"success": False, "message": error_msg}
                else:
                    return RedirectResponse(url="/?error=send_error", status_code=302)
                
        except Exception as e:
            error_msg = "An unexpected error occurred. Please try again."
            if is_ajax:
                return {"success": False, "message": error_msg}
            else:
                return RedirectResponse(url="/?error=unexpected_error", status_code=302) 