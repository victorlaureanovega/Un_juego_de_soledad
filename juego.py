import openai

user = openai.OpenAI(api_key="insertar llave")

print("JUEGO DE VOCABULARIO EN PYTHON CON CHATGPT\n\n")
print("Bienvenido. Generaré tres palabras aleatorias, con las que deberás escribir una oración.\n")
print("Cuando desees terminar el juego, escribe 'salir'.\n\n")

assistant = user.beta.assistants.create(
    name="Juego de vocabulario",
    instructions=f"Tienes excelentes conocimientos del lenguaje.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
)

thread = user.beta.threads.create()

while True:
    messages = user.beta.threads.messages.list(thread_id=thread.id)

    m1 = user.beta.threads.messages.create(
        thread_id=thread.id,
        role="assistant",
        content="Genera tres palabras aleatorias en español.",
    )

    run = user.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Recuerda las palabras generadas.",
    )

    if run.status == "completed":
        messages = user.beta.threads.messages.list(thread_id=thread.id)
        
        last = messages.data[0]
        assert last.content[0].type == "text"
        print(last.content[0].text.value)
    
    sentence = input(">>> ")
    if sentence.lower() == "salir":
        print("¡Hasta luego!")
        break

    m2 = user.beta.threads.messages.create(
        thread_id=thread.id,
        role="assistant",
        content=f"¿Es la oración {sentence} gramaticalmente correcta? ¿Contiene las palabras que generaste anteriormente?",
    )

    run = user.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Revisa cuidadosamente la oración y da retroalimentación concisa.",
    )

    if run.status == "completed":
        messages = user.beta.threads.messages.list(thread_id=thread.id)

        last = messages.data[0]
        assert last.content[0].type == "text"
        print(last.content[0].text.value)
    print("\n")

user.beta.assistants.delete(assistant.id)