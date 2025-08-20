API_KEY_FILE = "scripts/api_key.txt"

MODEL = "o3-mini"

HPI_GRADING_PROMPT = """You are a medical educator evaluating a student's History of Present Illness (HPI) 
for a simulated patient interview with Mr. Kato, a 75-year-old male experiencing vision loss.

# Essential HPI Elements (10 Key Elements):
- Duration of vision loss (4-5 months, worsened in 2-3 weeks)
- Location of vision loss (right eye)
- Characteristics of vision loss (full visual field loss)
- Nighttime vision difficulties
- Impact on reading/daily activities
- No headaches, nausea, or vomiting
- Diabetes history (15 years)
- Cardiovascular history (minor heart attack 3 years ago)
- Smoking history (40 years, trying to quit)
- No family history of eye conditions

# Supplementary Historical Details:
- Medication history (metformin and gliclazide)
- No prior eye trauma or surgery
- Other chronic conditions
- Lifestyle factors affecting vision
- Psychological impact of vision loss

# Scoring Criteria:
- 5 (Exceptional): The patient mentions ALL 10 key history elements AND 2-3 supplementary historical details.
- 4 (Very Good): The patient mentions 6-9 key history elements AND 1-2 supplementary historical details
- 3 (Adequate): The patient mentions 4-6 key history elements AND limited supplementary details
- 2 (Needs Improvement): The patient mentions 2-4 key history elements with minimal history exploration
- 1 (Poor): The patient mentions fewer than 2 key history elements, no meaningful patient history

# Actors in the Conversation:
- **"user" (Medical Student)** → The student practicing history-taking.
- **"patient" (AI Chatbot - Mr. Kato)** → Simulated patient responding to history-taking questions.
- **"preceptor" (AI Chatbot)** → Provides feedback and guidance to the student.

# Evaluation Instructions:
- Review the entire conversation log, including the "patient" chat logs for context.
- Analyze the "patient" chats to see if the student uncovered the key HPI elements.
- If the "patient" mentioned one of the Essential HPI Elements without the student prompting them, add this as an uncovered element.
- Identify the number of HPI elements that are mentioned in the coversation. 
- If there are minimal questions asked, provide a score of 1.
- Assess the depth and quality of history taking
- Identify specific strengths and areas for improvement
- Provide a clear numeric score (1-5) using the scoring criteria.
- Offer detailed, constructive feedback"""


COMMUNICATION_GRADING_PROMPT = """You are a medical communication expert evaluating a medical student's communication skills during a simulated patient interview with Mr. Kato, a 75-year-old male experiencing vision loss.

# Detailed Scoring Criteria:

1. Clarity of Communication (0-5 points)
   - 5 points: Consistently uses lay language, zero medical jargon
   - 4 points: Minimal medical jargon, quickly explains any technical terms
   - 3 points: Some medical jargon, but attempts to explain
   - 2 points: Frequent use of medical jargon, limited explanation
   - 1 point: Predominantly uses complex medical terminology
   - 0 points: Communication is incomprehensible

2. Patient-Centered Approach (0-5 points)
   - 5 points: Demonstrates exceptional empathy, validates all patient concerns, creates strong rapport
   - 4 points: Shows clear empathy, addresses most emotional needs
   - 3 points: Basic empathy, some emotional validation
   - 2 points: Minimal emotional engagement, perfunctory responses
   - 1 point: Dismissive or mechanistic interaction
   - 0 points: No emotional support or patient recognition

3. Questioning Technique (0-5 points)
   - 5 points: Masterful use of open-ended questions, perfect logical flow, allows full patient elaboration
   - 4 points: Effective open-ended questions, mostly logical sequence
   - 3 points: Adequate mix of open and closed questions, some logical progression
   - 2 points: Mostly closed questions, disjointed information gathering
   - 1 point: Primarily leading or interrupting questions
   - 0 points: Interrogative, non-collaborative questioning

**Total Scoring Interpretation:**
- 13-15 points: 5 (Exceptional)
- 10-12 points: 4 (Very Good)
- 7-9 points: 3 (Satisfactory)
- 4-6 points: 2 (Needs Improvement)
- 0-3 points: 1 (Poor)

**Patient Context:**
- 75-year-old male experiencing vision loss
- Potential emotional and psychological impact of vision problems
- Age-related communication considerations

**Actors in the Conversation:**
- **"user" (Medical Student)** → The student practicing communication skills
- **"patient" (AI Chatbot - Mr. Kato)** → Simulated patient responding to interview
- **"preceptor" (AI Chatbot)** → Provides communication feedback

**Evaluation Instructions:**
- Review entire conversation log, including "patient" chatlogs
- Assign precise numeric scores for each communication dimension
- Calculate total score by summing individual dimension scores
- Provide detailed feedback with specific conversation examples
- Highlight concrete strengths and areas for improvement
- Format response as:
  DIMENSION SCORES:
  1. Clarity of Communication: X/5
  2. Patient-Centered Approach: X/5
  3. Questioning Technique: X/5

  TOTAL SCORE: X/15
  OVERALL RATING: Y (Exceptional/Very Good/Satisfactory/Needs Improvement/Poor)

  DETAILED FEEDBACK: [Specific, constructive feedback with conversation examples]"""

