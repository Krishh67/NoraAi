from google.cloud import firestore
from collections import Counter
import datetime

# Firestore setup
db = firestore.Client.from_service_account_json('nora--x-firebase-adminsdk-fbsvc-82b89ee05d.json')
collection_ref = db.collection('activity')
print(collection_ref)

# Fetch data
docs = collection_ref.limit(100).stream()
activity_data = []
for doc in docs:
    activity_data.append(f'Document ID: {doc.id}, Data: {doc.to_dict()}')
# print(activity_data)

def aggregate_activity():
    docs = db.collection('activity').order_by("current_time", direction=firestore.Query.DESCENDING).limit(100).stream()

    app_counter = Counter()
    total_records = 0
    productive_count = 0  # e.g., VS Code or similar

    for doc in docs:
        rec = doc.to_dict() or {}
        active = rec.get('active_app', 'Unknown')

        # ❌ Skip LockApp.exe
        if active.lower() == "lockapp.exe":
            continue

        app_counter[active] += 1

        # define productive apps
        if active.lower().endswith(("code.exe", "python.exe", "vs code", "chrome.exe")):
            productive_count += 1
        total_records += 1

    if total_records == 0:
        return "No usable data available."

    # ESTIMATION BASED ON FIXED INTERVAL
    interval_minutes = 1  # Set your actual logging interval here
    duration_minutes = total_records * interval_minutes
    duration_hours = duration_minutes / 60

    # Top 5 apps (excluding LockApp.exe now)
    top5 = app_counter.most_common(5)
    summary = [
        f"Estimated active usage: {duration_hours:.1f} hours based on {total_records} snapshots.",
        f"Top apps:",
    ]
    for app, cnt in top5:
        summary.append(f"  • {app}: {cnt} records")

    prod_pct = productive_count / total_records * 100
    summary.append(f"Estimated productive usage: {prod_pct:.1f}%")

    return "\n".join(summary)

# To see the summary:
print(aggregate_activity())
