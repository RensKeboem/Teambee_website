import hashlib
import secrets
import smtplib
import os
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Tuple, Dict
from sqlalchemy import text
import logging
import sys
import pandas as pd
from urllib.parse import quote

# Import local database manager
from database_manager import DatabaseManager

class AuthManager:
    """Handles user authentication, registration, and password reset functionality."""
    
    def __init__(self, db_manager: DatabaseManager = None, translations: dict = None):
        """Initialize the AuthManager with database connection and translations."""
        self.db = db_manager or DatabaseManager()
        self.logger = logging.getLogger(__name__)
        self.translations = translations or {}
        
        # Email configuration - detect provider based on email domain
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", self.email_user)
        
        # Auto-detect SMTP settings if not explicitly set
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT")) if os.getenv("SMTP_PORT") else None
        
        # Clean up expired registration data on startup
        try:
            self.cleanup_expired_registration_data()
        except Exception as e:
            self.logger.warning(f"Initial cleanup failed: {e}")
    
    def get_email_text(self, language: str, email_type: str, key: str, default: str = "") -> str:
        """Get translated email text for the given language, email type, and key."""
        try:
            return self.translations.get(language, {}).get("emails", {}).get(email_type, {}).get(key, default)
        except (KeyError, AttributeError):
            return default
    
    def _load_email_template(self, template_name: str, language: str = "en") -> Optional[str]:
        """Load email template from file."""
        try:
            template_path = os.path.join("public", "email-templates", template_name, f"{template_name}_{language}.html")
            
            # Check if the language-specific template exists
            if not os.path.exists(template_path):
                # Fall back to English if the requested language doesn't exist
                template_path = os.path.join("public", "email-templates", template_name, f"{template_name}_en.html")
                
                if not os.path.exists(template_path):
                    self.logger.warning(f"Email template not found: {template_path}")
                    return None
            
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            self.logger.error(f"Error loading email template {template_name}-{language}: {e}")
            return None
    
    def _get_versioned_url(self, path: str) -> str:
        """Generate versioned URL for static assets, similar to main.py implementation."""
        if path.startswith("/static/"):
            # Get file-specific version based on modification time
            file_path = path.replace("/static/", "public/")
            
            try:
                # Use last modification time for the file
                if os.path.exists(file_path):
                    version = str(int(os.path.getmtime(file_path)))
                else:
                    # Fallback to timestamp if file doesn't exist
                    import time
                    version = str(int(time.time()))
            except:
                # Fallback to timestamp
                import time
                version = str(int(time.time()))
            
            # URL encode the path to handle spaces and special characters
            encoded_path = quote(path, safe='/:?=&')
            return f"{encoded_path}?v={version}"
        else:
            return path
    
    def _process_email_template(self, template_content: str, placeholders: dict) -> str:
        """Process email template by replacing placeholders."""
        try:
            processed_content = template_content
            
            # Get base URL from environment
            base_url = os.getenv('BASE_URL', 'http://localhost:8000')
            
            # Replace image sources with actual asset URLs
            image_replacements = {
                'src="images/image-1.png"': f'src="{base_url}{self._get_versioned_url("/static/assets/Teambee logo donker.png")}"',
                'src="images/image-2.png"': f'src="{base_url}{self._get_versioned_url("/static/assets/password-reset.svg")}"',
                'src="images/image-3.png"': f'src="{base_url}{self._get_versioned_url("/static/assets/facebook-round.png")}"',
                'src="images/image-4.png"': f'src="{base_url}{self._get_versioned_url("/static/assets/instagram-round.png")}"',
                'src="images/image-5.png"': f'src="{base_url}{self._get_versioned_url("/static/assets/linkedin-round.png")}"'
            }
            
            # Replace image sources
            for old_src, new_src in image_replacements.items():
                processed_content = processed_content.replace(old_src, new_src)
            
            # Replace button href if it exists (for both password reset and registration links)
            if 'reset_link' in placeholders:
                reset_link = placeholders['reset_link']
                # Replace empty href in button with actual reset link
                processed_content = processed_content.replace('href=""', f'href="{reset_link}"')
            elif 'registration_link' in placeholders:
                registration_link = placeholders['registration_link']
                # Replace empty href in button with actual registration link
                processed_content = processed_content.replace('href=""', f'href="{registration_link}"')
            
            # Replace all other placeholders
            for key, value in placeholders.items():
                placeholder = f"{{{key}}}"
                processed_content = processed_content.replace(placeholder, str(value))
                
            return processed_content
        except Exception as e:
            self.logger.error(f"Error processing email template: {e}")
            return template_content
        
    def _hash_password(self, password: str, salt: str = None) -> Tuple[str, str]:
        """Hash password with salt."""
        if salt is None:
            salt = secrets.token_hex(32)
        
        # Combine password and salt
        password_salt = password.encode('utf-8') + salt.encode('utf-8')
        
        # Hash using SHA-256
        password_hash = hashlib.sha256(password_salt).hexdigest()
        
        return password_hash, salt
    
    def _verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Verify password against stored hash."""
        computed_hash, _ = self._hash_password(password, salt)
        return computed_hash == stored_hash
    
    def _generate_token(self, length: int = 32) -> str:
        """Generate a secure random token."""
        return secrets.token_urlsafe(length)
    
    def cleanup_expired_registration_data(self) -> int:
        """Clean up expired registration tokens and temporary users."""
        try:
            cleaned_count = 0
            
            with self.db.engine.connect() as conn:
                # First, get all expired registration tokens with their temporary users
                expired_data = conn.execute(
                    text("""
                        SELECT pr.user_id, pr.token, u.email
                        FROM password_resets pr
                        JOIN users u ON pr.user_id = u.user_id
                        WHERE pr.expires_at < NOW()
                        AND u.email LIKE 'registration_token_%@temp.teambee.internal'
                        AND pr.used_at IS NULL
                    """)
                ).fetchall()
                
                if expired_data:
                    # Delete expired temporary users
                    user_ids = [row[0] for row in expired_data]
                    tokens = [row[1] for row in expired_data]
                    
                    # Delete temporary users
                    for user_id in user_ids:
                        conn.execute(
                            text("DELETE FROM users WHERE user_id = :user_id"),
                            {"user_id": user_id}
                        )
                    
                    # Delete expired password reset entries
                    for token in tokens:
                        conn.execute(
                            text("DELETE FROM password_resets WHERE token = :token"),
                            {"token": token}
                        )
                    
                    cleaned_count = len(expired_data)
                
                # Also clean up old used registration tokens (older than 7 days)
                old_used_data = conn.execute(
                    text("""
                        DELETE pr FROM password_resets pr
                        JOIN users u ON pr.user_id = u.user_id
                        WHERE pr.used_at IS NOT NULL
                        AND pr.used_at < DATE_SUB(NOW(), INTERVAL 7 DAY)
                        AND u.email LIKE 'registration_token_%@temp.teambee.internal'
                    """)
                )
                
                conn.commit()
                
            if cleaned_count > 0:
                self.logger.info(f"Cleaned up {cleaned_count} expired registration tokens and temporary users")
                
            return cleaned_count
            
        except Exception as e:
            self.logger.error(f"Error cleaning up expired registration data: {e}")
            return 0
    
    def create_user(self, email: str, password: str, club_id: int = None) -> Tuple[bool, str]:
        """Create a new user in the database."""
        try:
            # Check if user already exists with this email
            existing_user = self.db.fetch_one(
                "SELECT user_id FROM users WHERE email = :email",
                {"email": email}
            )
            
            if existing_user:
                return False, "User with this email already exists"
            
            # Check if club exists (only if club_id is provided)
            if club_id is not None:
                club = self.db.fetch_one(
                    "SELECT club_id FROM clubs WHERE club_id = :club_id",
                    {"club_id": club_id}
                )
                
                if not club:
                    return False, "Invalid club ID"
                
                # Check if there's a temporary registration user for this club that we can replace
                temp_user = self.db.fetch_one(
                    """SELECT user_id, email FROM users 
                       WHERE club_id = :club_id 
                       AND email LIKE 'registration_token_%@temp.teambee.internal'""",
                    {"club_id": club_id}
                )
                
                if temp_user:
                    user_id, existing_email = temp_user
                    
                    # This is a temporary user, we can replace it
                    # Hash password
                    password_hash, salt = self._hash_password(password)
                    
                    # Update the temporary user with real user data
                    with self.db.engine.connect() as conn:
                        conn.execute(
                            text("""
                                UPDATE users 
                                SET email = :email, password_hash = :password_hash, salt = :salt, 
                                    failed_login_attempts = 0, account_locked_until = NULL
                                WHERE user_id = :user_id
                            """),
                            {
                                "email": email,
                                "password_hash": password_hash,
                                "salt": salt,
                                "user_id": user_id
                            }
                        )
                        conn.commit()
                    
                    return True, "User created successfully"
                # If no temporary user exists, we'll create a new user (multiple users per club now allowed)
            
            # Hash password
            password_hash, salt = self._hash_password(password)
            
            # Insert new user
            with self.db.engine.connect() as conn:
                conn.execute(
                    text("""
                        INSERT INTO users (club_id, email, password_hash, salt)
                        VALUES (:club_id, :email, :password_hash, :salt)
                    """),
                    {
                        "club_id": club_id,
                        "email": email,
                        "password_hash": password_hash,
                        "salt": salt
                    }
                )
                conn.commit()
            
            return True, "User created successfully"
            
        except Exception as e:
            self.logger.error(f"Error creating user: {e}")
            return False, f"Error creating user: {str(e)}"
    
    def create_admin(self, email: str, password: str) -> Tuple[bool, str]:
        """Create an admin user (club_id = NULL)."""
        return self.create_user(email, password, club_id=None)
    
    def authenticate_user(self, email: str, password: str) -> Tuple[bool, Optional[Dict], str]:
        """Authenticate user login."""
        try:
            # Get user data
            user_data = self.db.fetch_one(
                """
                SELECT u.user_id, u.club_id, u.email, u.password_hash, u.salt, 
                       u.failed_login_attempts, u.account_locked_until, c.name as club_name
                FROM users u
                LEFT JOIN clubs c ON u.club_id = c.club_id
                WHERE u.email = :email
                """,
                {"email": email}
            )
            
            if not user_data:
                return False, None, "Invalid email or password"
            
            user_id, club_id, user_email, stored_hash, salt, failed_attempts, locked_until, club_name = user_data
            
            # Check if account is locked
            if locked_until and datetime.now() < locked_until:
                return False, None, f"Account is locked until {locked_until}"
            
            # Verify password
            if not self._verify_password(password, stored_hash, salt):
                # Increment failed attempts
                new_failed_attempts = failed_attempts + 1
                lock_until = None
                
                # Lock account after 10 failed attempts for 30 minutes
                if new_failed_attempts >= 10:
                    lock_until = datetime.now() + timedelta(minutes=30)
                
                with self.db.engine.connect() as conn:
                    conn.execute(
                        text("""
                            UPDATE users 
                            SET failed_login_attempts = :attempts, 
                                account_locked_until = :lock_until
                            WHERE user_id = :user_id
                        """),
                        {
                            "attempts": new_failed_attempts,
                            "lock_until": lock_until,
                            "user_id": user_id
                        }
                    )
                    conn.commit()
                
                return False, None, "Invalid email or password"
            
            # Reset failed attempts and update last login
            with self.db.engine.connect() as conn:
                conn.execute(
                    text("""
                        UPDATE users 
                        SET failed_login_attempts = 0, 
                            account_locked_until = NULL,
                            last_login = NOW()
                        WHERE user_id = :user_id
                    """),
                    {"user_id": user_id}
                )
                conn.commit()
            
            # Return user info
            user_info = {
                "user_id": user_id,
                "club_id": club_id,
                "email": user_email,
                "club_name": club_name
            }
            
            return True, user_info, "Login successful"
            
        except Exception as e:
            self.logger.error(f"Error authenticating user: {e}")
            return False, None, f"Authentication error: {str(e)}"
    
    def initiate_password_reset(self, email: str, language: str = "nl") -> Tuple[bool, str]:
        """Initiate password reset by sending email with reset link."""
        try:
            # Check if user exists
            user_data = self.db.fetch_one(
                "SELECT user_id, email FROM users WHERE email = :email",
                {"email": email}
            )
            
            if not user_data:
                # Don't reveal that email doesn't exist
                return True, "If the email exists in our system, a reset link has been sent"
            
            user_id, user_email = user_data
            
            # Generate reset token
            token = self._generate_token(32)
            expires_at = datetime.now() + timedelta(hours=1)  # Token expires in 1 hour
            
            # Store reset token
            with self.db.engine.connect() as conn:
                conn.execute(
                    text("""
                        INSERT INTO password_resets (user_id, token, expires_at, language)
                        VALUES (:user_id, :token, :expires_at, :language)
                    """),
                    {
                        "user_id": user_id,
                        "token": token,
                        "expires_at": expires_at,
                        "language": language
                    }
                )
                conn.commit()
            
            # Send reset email
            reset_link = f"{os.getenv('BASE_URL', 'http://localhost:8000')}/reset-password/{token}"
            success = self.send_password_reset_email(user_email, reset_link, language)
            
            if success:
                return True, "If the email exists in our system, a reset link has been sent"
            else:
                return False, "Error sending reset email"
                
        except Exception as e:
            self.logger.error(f"Error initiating password reset: {e}")
            return False, "Error processing password reset request"
    
    def reset_password(self, token: str, new_password: str) -> Tuple[bool, str]:
        """Reset password using token."""
        try:
            # Verify token
            reset_data = self.db.fetch_one(
                """
                SELECT pr.user_id, pr.expires_at, pr.used_at, pr.language
                FROM password_resets pr
                WHERE pr.token = :token
                """,
                {"token": token}
            )
            
            if not reset_data:
                return False, "Invalid or expired reset token"
            
            user_id, expires_at, used_at, language = reset_data
            
            # Check if token is expired
            if datetime.now() > expires_at:
                return False, "Reset token has expired"
            
            # Check if token was already used
            if used_at:
                return False, "Reset token has already been used"
            
            # Validate new password length
            if len(new_password) < 8:
                return False, "New password must be at least 8 characters long"
            
            # Get current password to check if new password is the same
            user_data = self.db.fetch_one(
                "SELECT password_hash, salt FROM users WHERE user_id = :user_id",
                {"user_id": user_id}
            )
            
            if not user_data:
                return False, "User not found"
            
            current_password_hash, current_salt = user_data
            
            # Check if new password is the same as current password
            if self._verify_password(new_password, current_password_hash, current_salt):
                return False, "New password cannot be the same as your current password"
            
            # Hash new password
            password_hash, salt = self._hash_password(new_password)
            
            # Update password and mark token as used
            with self.db.engine.connect() as conn:
                # Update password
                conn.execute(
                    text("""
                        UPDATE users 
                        SET password_hash = :password_hash, 
                            salt = :salt,
                            failed_login_attempts = 0,
                            account_locked_until = NULL
                        WHERE user_id = :user_id
                    """),
                    {
                        "password_hash": password_hash,
                        "salt": salt,
                        "user_id": user_id
                    }
                )
                
                # Mark token as used
                conn.execute(
                    text("""
                        UPDATE password_resets 
                        SET used_at = NOW()
                        WHERE token = :token
                    """),
                    {"token": token}
                )
                
                conn.commit()
            
            return True, "Password reset successfully"
            
        except Exception as e:
            self.logger.error(f"Error resetting password: {e}")
            return False, f"Error resetting password: {str(e)}"
    
    def get_reset_token_language(self, token: str) -> Optional[str]:
        """Get the language for a password reset token."""
        try:
            reset_data = self.db.fetch_one(
                "SELECT language FROM password_resets WHERE token = :token",
                {"token": token}
            )
            
            if reset_data:
                return reset_data[0] or "nl"  # Default to Dutch if language is None
            return "nl"  # Default fallback
            
        except Exception as e:
            self.logger.error(f"Error getting reset token language: {e}")
            return "nl"  # Default fallback
    
    def create_registration_token(self, club_id: int, expires_hours: int = 24) -> Optional[str]:
        """Create a single-use registration token for a specific club."""
        try:
            # Clean up expired registration data first
            self.cleanup_expired_registration_data()
            
            # Check if club exists
            club = self.db.fetch_one(
                "SELECT club_id FROM clubs WHERE club_id = :club_id",
                {"club_id": club_id}
            )
            
            if not club:
                self.logger.error(f"Club with ID {club_id} not found")
                return None
            
            # Generate token and store it
            # We'll use a simple file-based approach or create a dummy user to store against
            token = self._generate_token(32)
            expires_at = datetime.now() + timedelta(hours=expires_hours)
            
            # Create a temporary user entry to store the registration token against
            # We'll use a special email format to identify registration tokens
            temp_email = f"registration_token_{club_id}_{token}@temp.teambee.internal"
            
            with self.db.engine.connect() as conn:
                # First, create a temporary user entry
                conn.execute(
                    text("""
                        INSERT INTO users (club_id, email, password_hash, salt)
                        VALUES (:club_id, :email, 'temp', 'temp')
                        ON DUPLICATE KEY UPDATE email = :email
                    """),
                    {
                        "club_id": club_id,
                        "email": temp_email
                    }
                )
                
                # Get the user_id of the temporary user
                temp_user = conn.execute(
                    text("SELECT user_id FROM users WHERE email = :email"),
                    {"email": temp_email}
                ).fetchone()
                
                if not temp_user:
                    self.logger.error("Failed to create temporary user for registration token")
                    return None
                
                temp_user_id = temp_user[0]
                
                # Store registration token
                conn.execute(
                    text("""
                        INSERT INTO password_resets (user_id, token, expires_at)
                        VALUES (:user_id, :token, :expires_at)
                    """),
                    {
                        "user_id": temp_user_id,
                        "token": token,
                        "expires_at": expires_at
                    }
                )
                conn.commit()
            
            return token
            
        except Exception as e:
            self.logger.error(f"Error creating registration token: {e}")
            return None
    
    def validate_registration_token(self, token: str) -> Optional[int]:
        """Validate registration token and return club_id."""
        try:
            # Clean up expired registration data periodically
            self.cleanup_expired_registration_data()
            
            reset_data = self.db.fetch_one(
                """
                SELECT pr.user_id, pr.expires_at, pr.used_at, u.club_id, u.email
                FROM password_resets pr
                JOIN users u ON pr.user_id = u.user_id
                WHERE pr.token = :token
                """,
                {"token": token}
            )
            
            if not reset_data:
                return None
            
            user_id, expires_at, used_at, club_id, email = reset_data
            
            # Check if this is a registration token (identified by the special email format)
            if not email.startswith("registration_token_") or not email.endswith("@temp.teambee.internal"):
                self.logger.error(f"Token is not a registration token: {email}")
                return None
            
            # Check if token is expired
            if datetime.now() > expires_at:
                return None
            
            # Check if token was already used
            if used_at:
                return None
            
            return club_id
            
        except Exception as e:
            self.logger.error(f"Error validating registration token: {e}")
            return None
    
    def complete_registration(self, token: str, email: str, password: str) -> Tuple[bool, str]:
        """Complete user registration using token."""
        try:
            # Validate token and get club_id
            club_id = self.validate_registration_token(token)
            
            if not club_id:
                return False, "Invalid or expired registration token"
            
            # Create user
            success, message = self.create_user(email, password, club_id)
            
            if success:
                # Mark token as used and clean up temporary user
                with self.db.engine.connect() as conn:
                    # Mark token as used
                    conn.execute(
                        text("""
                            UPDATE password_resets 
                            SET used_at = NOW()
                            WHERE token = :token
                        """),
                        {"token": token}
                    )
                    
                    # Delete the temporary user that was created for this registration token
                    conn.execute(
                        text("""
                            DELETE u FROM users u
                            JOIN password_resets pr ON u.user_id = pr.user_id
                            WHERE pr.token = :token 
                            AND u.email LIKE 'registration_token_%@temp.teambee.internal'
                        """),
                        {"token": token}
                    )
                    
                    conn.commit()
            
            return success, message
            
        except Exception as e:
            self.logger.error(f"Error completing registration: {e}")
            return False, f"Error completing registration: {str(e)}"
    
    def get_clubs(self):
        """Get all clubs for admin purposes."""
        try:
            return self.db.fetch_dataframe("SELECT club_id, name, system_prefix, language, created_at FROM clubs ORDER BY club_id ASC")
        except Exception as e:
            self.logger.error(f"Error fetching clubs: {e}")
            return None
    
    def create_club(self, name: str, system_prefix: str, language: str) -> Tuple[bool, str, Optional[int]]:
        """Create a new club and return club_id if successful."""
        try:
            # Validate language
            if language not in ['nl', 'en']:
                return False, "Language must be 'nl' or 'en'", None
            
            # Check if club name already exists
            existing_club = self.db.fetch_one(
                "SELECT club_id FROM clubs WHERE name = :name",
                {"name": name}
            )
            
            if existing_club:
                return False, "Club with this name already exists", None
            
            # Insert club
            with self.db.engine.connect() as conn:
                result = conn.execute(
                    text("""
                        INSERT INTO clubs (name, system_prefix, language)
                        VALUES (:name, :system_prefix, :language)
                    """),
                    {
                        "name": name,
                        "system_prefix": system_prefix,
                        "language": language
                    }
                )
                club_id = result.lastrowid
                conn.commit()
            
            return True, "Club created successfully", club_id
            
        except Exception as e:
            self.logger.error(f"Error creating club: {e}")
            return False, f"Error creating club: {str(e)}", None
    
    def get_all_users(self):
        """Get all users with their club information."""
        try:
            return self.db.fetch_dataframe("""
                SELECT u.user_id, u.email, u.club_id, c.name as club_name, 
                       u.last_login, u.created_at,
                       CASE WHEN u.club_id IS NULL THEN 'Admin' ELSE 'User' END as user_type
                FROM users u
                LEFT JOIN clubs c ON u.club_id = c.club_id
                WHERE u.email NOT LIKE 'registration_token_%@temp.teambee.internal'
                ORDER BY u.user_id ASC
            """)
        except Exception as e:
            self.logger.error(f"Error fetching users: {e}")
            return None
    
    def is_admin(self, user_info: dict) -> bool:
        """Check if user is an admin (has no club_id)."""
        return user_info.get("club_id") is None
    
    def delete_user(self, user_id: int) -> Tuple[bool, str]:
        """Delete a user from the database."""
        try:
            # Check if user exists
            user = self.db.fetch_one(
                "SELECT user_id, email, club_id FROM users WHERE user_id = :user_id",
                {"user_id": user_id}
            )
            
            if not user:
                return False, "user_not_found"
            
            # Delete the user
            with self.db.engine.connect() as conn:
                conn.execute(
                    text("DELETE FROM users WHERE user_id = :user_id"),
                    {"user_id": user_id}
                )
                conn.commit()
            
            return True, "User deleted successfully"
            
        except Exception as e:
            self.logger.error(f"Error deleting user {user_id}: {e}")
            return False, "delete_error"
    
    def update_user_password(self, user_id: int, current_password: str, new_password: str) -> Tuple[bool, str]:
        """Update user password after verifying current password."""
        try:
            # Get user data
            user_data = self.db.fetch_one(
                "SELECT user_id, email, password_hash, salt FROM users WHERE user_id = :user_id",
                {"user_id": user_id}
            )
            
            if not user_data:
                return False, "User not found"
            
            user_id_db, email, stored_hash, salt = user_data
            
            # Verify current password
            if not self._verify_password(current_password, stored_hash, salt):
                return False, "Current password is incorrect"
            
            # Validate new password
            if len(new_password) < 8:
                return False, "New password must be at least 8 characters long"
            
            # Check if new password is the same as current password
            if self._verify_password(new_password, stored_hash, salt):
                return False, "New password cannot be the same as your current password"
            
            # Hash new password
            new_password_hash, new_salt = self._hash_password(new_password)
            
            # Update password in database
            with self.db.engine.connect() as conn:
                conn.execute(
                    text("""
                        UPDATE users 
                        SET password_hash = :password_hash, salt = :salt
                        WHERE user_id = :user_id
                    """),
                    {
                        "password_hash": new_password_hash,
                        "salt": new_salt,
                        "user_id": user_id
                    }
                )
                conn.commit()
            
            return True, "Password updated successfully"
            
        except Exception as e:
            self.logger.error(f"Error updating password for user {user_id}: {e}")
            return False, "Error updating password"
    
    def invite_user_to_club(self, club_id: int, email: str, inviter_email: str) -> Tuple[bool, str]:
        """Create an invitation for a new user to join a club."""
        try:
            # Validate email
            if not email or "@" not in email:
                return False, "Invalid email address"
            
            # Check if user already exists
            existing_user = self.db.fetch_one(
                "SELECT user_id FROM users WHERE email = :email",
                {"email": email}
            )
            
            if existing_user:
                return False, "A user with this email already exists"
            
            # Check if club exists
            club = self.db.fetch_one(
                "SELECT club_id, name, language FROM clubs WHERE club_id = :club_id",
                {"club_id": club_id}
            )
            
            if not club:
                return False, "Club not found"
            
            club_id_db, club_name, club_language = club
            
            # Create registration token
            token = self.create_registration_token(club_id)
            
            if not token:
                return False, "Failed to create registration token"
            
            # Send invitation email
            registration_link = f"{os.getenv('BASE_URL', 'http://localhost:8000')}/register/{token}?email={email}"
            
            success = self.send_invitation_email(email, registration_link, club_name, inviter_email, club_language)
            
            if success:
                return True, f"Invitation sent to {email}"
            else:
                return False, "Failed to send invitation email"
            
        except Exception as e:
            self.logger.error(f"Error inviting user to club: {e}")
            return False, "Error sending invitation"
    
    def send_password_reset_email(self, to_email: str, reset_link: str, language: str = "nl") -> bool:
        """Send password reset email using HTML template."""
        try:
            if not all([self.email_user, self.email_password, self.from_email]):
                self.logger.warning("Email configuration incomplete, cannot send reset email")
                return False
            
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = self.get_email_text(language, "password_reset", "subject", "Teambee - Password Reset Request")
            
            # Plain text version
            text_body = self.get_email_text(language, "password_reset", "plain_text", 
                "Dear User,\n\nYou requested a password reset for your Teambee account.\n\nPlease click the following link to reset your password:\n{reset_link}\n\nThis link will expire in 1 hour.\n\nIf you did not request this password reset, please ignore this email.\n\nBest regards,\nThe Teambee Team").format(reset_link=reset_link)
            
            # Try to load HTML template
            html_template = self._load_email_template("password_reset", language)
            
            if html_template:
                # Use the template and replace placeholders
                placeholders = {
                    "reset_link": reset_link,
                    "link": reset_link
                }
                html_body = self._process_email_template(html_template, placeholders)
            else:
                # If template loading fails, return False to prevent sending malformed emails
                self.logger.error(f"Could not load password reset template for {language}, email not sent")
                return False
            
            # Attach both parts
            text_part = MIMEText(text_body, 'plain')
            html_part = MIMEText(html_body, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending password reset email: {e}")
            return False
    
    def send_registration_email(self, to_email: str, registration_link: str, club_name: str, language: str = "nl") -> bool:
        """Send registration invitation email using HTML template."""
        try:
            if not all([self.email_user, self.email_password, self.from_email]):
                self.logger.warning("Email configuration incomplete, cannot send registration email")
                return False

            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = self.get_email_text(language, "registration", "subject", "Teambee - Registration Invitation for {club_name}").format(club_name=club_name)

            # Plain text version
            text_body = self.get_email_text(language, "registration", "plain_text", 
                "Dear User,\n\nYou have been invited to create an account for {club_name} on Teambee.\n\nPlease click the following link to complete your registration:\n{registration_link}\n\nThis link will expire in 24 hours.\n\nBest regards,\nThe Teambee Team").format(club_name=club_name, registration_link=registration_link)

            # Try to load HTML template
            html_template = self._load_email_template("account_creation", language)
            
            if html_template:
                # Use the template and replace placeholders
                placeholders = {
                    "registration_link": registration_link,
                    "link": registration_link
                }
                html_body = self._process_email_template(html_template, placeholders)
            else:
                # If template loading fails, return False to prevent sending malformed emails
                self.logger.error(f"Could not load account creation template for {language}, email not sent")
                return False

            # Attach both parts
            text_part = MIMEText(text_body, 'plain')
            html_part = MIMEText(html_body, 'html')

            msg.attach(text_part)
            msg.attach(html_part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)

            return True

        except Exception as e:
            self.logger.error(f"Error sending registration email: {e}")
            return False
    
    def send_invitation_email(self, to_email: str, registration_link: str, club_name: str, inviter_email: str, language: str = "nl") -> bool:
        """Send user invitation email using HTML template."""
        try:
            if not all([self.email_user, self.email_password, self.from_email]):
                self.logger.warning("Email configuration incomplete, cannot send invitation email")
                return False
            
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = self.get_email_text(language, "invitation", "subject", "Teambee - You're invited to join {club_name}").format(club_name=club_name)
            
            # Plain text version
            text_body = self.get_email_text(language, "invitation", "plain_text", 
                "Dear User,\n\nYou have been invited by {inviter_email} to join {club_name} on Teambee.\n\nPlease click the following link to create your account:\n{registration_link}\n\nThis invitation will expire in 24 hours.\n\nBest regards,\nThe Teambee Team").format(inviter_email=inviter_email, club_name=club_name, registration_link=registration_link)
            
            # Try to load HTML template
            html_template = self._load_email_template("account_creation", language)
            
            if html_template:
                # Use the template and replace placeholders
                placeholders = {
                    "registration_link": registration_link,
                    "link": registration_link
                }
                html_body = self._process_email_template(html_template, placeholders)
            else:
                # If template loading fails, return False to prevent sending malformed emails
                self.logger.error(f"Could not load account creation template for {language}, email not sent")
                return False
            
            # Attach both parts
            text_part = MIMEText(text_body, 'plain')
            html_part = MIMEText(html_body, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending invitation email: {e}")
            return False 