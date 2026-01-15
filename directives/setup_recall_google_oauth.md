# Setup Recall.ai Google OAuth Credentials

## Goal
Configure Google OAuth credentials to allow Recall.ai to access your Google Calendar and join Google Meet calls automatically for the Pete Intake Bot.

## Prerequisites
- Google account with access to Google Cloud Console
- Recall.ai account with OAuth setup page open

## Step-by-Step Instructions

### Part 1: Create OAuth Credentials in Google Cloud Console

1. **Navigate to Google Cloud Console**
   - Go to: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create or Select a Project**
   - Click the project dropdown at the top
   - Either select an existing project or click "New Project"
   - If creating new: Name it "Recall AI Integration" or similar
   - Click "Create" and wait for project creation

3. **Enable Google Calendar API**
   - In the left sidebar, go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click on it and press "Enable"
   - Wait for API to be enabled

4. **Configure OAuth Consent Screen** (if not already done)
   - Go to "APIs & Services" > "OAuth consent screen"
   - Select "External" user type (unless you have Google Workspace)
   - Click "Create"
   - Fill in required fields:
     - App name: "Pete Intake Bot" or "Recall AI Calendar Access"
     - User support email: Your email
     - Developer contact: Your email
   - Click "Save and Continue"
   - On Scopes page, click "Add or Remove Scopes"
   - Add these scopes:
     - `https://www.googleapis.com/auth/calendar.events.readonly`
     - `https://www.googleapis.com/auth/userinfo.email`
   - Click "Update" then "Save and Continue"
   - On Test users page, add your email address
   - Click "Save and Continue"

5. **Create OAuth 2.0 Client ID**
   - Go to "APIs & Services" > "Credentials"
   - Click "+ Create Credentials" at the top
   - Select "OAuth client ID"
   - Application type: "Web application"
   - Name: "Recall AI Bot"
   - Under "Authorized redirect URIs", click "+ Add URI"
   - Paste: `https://us-west-2.recall.ai/api/v1/calendar/google_oauth_callback/`
   - Click "Create"

6. **Copy Your Credentials**
   - A popup will show your Client ID and Client Secret
   - **IMPORTANT**: Copy both values immediately
   - Client ID looks like: `xxxxx.apps.googleusercontent.com`
   - Client Secret looks like: `GOCSPX-xxxxx`
   - Click "OK" (you can always retrieve these later from the Credentials page)

### Part 2: Add Credentials to Recall.ai

7. **Return to Recall.ai OAuth Setup**
   - Go back to the Recall.ai setup page (the one in your screenshot)
   - Click on "Google Calendar" section to expand it

8. **Enter Credentials**
   - Paste the Client ID into the "Client ID" field
   - Paste the Client Secret into the "Client Secret" field
   - Click "Save"

9. **Authorize Access**
   - After saving, you should see an "Authorize" or "Connect" button
   - Click it to start the OAuth flow
   - Sign in with your Google account
   - Review and accept the permissions requested
   - You should be redirected back to Recall.ai

10. **Verify Connection**
    - Check that the Google Calendar shows as "Connected" or has a green checkmark
    - Test by creating a test meeting and ensuring Recall.ai can access it

### Part 3: Update n8n Workflow (if needed)

11. **Verify Recall.ai API Key in n8n**
    - Open your n8n workflow
    - Check that the Recall.ai API key is correctly configured
    - The bot should now be able to fetch calendar events automatically

## Expected Outputs
- ✅ Google Cloud project with Calendar API enabled
- ✅ OAuth 2.0 credentials created with correct redirect URI
- ✅ Recall.ai connected to your Google Calendar
- ✅ Pete bot can automatically join scheduled Google Meet calls

## Troubleshooting

### "Redirect URI mismatch" error
- Double-check the redirect URI in Google Cloud Console matches exactly: `https://us-west-2.recall.ai/api/v1/calendar/google_oauth_callback/`
- No trailing spaces or extra characters

### "Access blocked: This app's request is invalid"
- Make sure you added the required scopes in the OAuth consent screen
- Verify the Calendar API is enabled

### Can't find credentials later
- Go to Google Cloud Console > APIs & Services > Credentials
- Click on your OAuth 2.0 Client ID name
- Client ID is visible; click "Download JSON" for full credentials

### "This app isn't verified" warning
- This is normal for apps in testing mode
- Click "Advanced" then "Go to [App Name] (unsafe)" to proceed
- For production, you'd need to verify the app with Google

## Security Notes
- Store Client ID and Client Secret securely
- Never commit these to public repositories
- Consider adding them to your `.env` file if needed by other scripts
- The OAuth token allows Recall.ai to read your calendar events only (readonly scope)

## Next Steps
After successful setup:
1. Test with a sample Google Meet meeting
2. Verify Pete joins automatically via n8n workflow
3. Monitor first few calls to ensure smooth operation
