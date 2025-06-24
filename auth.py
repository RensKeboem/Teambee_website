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

# Import local database manager
from database_manager import DatabaseManager

class AuthManager:
    """Handles user authentication, registration, and password reset functionality."""
    
    def __init__(self, db_manager: DatabaseManager = None):
        """Initialize the AuthManager with database connection."""
        self.db = db_manager or DatabaseManager()
        self.logger = logging.getLogger(__name__)
        
        # Email configuration - detect provider based on email domain
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", self.email_user)
        
        # Auto-detect SMTP settings if not explicitly set
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT")) if os.getenv("SMTP_PORT") else None
        
        if not self.smtp_server or not self.smtp_port:
            self._auto_configure_smtp()
        
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
    
    def _auto_configure_smtp(self) -> None:
        """Auto-configure SMTP settings based on email domain."""
        if not self.email_user:
            self.logger.warning("EMAIL_USER not configured, cannot auto-detect SMTP settings")
            return
        
        domain = self.email_user.split('@')[-1].lower()
        
        # SMTP configurations for common email providers
        smtp_configs = {
            'gmail.com': ('smtp.gmail.com', 587),
            'googlemail.com': ('smtp.gmail.com', 587),
            'outlook.com': ('smtp-mail.outlook.com', 587),
            'hotmail.com': ('smtp-mail.outlook.com', 587),
            'live.com': ('smtp-mail.outlook.com', 587),
            'msn.com': ('smtp-mail.outlook.com', 587),
            'yahoo.com': ('smtp.mail.yahoo.com', 587),
            'yahoo.co.uk': ('smtp.mail.yahoo.com', 587),
            'icloud.com': ('smtp.mail.me.com', 587),
            'me.com': ('smtp.mail.me.com', 587),
            'mac.com': ('smtp.mail.me.com', 587),
        }
        
        if domain in smtp_configs:
            self.smtp_server, self.smtp_port = smtp_configs[domain]
            self.logger.info(f"Auto-configured SMTP for {domain}: {self.smtp_server}:{self.smtp_port}")
        else:
            # Default fallback
            self.smtp_server = "smtp.gmail.com"
            self.smtp_port = 587
            self.logger.warning(f"Unknown email domain {domain}, using Gmail defaults. Please set SMTP_SERVER and SMTP_PORT manually.")
    
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
                
                # Lock account after 5 failed attempts for 30 minutes
                if new_failed_attempts >= 5:
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
    
    def initiate_password_reset(self, email: str) -> Tuple[bool, str]:
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
                        INSERT INTO password_resets (user_id, token, expires_at)
                        VALUES (:user_id, :token, :expires_at)
                    """),
                    {
                        "user_id": user_id,
                        "token": token,
                        "expires_at": expires_at
                    }
                )
                conn.commit()
            
            # Send reset email
            reset_link = f"{os.getenv('BASE_URL', 'http://localhost:8000')}/reset-password/{token}"
            success = self._send_password_reset_email(user_email, reset_link)
            
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
                SELECT pr.user_id, pr.expires_at, pr.used_at
                FROM password_resets pr
                WHERE pr.token = :token
                """,
                {"token": token}
            )
            
            if not reset_data:
                return False, "Invalid or expired reset token"
            
            user_id, expires_at, used_at = reset_data
            
            # Check if token is expired
            if datetime.now() > expires_at:
                return False, "Reset token has expired"
            
            # Check if token was already used
            if used_at:
                return False, "Reset token has already been used"
            
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
    
    def create_registration_token(self, club_id: int, expires_hours: int = 24) -> Optional[str]:
        """Create a single-use registration token for a specific club."""
        try:
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
    
    def _send_password_reset_email(self, to_email: str, reset_link: str) -> bool:
        """Send password reset email."""
        try:
            if not all([self.email_user, self.email_password, self.from_email]):
                self.logger.warning("Email configuration incomplete, cannot send reset email")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = "Teambee - Password Reset Request"
            
            body = f"""
            Dear User,
            
            You requested a password reset for your Teambee account.
            
            Please click the following link to reset your password:
            {reset_link}
            
            This link will expire in 1 hour.
            
            If you did not request this password reset, please ignore this email.
            
            Best regards,
            The Teambee Team
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending password reset email: {e}")
            return False
    
    def send_registration_email(self, to_email: str, registration_link: str, club_name: str) -> bool:
        """Send registration invitation email."""
        try:
            if not all([self.email_user, self.email_password, self.from_email]):
                self.logger.warning("Email configuration incomplete, cannot send registration email")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = f"Teambee - Registration Invitation for {club_name}"
            
            body = f"""
            Dear User,
            
            You have been invited to create an account for {club_name} on Teambee.
            
            Please click the following link to complete your registration:
            {registration_link}
            
            This link will expire in 24 hours.
            
            Best regards,
            The Teambee Team
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending registration email: {e}")
            return False 