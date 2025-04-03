import json
import os


import json

def clean_token(token):
    """Remove HTML-style tags from tokens like <P>, <Table>, etc."""
    return token if not (token.startswith('<') and token.endswith('>')) else ''

def get_all_gold_answers(input_path, output_path):
    
    with open(input_path, 'r', encoding='utf-8') as f:
        all_docs = json.load(f)
    
    for idx, eachDoc in enumerate(all_docs):
        
        print(f"Processing document {idx} : {eachDoc['document_url']}")
        
        #HTML to tokens
        tokens = eachDoc['document_text'].split() 
        
        #gind gold answer for each question
        for eachQuestion in eachDoc["questions"]:
            gold_long_answer,gold_short_answers = extract_gold_answer_for_question(tokens,eachQuestion)
            
            # Append to question
            eachQuestion["gold_answer"] = {
                "long_answer": gold_long_answer,
                "short_answers": gold_short_answers
            }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_docs, f, indent=2, ensure_ascii=False)
        
    print(f" Gold answers of {input_path} added and saved to {output_path}.")
    

def extract_gold_answer_for_question(tokens,in_question):
    
    annotation = in_question['annotations'][0] if in_question.get('annotations') else {}
        
    # Long Answer
    long_answer = None
    long_start = annotation.get('long_answer', {}).get('start_token', -1)
    long_end = annotation.get('long_answer', {}).get('end_token', -1)
    if long_start >= 0 and long_end > long_start:
        long_span_tokens = tokens[long_start:long_end]
        long_answer = ' '.join([clean_token(t) for t in long_span_tokens if clean_token(t)])

    # Short Answers
    short_answers = []
    for sa in annotation.get('short_answers', []):
        sa_start = sa.get('start_token', -1)
        sa_end = sa.get('end_token', -1)
        if sa_start >= 0 and sa_end > sa_start:
            sa_tokens = tokens[sa_start:sa_end]
            short = ' '.join([clean_token(t) for t in sa_tokens if clean_token(t)])
            short_answers.append(short)

    return long_answer,short_answers
       


def test_get_all_gold_answers():
    
    test_file_name = 'train_file_sample_selected.json'
    test_file_name = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "dataset", test_file_name)
    )
    
    output_file = 'gold_train_file_sample_selected.json'
    output_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "dataset",output_file)
    )

    get_all_gold_answers(test_file_name, output_file)
    
    

test_get_all_gold_answers()