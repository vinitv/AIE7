#!/usr/bin/env python3
"""
Script to add markdown explanations to the LangGraph notebook.
This script provides the markdown content that should replace each "YOUR MARKDOWN HERE" section.
"""

# Markdown explanations for each section
markdown_explanations = {
    "activity_5_first": """##### Creating the Graph Structure

This code creates a new LangGraph with helpfulness checking. We're setting up two main nodes: the "agent" node that handles the AI model calls, and the "action" node that executes tools when needed. Think of it as building the basic structure of our intelligent assistant.""",

    "activity_5_second": """##### Setting the Entry Point

Here we're telling the graph where to start. The "agent" node is our entry point, meaning every conversation begins with the AI model processing the user's input. It's like setting the starting line for a race.""",

    "activity_4_function": """##### Understanding the Smart Decision Maker

This function acts as a smart decision maker that determines what the agent should do next. It works like a traffic controller for our LangGraph workflow.

First, it checks if the last message from the agent contains tool calls. If it does, that means the agent wants to use a tool (like searching the web or looking up papers), so it sends the flow to the "action" node to execute those tools.

If there are no tool calls, it means the agent gave a direct response. Here's where it gets interesting - the function then evaluates whether that response is actually helpful to the user's original question. It does this by comparing the initial query with the final response using another AI model.

The function also includes a safety mechanism - if the conversation has gone through more than 10 messages, it automatically ends to prevent infinite loops.

If the helpfulness check says the response is good (contains "Y"), it ends the conversation. If not (contains "N"), it sends the flow back to the agent to try again and provide a better answer.""",

    "activity_5_third": """##### Adding Smart Routing Logic

This is where we add the smart routing logic. The conditional edge uses our `tool_call_or_helpful` function to decide what happens next. It can send the flow to the action node (if tools are needed), back to the agent (if the response needs improvement), or end the conversation (if we have a good answer). It's like having multiple paths that the conversation can take based on what's happening.""",

    "activity_5_fourth": """##### Connecting Tools Back to Agent

This creates a direct connection from the action node back to the agent node. Whenever tools are used (like searching the web), the results get sent back to the agent so it can process that information and provide a better response. It's like giving the agent the research it requested.""",

    "activity_5_fifth": """##### Compiling the Final System

This final step compiles all our graph components into a working application. It's like taking all the blueprints and building instructions and turning them into a functional system that can actually process user requests and provide intelligent responses.""",

    "activity_5_sixth": """##### Testing Our Intelligent Assistant

This code tests our newly created agent with helpfulness checking. We're asking it a complex question about machine learning concepts and watching how it processes the request through multiple steps, using tools when needed and evaluating its own responses for helpfulness."""
}

def print_markdown_for_section(section_name):
    """Print the markdown explanation for a specific section."""
    if section_name in markdown_explanations:
        print(f"\n=== {section_name.upper()} ===\n")
        print(markdown_explanations[section_name])
        print("\n" + "="*50 + "\n")
    else:
        print(f"Section '{section_name}' not found. Available sections:")
        for key in markdown_explanations.keys():
            print(f"  - {key}")

def print_all_markdown():
    """Print all markdown explanations."""
    print("ALL MARKDOWN EXPLANATIONS FOR THE NOTEBOOK")
    print("=" * 50)
    
    for section_name, markdown in markdown_explanations.items():
        print(f"\n=== {section_name.upper()} ===\n")
        print(markdown)
        print("\n" + "="*50)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        section = sys.argv[1]
        print_markdown_for_section(section)
    else:
        print_all_markdown()
        
    print("\nINSTRUCTIONS:")
    print("1. Copy each markdown section above")
    print("2. Replace the corresponding 'YOUR MARKDOWN HERE' in the notebook")
    print("3. The sections should be replaced in this order:")
    print("   - activity_5_first (after Activity #5, before graph creation)")
    print("   - activity_5_second (before set_entry_point)")
    print("   - activity_4_function (after Activity #4, explaining tool_call_or_helpful)")
    print("   - activity_5_third (before add_conditional_edges)")
    print("   - activity_5_fourth (before add_edge)")
    print("   - activity_5_fifth (before compile)")
    print("   - activity_5_sixth (before testing the agent)") 