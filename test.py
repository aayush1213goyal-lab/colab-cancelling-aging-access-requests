from utils import get_access_token, get_request_approvals_list, close_request_approval
from os import getenv
from dotenv import load_dotenv
load_dotenv()

def test_get_access_token():
    token = get_access_token()
    print("Access Token:", token)
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

def test_get_request_approvals_list():
    access_token = get_access_token()
    approvals_list = get_request_approvals_list(access_token)
    print("number of approvals:", len(approvals_list))
    #print("Approvals List:", approvals_list)
    assert approvals_list is not None
    return approvals_list
    #assert isinstance(approvals_list, dict)  
def test_close_request_approval(approval_id):
    access_token = get_access_token()  # Replace with a valid approval ID for testing
    response = close_request_approval(access_token, approval_id)
    print("Close Request Approval Response:", response)
    assert response is not None
    # Add more assertions based on the expected response structure

if __name__ == "__main__":
    approvals_list = test_get_request_approvals_list()
    approval_ids = []
    for approval in approvals_list:
        print(f"Approval ID: {approval.get('accessRequestId')}, Created Date: {approval.get('requestCreated')}")
        approval_ids.append(approval.get('accessRequestId'))
    #approval_id = approvals_list[0]['accessRequestId'] if approvals_list else None
    print(f"Number of approval IDs to close that are {getenv('DAYS_OLD')} or more days old:", len(approval_ids))
    for approval_id in approval_ids:
        test_close_request_approval(approval_id)
    