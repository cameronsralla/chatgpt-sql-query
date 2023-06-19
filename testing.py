import openai
openai.api_key = openai.api_key = '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'
models = openai.Model.list()
print(openai.api_base)
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)