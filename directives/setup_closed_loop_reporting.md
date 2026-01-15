# Directive: ElevenLabs Post-Call Email Reporting (Serverless)

## Objective
Establish a zero-infrastructure, "Serverless" reporting system that sends a professional "Lead Dossier" straight to your email as soon as an ElevenLabs call ends using n8n.

## Workflow (100% in n8n)
1.  **Trigger (Webhook):** Receives the `post_call_transcription` event from ElevenLabs.
2.  **Action (Gmail/Email):** Formats and sends the lead details, summary, and transcript to your inbox.

## Setup Instructions

### 1. In n8n: Create the "Receiver"
*   Create a **New Workflow**.
*   Add a **Webhook** node.
*   Set Method to **POST**.
*   **Copy the Test URL** provided (until you are ready to go live, then use the Production URL).

### 2. In ElevenLabs: Connect the Agent
*   Go to your **ElevenLabs Agent Settings**.
*   Find the **Post-call Webhook** field.
*   Paste your **n8n Webhook URL**.
*   Set the event type to `post_call_transcription`.

### 3. In n8n: Map the Email
*   Add an **Email** node (or Gmail node) connected to the Webhook.
*   **Connect your account** (SMTP or Gmail OAuth).
*   **Recipient:** Your email address.
*   **Subject:** `🔔 New Lead Dossier: {{$json["body"]["analysis"]["transcript_summary"]}}`
*   **HTML Content:** Construct your dossier by clicking on the items from the Webhook:
    *   **Summary:** `{{$json["body"]["analysis"]["transcript_summary"]}}`
    *   **Evaluation:** `{{$json["body"]["analysis"]["call_evaluation"]}}`
    *   **Transcript:** `{{$json["body"]["transcript"]}}`

## Advantages
*   **Self-Hostable:** n8n can be run on your own server or in their cloud.
*   **Visual Debugging:** Much clearer execution paths than Make.
*   **Flexible:** Easily add logic like "If lead is hot, send Slack alert".

