import json
from collections import Counter
import os

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
    

test_format_test_dataset()