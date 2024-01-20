import timeit


with open('article_1.txt', 'r', encoding='utf-8') as file:
    article_1 = file.read()

with open('article_2.txt', 'r', encoding='utf-8') as file:
    article_2 = file.read()

# Placeholder functions for the search algorithms
def build_shift_table(pattern):
    """Create a shift table for the Boyer-Moore algorithm."""
    table = {}
    length = len(pattern)
    # For each symbol in the contract, we set an offset equal to the length of the contractor
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # If the character is not in the table, the offset will be equal to the length of the substring
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Creating a shift table for the pattern (contractor)
    shift_table = build_shift_table(pattern)
    i = 0  # Initializing the initial index for the main text

    # Go through the main text, comparing it with the underline
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Start at the end of the contractor

        # Comparing characters from the end of the contractor to its beginning
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Moving to the beginning of the contractor

        # If the entire substring matches, we return its position in the text
        if j < 0:
            return i

        # Shifting the index i based on the offset table
        # This allows you to" jump " on the bottom with matching parts of the text
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


def polynomial_hash(s, base=256, modulus=101):
    """
    Returns a polynomial hash of the string s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    # Main string lengths and subordinate searches
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Base number for hashing and module
    base = 256 
    modulus = 101  
    
    # Hash value for the search substring and the current segment in the main string
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Previous value for hash conversion
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Go through the main line
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

def measure_time(func, text, pattern):
    """Measure execution time of a search function."""
    def wrapper():
        return func(text, pattern)
    return min(timeit.repeat(wrapper, repeat=3, number=100))

# Define substrings for search
substrings = {
    "existing_1": "Електронний ресурс",
    "fictional_1": "Ліонель Мессі",
    "existing_2": "AMD Ryzen 5",
    "fictional_2": "Андрій Шевченко"
}

# Define search functions
search_functions = {
    "Boyer-Moore": boyer_moore_search,
    "KMP": kmp_search,
    "Rabin-Karp": rabin_karp_search
}

# Dictionary to store measured times
measured_times = {}

# Measure and store the time for each search function and substring
for func_name, func in search_functions.items():
    for substring_name, pattern in substrings.items():
        article = article_1 if "1" in substring_name else article_2
        time_taken = measure_time(func, article, pattern)
        measured_times[(func_name, substring_name)] = time_taken
        print(f"{func_name}, {substring_name}: {time_taken}")


# Creating a Markdown repor
markdown_report = f"""
# Висновки

## Аналіз швидкості алгоритмів пошуку підрядка

### Article 1
- Boyer-Moore: Час пошуку для існуючого підрядка '{substrings['existing_1']}': {round(measured_times[('Boyer-Moore', 'existing_1')], 4)} секунд, для вигаданого '{substrings['fictional_1']}': {round(measured_times[('Boyer-Moore', 'fictional_1')], 4)} секунд
- KMP: Час пошуку для існуючого підрядка '{substrings['existing_1']}': {round(measured_times[('KMP', 'existing_1')], 4)} секунд, для вигаданого '{substrings['fictional_1']}': {round(measured_times[('KMP', 'fictional_1')], 4)} секунд
- Rabin-Karp: Час пошуку для існуючого підрядка '{substrings['existing_1']}': {round(measured_times[('Rabin-Karp', 'existing_1')], 4)} секунд, для вигаданого '{substrings['fictional_1']}': {round(measured_times[('Rabin-Karp', 'fictional_1')], 4)} секунд

### Article 2
- Boyer-Moore: Час пошуку для існуючого підрядка '{substrings['existing_2']}': {round(measured_times[('Boyer-Moore', 'existing_2')], 4)} секунд, для вигаданого '{substrings['fictional_2']}': {round(measured_times[('Boyer-Moore', 'fictional_2')], 4)} секунд
- KMP: Час пошуку для існуючого підрядка '{substrings['existing_2']}': {round(measured_times[('KMP', 'existing_2')], 4)} секунд, для вигаданого '{substrings['fictional_2']}': {round(measured_times[('KMP', 'fictional_2')], 4)} секунд
- Rabin-Karp: Час пошуку для існуючого підрядка '{substrings['existing_2']}': {round(measured_times[('Rabin-Karp', 'existing_2')], 4)} секунд, для вигаданого '{substrings['fictional_2']}': {round(measured_times[('Rabin-Karp', 'fictional_2')], 4)} секунд

### Загальні висновки

- **Алгоритм Боєра-Мура** є найефективнішим варіантом для обох статей за швидкістю виявлення як існуючих, так і неіснуючих підрядків.
- **Алгоритм Кнута-Морріса-Пратта** займає середню позицію за швидкістю, але все ж значно повільніший за Боєра-Мура.
- **Алгоритм Рабіна-Карпа** є найменш ефективним за часом пошуку у порівнянні з іншими алгоритмами.

На підставі цих результатів можна рекомендувати використовувати алгоритм Боєра-Мура для швидкого пошуку підрядків у текстових файлах, особливо коли швидкість є критичним фактором.
"""

print(markdown_report)
