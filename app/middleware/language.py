"""
Language Middleware

Contains language detection and setup middleware.
"""

from starlette.middleware.base import BaseHTTPMiddleware


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