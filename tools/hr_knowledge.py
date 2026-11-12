
import os
import boto3
from dotenv import load_dotenv
from strands import tool

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")

bedrock_agent = boto3.client(
    service_name="bedrock-agent-runtime",
    region_name=AWS_REGION
)


@tool
def search_hr_policies(question: str) -> str:
    """
    Search official HR policy documents for information
    relevant to an employee's question.

    Args:
        question: The employee's HR policy question.
    """

    if not KNOWLEDGE_BASE_ID:
        return "Knowledge Base ID is not configured."

    response = bedrock_agent.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalQuery={
            "text": question
        },
        retrievalConfiguration={
            "vectorSearchConfiguration": {
                "numberOfResults": 5
            }
        }
    )

    results = response.get("retrievalResults", [])

    if not results:
        return "No relevant information was found in the HR policy documents."

    retrieved_information = []

    for index, result in enumerate(results, start=1):

        content = result.get("content", {}).get("text", "")

        location = result.get("location", {})

        s3_location = location.get("s3Location", {})

        source = s3_location.get(
            "uri",
            "HR Policy Document"
        )

        if content:
            retrieved_information.append(
                f"""
                Result {index}
                Source: {source}
                Policy Information: {content}
                """
            )

    if not retrieved_information:
        return "No readable policy information was retrieved."

    return "\n\n".join(retrieved_information)
