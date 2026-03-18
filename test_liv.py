from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

model_name = "darko5723/fine-tuned-liv-model"

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=100)

print("Model loaded! Testing...")
result = generator("Hello Liv, how are you today?", do_sample=True, temperature=0.7)
print(result[0]["generated_text"])
