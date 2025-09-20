"""
Hackathon Interface Package

Quick start:
    from hackathon_interface import main

    client = main()
    # Use client for your hackathon project
"""

from .hackathon_example import main
from .setup_hackathon import setup_bim_portal

__all__ = ['main', 'setup_bim_portal']