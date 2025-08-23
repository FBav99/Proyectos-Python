#!/usr/bin/env python3
"""
Test script for OAuth configuration
Run this to verify your OAuth setup before using it in the main app
"""

import os
import sys
import requests
from urllib.parse import urlencode

def test_oauth_config():
    """Test OAuth configuration"""
    print("🔍 Testing OAuth Configuration...")
    
    # Check if secrets file exists
    secrets_path = ".streamlit/secrets.toml"
    if not os.path.exists(secrets_path):
        print("❌ .streamlit/secrets.toml not found")
        print("📝 Please create it from .streamlit/secrets.toml.example")
        return False
    
    # Check if oauth_configured is True
    try:
        import streamlit as st
        oauth_configured = st.secrets.get("oauth_configured", False)
        if not oauth_configured:
            print("⚠️ oauth_configured = False in secrets.toml")
            print("📝 Set it to True when you have configured OAuth")
            return False
    except Exception as e:
        print(f"❌ Error reading secrets: {e}")
        return False
    
    # Test Google OAuth config
    print("\n🔵 Testing Google OAuth...")
    google_config = st.secrets.get("google_oauth", {})
    if not google_config.get("client_id") or not google_config.get("client_secret"):
        print("❌ Google OAuth not configured")
        print("📝 Please configure google_oauth in secrets.toml")
    else:
        print("✅ Google OAuth configured")
    
    # Test Microsoft OAuth config
    print("\n🔴 Testing Microsoft OAuth...")
    microsoft_config = st.secrets.get("microsoft_oauth", {})
    if not microsoft_config.get("client_id") or not microsoft_config.get("client_secret"):
        print("❌ Microsoft OAuth not configured")
        print("📝 Please configure microsoft_oauth in secrets.toml")
    else:
        print("✅ Microsoft OAuth configured")
    
    # Test redirect URIs
    print("\n🌐 Testing Redirect URIs...")
    google_redirect = google_config.get("redirect_uri", "")
    microsoft_redirect = microsoft_config.get("redirect_uri", "")
    
    if "localhost:8501" in google_redirect or "localhost:8501" in microsoft_redirect:
        print("✅ Redirect URIs configured for localhost")
    else:
        print("⚠️ Redirect URIs may not be configured for localhost")
    
    return True

def test_oauth_endpoints():
    """Test OAuth endpoints are accessible"""
    print("\n🔗 Testing OAuth Endpoints...")
    
    endpoints = [
        ("Google OAuth", "https://accounts.google.com/o/oauth2/v2/auth"),
        ("Google Token", "https://oauth2.googleapis.com/token"),
        ("Microsoft OAuth", "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"),
        ("Microsoft Token", "https://login.microsoftonline.com/common/oauth2/v2.0/token")
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 400, 401]:  # These are expected
                print(f"✅ {name}: Accessible")
            else:
                print(f"⚠️ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {e}")

def main():
    """Main test function"""
    print("🚀 OAuth Configuration Test")
    print("=" * 40)
    
    # Test configuration
    config_ok = test_oauth_config()
    
    # Test endpoints
    test_oauth_endpoints()
    
    print("\n" + "=" * 40)
    if config_ok:
        print("✅ OAuth configuration test completed")
        print("📝 Next steps:")
        print("   1. Configure OAuth providers (Google/Microsoft)")
        print("   2. Update secrets.toml with your credentials")
        print("   3. Set oauth_configured = true")
        print("   4. Run: streamlit run Inicio.py")
    else:
        print("❌ OAuth configuration needs attention")
        print("📝 Please check the errors above and fix them")

if __name__ == "__main__":
    main()
