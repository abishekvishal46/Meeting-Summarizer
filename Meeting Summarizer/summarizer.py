import openai
import json

#Set up your OpenAI API key
openai.api_key = 'use-the-api-key'

def summarize_meeting_transcript(transcript):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"""
    Analyze and summarize the meeting transcript in JSON format. Transcript:

    {transcript}

    Format:

    {{
        "MEET_INFO": [{{"MEMBERS": ["list of participants if not available then empty list"]}}],
        "SUMMARY": [
            {{
                "SUBHEADINGS": [
                    {{"subheading 1": "summarization 1"}},
                    ...
                    {{"subheading N": "summarization N"}}
                ]
            }}
        ]
    }} Note: Only generate the JSON text with the exact keys MEET_INFO, MEMBERS, SUMMARY, and SUBHEADINGS and generate more than 4 SUBHEADINGS.
    """}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,  # adjust token limit as needed
        n=1,
        temperature=0.6,  # adjust temperature for creativity
    )

    # Extract the summary from the response
    summary_json = response.choices[0].message['content'].strip()
    print(type(summary_json))
    # Parse the JSON response


    # Get token usage information
    prompt_tokens = response['usage']['prompt_tokens']
    completion_tokens = response['usage']['completion_tokens']
    total_tokens = response['usage']['total_tokens']

    # Calculate the cost
    cost_input = (prompt_tokens / 1000) * 0.0015
    cost_output = (completion_tokens / 1000) * 0.002
    total_cost = cost_input + cost_output

    return summary_json
