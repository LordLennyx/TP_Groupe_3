import google.generativeai as genai
genai.configure(api_key="AIzaSyDZXeR1JVQHrv7tYWpJ1GWcSyNNxFn7KzQ")

for m in genai.list_models():
    # certains modèles n'acceptent pas generateContent, on filtre
    if "generateContent" in m.supported_generation_methods:
        print(m.name)
