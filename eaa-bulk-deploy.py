import requests
from akamai.edgegrid import EdgeGridAuth
from urllib.parse import urljoin
import json

# Collect the edge authentication details
def get_user_inputs():
    base_url = input("Enter the Base URL (eg. https://endpoint-akamai.com/crux/v1/mgmt-pop): ").strip()
     client_token = input("Enter the Client Token: ").strip()
     client_secret = input("Enter the Client Secret: ").strip()
     access_token = input("Enter the Access Token: ").strip()
     return base_url, client_token, client_secret, access_token

BASE_URL, CLIENT_TOKEN, CLIENT_SECRET, ACCESS_TOKEN = get_user_inputs()

# Create the session authentication
session = requests.Session()
session.auth = EdgeGridAuth(
    client_token=CLIENT_TOKEN,
    client_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN
)

# Generate the list of apps with pending changes
# If you want to limit this to certain amount of apps, add max_apps so the function definition looks as such:
    ## def get_apps_pending_deployment(max_apps=15):
# If using max_apps, also uncomment the if statement on lines 57-58
def get_apps_pending_deployment():
    pending_uuids = []
    offset = 0
    limit = 1

    while True:
        response = session.get(
            f"{BASE_URL}/apps",
            headers=HEADERS,
            params={"limit": limit, "offset": offset}
        )
        response.raise_for_status()
        data = response.json()

        apps = data.get("objects", [])

        # No more apps to process
        if not apps:
            break

        app = apps[0]
        app_status = app.get("app_status")
        uuid_url = app.get("uuid_url")

        if app_status != 2:
            print(f"App {uuid_url} has status {app_status} - marking for deployment")
            pending_uuids.append(uuid_url)

        # Uncomment the below if statement if limit with max_apps=
        #if len(pending_uuids) >= max_apps:
        #    break

        # Stop if we've reached the total count
        total = data.get("meta", {}).get("total_count", 0)
        offset += 1
        if offset >= total:
            break

    return pending_uuids

# Function that deploys the apps generated from the above list
def deploy_apps(pending_uuids):
    for uuid_url in pending_uuids:
        print(f"Deploying app: {uuid_url}")
        response = session.post(
            f"{BASE_URL}/apps/{uuid_url}/deploy",
            headers=HEADERS
        )
        response.raise_for_status()
        print(f"Successfully deployed: {uuid_url}")


if __name__ == "__main__":
    print("Stage 1: Finding apps with pending deployments...")
    pending_uuids = get_apps_pending_deployment()
    print(f"\nFound {len(pending_uuids)} apps to deploy: {pending_uuids}")

    if pending_uuids:
        print("\nStage 2: Deploying apps...")
        deploy_apps(pending_uuids)
        print("\nAll deployments complete.")
    else:
        print("\nNo apps require deployment.")
