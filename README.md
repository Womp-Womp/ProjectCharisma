
# Technical Architecture Specification: Project Charisma

**Document Version:** 1.0
**Status:** Technical Scoping
**Lead Engineer:** Jules (AI)
**Associated Document:** PRD: Project Charisma v1.0

---

## 1. Guiding Philosophy & Architectural Goals

This document outlines the technical implementation plan for **Project Charisma**. It builds upon the functional requirements defined in the associated PRD. The primary architectural goals are:

1.  **Maximize Development Velocity:** The architecture and technology stack are chosen to facilitate the fastest possible path from concept to a working feature. We will favor high-level frameworks and libraries over low-level, from-scratch implementations.
2.  **Maintain Decoupling:** The **Editor (IDE)** and the **Game Engine (Player)** will be developed as two separate but connected applications. This separation of concerns is critical for maintainability. The Editor *writes data*; the Engine *reads data*. They communicate only through a well-defined project data structure on disk.
3.  **Prioritize Simplicity and Readability:** The codebase should be clear, well-commented, and use established design patterns. Given that the entire project is managed by a single AI entity (Jules), consistency is key.
4.  **Embrace a Data-Driven Design:** All game logic, content, and behavior should be defined as data (e.g., JSON, Lua scripts) where possible. The C++ (or Python) engine code should be a generic interpreter of this data. This makes the project highly moddable by its very nature.

## 2. Technology Stack Rationale: The Case for Python

The PRD proposed a C++/Qt stack, which is optimal for a high-performance, commercially distributable product. However, the revised goal is a tool for a single user's personal enjoyment and creation. This fundamentally changes the trade-offs.

**Conclusion: We will build the entire project in Python.**

### Justification:

*   **Speed of Iteration:** Python's dynamic nature, concise syntax, and lack of a separate compilation step will reduce development time by an estimated 50-70% compared to C++. This allows for more features to be implemented and refined in the same amount of time.
*   **Powerful Ecosystem:** Python has mature, high-quality libraries for every aspect of this project:
    *   **GUI:** PyQt / PySide provide complete bindings for the powerful Qt framework.
    *   **Game Development:** The Arcade library offers a modern, Pythonic, high-level API for 2D games, handling rendering, sprites, and tilemaps out of the box.
    *   **Data Handling:** The built-in `json` library is perfect for our data format.
    *   **Lua Integration:** The `lupa` library provides a seamless and powerful bridge to Lua/LuaJIT.
*   **Sufficient Performance:** For a turn-based strategy game, even with hundreds of units, Python's performance will be more than adequate. Turn processing is CPU-bound but not real-time critical. Modern Python (3.9+) with well-written algorithms will not be a bottleneck for a single-player experience.
*   **Simplicity:** Managing dependencies (`pip`, `poetry`), memory (automatic garbage collection), and project structure is simpler in Python, freeing up cognitive load to focus on feature implementation.

### Recommended Python Stack:

*   **Language:** Python 3.10+
*   **Editor GUI Framework:** **PyQt6** (preferred for its up-to-date features) or PySide6.
*   **Game Engine Framework:** **Arcade** (modern, object-oriented, built on OpenGL via Pyglet, excellent for 2D sprite/tile games). We will choose this over Pygame for its higher-level abstractions.
*   **Scripting Bridge:** **Lupa** (connects Python to LuaJIT, offering high performance and ease of use).
*   **Code Formatting:** Black & isort (for enforced consistency).
*   **Dependency Management:** Poetry.

---

## 3. High-Level System Architecture

The project consists of two main executables and a shared data format.



1.  **Charisma Editor (`editor.py`):**
    *   A PyQt6-based desktop application.
    *   **Purpose:** To create and modify game data.
    *   **Output:** Writes to a "Project Folder" on disk. Its view of the world is purely data-centric.
    *   It does **not** contain game logic (e.g., how to calculate damage). It only provides fields to enter the numbers and formulas.

2.  **Charisma Engine (`game.py`):**
    *   An Arcade-based application.
    *   **Purpose:** To load a Project Folder and execute it as a playable game.
    *   **Input:** Reads from a "Project Folder." It cannot modify the master project data (it will handle saves separately).
    *   It contains all the simulation and presentation logic (game loops, rendering, AI, combat calculation).

