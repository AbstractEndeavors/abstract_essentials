# Abstract AI

## Table of Contents
- [Abstract AI](#abstract-ai)
  - [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Images](#images)
- [Installation](#installation)
- [Usage](#usage)
- [Abstract AI Module](#abstract-ai-module)
  - [GptManager Overview](#gptmanager-overview)
  - [Purpose](#purpose)
  - [Motivation](#motivation)
  - [Objective](#objective)
    - [Extended Overview](#extended-overview)
  - [Main Components](#main-components)
    - [GptManager](#gptmanager)
    - [ApiManager](#apimanager)
    - [ModelManager](#modelmanager)
    - [PromptManager](#promptmanager)
    - [InstructionManager](#instructionmanager)
    - [ResponseManager](#responsemanager)
  - [Dependencies](#dependencies)
  - [Detailed Components Documentation](#detailed-components-documentation)
    - [ModelManager](#modelmanager-1)
    - [InstructionManager](#instructionmanager-1)
    - [PromptManager](#promptmanager-1)
  - [Additional Information](#additional-information)
- [Contact](#contact)
- [License](#license)

## Overview

`api_calls.py` serves as a bridge between your application and the OpenAI GPT-3 API. It provides a convenient interface for sending requests, managing responses, and controlling the behavior of the API calls. This module is highly customizable, allowing you to establish prompts, instructions, and response handling logic.

## Images

![URL Grabber Component](https://github.com/AbstractEndeavors/abstract_essentials/blob/main/abstract_ai/src/abstract_ai/documentation/images/url_grabber_bs4_component.png)

*URL grabber component: Allows users to add URL source code or specific portions of the URL source code to the prompt data.*

![Settings Tab](https://github.com/AbstractEndeavors/abstract_essentials/blob/main/abstract_ai/src/abstract_ai/documentation/images/settings_tab.png)

*Settings Tab: Contains all selectable settings, including available, desired, and used prompt and completion tokens.*

![Instructions Display](https://github.com/AbstractEndeavors/abstract_essentials/blob/main/abstract_ai/src/abstract_ai/documentation/images/instructions_display.png)

*Instructions Display: Showcases all default instructions, which are customizable in the same pane. All instructions are derived from the `instruction_manager` class.*

![File Content Chunks](https://github.com/AbstractEndeavors/abstract_essentials/blob/main/abstract_ai/src/abstract_ai/documentation/images/file_content_chunks.png)

*File Browser Component: Enables users to add the contents of files or specific portions of file content to the prompt data.*

## Installation

To utilize the `api_calls.py` module, install the necessary dependencies and configure your OpenAI API key:

1. Install the required Python packages:

   ```bash
   pip install abstract_ai
   ```

2. Set your OpenAI API key as an environment variable. By default, the module searches for an environment variable named `OPENAI_API_KEY` for API call authentication. Ensure your `.env` is saved in `home/envy_all`, `documents/envy_all`, within the `source_folder`, or specify the `.env` path in the GUI settings tab.

## Usage

```python
from abstract_ai import abstract_ai_gui_main
```

# `abstract_ai` Module

The `abstract_ai` module is an advanced class management system crafted to seamlessly interact with the GPT model. Incorporating a myriad of sub-modules and components, it refines the process of querying, interpreting, and managing GPT model responses.

## GptManager Overview

This tool is an innovative solution designed to simplify the application of artificial intelligence. Perfect for individuals and professionals leveraging AI for work, research, or education, it addresses a major challenge that's often been neglected. The software features a request section, where users pinpoint their primary goals, complemented by adaptable instructions that are highly effective in their default state.

A distinguishing feature is its distinct data prompt handling. Typically, the AI system can consume around ~8200 tokens per instance. This cap often limits users, compelling them to manually segment their prompts, potentially undermining information precision and expectations. Contrarily, this software retains the prompt and instruction across every data query, smartly breaking the data into 'chunks' that are easy to handle.

User control is paramount. Individuals can tweak these 'chunks' as they see fit, striking a balance between anticipated completion and prompt percentages. Notably, the software empowers the AI with a degree of autonomy, letting it request particular annotations to maintain context between data queries, answer multiple times for each data chunk, or even revisit earlier data chunks for enhanced data understanding.
## Purpose

The abstract_ai module enhances class management for seamless interaction with the GPT model, streamlining query handling.

## Motivation

The module aims to simplify AI application and address the token constraint challenge faced when working with GPT models.

## Objective

The objective of this module is to improve the ease of using AI for tasks like creating docstrings and generating READMEs by automating code segmentation and interaction.

### Extended Overview

Instead of the user making multiple attempts to format their queries correctly and getting feedback from the AI, and subsequently manually sending multiple prompts; this module equips the system with enough autonomy to address these challenges independently, minimizing the back-and-forth interactions after the initial prompt submission. It addresses the need to automate code segmentation, provide relevant instructions, and reduce manual interaction with the AI, improving efficiency.

### Main Components

- **GptManager**: The core, orchestrating interactions and flow among components.
- **ApiManager**: Manages OpenAI API keys and headers.
- **ModelManager**: Handles model selection and querying.
- **PromptManager**: Responsible for generating and managing prompts.
- **InstructionManager**: Dictates instructions for the GPT model.
- **ResponseManager**: Processes model responses.

### Dependencies

- **abstract_webtools**: Provides web-centric tools.
- **abstract_gui**: Houses GUI-related tools and components.
- **abstract_utilities**: Contains general-purpose utility functions and classes.
- **abstract_ai_gui_layout**: Lays out the AI GUI.

### Detailed Components Documentation

#### ModelManager

Manages models for the communication system. Key attributes include lists of all models, endpoints, and selected model details.

#### InstructionManager

Controls instructions for ChatGPT. Among its methods, it can interpret 'additional_responses' and determine the 'generate_title' value.

#### PromptManager

Focuses on prompts and their processing, determining token distribution and counting tokens in given text.

### Additional Information

- **Author**: putkoff
- **Date**: 10/29/2023
- **Version**: 1.0.0

## Contact

For issues, suggestions, or contributions, open a new issue on our [Github repository](https://github.com/AbstractEndeavors/abstract-ai/).

## License

`abstract_ai` is distributed under the [MIT License](https://opensource.org/licenses/MIT).

