# Fix Pete Audio Issue in n8n Workflow

## Problem
Pete joins the Google Meet call but has no audio/sound.

## Root Cause
The Recall.ai bot configuration is missing critical audio parameters that were present in the Make.com workflow.

## Solution

### Update the Recall.ai HTTP Request

Add these parameters to the Recall.ai API call in your n8n workflow:

```json
{
  "meeting_url": "{{ $json.meeting_url }}",
  "bot_name": "Pete Intake Bot",
  "join_at": "{{ $json.start_time }}",
  "recording_mode": "speaker_view",
  "automatic_leave": {
    "waiting_room_timeout": 600
  },
  "browser_rendering_options": {
    "url": "https://jossengaibonaaffiliate-bit.github.io/flow-stem-lab/bot.html?first_name={{ $json.first_name }}&email={{ $json.email }}",
    "variant": "web_4_core"
  }
}
```

### Key Changes:

1. **`recording_mode": "speaker_view"`** - Ensures audio is captured properly
2. **`automatic_leave`** - Prevents the bot from leaving prematurely
3. **`variant": "web_4_core"`** - Uses the optimized browser variant for better audio performance (this was critical in Make.com)

### Implementation Steps:

1. **Open your n8n workflow**
2. **Click on the "Send to Recall.ai" HTTP Request node**
3. **Update the JSON Body** to include the parameters above
4. **Save the workflow**
5. **Test with a new meeting**

### Alternative: Import the Fixed Workflow

Use the file: `pete_n8n_workflow_v5_audio_fix.json`

This includes:
- Google Calendar integration (Google Meet URL fix)
- Proper audio configuration
- web_4_core variant for optimal performance

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
- The `web_4_core` variant should auto-grant permissions
- If still failing, check Recall.ai dashboard for browser console errors

### Pete's audio is choppy/stuttering
- This was the original issue with Make.com
- Already fixed by using `web_4_core` variant
- If still happening, check your bot.html CPU usage

## Comparison to Make.com

The Make.com workflow had these same parameters:
- ✅ `recording_mode`: "speaker_view"
- ✅ `variant`: "web_4_core"  
- ✅ `automatic_leave` configuration

The n8n workflow was missing these, which is why audio wasn't working.

## Next Steps

After audio is working:
1. Test the full conversation flow
2. Verify transcript is being captured
3. Check that the dossier generation works
4. Monitor a few real calls to ensure reliability
