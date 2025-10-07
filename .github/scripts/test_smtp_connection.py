#!/usr/bin/env python3
"""
Test SMTP connection and credentials
"""
import sys
import os
import smtplib
from email.mime.text import MIMEText

def test_smtp_connection(host, port, username, password, use_tls=True, timeout=30):
    """Test SMTP connection"""
    print("=" * 70)
    print("  SMTP Connection Test")
    print("=" * 70)
    print()
    
    print(f"📮 Testing SMTP connection...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Username: {username}")
    print(f"   Use TLS: {use_tls}")
    print(f"   Timeout: {timeout}s")
    print()
    
    try:
        # Connect to SMTP server
        print("🔌 Connecting to SMTP server...")
        if use_tls:
            server = smtplib.SMTP(host, port, timeout=timeout)
            print("✅ Connection established")
            
            print("🔒 Starting TLS...")
            server.starttls()
            print("✅ TLS started")
        else:
            server = smtplib.SMTP_SSL(host, port, timeout=timeout)
            print("✅ SSL connection established")
        
        # Login
        print("🔑 Authenticating...")
        server.login(username, password)
        print("✅ Authentication successful")
        
        # Check server capabilities
        print("\n📋 Server capabilities:")
        for feature, params in server.esmtp_features.items():
            print(f"   - {feature}: {params}")
        
        # Close connection
        server.quit()
        print("\n✅ SMTP connection test PASSED")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ Authentication failed: {e}")
        print("   Check username and password")
        return False
    
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ Connection failed: {e}")
        print("   Check host and port")
        return False
    
    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP error: {e}")
        return False
    
    except TimeoutError:
        print(f"\n❌ Connection timeout")
        print("   Server might be unreachable or port blocked")
        return False
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test SMTP connection')
    parser.add_argument('--host', help='SMTP host')
    parser.add_argument('--port', type=int, help='SMTP port')
    parser.add_argument('--username', help='SMTP username')
    parser.add_argument('--password', help='SMTP password')
    parser.add_argument('--no-tls', action='store_true', help='Disable TLS')
    parser.add_argument('--timeout', type=int, default=30, help='Connection timeout')
    
    args = parser.parse_args()
    
    # Get from environment variables if not provided
    host = args.host or os.environ.get('SMTP_HOST')
    port = args.port or int(os.environ.get('SMTP_PORT', 587))
    username = args.username or os.environ.get('SMTP_USER')
    password = args.password or os.environ.get('SMTP_PASS')
    
    if not all([host, port, username, password]):
        print("❌ Missing SMTP credentials")
        print("\nProvide via arguments or environment variables:")
        print("  --host or SMTP_HOST")
        print("  --port or SMTP_PORT")
        print("  --username or SMTP_USER")
        print("  --password or SMTP_PASS")
        print("\nExample:")
        print("  python test_smtp_connection.py --host smtp.gmail.com --port 587 --username user@gmail.com --password 'secret'")
        print("\nOr with environment variables:")
        print("  export SMTP_HOST=smtp.gmail.com")
        print("  export SMTP_PORT=587")
        print("  export SMTP_USER=user@gmail.com")
        print("  export SMTP_PASS='secret'")
        print("  python test_smtp_connection.py")
        return 1
    
    success = test_smtp_connection(
        host=host,
        port=port,
        username=username,
        password=password,
        use_tls=not args.no_tls,
        timeout=args.timeout
    )
    
    print()
    print("=" * 70)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
