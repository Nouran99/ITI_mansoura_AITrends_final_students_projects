# YouTube Shorts Generator with Google ADK

This project automates the creation of YouTube Shorts using a multi-agent system powered by the [Google Agent Development Kit (ADK)](https://github.com/google/agent-development-kit). It generates a short-form video script, visual descriptions, and a fully formatted output saved as a Markdown file.

## Overview

The system uses four specialized agents working together:

* **youtube\_shorts\_agent**: The orchestrator agent. It delegates tasks to sub-agents and consolidates results.
* **scriptwriter\_agent**: Writes concise and engaging scripts.
* **visualizer\_agent**: Suggests visual scenes and cues to complement the script.
* **formatter\_agent**: Formats everything into a clear and structured Markdown file.

The final output is stored in the `outputs/` directory as a `.md` file.

## File Structure

```
.
├── instructions/
│   └── instructions.py          # Prompt instructions for agents
│
├── outputs/
│   └── yt_shorts_1.md           # Generated YouTube Shorts content
│
├── tools/
│   ├── __init__.py
│   ├── write_outputs.py         # Utility to save final content to Markdown
│
├── agent.py                     # Main file to run the multi-agent pipeline
├── instructions.py              # Global or shared prompt instructions
├── .env                         # Environment variables (e.g., API keys)
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
```

## Features

* Modular, multi-agent architecture with clear task separation
* Uses Google ADK to define and manage agents
* Supports flexible topic input
* Saves structured output to `outputs/yt_shorts_1.md`
* Easy to extend for other platforms like TikTok or Reels

## Getting Started

### Prerequisites

* Python 3.9 or later
* [Google Agent Development Kit (ADK)](https://github.com/google/agent-development-kit)
* OpenAI or Gemini API key (set in `.env`)

### Installation

```bash
git clone https://github.com/yourusername/youtube-shorts-agent.git
cd youtube-shorts-agent
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the root directory with the following:

```
GOOGLE_API_KEY=your_key_here
```

### Run the Generator

```bash
python agent.py
```

You will be prompted to enter a topic. The system will generate:

* A script
* Visual scene ideas
* A formatted Markdown file (`outputs/yt_shorts_1.md`)

## Example Output (Markdown)

```
# Title: The Power of AI in 60 Seconds

## Script
"AI is transforming every industry..."

## Visuals
- Opening shot of a robot handshake
- Cut to a screen showing code automation
...

## Notes
Keep transitions fast. Use captions and bold text.
```

## Customization

* Modify `instructions/instructions.py` to tweak agent behavior
* Change output formatting in `tools/write_outputs.py`
* Add more agents or tools for editing, voice-over generation, etc.

## License

This project is licensed under the MIT License.

---