3.  **Project Folder (The Contract):**
    *   A directory on the user's computer that represents a single game or mod.
    *   This is the critical "API" between the Editor and the Engine. Its structure must be rigorously defined.

---

## 4. Component Deep Dive: Charisma Editor (`editor.py`)

The Editor will be built using the **Model-View-Controller (MVC)** pattern to ensure a clean separation of data and presentation.

*   **Model:** Plain Python objects (`dataclasses` are perfect for this) that represent all game data (e.g., a `Unit` class with fields for `name`, `hp`, etc.). This layer handles loading/saving the data from/to JSON files.
*   **View:** All PyQt6 widgets. These are responsible for displaying the data and capturing user input. They are "dumb" and do not contain application logic.
*   **Controller:** The coordinator. It responds to user actions in the View, updates the Model, and refreshes the View with the new data from the Model.

### Key Editor Modules:

*   **Main Window (`MainWindow` class):**
    *   A `QMainWindow` container with a central MDI (Multi-Document Interface) area, dockable widgets for different editors, a main menu, and a toolbar.
    *   Responsible for project loading/saving and orchestrating the different editor panels.
*   **Project Manager (`Project` class):**
    *   A singleton or globally accessible object that holds the state of the currently loaded project, including paths to all data files and the in-memory representation of that data (the Models).
*   **Map/Level Editor:**
    *   A custom widget inheriting from `QGraphicsView`. The map itself will be a `QGraphicsScene`.
    *   Each tile will be a `QGraphicsPixmapItem`.
    *   The Controller will handle mouse events (paint, fill, select) on the scene to update the underlying map data model.
    *   Will feature selectable brushes for tiles, entities, and locations.
*   **Database Editors (Unit, Faction, etc.):**
    *   These will use a `QSplitter` layout.
    *   Left side: `QTreeView` or `QListView` showing a filterable list of all items (e.g., all units). The model for this view will be a `QAbstractItemModel` subclass that wraps our list of data objects.
    *   Right side: A `QFormLayout` with various input widgets (`QLineEdit`, `QSpinBox`, etc.) to edit the properties of the selected item. `QDataWidgetMapper` will be used to automatically link form widgets to the data model fields.
*   **Event/Scripting Editor:**
    *   This is a complex composite widget.
    *   The GUI-based trigger editor will be a series of dynamically added widgets that build up a JSON representation of the event. `(Dropdown: Condition) (Input: Value)` -> `(Dropdown: Action)`.
    *   For the Lua editor, integrate **pyqode.core** or a similar rich text editor widget that provides Lua syntax highlighting and line numbers. A simple `QTextEdit` is a fallback but less user-friendly.

---

## 5. Component Deep Dive: Charisma Engine (`game.py`)

The Engine will be architected around a **Finite State Machine (FSM)**.

*   **`Game` class (inherits from `arcade.Window`):** The main application entry point. It manages the window, the game clock, and holds the active `State`. Its `on_update` and `on_draw` methods will simply delegate to the current state.
*   **`State` (Abstract Base Class):** Defines the interface for all game states (`on_enter`, `on_exit`, `handle_input`, `update`, `draw`).
*   **Concrete States:**
    *   `MainMenuState`: Shows options like "New Game", "Load Game", "Options".
    *   `StrategicMapState`: The main gameplay screen. Renders the strategic map, handles unit selection and movement commands. This is where the player spends most of their time.
    *   `CombatState`: When combat occurs, the game pushes this state onto the stack. It renders the cinematic battle scene. When finished, it pops itself and returns the result to the `StrategicMapState`.
    *   `EventViewState`: Pushed when an event trigger fires. It displays dialogue, portraits, and choices, pausing the underlying game state.

### Key Engine Modules:

*   **Data Loader:** A set of functions at startup that read all the JSON files from the project folder and instantiate the corresponding Python game objects (Units, Factions, etc.). This data is then passed to the relevant states.
*   **Turn Manager:** A class responsible for tracking the current turn, the current faction, and executing the game loop: `start_turn` -> `process_player_input` / `run_ai` -> `end_turn` -> `check_event_triggers` -> `next_faction`.
*   **Map Renderer:**
    *   `arcade.TileMap` is the ideal class for this. It can efficiently render the tile-based map from a TMX file or a 2D array.
    *   Units will be `arcade.Sprite` objects rendered on a layer above the map.
