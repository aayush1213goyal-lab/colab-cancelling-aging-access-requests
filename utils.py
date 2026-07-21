import json
import os
import requests
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

def get_access_token():
    tenant = os.getenv("TENANT")
    domain = os.getenv("DOMAIN")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not tenant or not domain or not client_id or not client_secret:
        raise ValueError("TENANT, DOMAIN, CLIENT_ID, CLIENT_SECRET must be set in .env")

    token_url = f"https://{tenant}.api.{domain}.com/oauth/token"

    resp = requests.post(
        token_url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
        headers={"Accept": "application/json"},
        timeout=30,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Token request failed: {resp.status_code} {resp.text}")

    token_data = resp.json()
    access_token = token_data.get("access_token")
    if not access_token:
        raise RuntimeError("access_token missing in token response")
    return access_token



def get_request_approvals_list(access_token):
    # Load environment variables
    url = os.getenv("API_URL")
    
    if not url or not access_token:
        raise ValueError("API_URL and ACCESS_TOKEN must be set in environment variables")
    
    # Set up headers
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    

def get_requester_email(approval):
    if not approval:
        return None

    if approval.get("requesterEmail"):
        return approval["requesterEmail"]

    requester = approval.get("requester") or approval.get("requestedBy") or approval.get("requesterDetails")
    if isinstance(requester, dict):
        return requester.get("email") or requester.get("userEmail") or requester.get("mail")

    user = approval.get("user")
    if isinstance(user, dict):
        return user.get("email") or user.get("userEmail") or user.get("mail")

    return None


def send_closure_email(requester_email, approval_id, created_date):
    smtp_server = os.getenv("EMAIL_SMTP_SERVER")
    smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    from_email = os.getenv("EMAIL_FROM")

    if not all([smtp_server, username, password, from_email]):
        raise ValueError("EMAIL_SMTP_SERVER, EMAIL_USERNAME, EMAIL_PASSWORD, and EMAIL_FROM must be set in .env")
    if not requester_email:
        raise ValueError("requester_email is required to send a closure notification")

    subject = "Your access request has been closed"
    body = f"""
Hello,

Your access request with ID {approval_id}, created on {created_date}, has been automatically closed by the IAM Ops Team because it exceeded the configured age threshold.

If you believe this closure was in error, please submit a new access request.

Regards,
IAM Ops Team
"""

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = requester_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    if smtp_port == 465:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
    else:
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        server.starttls()

    with server:
        server.login(username, password)
        server.sendmail(from_email, requester_email, message.as_string())


def close_request_approval(access_token, approval_id):
    url = f"{os.getenv('API_URL1')}"
    
    if not url or not access_token:
        raise ValueError("API_URL1 and ACCESS_TOKEN must be set in environment variables")
    
    payload = json.dumps({
        "accessRequestIds": [approval_id],
        "executionStatus": "Terminated",
        "completionStatus": "Failure",
        "message": "This request has been closed by IAM Ops Team due to being older than the 30 days."
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f"Bearer {access_token}"
    }

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 202:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


    