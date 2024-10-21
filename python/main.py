import nltk
from nltk import grammar, parse
import argparse
from nltk.parse.generate import generate

# Function to write content to a file
def write_file(file_name, content):
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(content)

# 2.1. Giai thuat sinh cau
def generate_sentences(grammar, max_sentences):
    generated_sentences = set()

    for sentence in generate(grammar, n=max_sentences):
        generated_sentences.add(' '.join(sentence))

    write_file('./nlp/output/samples.txt', "\n".join(generated_sentences))
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
    
    write_file('./nlp/output/parse_result.txt', parse_result)
    print("Parse results written to output/parse_result.txt")

def main(args):
    print("Loading grammar from file...")
    nlp_grammar = nltk.load_parser(args.cfg, trace=0)
    my_parser(nlp_grammar, './nlp/input/sentences.txt')

    print("Generating sentences...")
    grammar = nltk.data.load(args.cfg, format='fcfg')
    max_sentences = 10000
    generate_sentences(grammar, max_sentences)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="NLP Assignment Command Line")
    
    parser.add_argument(
        '--cfg',
        default="grammar.fcfg",
        help="Context Free Grammar file to be parsed. Default = 'grammar.fcfg'"
    )
    
    args = parser.parse_args()
    main(args)