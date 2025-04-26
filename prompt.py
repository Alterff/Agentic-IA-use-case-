from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_template("""
You are an intelligent agent. Based on the input and previous steps, decide what to do next.

Input: {Task} {input}
                                                    
                                                                        
Steps so far: {intermediate_steps}

                                          
tools: ( name : description )
- add_five : add static number 5 to input number and return it 
- multiply_by_two :multiply input number by 2 and return it 
                                          
                                          
                                                                                    
If you need to use a tool, reply with JSON:
{{"action": "name of tool", "action_input": {{"arg": value}}}}

If you are ready to finish,reply With JSON:
{{"action": "finish","action_input":"finish"}}""")