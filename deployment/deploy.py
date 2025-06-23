import logging
import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp
from app import agent  

PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"  
STAGING_BUCKET = f"gs://{PROJECT_ID}-vertexai-staging"
AGENT_WHL_FILE = None  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=STAGING_BUCKET,
    )

    
    app = AdkApp(agent= agent, enable_tracing=False)

    
    logger.info("Deploying agent to Vertex AI Reasoning Engine...")
    create_kwargs = {"app": app}
    if AGENT_WHL_FILE:
        create_kwargs["requirements"] = [AGENT_WHL_FILE]
        create_kwargs["extra_packages"] = [AGENT_WHL_FILE]
    remote_app = agent_engines.create(**create_kwargs)

   
    logger.info("Testing deployment...")
    session = remote_app.create_session(user_id="test-user")
    for event in remote_app.stream_query(
        user_id="test-user",
        session_id=session["id"],
        message="hello!",
    ):
        if event.get("content", None):
            print(f"Agent deployed successfully under resource name: {remote_app.resource_name}")
            break

if __name__ == "__main__":
    main() 