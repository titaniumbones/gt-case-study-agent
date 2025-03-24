"""Main entry point for the GivingTuesday Campaign Advisor."""

import sys

if __name__ == "__main__":
    # Check for the correct command line arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py [cli|web|search]")
        print("  cli:    Run the command line interface")
        print("  web:    Run the web application")
        print("  search: Run vector search directly (for developers)")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "cli":
        # Run the CLI application
        from src.cli.app import main

        sys.argv = [sys.argv[0]] + sys.argv[2:]
        main()

    elif command == "web":
        # Run the web application
        import uvicorn

        uvicorn.run("src.web.app:app", host="127.0.0.1", port=8001, reload=True)

    elif command == "search":
        # Run the search command directly (for developers)
        from src.cli.app import search

        # If no additional args provided, show help
        if len(sys.argv) < 3:
            print(
                'Usage: python main.py search "your search query" [--top-k=5] [--show-content] [--json] [--recreate]'
            )
            print("  --recreate    Force recreation of the vector database")
            sys.exit(1)

        # Pass the query and any other args
        from src.cli.app import app

        sys.argv = [sys.argv[0], "search"] + sys.argv[2:]
        app()

    else:
        print(f"Unknown command: {command}")
        print("Usage: python main.py [cli|web|search]")
        print("  cli:    Run the command line interface")
        print("  web:    Run the web application")
        print("  search: Run vector search directly (for developers)")
        sys.exit(1)
