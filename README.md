# AI-Student-Grader
Using OpenAI's o3-mini model to grade student chat data from an application called 'Mr. Kato'; a virtual AI patient which they can chat with to develop their clinical skills.

This code takes conversation data, and chains multiple API calls to grade students in 4 different sections following a pre-made rubric. This was a prototype which was planned to be incorporated into the application after they finish their chat.

How it works:
<img width="1380" height="860" alt="Flowchart" src="https://github.com/user-attachments/assets/4d7146f5-a957-47e5-8e20-0fbcb73154dc" />

Due to the way the API calls were chained, it only took around 15 seconds per student and cost $0.04 per evaluation in API usage.

Results:
<img width="298" height="201" alt="image" src="https://github.com/user-attachments/assets/fa68c17f-ee5c-4f57-8030-44e968855b86" />

Example Output:

<img width="464" height="182" alt="image" src="https://github.com/user-attachments/assets/0e456187-862b-435f-8421-b57750c91d74" />

Read the full report here.
