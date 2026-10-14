from search.semantic_search import SemanticSearch


def main():

    search_engine = SemanticSearch()

    print("=" * 60)
    print("Semantic Search")
    print("=" * 60)

    while True:

        question = input("\nEnter your question (or type 'exit'):\n> ")

        if question.lower() == "exit":
            print("\nGoodbye!")
            break

        search_engine.run(question)

    search_engine.close()


if __name__ == "__main__":
    main()