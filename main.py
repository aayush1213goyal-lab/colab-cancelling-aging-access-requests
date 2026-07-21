from utils import (
    get_access_token,
    get_request_approvals_list,
    close_request_approval,
    get_requester_email,
    send_closure_email,
)
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()

def main():
    access_token = get_access_token()
    approvals_list = get_request_approvals_list(access_token)
    days_old = int(os.getenv("DAYS_OLD", "1"))
    print(f"Total approvals retrieved: {len(approvals_list)}")
    request_reject_list = []
    for approval in approvals_list:
        created_date = approval.get( 'requestCreated')
        if created_date:
            created_datetime = datetime.strptime(created_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            if created_datetime < datetime.utcnow() - timedelta(days=days_old):
                approval_id = approval.get('accessRequestId')
                requester_email = get_requester_email(approval)
                request_reject_list.append({
                    "Approval ID": approval_id,
                    "Created Date": created_date,
                    "Requester Email": requester_email,
                })
                print(f"Approval ID: {approval_id}, Created Date: {created_date}, Requester Email: {requester_email}")
                close_request_response = close_request_approval(access_token, approval_id)
                print(f"Close Request Response for Approval ID {approval_id}: {close_request_response}")
                if requester_email:
                    try:
                        send_closure_email(requester_email, approval_id, created_date)
                        print(f"Email sent to {requester_email} for Approval ID {approval_id}")
                    except Exception as email_error:
                        print(f"Failed to send email for Approval ID {approval_id}: {email_error}")
                else:
                    print(f"No requester email available for Approval ID {approval_id}")
    print(f"Number of approvals older than {days_old} days: {len(request_reject_list)}")
    

if __name__ == "__main__":
    main()