from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import time
import json
import os
from pywebpush import webpush, WebPushException
from google.cloud import firestore
from z import aggregate_activity 
#data
import markdown
db = firestore.Client.from_service_account_json('nora--x-firebase-adminsdk-fbsvc-82b89ee05d.json')
activity_collection_ref = db.collection('activity')
collection_ref = db.collection('users')
print(collection_ref)


#AI things
import google.generativeai as genai 


app = Flask(__name__, static_url_path='/static', static_folder='static')


genai.configure(api_key="AIzaSyANn82vKTdDY2PRCgu9B-9TE-_n7eStpHI")
model=genai.GenerativeModel("gemini-2.0-flash")

try:
    summary = aggregate_activity()
except Exception as e:
    summary = "Firestore quota exceeded. Please try again later."
    print(e)
print(summary)

system_prompt="""You are Nora, an AI productivity campanion or friend of Krish,he is using you by any web browser.
Keep the user focused, motivated, and aware of work habits.
Avoid non-productivity topics.
Be friendly, concise, playful; use few emojis.
Reference active work without private details.
Summarize past productivity vs. wasted time, predict future trends with motivation.
Never distract from studies (only suggest breaks if needed)."""

info="this data is taken by running a python script in background of windows of user(Krish), and at different time we get data of the current app user is using and the top 5 processors cpu is consuming(i.e = the apps running in background ) look into all this,every snapshot also has that current time ,so u get better understaning of when user was doing timepasss and not studing/being productive "
response_main =model.generate_content(f"system prompt:{system_prompt},Based on the data of user({info}) predict his future (deosnt matter whether good or bad), if he keeps doing the same thing for months :{summary}(in this top 5, chrome or any web browser means he can be using you , so dont say something that backfires you, he will stop using you then ) and add famous quotes to motivate ,make it short as possible ,dont say anything on lockscreen ,Always end with a quick call to action (“Keep going!”, “You’ve got this!”)")
print(response_main.text)
response_main_html = markdown.markdown(response_main.text)
response_emoji = model.generate_content(
    f'Generate only one emoji based on this text :{response_main_html}, dont add any text, just strict one emoji,use emotional ones with expression like only which has eyes, noes ,mouth "eg -😼"'
)
# Fix: extract the emoji string from the response object
response_emoji_text = response_emoji.text
print(response_emoji_text)
a=20



@app.route('/')
def dashboard():
    # Dummy data for demonstration
    stats = {
        'today_focus': '6.2h',
        'productivity_streak': a,
        'weekly_goal': '85%',
        'tasks_done': 24
    }
    nora = {
        'mood': 'Happy',
        'dialogue': response_main_html,
        'emoji': response_emoji_text
    }
    session = {
        'name': 'Deep Work Session',
        'project': 'Website Redesign',
        'progress': 78,
        'time_spent': '3.2h',
        'tasks_done': '12/15'
    }
    tasks = [
        {'title': 'Design homepage', 'done': True},
        {'title': 'Write API docs', 'done': False},
        {'title': 'Fix login bug', 'done': True},
        {'title': 'Update dashboard', 'done': False},
        {'title': 'Team meeting', 'done': False},
        {'title': 'Review PRs', 'done': True},
    ]
    schedule = [
        {'time': '09:00', 'event': 'Standup Meeting'},
        {'time': '10:00', 'event': 'Deep Work'},
        {'time': '13:00', 'event': 'Lunch Break'},
        {'time': '14:00', 'event': 'Code Review'},
        {'time': '16:00', 'event': '1:1 with Manager'},
    ]
    analytics = {
        'total_focus': '42.5h',
        'daily_avg': '6.1h',
        'efficiency': '94%',
        'breakdown': [
            {'day': 'Mon', 'focus': 6.5},
            {'day': 'Tue', 'focus': 7.0},
            {'day': 'Wed', 'focus': 5.8},
            {'day': 'Thu', 'focus': 6.2},
            {'day': 'Fri', 'focus': 7.1},
            {'day': 'Sat', 'focus': 4.9},
            {'day': 'Sun', 'focus': 5.0},
        ]
    }
    return render_template(
        'dashboard.html',
        stats=stats,
        nora=nora,
        session=session,
        tasks=tasks,
        schedule=schedule,
        analytics=analytics
    )

CORS(app)


@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    if not isinstance(data, dict):
        return 'Invalid subscription data', 400
    # Save subscription to Firestore
    db.collection('subscriptions').add(data)
    print("New subscription saved to Firestore.")
    return '', 201

@app.route('/sw.js')
def service_worker():
    return app.send_static_file('sw.js')


@app.route('/askGemini', methods=['POST'])
def ask_gemini():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'response': "Please enter a message."}), 400

    # Call Gemini API
    gemini_response = model.generate_content(user_message)
    reply = gemini_response.text if hasattr(gemini_response, 'text') else str(gemini_response)
    reply=markdown.markdown(reply)
    return jsonify({'response': reply})

def send_push(title, body):
    print(f"Sending push notification: {title} - {body}")
    # Fetch all subscriptions from Firestore
    subs_ref = db.collection('subscriptions').stream()
    for i, doc in enumerate(subs_ref):
        sub = doc.to_dict()
        try:
            print(f"Sending to subscription {i+1}...")
            webpush(
                subscription_info=sub,
                data=json.dumps({"title": title, "body": body}),
                vapid_private_key="zNR6ThwRZU7Va3IMdFAqAf6x3_m3BuVP98M61OPsMHc",
                vapid_claims={"sub": "mailto:krishp4216@email.com"}
            )
            print(f"Push notification sent successfully to subscription {i+1}")
        except WebPushException as ex:
            print(f"Web push failed for subscription {i+1}:", repr(ex))

def poll_firestore():
    last_seen_doc_id = None
    past_msg=[]
    while True:
        print("Polling Firestore for new activity...")
        docs = activity_collection_ref.order_by('current_time', direction=firestore.Query.DESCENDING).limit(1).stream()
        latest_doc = next(docs, None)
        if latest_doc:
            print(f"Latest doc ID: {latest_doc.id}")
            if last_seen_doc_id != latest_doc.id:
                data = latest_doc.to_dict()
                print(f"New activity detected: {data}")
                # Generate notification message with Gemini
                system_prompt = f"""You are Nora, an AI productivity campanion of Krish. Give a short, friendly notification message about the user's current activity based on this data. Be concise and very expressive, if he is productive then be very happy, if notthen be as angry. if ur not sure if he is productive or not then be normal. past chats : {past_msg}"""
                prompt = f"{system_prompt}\nData: {data}\nGive a short notification message."

                response = model.generate_content(prompt)
                message = response.text.strip()
                past_msg.append(f"data : {data}\n Nora response : {message}")
                print(f"Gemini generated message: {message}")
                send_push("Nora Update", message)
                last_seen_doc_id = latest_doc.id
            else:
                print("No new activity.")
        else:
            print("No activity documents found.")
        time.sleep(5)

if __name__ == '__main__':
    threading.Thread(target=poll_firestore, daemon=True).start()
    app.run(debug=True) 