
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

## Remote Inference via Inference Providers
def get_llama_completion(
    prompt: str,
    system_message: str = "You are a helpful AI assistant that provides accurate and concise answers.",
    # later put a jinja template here/can be made dynamic
):
    try:
        client = InferenceClient(
            provider="auto",
            api_key=os.environ["HUGGINGFACE_TOKEN"],
        )

        completion = client.chat.completions.create( # chat completion does not support summ tasks
            model="meta-llama/Llama-3.3-70B-Instruct",
            # model="facebook/bart-large-cnn",
            # Error making inference request: Model 'facebook/bart-large-cnn' doesn't support task 'conversational'. Supported tasks: 'summarization', got: 'conversational'
            # max_new_tokens=100,
            # temperature=0.7,
            # top_p=0.95,
            # top_k=40,
            # repetition_penalty=1.0,
            # max_time=60,
            # stop_sequences=["\n\n"],
            # stop_token_ids=[198],
            # stop_strings=["\n\n"],
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )

        return completion.choices[0].message

    except KeyError:
        print("❌ Error: HUGGINGFACE_TOKEN environment variable not found")
        return None
    except Exception as e:
        print(f"❌ Error making inference request: {str(e)}")
        return None


if __name__ == "__main__":
    response = get_llama_completion("What is the capital of France?")
    if response:
        print("Full response:", response)
        print("Content:", response.content)
