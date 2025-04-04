import json
from collections import Counter
import os
import random

NQ_dataset_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "dataset", "simplified-nq-train.jsonl")
)

# print(f"Resolved dataset path: {NQ_dataset_path}")

#Extracts the first n elements from a large JSON file.
def get_first_n_elements(input_file, output_file_name, n=10):
    print(f"Extracting the frist {n} elements... ")
    
    if not os.path.exists(input_file):
        print(f"Error: File not found -> {input_file}")
        return
    
    output_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "dataset", output_file_name)
    )
    
    with open(input_file, "r", encoding="utf-8") as f:
        data = [json.loads(line) for _, line in zip(range(n), f)]  # Load only the first 'n' lines
    
    # Save the extracted data
    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(data, out, indent=4)

    print(f"Saved first {n} elements to {output_file}")

def count_each_wiki_occurence(input_file):
    
    print(f"Counting number of questions for each wiki doc in {input_file}... ")
        
    if not os.path.exists(input_file):
        print(f"Error: File not found -> {input_file}")
        return

    url_counter = Counter()

    # Read the JSON file and process it
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Start counting...")
    # Count occurrences of each document URL
    for entry in data:
        doc_url = entry["document_url"]
        url_counter[doc_url] += 1

    # Display the most common document URLs
    print("Top 10 most common document URLs:")
    for url, count in url_counter.most_common(10):
        print(f"{url}: {count} occurrences")

    # Save the URL count data to a JSON file
    output_file = "document_url_counts_1.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(url_counter, f, indent=4)

    print(f"\nDocument URL occurrences saved to {output_file}")

def format_test_dataset(url_count_filename, input_file,output_file):
    
    #Get the top_10 frequent urls
    with open(url_count_filename, "r", encoding="utf-8") as f:
        url_counts = json.load(f)

    top_10_urls = sorted(url_counts, key=url_counts.get, reverse=True)[:10]
    print(f"The first 10 urls are {top_10_urls}")
    
    
    #extract questions for those urls and save to a new file with new format
    with open(input_file, "r", encoding="utf-8") as f:
        doc_data = json.load(f)

    organized_data = {}

    # Extract relevant entries and organize them
    for eachQuestion in doc_data:
        doc_url = eachQuestion["document_url"]
        
        if doc_url in top_10_urls:
            doc_text = eachQuestion["document_text"]
            question_text = eachQuestion["question_text"]
            long_answer_candidates = eachQuestion.get("long_answer_candidates", [])
            annotations = eachQuestion.get("annotations", [])
            example_id = eachQuestion["example_id"]

            # Initialize the document entry if it does not exist
            if doc_url not in organized_data:
                organized_data[doc_url] = {
                    "document_url": doc_url,
                    "document_text": doc_text,
                    "questions": []
                }

            # Append question details
            organized_data[doc_url]["questions"].append({
                "question_text": question_text,
                "long_answer_candidates":long_answer_candidates,
                "annotations": annotations,
                "example_id": example_id
            })
    
    # Convert dictionary values to a list
    final_output = list(organized_data.values())
    
    output_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "dataset", output_file)
    )

    # Save the structured dataset as a JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    print(f"Organized dataset for top 10 document URLs saved to {output_file}")


def has_valid_annotation(entry):
    for annotation in entry.get("annotations", []):
        long_ans = annotation.get("long_answer", {})
        short_ans = annotation.get("short_answers", [])

        valid_long = long_ans.get("start_token", -1) != -1 and long_ans.get("end_token", -1) != -1
        valid_short = any("start_token" in ans and "end_token" in ans for ans in short_ans)

        if valid_long or valid_short:
            return True
    return False


def get_test_dataset(filename,output_filename,dataset_size):
    
    with open(filename, "r") as f:
        data = json.load(f)
    
    print("Start Filtering questions with no gold answer")
    #Filter valid samples: has gold answer 
    valid_samples = [entry for entry in data if has_valid_annotation(entry)]
    print(f"{len(valid_samples)} has gold answers")

    print(f"Start Random selecting {dataset_size} samples")
    unique_doc_map = {}
    for sample in valid_samples:
        doc_url = sample.get("document_url")
        if doc_url not in unique_doc_map:
            unique_doc_map[doc_url] = sample
    
    # Randomly {dataset_size} sample  with unique document_url
    unique_samples = list(unique_doc_map.values())
    if len(unique_samples) < dataset_size:
        raise ValueError("Not enough unique document_url entries with valid annotations.")

    sampled = random.sample(unique_samples, dataset_size)
    
    #Saved to output file
    with open(output_filename, "w") as f:
        json.dump(sampled, f, indent=2)
    


def get_N_sample_from_file(in_filename,dataset_size,output_filename):
    
    with open(in_filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if len(data) < dataset_size:
        raise ValueError(f"Only {len(data)} items in the file, but you asked for {N}.")

    sampled_data = random.sample(data, dataset_size)
    
    # Save the sampled objects into a new file
    with open(output_filename, "w") as f:
        json.dump(sampled_data, f, indent=2)

    print(f"Successfully saved {dataset_size} random samples to file {output_filename}")

    

def test_get_first_n_elements(n):
    #n=100
    get_first_n_elements(NQ_dataset_path, f"train_file_sample_{n}.json",n)


def test_count_each_wiki_occurence():
    
    sample_file_name = 'train_file_sample_10000.json'
    sample_file_name = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "dataset", sample_file_name)
    )

    count_each_wiki_occurence(sample_file_name)

def test_format_test_dataset():
    
    url_count_filename = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "dataset", 'document_url_counts.json')
    )
    input_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "dataset", 'train_file_sample_10000.json')
    )
    output_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "dataset", 'train_file_sample_selected.json')
    )
    
    format_test_dataset(url_count_filename, input_file,output_file)
    

def test_get_test_dataset():
    
    dataset_size = 100
    input_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "dataset", 'train_file_sample_10000.json')
    )
    output_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "dataset", f'test_file_{dataset_size}.json')
    )
    
    get_test_dataset(input_file,output_file,dataset_size)

def test_get_N_sample_from_file():
    
    dataset_size = 30
    input_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "dataset", 'gold_test_file_100.json')
    )
    output_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "dataset", f'gold_test_file_{dataset_size}.json')
    )
    get_N_sample_from_file(input_file,dataset_size,output_file)

test_get_N_sample_from_file()