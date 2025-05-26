from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text_recursive(
    text: str,
    chunk_size: int = 1100,
    chunk_overlap: int = 100,
) -> list[str]:
    split_text_recursive = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    return split_text_recursive.split_text(text)
