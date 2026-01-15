import os
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', 'YOUR_ELEVENLABS_API_KEY_HERE')
USER_EMAIL = os.getenv('USER_EMAIL', 'YOUR_EMAIL@EXAMPLE.COM')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = os.getenv('SMTP_PORT', 587)
SMTP_USER = os.getenv('SMTP_USER', 'YOUR_SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS', 'YOUR_SMTP_PASSWORD')

def fetch_elevenlabs_conversation(conversation_id):
    """Fetches full conversation data and analysis from ElevenLabs."""
    url = f"https://api.elevenlabs.io/v1/convai/conversations/{conversation_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def format_transcript(transcript_data):
    """Converts ElevenLabs transcript object into readable text."""
    formatted_transcript = ""
    for turn in transcript_data:
        role = turn.get('role', 'Unknown').capitalize()
        message = turn.get('message', '')
        formatted_transcript += f"**{role}**: {message}\n\n"
    return formatted_transcript

def send_summary_email(conversation_id, lead_info, analysis, transcript_text):
    """Sends a professional summary email to the user."""
    subject = f"🔔 New Lead Captured: {lead_info.get('name', 'Unknown')}"
    
    # Extract analysis fields if they exist
    summary = analysis.get('transcript_summary', 'No summary available.')
    call_evaluation = analysis.get('call_evaluation', 'N/A')
    
    body = f"""
    <h2>New Lead Dossier</h2>
    <hr>
    <p><strong>Lead Name:</strong> {lead_info.get('name', 'N/A')}</p>
    <p><strong>Email:</strong> {lead_info.get('email', 'N/A')}</p>
    <p><strong>Goal:</strong> {lead_info.get('goal', 'N/A')}</p>
    <hr>
    <h3>AI Summary</h3>
    <p>{summary}</p>
    <p><strong>Evaluation:</strong> {call_evaluation}</p>
    <hr>
    <h3>Full Transcript</h3>
    <div style="background: #f4f4f4; padding: 15px; border-radius: 8px;">
        {transcript_text.replace('\n', '<br>')}
    </div>
    <hr>
    <p><small>Conversation ID: {conversation_id}</small></p>
    """

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = USER_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def main(conversation_id, lead_info=None):
    if not lead_info:
        lead_info = {}
        
    try:
        print(f"Processing ElevenLabs Conversation: {conversation_id}")
        data = fetch_elevenlabs_conversation(conversation_id)
        
        # Get transcript and analysis
        transcript_data = data.get('transcript', [])
        analysis = data.get('analysis', {})
        
        # Format transcript
        transcript_text = format_transcript(transcript_data)
        
        # If lead info wasn't passed, try to extract it from the analysis or transcript
        if not lead_info.get('name'):
            # Simple fallback: use the first turn or name from analysis
             lead_info['name'] = data.get('metadata', {}).get('user_name', 'Web Lead')

        # Send the email
        success = send_summary_email(conversation_id, lead_info, analysis, transcript_text)
        
        if success:
            print(f"Summary email sent successfully to {USER_EMAIL}")
        else:
            print("Failed to send summary email.")
            
    except Exception as e:
        print(f"Error processing ElevenLabs call: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        conv_id = sys.argv[1]
        # In a real webhook flow, we'd pass lead info too
        test_info = {'name': 'Sarah Smith', 'email': 'sarah@example.com', 'goal': 'Listing Appointment'}
        main(conv_id, test_info)
    else:
        print("Usage: python process_call.py <conversation_id>")
