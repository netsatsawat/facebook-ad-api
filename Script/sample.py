from facebookads.api import FacebookAdsApi
from facebookads.adobjects.campaign import Campaign
import facebookads 

# Note of Graph API version, this can be used to scrape the page, post, comments
# graph_api = "https://graph.facebook.com/v2.8" 

# Initialize
my_app_id = '<APP_ID>'
my_app_secret = '<APP_SECRET>'
my_access_token = '<ACCESS_TOKEN>'

# For operation process, multiple user may try to access the ad account in the same time.
# Should use the session for each access.
def startSession():
    session = facebookads.FacebookSession(
        my_app_id,
        my_app_secret,
        my_access_token
    )
    return(session)

# Initialize API session
api = FacebookAdsApi(startSession())

me = facebookads.objects.AdUser(fbid='me', api=api)
my_accounts = list(me.get_ad_accounts())
ad_account = my_accounts[0]
ad_account = ad_account.get_id_assured() # Sandbox ad account id: 1027868XXXXXXXXXX

account = facebookads.objects.AdAccount(fbid = ad_account, api=api)
account.remote_read(fields=[facebookads.objects.AdAccount.Field.timezone_name])

### OUTPUT
<AdAccount> {
    "id": "act_1027868XXXXX", ## >> This should be the same as ad_account
    "timezone_name": "Asia/Bangkok"
}

### Example of insight retrieval
fields = [
    facebookads.objects.Insights.Field.campaign_name,
    facebookads.objects.Insights.Field.campaign_id,
    facebookads.objects.Insights.Field.impressions,
    facebookads.objects.Insights.Field.reach,
    facebookads.objects.Insights.Field.actions,
    facebookads.objects.Insights.Field.spend,
    facebookads.objects.Insights.Field.ad_id
]

params = {
    'level': 'ad',
    'limit': 100
}

account.get_insights()
insights = account.get_insights(fields=fields, params=params)



### Generate Campaign manually
# Create campaign object
campaign = Campaign(parent_id=ad_account.get_id_assured())
campaign[Campaign.Field.name] = 'Test Campaign'
campaign[Campaign.Field.objective] = Campaign.Objective.link_clicks
campaign[Campaign.Field.configured_status] = Campaign.Status.paused
campaign.remote_create()

account.get_campaigns()

### Output
<Campaign> {
    "id": "120330000000337018"
}, <Campaign> {
    "id": "120330000000333018"
}]
