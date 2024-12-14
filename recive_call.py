from fastapi import FastAPI, Request, Response
from twilio.twiml.voice_response import VoiceResponse
from logger.__init__ import get_logger, __init__ as init_logger


logger = get_logger(__name__)
app = FastAPI()


@app.post("/process_recording")
async def process_recording(request: Request):
    try:
        # Log the request details
        logger.info("Recording received.")
        
        # Parse recording data from Twilio webhook
        form_data = await request.form()
        logger.info(f"Form data received: {form_data}")
        
        recording_url = form_data.get("RecordingUrl", "")
        caller_number = form_data.get("From", "Unknown")
        logger.info(f"Received recording from {caller_number}: {recording_url}")
        
        # Placeholder for further processing (e.g., transcribe and summarize)
        logger.info("Processing recording (placeholder).")
        
        # Respond to Twilio to finalize the call
        response = VoiceResponse()
        response.say("Your message has been recorded. Goodbye!", voice="alice")
        logger.info("Returning Twilio VoiceResponse for recording.")
        return Response(content=response.to_xml(), media_type="application/xml")
    except Exception as e:
        logger.error(f"Error in /process_recording: {e}")
        return Response(content="<Response><Say>An error occurred while processing your recording. Please try again later.</Say></Response>", media_type="application/xml")
    
    
@app.post("/receive_call")
async def receive_call(request: Request):
    try:
        # Log the request details
        logger.info("Incoming call received.")
        
        # Parse incoming Twilio webhook data
        form_data = await request.form()
        logger.info(f"Form data received: {form_data}")
        
        # Extract caller information
        caller_number = form_data.get("From", "Unknown")
        called_number = form_data.get("To", "Unknown")
        logger.info(f"Call from {caller_number} to {called_number}")
        
        # Create Twilio VoiceResponse
        response = VoiceResponse()

        # Respond with a simple message and gather input (optional)
        response.say("Hello! You have reached the AI assistant. Please leave a message after the beep.", voice="alice")
        response.record(max_length=60, action="/process_recording", finish_on_key="#")
        response.say("Thank you for your message. Goodbye!")
        
        # Return response as XML
        logger.info("Returning Twilio VoiceResponse.")
        return Response(content=response.to_xml(), media_type="application/xml")
    except Exception as e:
        logger.error(f"Error in /receive_call: {e}")
        return Response(content="<Response><Say>An error occurred while processing your call. Please try again later.</Say></Response>", media_type="application/xml")


# Run the FastAPI app if executed directly
if __name__ == "__main__":
    import uvicorn
    init_logger()
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

