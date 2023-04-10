import gradio as gr
from app.run import BibleIndex


def calculator(num1, operation, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise gr.Error("Cannot divide by zero!")
        return num1 / num2


def query_index(query, testament, top_n):
    _index = BibleIndex(testament)
    items = _index.query(query, top_n=top_n)

    item_list = f"<h2>{query}</h2>"
    item_list += "<ul>"
    for item in items:
        item_list += f"<h3>{item.get('src')}</h3>"
        item_list += f"<li>{item.get('text')}</li>"
    item_list += "</ul>"
    return item_list


demo = gr.Interface(
    query_index,
    [
        gr.Textbox(label="Query text"),
        gr.Radio(["all", "old", "new"], label="Section of the Bible"),
        gr.Slider(0, 10, step=1, label="Top N results"),
    ],
    outputs="html",
    examples=[
        ["What is love", "new", 5],
        ["How old was Adam?", "old", 3],
        ["Who is God?", "all", 7],
    ],
    title="Bible Search Index",
    description="""
        A search index for The Bible using *sentence_transformer*.
    """,
)
demo.launch()