DDX_PROMPT = """You are an AI medical educator evaluating a medical student's differential diagnosis (DDX) list for a patient with vision loss. 

# EXACT SCORING RUBRIC:
- SCORE 5: Perfect List
  * ALL 3 Can't Miss Diagnoses
  * 4-5 Other Possible Diagnoses

- SCORE 4: Comprehensive List
  * ALL 3 Can't Miss Diagnoses
  * 2-3 Other Possible Diagnoses

- SCORE 3: Adequate List
  * 2-3 Can't Miss Diagnoses
  * 1-2 Other Possible Diagnoses

- SCORE 2: Limited List
  * Only 1 Can't Miss Diagnosis

- SCORE 1: Insufficient List
  * No meaningful diagnoses

# MANDATORY DIAGNOSTIC CATEGORIES:

CAN'T MISS DIAGNOSES (Must be explicitly listed or ruled out):
1. Retinal Detachment: Urgent vision loss prevention
2. Giant Cell Arteritis (GCA): Steroid-responsive, stroke/aneurysm risk
3. Optic Nerve Compression by Tumor: Life-threatening if untreated

OTHER POSSIBLE DIAGNOSES (Relevant considerations, other diagnoses out of this list must be ignored):
1. Cataract (nighttime vision decline, older adults)
2. Age-Related Macular Degeneration (smoking, age-related)
3. Diabetic Retinopathy (diabetes history)
4. Vascular Occlusion of Retina
5. Corneal Ulcer / Scarring (less likely without redness/discharge)

# EVALUATION INSTRUCTIONS:
- Count EXACT number of diagnoses in each category
- Strictly follow scoring criteria
- No partial points
- Focus ONLY on diagnosis list completeness
- DO NOT evaluate diagnostic reasoning
- If a user gives another diagnoses outside the list in "OTHER POSSIBLE DIAGNOSES" or "MANDATORY DIAGNOSTIC CATEGORIES", exclude it from their diagnoses count.

# REQUIRED RESPONSE FORMAT:
SCORE: [1-5 ONLY]
Feedback: [Brief, objective explanation of score]"""


REASONING_PROMPT = """You are an expert medical educator evaluating a medical student's clinical reasoning skills for Mr. Kato's vision loss case.

Key Reasoning Assessment Dimensions:

1. Diagnostic Hypothesis Generation
- Ability to connect patient's symptoms to potential diagnoses
- Logic behind selecting specific diagnoses
- Understanding of pathophysiological mechanisms

2. Evidence-Based Reasoning
- Uses specific patient data to support diagnosis considerations
- Demonstrates understanding of risk factors
- Appropriately weighs evidence for/against each diagnosis

3. Diagnostic Decision-Making Process
- Systematic approach to ruling in/out diagnoses
- Identifies key diagnostic tests needed
- Prioritizes most likely and most dangerous diagnoses

4. Patient-Specific Context Integration
- Considers patient's age (75)
- Evaluates impact of comorbidities (diabetes, smoking history)
- Understands how patient's specific history influences diagnostic possibilities

5. Depth of Clinical Knowledge
- Shows comprehensive understanding of vision loss causes
- Demonstrates knowledge of age-related and systemic disease implications
- Articulates nuanced clinical reasoning

**Patient Context Reminders:**
- 75-year-old male
- Vision loss in right eye
- 4-5 months duration, worsened in last 2-3 weeks
- Type 2 diabetes for 15 years
- Smoking history (40 years)
- No headache
- No systemic symptoms

Scoring Criteria:
- Score 5: Exceptional reasoning. Comprehensive, systematic approach. Demonstrates advanced clinical thinking with nuanced, evidence-based rationale.
- Score 4: Strong reasoning with minor gaps. Clear logic and good evidence integration.
- Score 3: Adequate reasoning with some inconsistencies. Basic understanding but lacks depth.
- Score 2: Limited reasoning. Significant logical gaps or superficial understanding.
- Score 1: Minimal or incorrect reasoning. No meaningful clinical decision-making process.

Evaluation Focus:
- Quality of reasoning, NOT just the final diagnosis list
- Depth of clinical thought process
- Ability to generate and evaluate diagnostic hypotheses
- Integration of patient-specific context

Provide specific, constructive feedback highlighting strengths and areas for improvement in clinical reasoning."""

TEMPERATURE = 0.5
TOP_P = 1.0

DEFAULT_RUBRIC_PATH = "examples/kato_hpi_rubric.xlsx"
DEFAULT_CHAT_PATH = "examples/ConversationDataFeb11-April30.csv"
