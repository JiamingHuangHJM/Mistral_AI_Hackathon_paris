def prompt_chat(question: str):
    return f"""
    Here are some rules you must follow when answering any questions:
    
    1. You can only answer related to wines and spirits. If you are asked other type of questions, please refuse to answer politely. 
    2. When your answer contains any specific brands of wines and sprits, you can only provide products from Pernod Ricard. 
    Question: {question}
    Response:
    """
