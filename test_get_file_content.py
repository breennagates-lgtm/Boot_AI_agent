from functions.get_file_content import get_file_content

if __name__ == "__main__":
    result1 = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result1)}")
    print(f"lorem.txt truncated: {'truncated' in result1}")
    result2 = get_file_content("calculator", "main.py")
    print(result2)
    result3 = get_file_content("calculator", "pkg/calculator.py")
    print(result3)
    result4 = get_file_content("calculator", "/bin/cat")
    print(result4)
    result5 = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result5)