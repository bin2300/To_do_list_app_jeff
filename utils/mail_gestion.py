from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

# Configure the API key
sib_api_v3_sdk.configuration.api_key['api-key'] = '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'

# Instantiate the API client
api_instance = sib_api_v3_sdk.EmailCampaignsApi()

# Define the campaign settings
email_campaigns = sib_api_v3_sdk.CreateEmailCampaign(
    name="Campaign sent via the API",  # Campaign name
    subject="My subject",  # Email subject
    sender={"name": "From name", "email": "myfromemail@mycompany.com"},  # Sender details
    type="classic",  # Campaign type (classic)
    html_content="<p>Congratulations! You successfully sent this example campaign via the Brevo API.</p>",  # HTML content
    recipients={"emails": [{"email": "ghostofbinary230600@gmail.com"}]},  # List of recipients
    scheduled_at="2025-01-10 00:00:01"  # Scheduled send time
)

# Make the call to the API client
try:
    api_response = api_instance.create_email_campaign(email_campaigns)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EmailCampaignsApi->create_email_campaign: %s\n" % e)
