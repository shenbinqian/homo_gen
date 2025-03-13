import ast

def process_homophone_data(filename='./freq_candidates/freq_error_words_homo.txt'):
    """
    Process the freq_error_words_homo.txt file:
    1. Read each line (containing a list of tuples)
    2. Sort each list in descending order based on the second value
    3. Write the sorted lists back to the file
    4. Create separate text files with just the words
    """
    # Read the content of the file
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    sorted_lists = []
    
    # Process each line (each line is a list of tuples)
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or not (line.startswith('[') and line.endswith(']')):
            continue
        
        try:
            # Parse the list string to get actual tuples
            tuple_list = ast.literal_eval(line)
            
            # Sort the list in descending order based on second value
            sorted_tuple_list = sorted(tuple_list, key=lambda x: x[1], reverse=True)
            
            # Add to our collection of sorted lists
            sorted_lists.append(sorted_tuple_list)
            
            # Create a file for this group with just the words
            filename = f"./freq_candidates/homophone_group_{i+1}.txt"
            with open(filename, 'w', encoding='utf-8') as outfile:
                # Write each word (first element of tuple) to the file
                for word, _ in sorted_tuple_list:
                    outfile.write(word + '\n')
                    
            print(f"Created {filename} with {len(sorted_tuple_list)} words")
                    
        except Exception as e:
            print(f"Error processing line {i+1}: {e}")
    
    # Write the sorted lists back to the file
    with open('./freq_candidates/freq_error_words_homo_sorted.txt', 'w', encoding='utf-8') as outfile:
        for sorted_list in sorted_lists:
            outfile.write(str(sorted_list) + '\n')
    
    print(f"Created freq_error_words_homo_sorted.txt with sorted lists")


if __name__ == "__main__":
    process_homophone_data()