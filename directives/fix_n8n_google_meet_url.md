# Fix Pete n8n Workflow - Get Google Meet URL Instead of Calendly URL

## Problem
Pete isn't joining calls because the workflow is sending the **Calendly join URL** to Recall.ai instead of the **Google Meet URL**. Recall.ai can only join Google Meet links, not Calendly links.

## Root Cause
In the current workflow (`pete_n8n_workflow_v3.json`), line 116 extracts:
```javascript
"meeting_url": "={{ $node[\"Poll Event API\"].json.resource.location.join_url }}"
```

This gets the Calendly URL (like `https://calendly.com/events/...`), but Recall.ai needs the actual Google Meet URL (like `https://meet.google.com/xxx-yyyy-zzz`).

## Solution
Add a **Google Calendar node** to fetch the event from Google Calendar, which contains the `hangoutLink` field with the actual Google Meet URL.

## Implementation Steps

### Step 1: Set Up Google Calendar Credentials in n8n

1. **In n8n**, go to **Credentials** (left sidebar)
2. Click **"+ Add Credential"**
3. Search for **"Google Calendar OAuth2 API"**
4. Click **"Connect my account"** or fill in OAuth details:
   - If you already completed the Google Cloud Console setup, use those credentials
   - Otherwise, follow the OAuth setup we started earlier
5. **Authorize** your Google account
6. **Save** the credential and note its ID

### Step 2: Import the Fixed Workflow

1. **In n8n**, go to **Workflows**
2. Click **"+ Add Workflow"** or **"Import from File"**
3. **Import** the file: `pete_n8n_workflow_v4_google_meet_fix.json`
4. **Update the Google Calendar credential**:
   - Click on the "Get Google Calendar Event" node
   - Select your Google Calendar credential from the dropdown
5. **Save** the workflow

### Step 3: How the Fixed Workflow Works

```
Calendly Trigger
    ↓
Wait 10s (give Calendly time to create the Google Calendar event)
    ↓
Get Google Calendar Event (search for event by email and time)
    ↓
Extract Google Meet URL (get the hangoutLink field)
    ↓
Send to Recall.ai (with the correct Google Meet URL)
```

### Key Changes:

1. **Removed**: The "Poll Event API" node that was checking Calendly's processing status
2. **Added**: "Get Google Calendar Event" node that searches your Google Calendar
3. **Changed**: The meeting_url now comes from `$json.hangoutLink` (Google Meet URL) instead of Calendly's join_url

### Step 4: Configure the Google Calendar Node

The node searches for the event using:
- **Time range**: From start_time to end_time of the Calendly booking
- **Query**: The invitee's email address
- **Calendar**: Primary calendar

This should find the exact event that Calendly created in your Google Calendar.

### Step 5: Test the Workflow

1. **Activate** the workflow in n8n
2. **Book a test meeting** on your Calendly page
3. **Check the workflow execution**:
   - Go to **Executions** in n8n
   - Click on the latest execution
   - Verify each node:
     - Calendly Trigger: Should show the booking data
     - Get Google Calendar Event: Should show the event with `hangoutLink`
     - Extract Google Meet URL: Should show the Google Meet URL
     - Send to Recall.ai: Should return success
4. **Join the meeting** and verify Pete joins automatically

## Troubleshooting

### "No meeting was found at the given link" (FATAL ERROR)
- **Cause**: The bot tried to join before the meeting was actually live in Google Meet
- **Symptoms**: 
  - Recall.ai status shows "fatal" with message "No meeting was found at the given link"
  - The bot never joins even though the Google Meet URL is correct
- **Fix**: The workflow now adds **60 seconds (1 minute)** to the start time
  - This gives you time to join as the host first
  - Ensures the Google Meet room is actually created and active
  - The `join_at_delayed` field calculates: `start_time + 60000ms (1 minute)`
- **Adjust if needed**: If 1 minute isn't enough, you can change `60000` to:
  - `90000` for 90 seconds (1.5 minutes)
  - `120000` for 2 minutes
  - Located in the "Extract Google Meet URL" node

### "No events found" in Google Calendar node
- **Cause**: The wait time (10s) might not be enough for Calendly to create the Google Calendar event
- **Fix**: Increase the wait time to 15-20 seconds

### "hangoutLink is undefined"
- **Cause**: The Google Calendar event doesn't have a Google Meet link
- **Fix**: Make sure your Calendly event type is configured to add Google Meet conferencing
  - In Calendly: Event Type Settings → Location → Google Meet

### Pete still doesn't join
- **Check**: The Recall.ai response in the execution log
- **Verify**: The meeting_url is a valid Google Meet link (starts with `https://meet.google.com/`)
- **Test**: Manually copy the meeting_url and try to join it yourself

## Alternative: Use Calendly's Google Meet Integration

If you're still having issues, make sure:
1. Your Calendly is connected to Google Calendar
2. Your Calendly event type uses "Google Meet" as the location
3. Calendly is set to "Add conferencing" automatically

## Next Steps

After this fix works:
1. Monitor a few test meetings to ensure reliability
2. Update any other workflows that might have the same issue
3. Consider adding error handling for cases where Google Calendar event isn't found

## Comparison to Make.com Fix

This is the same fix you implemented in Make.com:
- **Make.com**: Used "Google Calendar: Search Events" module
- **n8n**: Uses "Google Calendar: Get All Events" node
- **Both**: Extract the `hangoutLink` field instead of Calendly's join URL
