from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import base64

# Add the src directory to the path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

# Import our application code
from src.data.schema import CampaignAdvice
from src.models.advisor import CampaignAdvisor
from src.models.factory import create_reasoning_model, create_cost_effective_model
from src.utils.markdown import markdown_to_html

# In a full implementation, you would use Netlify's environment variables to store API keys
# For the demo, we'll create a simple mock implementation

class MockIndex:
    """Mock vector store index for demo purposes.
    
    In a production environment, you would:
    1. Use a cloud-based vector store service
    2. Or implement persistent storage via Netlify's storage options
    3. Or connect to an external database service
    """
    def __init__(self):
        self._vector_store = None
        
    def as_retriever(self, **kwargs):
        return self

    def retrieve(self, query_str):
        """Return mock nodes for demonstration"""
        return [
            type('MockNode', (), {
                'text': 'Example campaign about volunteer mobilization.',
                'metadata': {
                    'case_study_entry': 'Example Campaign 1',
                    'country': 'United States',
                    'focus_area': 'Volunteer Engagement',
                    'main_theme': 'Community Building'
                },
                'score': 0.95
            }),
            type('MockNode', (), {
                'text': 'Example campaign about social media strategy.',
                'metadata': {
                    'case_study_entry': 'Example Campaign 2',
                    'country': 'Canada',
                    'focus_area': 'Digital Marketing',
                    'main_theme': 'Awareness'
                },
                'score': 0.85
            })
        ]

class MockModel:
    """Mock LLM for demo purposes.
    
    In a production environment, you would use the actual LLM APIs
    with API keys stored in Netlify environment variables.
    """
    def __init__(self, model_name="demo"):
        self.model = model_name
        
    def complete(self, prompt):
        """Return a mock completion"""
        query = prompt.split("USER QUERY:")[1].split("\n")[0].strip()
        return type('MockCompletion', (), {
            'text': f"""# Campaign Advice: {query}

Based on our analysis of successful GivingTuesday campaigns, here are some key recommendations:

## 1. Leverage Social Media Strategically

"**Example Campaign 2**" demonstrated that creating a content calendar with specific hashtags increased engagement by 45%. Schedule posts in advance and use platform-specific features.

## 2. Mobilize Volunteers Effectively

According to "**Example Campaign 1**", organizing volunteers into small teams with clear responsibilities increased participation rates by 30%.

## 3. Create Compelling Visual Stories

Visual content performs 40% better than text-only communications. The "**Example Campaign 2**" used short videos to showcase impact.

These strategies have proven successful across multiple campaigns and can be adapted to your specific needs and resources."""
        })

def handler(event, context):
    """Netlify function handler"""
    
    # Parse the incoming request
    path = event['path'].replace('/.netlify/functions/api', '/api')
    method = event['httpMethod']
    
    # Only handle POST requests to /api/advice
    if method == 'POST' and path == '/api/advice':
        try:
            # Parse the request body
            body = json.loads(event['body'])
            query = body.get('query', '')
            fast_mode = body.get('fast', False)
            
            # In a production environment, you would connect to your actual
            # vector database and use real API keys here
            
            # For the demo, we'll use our mock implementations
            model = MockModel("demo-fast" if fast_mode else "demo-standard")
            mock_index = MockIndex()
            advisor = CampaignAdvisor(mock_index, model=model, use_query_enhancement=True)
            
            # Generate advice
            advice = advisor.get_advice(query)
            
            # Return the response
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': json.dumps({
                    'advice': advice.advice,
                    'references': advice.references
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': f'An error occurred: {str(e)}'
                })
            }
    
    # Return 404 for any other request
    return {
        'statusCode': 404,
        'body': json.dumps({
            'error': 'Not found'
        })
    }