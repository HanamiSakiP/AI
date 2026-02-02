> ## A2UI install
> 1. Clone the repository:
> ```bash
> git clone https://github.com/google/A2UI.git
> cd A2UI
> ```
> 2. Set your API key:
> ```bash
> export GEMINI_API_KEY="your_gemini_api_key"
> ```
> 3. Run the Agent (Backend):
> ```bash
> cd samples/agent/adk/restaurant_finder
> uv run .
> ```
> 4. Run the Client (Frontend): Open a new terminal window:
> ```bash
> # Install and build the Web Core library
> cd renderers/web_core
> npm install
> npm run build
> # Install and build the Lit renderer
> cd ../lit
> npm install
> npm run build
> # Install and run the shell client
> cd ../../samples/client/lit/shell
> npm install
> npm run dev
> ```
