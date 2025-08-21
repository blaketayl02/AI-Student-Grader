# AI-Student-Grader
Using OpenAI's o3-mini model to grade student chat data from an application called 'Mr. Kato'; a virtual AI patient which they can chat with to develop their clinical skills.

This code takes conversation data, and chains multiple API calls to grade students in 4 different sections following a pre-made rubric. This was a prototype which was planned to be incorporated into the application after they finish their chat.

## How it works:
<img width="1380" height="860" alt="Flowchart" src="https://github.com/user-attachments/assets/4d7146f5-a957-47e5-8e20-0fbcb73154dc" />

Due to the way the API calls were chained, it only took around 15 seconds per student and cost $0.04 per evaluation in API usage.

## Results:
- HPI Score: ICC: 0.8869 95% Confidence Interval: (0.9353, 0.6748) 

- Communication Score: ICC: 0.8643 95% Confidence Interval: (0.9204, 0.5997) 

- DDX Score: ICC: 1.0000 95% Confidence Interval: (1.0000, 1.0000) 

- Reasoning Score: ICC: 0.9889 95% Confidence Interval: (0.9943, 0.9713)
  
## Example Output:

<img width="464" height="182" alt="image" src="https://github.com/user-attachments/assets/0e456187-862b-435f-8421-b57750c91d74" />

Read the full report here.
