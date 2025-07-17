"""
Admin Routes Handler

Contains all admin panel route handlers.
"""

from fasthtml.common import *
from starlette.responses import RedirectResponse
from app.components.layouts.admin_layout import AdminPanelLayout
from app.components.forms.club_form import ClubForm
from app.components.forms.admin_invite_form import AdminInviteForm


class AdminRoutes:
    """Admin route handlers for administrative functions."""
    
    def __init__(self, app):
        """Initialize admin routes with app reference."""
        self.app = app
        
    def setup_routes(self, rt):
        """Set up admin routes."""
        
        @rt("/admin")
        async def admin_redirect(request):
            """Redirect to admin users page."""
            if not self.app.require_admin(request):
                return RedirectResponse(url="/", status_code=302)
            
            return RedirectResponse(url="/admin/users", status_code=302)
        
        @rt("/admin/users")
        async def admin_users(request):
            """Admin users page."""
            if not self.app.require_admin(request):
                return RedirectResponse(url="/", status_code=302)
            
            user_info = self.app.get_current_user(request)
            admin_layout = AdminPanelLayout(self.app.versioned_url)
            
            # Get all users
            users_df = self.app.auth.get_all_users()
            
            if users_df is None or users_df.empty:
                user_rows = [Tr(Td("No users found", colspan="6", cls="text-center text-gray-500 py-4"))]
            else:
                user_rows = []
                for _, user in users_df.iterrows():
                    user_rows.append(
                        Tr(
                            Td(user['email'], cls="px-4 py-2 text-sm"),
                            Td(user['user_type'], cls="px-4 py-2 text-sm"),
                            Td(user['club_name'] if user['club_name'] else 'N/A', cls="px-4 py-2 text-sm"),
                            Td(str(user['last_login']) if user['last_login'] else 'Never', cls="px-4 py-2 text-sm text-gray-500"),
                            Td(str(user['created_at']), cls="px-4 py-2 text-sm text-gray-500"),
                            Td(
                                Button(
                                    "Delete",
                                    cls="delete-user-btn text-red-600 border border-red-600 hover:bg-red-600 hover:text-white transition-colors px-2 py-1 rounded text-xs",
                                    data_user_id=user['user_id'],
                                    data_user_email=user['email'],
                                    disabled=user['user_id'] == user_info['user_id']  # Can't delete self
                                ) if user['user_id'] != user_info['user_id'] else "",
                                cls="px-4 py-2 text-sm"
                            ),
                            cls="border-b hover:bg-gray-50 user-row",
                            data_email=user['email'].lower()
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
                        cls="bg-white shadow-sm rounded-lg overflow-hidden"
                    ),
                    
                    # Pagination container for users
                    Div(id="users-pagination-container"),
                    
                    cls="container mx-auto px-4"
                )
            )
            
            return admin_layout.render(user_info, content)
        
        @rt("/admin/clubs")
        async def admin_clubs(request):
            """Admin clubs page."""
            if not self.app.require_admin(request):
                return RedirectResponse(url="/", status_code=302)
            
            user_info = self.app.get_current_user(request)
            admin_layout = AdminPanelLayout(self.app.versioned_url)
            
            # Get all clubs
            clubs_df = self.app.auth.get_clubs()
            
            if clubs_df is None or clubs_df.empty:
                club_rows = [Tr(Td("No clubs found", colspan="5", cls="text-center text-gray-500 py-8"))]
            else:
                club_rows = []
                for _, club in clubs_df.iterrows():
                    club_rows.append(
                        Tr(
                            Td(club['name'], cls="px-4 py-3 text-sm font-medium"),
                            Td(club['system_prefix'], cls="px-4 py-3 text-sm"),
                            Td(club['language'].upper(), cls="px-4 py-3 text-sm"),
                            Td(str(club['created_at']), cls="px-4 py-3 text-sm text-gray-500"),
                            Td(
                                Div(
                                    A(
                                        "See Dashboard",
                                        href=f"/admin/view-club-dashboard/{club['club_id']}",
                                        cls="text-blue-600 border border-blue-600 hover:bg-blue-600 hover:text-white transition-colors px-2 py-1 rounded text-sm mr-2"
                                    ),
                                    Button(
                                        "Send Invitation",
                                        cls="text-[#3D2E7C] border border-[#3D2E7C] hover:bg-[#3D2E7C] hover:text-white transition-colors px-2 py-1 rounded text-sm admin-invite-trigger",
                                        data_club_id=str(club['club_id']),
                                        data_club_name=club['name']
                                    ),
                                    cls="flex gap-2"
                                ),
                                cls="px-4 py-3 text-sm w-72"
                            ),
                            cls="border-b hover:bg-gray-50 club-row"
                        )
                    )
            
            content = Div(
                Div(
                    H1("All Clubs", cls="text-3xl font-bold text-[#3D2E7C] mb-4"),
                    
                    # Search bar
                    Div(
                        Input(
                            type="text",
                            id="club-search",
                            placeholder="Search by club name...",
                            cls="w-full max-w-md px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#3D2E7C] focus:border-[#3D2E7C]"
                        ),
                        cls="mb-6"
                    ),
                    
                    Div(
                        Table(
                            Thead(
                                Tr(
                                    Th("Club Name", cls="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("System Prefix", cls="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Language", cls="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Created", cls="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    Th("Actions", cls="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"),
                                    cls="bg-gray-50"
                                )
                            ),
                            Tbody(*club_rows, id="clubs-tbody"),
                            cls="min-w-full divide-y divide-gray-200 bg-white"
                        ),
                        cls="shadow-sm rounded-lg overflow-hidden"
                    ),
                    
                    # Pagination container for clubs
                    Div(id="clubs-pagination-container"),
                    
                    # Admin Invite Popup
                    AdminInviteForm(self.app.versioned_url).render(),
                    
                    cls="container mx-auto px-4"
                )
            )
            
            return admin_layout.render(user_info, content)
        
        @rt("/admin/create-club", methods=["GET", "POST"])
        async def admin_create_club_handler(request):
            """Handle both GET and POST for club creation."""
            if not self.app.require_admin(request):
                return RedirectResponse(url="/", status_code=302)
            
            if request.method == "GET":
                # Show the form
                user_info = self.app.get_current_user(request)
                admin_layout = AdminPanelLayout(self.app.versioned_url)
                club_form = ClubForm(self.app.versioned_url)
                
                content = Div(
                    Div(
                        club_form.render(),
                        cls="container mx-auto px-4"
                    ),
                )
                
                return admin_layout.render(user_info, content)
            
            elif request.method == "POST":
                # Handle form submission
                if not self.app.auth:
                    return RedirectResponse(url="/admin/create-club?error=auth_not_available", status_code=302)
                
                try:
                    form = await request.form()
                    name = form.get("name", "").strip()
                    system_prefix = form.get("system_prefix", "").strip()
                    language = form.get("language", "").strip()
                    
                    if not all([name, system_prefix, language]):
                        return RedirectResponse(url="/admin/create-club?error=missing_fields", status_code=302)
                    
                    # Create club
                    success, message, club_id = self.app.auth.create_club(name, system_prefix, language)
                    
                    if success:
                        return RedirectResponse(url="/admin/create-club?success=club_created", status_code=302)
                    else:
                        return RedirectResponse(url=f"/admin/create-club?error={message}", status_code=302)
                    
                except Exception as e:
                    return RedirectResponse(url="/admin/create-club?error=unexpected_error", status_code=302)
        
        @rt("/admin/send-registration-link", methods=["POST"])
        async def admin_send_registration_link(request):
            """Send registration link via email to specified address."""
            if not self.app.require_admin(request):
                return {"success": False, "message": "Access denied"}
            
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            if not self.app.auth:
                error_message = "Authentication service is not available"
                if is_ajax:
                    return {"success": False, "message": error_message}
                else:
                    return RedirectResponse(url="/admin/clubs?error=auth_not_available", status_code=302)
            
            try:
                form = await request.form()
                club_id = form.get("club_id", "").strip()
                email = form.get("email", "").strip()
                
                # Validate input
                if not club_id or not email:
                    error_message = "Both club ID and email are required"
                    if is_ajax:
                        return {"success": False, "message": error_message}
                    else:
                        return RedirectResponse(url="/admin/clubs?error=missing_fields", status_code=302)
                
                # Validate email format
                if "@" not in email or "." not in email:
                    error_message = "Please enter a valid email address"
                    if is_ajax:
                        return {"success": False, "message": error_message}
                    else:
                        return RedirectResponse(url="/admin/clubs?error=invalid_email", status_code=302)
                
                # Convert club_id to int
                club_id = int(club_id)
                
                # Get club information
                clubs_df = self.app.auth.get_clubs()
                if clubs_df is None or clubs_df.empty:
                    error_message = "No clubs found in the system"
                    if is_ajax:
                        return {"success": False, "message": error_message}
                    else:
                        return RedirectResponse(url="/admin/clubs?error=no_clubs", status_code=302)
                
                # Find the specific club
                club_row = clubs_df[clubs_df['club_id'] == club_id]
                if club_row.empty:
                    error_message = "Club not found"
                    if is_ajax:
                        return {"success": False, "message": error_message}
                    else:
                        return RedirectResponse(url="/admin/clubs?error=club_not_found", status_code=302)
                
                club_name = club_row.iloc[0]['name']
                club_language = club_row.iloc[0]['language']
                
                # Create registration token
                token = self.app.auth.create_registration_token(club_id)
                
                if not token:
                    error_message = "Failed to create registration token"
                    if is_ajax:
                        return {"success": False, "message": error_message}
                    else:
                        return RedirectResponse(url="/admin/clubs?error=token_creation_failed", status_code=302)
                
                # Generate registration link
                base_url = getattr(self.app.auth, 'base_url', 'http://localhost:8000')
                registration_link = f"{base_url}/register/{token}?email={email}"
                
                # Send invitation email
                success = self.app.auth.send_registration_email(email, registration_link, club_name, club_language)
                
                if success:
                    success_message = f"Registration link sent successfully to {email}"
                    if is_ajax:
                        return {"success": True, "message": success_message}
                    else:
                        return RedirectResponse(url="/admin/clubs?success=invitation_sent", status_code=302)
                else:
                    error_message = "Failed to send email. Please try again."
                    if is_ajax:
                        return {"success": False, "message": error_message}
                    else:
                        return RedirectResponse(url="/admin/clubs?error=email_send_failed", status_code=302)
                
            except ValueError:
                error_message = "Invalid club ID"
                if is_ajax:
                    return {"success": False, "message": error_message}
                else:
                    return RedirectResponse(url="/admin/clubs?error=invalid_club_id", status_code=302)
            except Exception as e:
                print(f"Admin send registration link error: {e}")
                error_message = "An unexpected error occurred. Please try again."
                if is_ajax:
                    return {"success": False, "message": error_message}
                else:
                    return RedirectResponse(url="/admin/clubs?error=unexpected_error", status_code=302)
        
        @rt("/admin/view-club-dashboard/{club_id}")
        async def admin_view_club_dashboard(request):
            """Allow admin to view a club's dashboard."""
            if not self.app.require_admin(request):
                return RedirectResponse(url="/", status_code=302)
            
            club_id = int(request.path_params["club_id"])
            
            if not self.app.auth:
                return RedirectResponse(url="/admin/clubs?error=auth_not_available", status_code=302)
            
            # Get club information
            club_info = self.app.auth.db.fetch_one(
                "SELECT club_id, name, language FROM clubs WHERE club_id = :club_id",
                {"club_id": club_id}
            )
            
            if not club_info:
                return RedirectResponse(url="/admin/clubs?error=club_not_found", status_code=302)
            
            club_id, club_name, club_language = club_info
            
            # Get current admin user info
            admin_user = self.app.get_current_user(request)
            
            # Create simulated user info for the club dashboard
            simulated_user_info = {
                "user_id": admin_user["user_id"],  # Keep admin's user_id for admin context
                "club_id": club_id,
                "email": admin_user["email"],  # Keep admin's email
                "club_name": club_name,
                "is_admin_viewing": True  # Flag to indicate this is admin viewing
            }
            
            # Store request for translation context
            self.app.request = request
            
            # Use club's language for dashboard, but allow override via query parameter
            requested_lang = request.query_params.get("lang")
            if requested_lang in ["nl", "en"]:
                current_lang = requested_lang
            else:
                current_lang = club_language
            
            # Get dashboard translations for the club's language
            dashboard_translations = self.app.translations.get(current_lang, {}).get("dashboard", {})
            
            # Import DashboardLayout here to avoid circular imports
            from app.components.layouts.dashboard_layout import DashboardLayout
            
            dashboard_layout = DashboardLayout(dashboard_translations, self.app.versioned_url, current_lang)
            
            # Render dashboard with admin context
            return dashboard_layout.render(simulated_user_info)
        
        @rt("/admin/delete-user/{user_id}", methods=["POST"])
        async def admin_delete_user(request):
            """Delete a user."""
            if not self.app.require_admin(request):
                return RedirectResponse(url="/", status_code=302)
            
            user_id = int(request.path_params["user_id"])
            is_htmx = request.headers.get('HX-Request') == 'true'
            
            if not self.app.auth:
                if is_htmx:
                    return Div("Authentication service not available", cls="text-red-600 text-sm p-2")
                return RedirectResponse(url="/admin/users?error=auth_not_available", status_code=302)
            
            # Prevent admin from deleting themselves
            current_user = self.app.get_current_user(request)
            if current_user and current_user["user_id"] == user_id:
                if is_htmx:
                    return Div("Cannot delete yourself", cls="text-red-600 text-sm p-2")
                return RedirectResponse(url="/admin/users?error=cannot_delete_self", status_code=302)
            
            success, message = self.app.auth.delete_user(user_id)
            
            if success:
                if is_htmx:
                    # Return empty content to remove the row
                    return ""
                return RedirectResponse(url="/admin/users?success=user_deleted", status_code=302)
            else:
                if is_htmx:
                    return Div(f"Error: {message}", cls="text-red-600 text-sm p-2")
                return RedirectResponse(url=f"/admin/users?error={message}", status_code=302) 