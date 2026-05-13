import cv2
import base64
import requests
import json
import os
import argparse

def identify_cat(image_path, api_url):
    """
    Sends an image to the gemma4:e2b API to identify if a cat is present.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found. Please provide a valid image path.")
        return

    # 1. Read the image using OpenCV
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not decode image at '{image_path}'.")
        return

    # 2. Encode the image to base64 format
    # We encode as JPEG to keep the payload size reasonable
    _, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    # 3. Prepare the API payload
    # Assuming an OpenAI-compatible multimodal API structure
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gemma4:e2b",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": "Is there a cat in this image? If so, please describe it in detail."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }

    # 4. Execute the API call
    try:
        print(f"Connecting to {api_url}...")
        print("Sending image data...")
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        # Check if the request was successful
        response.raise_for_status()
        
        result = response.json()
        
        # 5. Parse and display the result
        # The Gemma model may put the reasoning in 'reasoning' field and content in 'content' field
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0]['message']
            
            # Try to get the answer from content or reasoning field
            answer = message.get('content', '').strip() or message.get('reasoning', '').strip()
            
            if answer:
                print("\n" + "="*30)
                print("AI ANALYSIS RESULT")
                print("="*30)
                print(answer)
                print("="*30 + "\n")
                
                # Show finish reason to indicate if response was truncated
                finish_reason = result['choices'][0].get('finish_reason', 'unknown')
                if finish_reason == 'length':
                    print("(Note: Response was truncated due to token limit)\n")
            else:
                print("Error: No response content received.")
                print("Full response:", json.dumps(result, indent=2))
        else:
            print("Error: Unexpected API response format.")
            print("Available keys in response:", list(result.keys()))

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.text:
            print(f"Server response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the server. Check the URL and your internet connection.")
    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gemma 4:e2b Image Identification Tool")
    parser.add_argument(
        "--api-url",
        type=str,
        default="",
        help="API endpoint URL (default: https://ai.server/v1/chat/completions)"
    )
    parser.add_argument(
        "--image",
        type=str,
        default="cat.jpg",
        help="Path to the image file to analyze (default: cat.jpg)"
    )
    
    args = parser.parse_args()
    
    print("--- Gemma 4:e2b Image Identification Tool ---")
    identify_cat(args.image, args.api_url)
