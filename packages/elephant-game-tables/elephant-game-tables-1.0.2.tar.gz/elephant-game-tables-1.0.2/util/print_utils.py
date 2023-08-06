def print_block(title, data_contents=None):
    print("============================================================================")
    print(f"| ---------- {title} ------------")
    if data_contents:
        for key, content in data_contents.items():
            print(f"| {key}: {content}")
    print("============================================================================")
