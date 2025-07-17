"""
Helper Utilities

Contains common utility functions used throughout the application.
"""

import os
import time
from urllib.parse import quote


def get_versioned_url(path: str, version: str = None) -> str:
    """
    Generate versioned URL for static assets to handle cache busting.
    
    Args:
        path: The asset path
        version: Optional version string, will generate from file mtime if None
        
    Returns:
        Versioned URL string
    """
    if path.startswith("/static/"):
        # Get file-specific version based on modification time
        file_path = path.replace("/static/", "public/")
        
        if version is None:
            try:
                # Use last modification time for the file
                if os.path.exists(file_path):
                    version = str(int(os.path.getmtime(file_path)))
                else:
                    # Fallback to timestamp if file doesn't exist
                    version = str(int(time.time()))
            except:
                # Fallback to timestamp
                version = str(int(time.time()))
        
        # URL encode the path to handle spaces and special characters
        encoded_path = quote(path, safe='/:?=&')
        return f"{encoded_path}?v={version}"
    else:
        return path


def get_current_language_from_path(path: str) -> str:
    """
    Determine language from URL path.
    
    Args:
        path: The URL path
        
    Returns:
        Language code ('en' or 'nl')
    """
    return "en" if path.startswith("/en") else "nl"


def get_language_root_url(language: str) -> str:
    """
    Get the root URL for the specified language.
    
    Args:
        language: Language code ('en' or 'nl')
        
    Returns:
        Root URL for the language
    """
    return "/en" if language == "en" else "/"


def get_translated_text(translations: dict, language: str, section: str, key: str, default: str = "") -> str:
    """
    Get translated text for the given language, section, and key.
    
    Args:
        translations: Translation dictionary
        language: Language code
        section: Translation section
        key: Translation key
        default: Default value if translation not found
        
    Returns:
        Translated text or default value
    """
    try:
        return translations.get(language, {}).get(section, {}).get(key, default)
    except (KeyError, AttributeError):
        return default


def generate_meta_tags(title: str = "Teambee", description: str = None, url: str = None) -> list:
    """
    Generate standard meta tags for SEO.
    
    Args:
        title: Page title
        description: Page description
        url: Page URL
        
    Returns:
        List of meta tag elements
    """
    from fasthtml.common import Meta, Link
    
    default_description = "Teambee helps premium high-end fitness clubs transform members into loyal ambassadors through personalized attention at scale."
    
    meta_tags = [
        Meta(name="description", content=description or default_description),
        Meta(name="keywords", content="fitness clubs, member retention, loyalty, personalized experience, teambee"),
        Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        Meta(property="og:title", content=title),
        Meta(property="og:description", content=description or default_description),
        Meta(property="og:type", content="website"),
    ]
    
    if url:
        meta_tags.append(Meta(property="og:url", content=url))
    
    # Language alternates
    meta_tags.extend([
        Link(rel="alternate", hreflang="nl", href="https://teambee.fit/"),
        Link(rel="alternate", hreflang="en", href="https://teambee.fit/en"),
        Link(rel="alternate", hreflang="x-default", href="https://teambee.fit/"),
    ])
    
    return meta_tags


def generate_script_tags(versioned_url_func) -> list:
    """
    Generate standard script tags for the application.
    
    Args:
        versioned_url_func: Function to generate versioned URLs
        
    Returns:
        List of script tag elements
    """
    from fasthtml.common import Script
    
    return [
        Script(src=versioned_url_func("/static/js/shared-utils.js")),
        Script(src=versioned_url_func("/static/js/ui-enhancements.js")),
        Script(src=versioned_url_func("/static/js/popup-dropdown.js")),
        Script(src=versioned_url_func("/static/js/form-handlers.js")),
        Script(src=versioned_url_func("/static/js/carousel.js")),
        Script(src=versioned_url_func("/static/js/success-stories.js")),
        Script(src=versioned_url_func("/static/js/auto-open-success-stories.js")),
    ]


def create_error_response(message: str, is_ajax: bool = False, redirect_url: str = "/") -> dict:
    """
    Create standardized error response.
    
    Args:
        message: Error message
        is_ajax: Whether this is an AJAX request
        redirect_url: URL to redirect to if not AJAX
        
    Returns:
        Error response dictionary or redirect response
    """
    if is_ajax:
        return {"success": False, "message": message}
    else:
        from starlette.responses import RedirectResponse
        return RedirectResponse(url=f"{redirect_url}?error={message}", status_code=302)


def create_success_response(message: str, redirect_url: str, is_ajax: bool = False) -> dict:
    """
    Create standardized success response.
    
    Args:
        message: Success message
        redirect_url: URL to redirect to
        is_ajax: Whether this is an AJAX request
        
    Returns:
        Success response dictionary
    """
    if is_ajax:
        return {"success": True, "message": message, "redirect_url": redirect_url}
    else:
        from starlette.responses import RedirectResponse
        return RedirectResponse(url=redirect_url, status_code=302) 