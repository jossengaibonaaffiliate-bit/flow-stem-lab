# Fix Pete Audio Issue in n8n Workflow

## Problem
Pete joins the Google Meet call but has no audio/sound.

## Root Cause
The Recall.ai bot configuration is missing critical audio parameters that were present in the Make.com workflow.

## Solution

### Update the Recall.ai HTTP Request

Add these parameters to the Recall.ai API call in your n8n workflow. The critical addition is the **microphone permission** which was missing in previous versions.

```json
{
```json
{
  "meeting_url": "{{ $json.meeting_url }}",
  "bot_name": "Pete Intake Bot",
  "join_at": "{{ $json.join_at }}",
  "automatic_leave": {
    "waiting_room_timeout": 600
  },
  "variant": {
    "google_meet": "web_4_core",
    "zoom": "web_4_core"
  },
  "output_media": {
    "camera": {
      "kind": "webpage",
      "config": {
        "url": "https://jossengaibonaaffiliate-bit.github.io/flow-stem-lab/bot.html?first_name={{ $json.first_name }}&email={{ $json.email }}"
      }
    }
  },
  "browser_rendering_options": {
    "permissions": ["microphone"]
  }
}
```

### Key Changes:

1. **`"permissions": ["microphone"]`** - **CRITICAL FIX**. Without this, the bot cannot transmit audio into the meeting.
2. **`output_media` Structure** - Correctly defines the bot's video feed URL.
3. **`variant` placement** - Moved to the top level to ensure `web_4_core` is applied correctly.
4. **`join_at` Calculation** - We now calculate a time **10 minutes before** the meeting starts.
   - n8n Expression: `{{ new Date(new Date($node["Calendly Trigger"].json.payload.scheduled_event.start_time).getTime() - 10 * 60 * 1000).toISOString() }}`

### Implementation Steps:

1. **Open your n8n workflow**
2. **Updates to "Extract Google Meet URL" Node:**
   - Add a new value called `join_at`.
   - Use the expression: `{{ new Date(new Date($node["Calendly Trigger"].json.payload.scheduled_event.start_time).getTime() - 10 * 60 * 1000).toISOString() }}`
3. **Updates to "Send to Recall.ai" Node:**
   - Update `join_at` in the JSON body to use `{{ $json.join_at }}`.
4. **Save the workflow**

### Alternative: Import the Fixed Workflow

Use the file: `pete_n8n_workflow_v9_early_join.json`

This includes:
- Google Calendar integration (Google Meet URL fix)
- **Microphone Permissions Fix**
- Proper `output_media` structure
- web_4_core variant

## Testing

1. Book a test meeting
2. Join the meeting yourself
3. Verify Pete joins
4. **Check that Pete's microphone icon is active** in Google Meet
5. Speak to Pete and verify he responds

## Troubleshooting

### Pete joins but still no audio
- Check if Pete's microphone is muted in Google Meet
- Look at the Recall.ai bot status page - check for audio-related errors
- Verify bot.html is loading correctly (check browser console in Recall.ai dashboard)

### "Microphone permission denied" error
- This means bot.html couldn't get mic permissions
- The `permissions: ["microphone"]` setting in `browser_rendering_options` should fix this.

### Pete's audio is choppy/stuttering
- This was the original issue with Make.com
- Already fixed by using `web_4_core` variant
- If still happening, check your bot.html CPU usage

## Comparison to Make.com

The Make.com workflow had these critical parameters that were missing in n8n:
- ✅ **`permissions: ["microphone"]`** in `browser_rendering_options` (This was the main issue)
- ✅ `output_media` structure for the bot's camera info
- ✅ `variant` configured for both Google Meet and Zoom

The previous n8n workflow was missing the microphone permission, which is why audio wasn't working.

## Next Steps

After audio is working:
1. Test the full conversation flow
2. Verify transcript is being captured
3. Check that the dossier generation works
4. Monitor a few real calls to ensure reliability
