"""
Routes Package

Contains all route handler classes.
"""

from .auth import AuthRoutes
from .public import PublicRoutes
from .dashboard import DashboardRoutes
from .admin import AdminRoutes

__all__ = [
    'AuthRoutes',
    'PublicRoutes',
    'DashboardRoutes',
    'AdminRoutes'
] 