*   **Lua API Bridge (`api.py`):**
    *   A crucial Python module that contains all functions exposed to Lua.
    *   `lupa.LuaRuntime()` will be used to create the Lua environment.
    *   The Python `api` module will be injected into the Lua global namespace (e.g., as `Charisma`).
    *   **Implementation:** Every function in the Lua API (`Charisma.GetUnitById(...)`) will be a corresponding Python function in the `api` module that manipulates the Python game state objects directly. This is the heart of the engine's moddability.
*   **AI Controller:**
    *   A baseline `AIController` class will be implemented in Python.
    *   It will have methods like `evaluate_threats`, `plan_economy`, `execute_moves`.
    *   The Turn Manager will call `ai_controller.take_turn(faction_data)` when it is an AI's turn.
    *   The Faction data in JSON can specify a Lua script to override or augment the baseline AI, providing a powerful hook for advanced users.

---

## 6. Data Persistence & Project Structure

The structure must be strict to ensure interoperability between the Editor and Engine.


/MyGundamMod/ (Root Project Folder)
|-- project.json # Main project file: name, author, starting faction, map file etc.
|
|-- /assets/
| |-- /sprites/ # PNG files for units, map tiles.
| |-- /portraits/ # PNG files for characters.
| |-- /sfx/ # OGG/WAV for sound effects.
| |-- /music/ # OGG/MP3 for background music.
|
|-- /data/
| |-- units.json # Array of all unit definitions.
| |-- factions.json # Array of all faction definitions.
| |-- characters.json # Array of all character/leader definitions.
| |-- tech_tree.json # Node-based graph of technologies.
| |-- abilities.json # Library of special abilities.
|
|-- /maps/
| |-- earth_sphere.json # Map data: dimensions, tile layout, node locations.
|
|-- /scripts/
| |-- /events/ # Lua scripts for events (e.g., odessa_day.lua).
| |-- /ai/ # Lua scripts for custom AI behaviors.

*   **Data Format:** All `.json` files will use a clear, well-documented schema. Use IDs (e.g., `unit_id: "ms-06j"`) to link data between files instead of embedding objects.
*   **Export Package (`.cpx`):** This will be a standard `.zip` archive of the entire Project Folder, renamed with a custom extension. The engine will know how to load from a folder or transparently from a zip archive.
*   **Save Games:** Will be stored separately by the Engine (e.g., in the user's Documents folder), not in the project directory. A save game is essentially a snapshot (a serialization using `pickle` or a deep JSON dump) of the current game state (all unit positions, HPs, faction resources, event flags, etc.).

---

## 7. Development Workflow for Jules

1.  **Setup:** Initialize a Poetry project. Add `pyqt6`, `arcade`, `lupa`, `black`, `isort`. Set up a Git repository.
2.  **Scaffolding:** Create the basic file structures: `editor.py`, `game.py`, and the directories for modules (`editor_modules/`, `engine_modules/`).
3.  **Data Models First:** Define the Python `dataclasses` for all core game concepts (Unit, Faction, MapTile). Make them serializable to/from JSON. This is the foundation.
4.  **Editor Development:**
    *   Build the main window and project management.
    *   Implement one "Database Editor" (e.g., for Units) fully, including the MVC pattern. This will serve as a template for all others.
    *   Implement the Map Editor.
    *   Implement the Event Editor last, as it depends on all other data types.
5.  **Engine Development:**
    *   Build the data loader that can parse a project folder.
    *   Implement the FSM and the `StrategicMapState`.
    *   Render the map and a static unit sprite.
    *   Implement unit movement and turn management.
    *   Build the Lua API bridge (`api.py`) and test it with a simple "Hello World" event.
    *   Implement combat, AI, and other game mechanics, hooking them into the Lua API as you go.
6.  **Continuous Integration:** A GitHub Action should be configured to run `black --check .` and `isort --check .` on every commit to maintain code quality.

