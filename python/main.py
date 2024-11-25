import nltk
from nltk import grammar, parse
import argparse
from nltk.parse.generate import generate
import shutil
from utils.nlp_parser import parse_to_procedure
from utils.nlp_data import retrieve_result
# Function to write content to a file
def write_file(file_name, content):
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(content)

# 2.1. Giai thuat sinh cau
def generate_sentences(grammar, max_sentences):
    generated_sentences = set()

    for sentence in generate(grammar, n=max_sentences):
        generated_sentences.add(' '.join(sentence))

    write_file('output/samples.txt', "\n".join(generated_sentences))
    print(f"Sample sentences written to output/samples.txt")

# 2.2. Phan tich cu phap 
def my_parser(grammar, input_file_name):
    with open(input_file_name, 'r', encoding="utf-8") as file:
        sentences = file.read()

    sentences = sentences.split('\n')
    parse_result = ""
    for sentence in sentences:
        sentence = sentence.replace("?", "").split()
        tree = grammar.parse_one(sentence)
        if tree is None:
            parse_result += "()\n"
        else:
            parse_result += str(tree) + "\n"
    
    write_file('output/parse_result.txt', parse_result)
    print("Parse results written to output/parse_result.txt")

# 3.1. Phan tich cau hoi
def base_question_parser(grammar, input_file_name):
    with open(input_file_name, 'r', encoding="utf-8") as file:
        questions = file.readlines()

    for idx, question in enumerate(questions, 1):
        question = question.strip()  # Xóa khoảng trắng thừa và ký tự xuống dòng
        if not question:  # Bỏ qua dòng trống
            continue

        tree = grammar.parse_one(question.replace('?', '').split())
        
        if tree is None:
            parse_result = f"No parse tree found for question: {question}\n"
            file_name = f"output/p2-q-none-{idx}.txt"
        else:
            # Parse to logical form
            logical_form = str(tree.label()['SEM']).replace(',', ' ')
            
            # Get procedure semantics
            procedure_semantics = parse_to_procedure(tree)
            
            # Retrieve result
            results, question_type = retrieve_result(procedure_semantics)
            
            # Prepare output
            parse_result = (
                f"Parsed structure:\n {tree}\n"
                f"Parsed logical form: {logical_form}\n"
                f"Procedure semantics: {procedure_semantics}\n"
                f"Results: {results}\n"
            )
            file_name = f"output/p2-q-{idx}.txt"

        # Save result to a file
        write_file(file_name, parse_result)
        print(f"Question {idx} parsed and written to {file_name}")

def question_parser(grammar, question):
    tree = grammar.parse_one(question.replace('?', '').split())
    
    if tree is None:
        parse_result = f"No parse tree found for question: {question}\n"
        file_name = "output/p2-q-none.txt"
    else:
        # Parse to logical form
        logical_form = str(tree.label()['SEM']).replace(',', ' ')
        
        # Get procedure semantics
        procedure_semantics = parse_to_procedure(tree)
        
        # Retrieve result
        results, question_type = retrieve_result(procedure_semantics)
        
        # Prepare output
        parse_result = (
            f"Parsed structure:\n {tree}\n"
            f"Parsed logical form: {logical_form}\n"
            f"Procedure semantics: {procedure_semantics}\n"
            f"Results: {results}\n"
        )
        file_name = f"output/command-q.txt"

    # Save result to a file
    write_file(file_name, parse_result)


def main(args):
    # Load grammar
    print("Loading grammar from file...")
    nlp_grammar = nltk.load_parser(args.cfg, trace=0)
    print("Loading grammar completed")

    #Generate sample sentences
    grammar = nltk.data.load(args.cfg1, format='fcfg')
    max_sentences = 10000
    generate_sentences(grammar, max_sentences)
    
    my_parser(nlp_grammar, './base_input/sentences.txt')
    shutil.copy("./base_input/sentences.txt", "./input")

    # Call question_parser for multiple questions
    base_question_parser(nlp_grammar, './base_input/input_question.txt')
    shutil.copy("./base_input/input_question.txt", "./input")
    question_parser(nlp_grammar, args.question)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="NLP Assignment Command Line")
    
    parser.add_argument(
        '--cfg',
        default="./grammar/grammar.fcfg",
        help="Context Free Grammar file to be parsed. Default = 'grammar.fcfg'"
    )

    # Grammar nay duoc su dung cho phan 1
    parser.add_argument(
        '--cfg1',
        default="./grammar/gen_sentences_grammar.fcfg",
        help="Context Free Grammar file to be parsed. Default = 'gen_sentences_grammar.fcfg'"
    )


    parser.add_argument(
      '--question',
      default= "đi Đà Nẵng có những ngày nào nhỉ?",
      help= "Question to be parsed.'"
      )
    
    args = parser.parse_args()
    main(args)