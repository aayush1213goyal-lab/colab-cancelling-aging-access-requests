# Access Request Automation Script

## Overview

This Python-based tool automates the management of access requests in SailPoint IdentityNow. It retrieves pending access request approvals, identifies those older than a specified number of days, and automatically closes them with a termination status. This helps maintain a clean access request queue by removing stale requests that may no longer be relevant.

The tool is designed for Identity and Access Management (IAM) operations teams to streamline request lifecycle management without manual intervention.

## Features

- **OAuth 2.0 Authentication**: Securely authenticates with SailPoint IdentityNow using client credentials flow.
- **Pending Approvals Retrieval**: Fetches all pending access request approvals from the configured tenant.
- **Age-Based Filtering**: Identifies requests older than a configurable threshold (default: 1 day).
- **Automated Closure**: Closes identified old requests with a standardized termination message.
- **Email Notifications**: Sends closure notification emails to requesters when an email address is available.
- **Configurable**: Uses environment variables for all configuration, making it adaptable to different environments.
- **Testing Support**: Includes unit tests for key functions to ensure reliability.
- **Error Handling**: Comprehensive error handling for API failures and missing configurations.

## Prerequisites

- Python 3.7 or higher
- Access to a SailPoint IdentityNow tenant with appropriate API permissions
- Client ID and Client Secret for OAuth authentication
- Internet connection for API calls

## Installation

1. **Clone or Download the Repository**:
   ```
   git clone <repository-url>
   cd access_request
   ```

2. **Set Up Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install requests python-dotenv
   ```

   Create a `requirements.txt` file with:
   ```
   requests==2.28.1
   python-dotenv==0.19.2
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# SailPoint IdentityNow Configuration
TENANT=your-tenant-name
DOMAIN=identitynow-demo  # or production domain
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret

# API Endpoints
API_URL=https://your-tenant.api.identitynow-demo.com/v2025/access-request-approvals/pending
API_URL1=https://your-tenant.api.identitynow-demo.com/v2025/access-requests/close

# Email Configuration
EMAIL_SMTP_SERVER=smtp.example.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your-email@example.com
EMAIL_PASSWORD=your-email-password
EMAIL_FROM=your-email@example.com

# Processing Configuration
DAYS_OLD=30  # Number of days after which requests are considered old
```

### Environment Variable Details

- `TENANT`: Your SailPoint tenant name (e.g., `devrel-ga-20967`)
- `DOMAIN`: The domain for your SailPoint instance (`identitynow-demo` for sandbox, `identitynow` for production)
- `CLIENT_ID` & `CLIENT_SECRET`: Obtained from SailPoint Admin Console under API Management
- `API_URL`: Endpoint to retrieve pending approvals
- `API_URL1`: Endpoint to close requests
- `DAYS_OLD`: Threshold in days for closing requests (default: 1)

**Security Note**: Never commit the `.env` file to version control. Add it to `.gitignore`.

## Usage

### Running the Main Script

Execute the main automation script:

```bash
python main.py
```

This will:
1. Authenticate with SailPoint
2. Retrieve all pending approvals
3. Filter requests older than `DAYS_OLD` days
4. Close each old request
5. Send email notifications for closed requests when a requester email is available
6. Print summary statistics

### Sample Output

```
Total approvals retrieved: 150
Approval ID: abc123, Created Date: 2023-01-01T10:00:00.000Z
Close Request Response for Approval ID abc123: {'status': 'success'}
Number of approvals older than 30 days: 5
```

### Running Tests

Execute the test suite:

```bash
python test.py
```

This will run tests for authentication, data retrieval, and request closure functions.

## Code Structure

- `main.py`: Entry point for the automation script
- `utils.py`: Utility functions for API interactions
  - `get_access_token()`: Obtains OAuth token
  - `get_request_approvals_list()`: Retrieves pending approvals
  - `close_request_approval()`: Closes a specific request
- `test.py`: Unit tests for the utility functions
- `.env`: Environment configuration (not in repository)
- `README.md`: This documentation

## API Integration Details

### Authentication
Uses OAuth 2.0 Client Credentials flow:
- Endpoint: `https://{TENANT}.api.{DOMAIN}.com/oauth/token`
- Method: POST
- Headers: `Accept: application/json`
- Body: `grant_type=client_credentials`

### Get Pending Approvals
- Endpoint: Configured in `API_URL`
- Method: GET
- Headers: `Authorization: Bearer {access_token}`, `Accept: application/json`
- Returns: JSON array of approval objects

### Close Request
- Endpoint: Configured in `API_URL1`
- Method: POST
- Headers: `Authorization: Bearer {access_token}`, `Content-Type: application/json`
- Body:
  ```json
  {
    "accessRequestIds": ["request-id"],
    "executionStatus": "Terminated",
    "completionStatus": "Failure",
    "message": "This request has been closed by IAM Ops Team due to being older than 30 days."
  }
  ```

## Error Handling

The tool includes comprehensive error handling:
- Missing environment variables raise `ValueError`
- API authentication failures raise `RuntimeError`
- HTTP errors raise `Exception` with status code and message

## Customization

### Changing the Closure Message
Edit the `message` field in `close_request_approval()` in `utils.py`.

### Modifying Age Threshold
Adjust `DAYS_OLD` in `.env` or make it dynamic.

### Adding Email Notifications
This script now supports email notifications for closed requests. Configure SMTP settings in `.env`, and when the approval object contains a requester email address, the system will send a closure notification automatically.

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify `CLIENT_ID` and `CLIENT_SECRET` are correct
   - Ensure the client has appropriate permissions in SailPoint

2. **API Endpoint Errors**
   - Check `TENANT` and `DOMAIN` configuration
   - Verify API URLs match your SailPoint version

3. **No Approvals Retrieved**
   - Confirm there are pending approvals in your tenant
   - Check API permissions

4. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

### Debugging
- Enable verbose logging by adding `print` statements or using `logging` module
- Test individual functions using `test.py`

## Security Considerations

- Store credentials securely using environment variables
- Use HTTPS for all API communications
- Rotate client secrets regularly
- Limit script execution to authorized personnel

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For issues or questions:
- Check the troubleshooting section
- Review SailPoint IdentityNow API documentation
- Contact your IAM team

## Version History

- v1.0: Initial release with basic automation functionality