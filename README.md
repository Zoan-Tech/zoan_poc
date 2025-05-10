# Zoan POC on AI Agent
This proof-of-concept project demonstrates an AI agent implementation. It showcases autonomous decision-making capabilities and interactive conversational abilities in a controlled environment. Built with Python, it serves as a foundation for exploring AI agent architectures and behaviors.

## Getting Started

```bash
python3.11 -m venv .venv
source .venv/bin/activate
.venv/bin/python3 -m pip install -r requirements.txt
make
```

## Overview
This POC contains 2 module:

* Game asset generator: the generated assets will be stored in folder generated_img.

* Game generator: the generated game will be stored in folder generated_game.
The game generator in this POC employs Python and pygame to generate game, in the final MVP, this will be change to some game-native engines.