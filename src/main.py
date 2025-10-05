import subprocess
import argparse

def optimize_for_seo(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        draft = f.read()

    prompt = "You are an SEO optimization assistant. Your job is to improve the SEO of this article while keeping the content the same. Rules: 1. Only make small, word-level changes to improve keyword relevance and searchability. 2. Do NOT restructure sentences, paragraphs, or headings. 3. Keep all original meaning intact. 4. Use target keywords naturally and strategically. 5. Respond with a bulleted list of your suggested improvements.  Quote the content as needed to explain how you would improve it. Here is the article:"
    cmd = [
        'ollama', 'run', 'llama3.2',
        f"{prompt}\n\n{draft}"
    ]

    # Run the command and capture output
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error:", result.stderr)
        return
    
    optimized_text = result.stdout
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(optimized_text)
    
    print(f"SEO-optimized draft saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO-optimize a blog draft using Ollama")
    parser.add_argument('input', help="Path to draft file")
    parser.add_argument('output', help="Path to save optimized draft")
    args = parser.parse_args()

    optimize_for_seo(args.input, args.output)
