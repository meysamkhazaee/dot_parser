from process_graph import process_graph
import sys
import os

def main():
    
    # Handle command-line arguments or prompt the user for input
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter the path to the DOT file: ")
    
    root = os.path.dirname(__file__)

    full_path = os.path.join(root, file_path)
    full_path = os.path.normpath(full_path)
    file_name, file_ext = os.path.splitext(full_path)
    file_name = os.path.basename(file_name)

    # Ensure the output directory exists
    output_dir = os.path.join(os.path.dirname(__file__), f"output/{file_name}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    process_obj = process_graph(file_path)

    original_png_path = os.path.join(output_dir, f'{file_name}.png')
    process_obj.generate_png(original_png_path)

    process_obj.handle_function_call_subgraph(process_obj.root_graph)

    updated1_dot_path = os.path.join(output_dir, f'{file_name}_updated1.dot')
    process_obj.generate_dot(updated1_dot_path)

    updated1_png_path = os.path.join(output_dir, f'{file_name}_updated1.png')
    process_obj.generate_png(updated1_png_path)

    process_obj.combine_consecutive_nodes(process_obj.root_graph)
    
    updated2_dot_path = os.path.join(output_dir, f'{file_name}_updated2.dot')
    process_obj.generate_dot(updated2_dot_path)

    updated2_png_path = os.path.join(output_dir, f'{file_name}_updated2.png')
    process_obj.generate_png(updated2_png_path)

if __name__ == "__main__":
    main()
