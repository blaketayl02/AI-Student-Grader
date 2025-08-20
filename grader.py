import argparse
import pandas as pd
import datetime
import os
import json
import config
from openai import OpenAI
import concurrent.futures

def get_api_key():
    try:
        with open(config.API_KEY_FILE, 'r', encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Error: API key file not found.")
        exit(1)

client = OpenAI(api_key=get_api_key())

def log_interaction(log_file, messages, response):
    with open(log_file, 'a', encoding="utf-8") as log:
        log.write("----- Interaction -----\n")
        for message in messages:
            log.write(f"{message['role']}: {message['content']}\n")
        log.write(f"Response: {response}\n")
        log.write("-----------------------\n\n")

#Normalize the score such that its in a 1-5 int range
def validate_score(score):
    try:
        normalized_score = int(''.join(filter(str.isdigit, str(score))))
    except ValueError:
        return 0
    
    if normalized_score > 5:
        if normalized_score > 45:
            normalized_score = normalized_score % 10
        else:
            normalized_score = normalized_score // (normalized_score // 5)
    
    return max(1, min(5, normalized_score))

#handle multiple attempts for grading if reattempts are needed
def grade_with_retry(grade_function, conversation, context, actor_name, log_file, max_retries=3):
    for attempt in range(max_retries):
        try:
            return grade_function(conversation, context, actor_name, log_file)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {actor_name}: {str(e)}")
            if attempt == max_retries - 1:
                return "0\nUnable to process evaluation after multiple attempts"

#hpi grading section
def grade_hpi(conversation, context, actor_name, log_file):
    messages = [
        {"role": "system", "content": config.HPI_GRADING_PROMPT},
        {"role": "user", "content": f"""
        Use the following context (preceptor and patient responses) to aid in grading. If the patient mentions any HPI element it counts as the student uncovering that information:
        {context}
        
        Evaluate the HPI section from user {actor_name}:
        {conversation}
        
        IMPORTANT: Your score MUST be between 1 and 5 ONLY. 
        Format your response as:
        SCORE: X
        Feedback: [Your detailed feedback]
        """}
    ]
    
    response = client.chat.completions.create(
        model=config.MODEL,
        messages=messages,
        reasoning_effort="high",
        top_p=config.TOP_P,
    )
    
    score_text = response.choices[0].message.content.strip()
    log_interaction(log_file, messages, score_text)
    
    lines = score_text.split('\n')
    if not lines:
        raise ValueError("Empty response from AI")
    
    try:
        score_line = next((line for line in lines if 'SCORE:' in line.upper()), lines[0])
        score = int(''.join(filter(str.isdigit, score_line)))
    except (ValueError, IndexError):
        score = 0
    
    validated_score = validate_score(score)
    
    feedback = '\n'.join(lines[1:]) if len(lines) > 1 else "No detailed feedback provided"
    
    return f"{validated_score}\n{feedback}"

#communication grading
def grade_communication(conversation, context, actor_name, log_file):
    messages = [
        {"role": "system", "content": config.COMMUNICATION_GRADING_PROMPT},
        {"role": "user", "content": f"""
        Use the following context (preceptor and patient responses) to aid in grading:
        {context}
        
        Evaluate the communication skills of user {actor_name}:
        {conversation}
        
        IMPORTANT: Your score MUST be between 1 and 5 ONLY. 
        Format your response as:
        SCORE: X
        Feedback: [Your detailed feedback]
        """}
    ]
    
    response = client.chat.completions.create(
        model=config.MODEL,
        messages=messages,
        reasoning_effort="high",
        top_p=config.TOP_P,
    )
    
    score_text = response.choices[0].message.content.strip()
    log_interaction(log_file, messages, score_text)
    
    lines = score_text.split('\n')
    if not lines:
        raise ValueError("Empty response from AI")
    
    try:
        score_line = next((line for line in lines if 'SCORE:' in line.upper()), lines[0])
        score = int(''.join(filter(str.isdigit, score_line)))
    except (ValueError, IndexError):
        score = 0
    
    validated_score = validate_score(score)
    
    feedback = '\n'.join(lines[1:]) if len(lines) > 1 else "No detailed feedback provided"
    
    return f"{validated_score}\n{feedback}"

#ddx grading
def grade_ddx(conversation, context, actor_name, log_file):
    messages = [
        {"role": "system", "content": config.DDX_PROMPT},
        {"role": "user", "content": f"""
        Use the following context (preceptor interactions) to aid in grading:
        {context}
        
        Evaluate the Differential Diagnosis (DDX) list from user {actor_name}:
        {conversation}
        
        IMPORTANT: Your score MUST be between 1 and 5 ONLY. 
        Format your response as:
        SCORE: X
        Feedback: [Your detailed feedback]
        """}
    ]
    
    response = client.chat.completions.create(
        model=config.MODEL,
        messages=messages,
        reasoning_effort="high",
        top_p=config.TOP_P,
    )
    
    score_text = response.choices[0].message.content.strip()
    log_interaction(log_file, messages, score_text)
    
    lines = score_text.split('\n')
    if not lines:
        raise ValueError("Empty response from AI")
    
    try:
        score_line = next((line for line in lines if 'SCORE:' in line.upper()), lines[0])
        score = int(''.join(filter(str.isdigit, score_line)))
    except (ValueError, IndexError):
        score = 0
    
    validated_score = validate_score(score)
    
    feedback = '\n'.join(lines[1:]) if len(lines) > 1 else "No detailed feedback provided"
    
    return f"{validated_score}\n{feedback}"

#reasoning grading
def grade_reasoning(conversation, context, actor_name, log_file):
    messages = [
        {"role": "system", "content": config.REASONING_PROMPT},
        {"role": "user", "content": f"""
        Use the following context (preceptor interactions) to aid in grading:
        {context}
        
        Evaluate the clinical reasoning skills of user {actor_name}:
        {conversation}
        
        IMPORTANT: Your score MUST be between 1 and 5 ONLY. 
        Format your response as:
        SCORE: X
        Feedback: [Your detailed feedback]
        """}
    ]
    
    response = client.chat.completions.create(
        model=config.MODEL,
        messages=messages,
        reasoning_effort="high",
        top_p=config.TOP_P,
    )
    
    score_text = response.choices[0].message.content.strip()
    log_interaction(log_file, messages, score_text)
    
    lines = score_text.split('\n')
    if not lines:
        raise ValueError("Empty response from AI")
    
    try:
        score_line = next((line for line in lines if 'SCORE:' in line.upper()), lines[0])
        score = int(''.join(filter(str.isdigit, score_line)))
    except (ValueError, IndexError):
        score = 0
    
    validated_score = validate_score(score)
    
    feedback = '\n'.join(lines[1:]) if len(lines) > 1 else "No detailed feedback provided"
    
    return f"{validated_score}\n{feedback}"

#process dataset and make API calls synchronously
def process_chat_file(chat_file, output_file):
    df = pd.read_csv(chat_file)
    log_file = os.path.splitext(output_file)[0] + ".log"

    hpi_roles = ['user']
    communication_roles = ['user']
    ddx_roles = ['user-level2']
    reasoning_roles = ['user-level2']
    context_roles = ['patient', 'preceptor-level2']
    
    grouped_hpi = df[df['ROLE'].isin(hpi_roles)].groupby('actor.name')['CONTENT'].apply(lambda x: "\n".join(x)).reset_index()
    grouped_communication = df[df['ROLE'].isin(communication_roles)].groupby('actor.name')['CONTENT'].apply(lambda x: "\n".join(x)).reset_index()
    grouped_ddx = df[df['ROLE'].isin(ddx_roles)].groupby('actor.name')['CONTENT'].apply(lambda x: "\n".join(x)).reset_index()
    grouped_reasoning = df[df['ROLE'].isin(reasoning_roles)].groupby('actor.name')['CONTENT'].apply(lambda x: "\n".join(x)).reset_index()
    
    context_data = "\n".join(df[df['ROLE'].isin(context_roles)]['CONTENT'])
    
    output_data = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        #Iterate through unique actors across all evaluation types
        unique_actors = set(grouped_hpi['actor.name']).union(
            set(grouped_communication['actor.name'])).union(
            set(grouped_ddx['actor.name'])).union(
            set(grouped_reasoning['actor.name'])
        )
        
        for actor_name in unique_actors:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time} - Processing evaluations for user {actor_name}...")
            
            #Prepare futures for each evaluation type
            futures = {}
            
            #HPI Grading
            hpi_match = grouped_hpi[grouped_hpi['actor.name'] == actor_name]
            if not hpi_match.empty:
                futures['hpi'] = executor.submit(
                    grade_with_retry, 
                    grade_hpi, 
                    hpi_match.iloc[0]['CONTENT'], 
                    context_data, 
                    actor_name, 
                    log_file
                )
            
            #Communication Grading
            comm_match = grouped_communication[grouped_communication['actor.name'] == actor_name]
            if not comm_match.empty:
                futures['communication'] = executor.submit(
                    grade_with_retry, 
                    grade_communication, 
                    comm_match.iloc[0]['CONTENT'], 
                    context_data, 
                    actor_name, 
                    log_file
                )
            
            #DDX Grading
            ddx_match = grouped_ddx[grouped_ddx['actor.name'] == actor_name]
            if not ddx_match.empty:
                futures['ddx'] = executor.submit(
                    grade_with_retry, 
                    grade_ddx, 
                    ddx_match.iloc[0]['CONTENT'], 
                    context_data, 
                    actor_name, 
                    log_file
                )
            
            #Reasoning Grading
            reasoning_match = grouped_reasoning[grouped_reasoning['actor.name'] == actor_name]
            if not reasoning_match.empty:
                futures['reasoning'] = executor.submit(
                    grade_with_retry, 
                    grade_reasoning, 
                    reasoning_match.iloc[0]['CONTENT'], 
                    context_data, 
                    actor_name, 
                    log_file
                )
            
            #Process results
            result_data = {
                'actor.name': actor_name,
                'hpi_score': 0,
                'hpi_feedback': "No HPI evaluation",
                'communication_score': 0,
                'communication_feedback': "No communication evaluation",
                'ddx_score': 0,
                'ddx_feedback': "No DDX evaluation",
                'reasoning_score': 0,
                'reasoning_feedback': "No reasoning evaluation"
            }
            
            #Collect and parse results from futures
            for eval_type, future in futures.items():
                try:
                    evaluation = future.result()
                    lines = evaluation.split('\n')
                    
                    try:
                        score = int(lines[0])
                        feedback = '\n'.join(lines[1:])
                    except (ValueError, IndexError):
                        score = 0
                        feedback = "Unable to parse evaluation"
                    
                    #Update result dictionary based on evaluation type
                    if eval_type == 'hpi':
                        result_data['hpi_score'] = score
                        result_data['hpi_feedback'] = feedback
                    elif eval_type == 'communication':
                        result_data['communication_score'] = score
                        result_data['communication_feedback'] = feedback
                    elif eval_type == 'ddx':
                        result_data['ddx_score'] = score
                        result_data['ddx_feedback'] = feedback
                    elif eval_type == 'reasoning':
                        result_data['reasoning_score'] = score
                        result_data['reasoning_feedback'] = feedback
                
                except Exception as e:
                    print(f"Error processing {eval_type} evaluation for {actor_name}: {str(e)}")
            
            output_data.append(result_data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"HPI, Communication, DDX, and Reasoning grading completed. Results saved to {output_file}. Log saved to {log_file}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Grade HPI, Communication, DDX, and Reasoning skills of medical student interactions')
    parser.add_argument('--chat', type=str, default=config.DEFAULT_CHAT_PATH, help='The path to the chat data file')
    parser.add_argument('--output', type=str, default='05_05_25.json', help='The path to save the graded output file')
    args = parser.parse_args()
    
    process_chat_file(args.chat, args.output)