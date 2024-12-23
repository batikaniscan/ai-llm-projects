from projects.company_brochure import generate_company_brochure
import gradio as gr

def process_p2(text):
    return f"P2 processing: {text.lower()}"

# Interface for Company Brochure Generator
company_brochure_generator_interface = gr.Interface(
    fn=generate_company_brochure,
    inputs=[
        gr.Textbox(label="Company Name"),
        gr.Textbox(label="Company URL")
    ],
    outputs=gr.Markdown(label="Company Brochure Output"),
    title="Company Brochure Generator"
)

# Create interface for P2
p2_interface = gr.Interface(
    fn=process_p2,
    inputs=gr.Textbox(label="P2 Input Text"),
    outputs=gr.Markdown(label="P2 Processed Output"),
    title="P2 Processing"
)

# Create tabbed interface
demo = gr.TabbedInterface(
    interface_list=[company_brochure_generator_interface, p2_interface],
    tab_names=["Company Brochure Generator", "Company Chatbot"],
    title="Batikan Iscan AI Projects Showcase"
)

if __name__ == "__main__":
    demo.launch()