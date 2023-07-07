import os
import sys
import re
from PyPDF2 import PdfMerger

def main(args):
    if len(args) < 1:
        source_folder = input("Enter source folder where ipynb files are located:")
    else:
        source_folder = args[0]
        if len(args) == 1:
            merge_all = True
        else:
            merge_all = False

    list_files = os.listdir(source_folder)

    def numeric_sort(string_list):
    # Function to extract the numeric part from a string
        def extract_number(string):
            match = re.search(r'\d+', string)
            if match:
                return int(match.group())
            return 0

        return sorted(string_list, key=extract_number)

    # Example usage
    # string_list = ['12name', '3name', '1name', '9name', '11name']
    sorted_list = numeric_sort(list_files)
    
    sorted_list = [file for file in sorted_list if file.endswith('.ipynb')]
    print(sorted_list)

    for file in sorted_list: 
        file_name = source_folder + file
        # Convert the notebook to PDF
        try:
           os.system(f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace '{file_name}'")
           os.system(f"jupyter nbconvert --to pdf '{file_name}'")

        except Exception as e:
            print(f"Error: {e}")
            continue

    pdf_files = os.listdir(source_folder)
    desired_extension = '.pdf' 
    filtered_files = [file for file in pdf_files if file.endswith(desired_extension)]
    
    filtered_files = numeric_sort(filtered_files)
    print(filtered_files)

    def merge_pdfs(output_path, *input_paths):
        merger = PdfMerger()
        for path in input_paths:
            print(path)
            merger.append(source_folder + path)
        merger.write(output_path)
        merger.close()

    if merge_all == True:
        # Example usage
        input_files = filtered_files
        output_file = source_folder + "activeloop_course_merged.pdf"

        merge_pdfs(output_file, *input_files)
    

if __name__ == '__main__':
    arguments = sys.argv[1: ]
    main(arguments)



    