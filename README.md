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

"hpi_feedback": "Your HPI questioning captured only a few of the 10 essential elements. You asked about laterality (“is it only in your right eye?”), the impact on the patient’s life (“how has this impacted your life?”), and family history of eye disease. However, many critical aspects were not addressed. You did not ask about the duration of the vision loss (which should capture that it started 4–5 months ago with notable worsening in the last 2–3 weeks), the specific characteristics of the vision loss (i.e. full visual field loss), or if the patient has increased difficulty with tasks such as night driving or reading. You also did not explicitly inquire about his detailed diabetes history (15 years of type 2 diabetes) and cardiovascular history (minor heart attack 3 years ago), nor his smoking history. Focusing on these areas during the interview would improve your history taking to ensure all 10 key elements are systematically and explicitly addressed."

Read the full report here: `Mr. Kato AI Conversation Grader REPORT.pdf`.
