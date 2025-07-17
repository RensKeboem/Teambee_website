"""
Session Service

Handles user session management functionality.
"""

from typing import Optional, Dict


class SessionService:
    """Service for managing user sessions."""
    
    @staticmethod
    def login_user(request, user_info: Dict) -> None:
        """Store user information in session."""
        request.session["user_id"] = user_info["user_id"]
        request.session["club_id"] = user_info["club_id"]
        request.session["email"] = user_info["email"]
        request.session["club_name"] = user_info.get("club_name")
    
    @staticmethod
    def logout_user(request) -> None:
        """Clear user session."""
        session_keys = ["user_id", "club_id", "email", "club_name"]
        for key in session_keys:
            request.session.pop(key, None)
    
    @staticmethod
    def get_current_user(request) -> Optional[Dict]:
        """Get current user information from session."""
        if "user_id" in request.session:
            return {
                "user_id": request.session["user_id"],
                "club_id": request.session.get("club_id"),
                "email": request.session["email"],
                "club_name": request.session.get("club_name")
            }
        return None
    
    @staticmethod
    def is_authenticated(request) -> bool:
        """Check if user is authenticated."""
        return "user_id" in request.session
    
    @staticmethod
    def require_admin(request, auth_service) -> bool:
        """Check if user is admin and authenticated."""
        if not SessionService.is_authenticated(request):
            return False
        
        user_info = SessionService.get_current_user(request)
        if not user_info or not auth_service:
            return False
        
        return auth_service.is_admin(user_info) 