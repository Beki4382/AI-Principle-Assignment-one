from typing import List, Optional, Set
from collections import deque


def word_ladder_length(begin_word: str, end_word: str, word_list: List[str]) -> int:
    word_set = set(word_list)
    
    # If end_word is not in the dictionary, no solution exists
    if end_word not in word_set:
        return 0
    
    # BFS
    queue = deque([(begin_word, 1)])  # (current_word, path_length)
    visited = {begin_word}
    
    while queue:
        current_word, path_length = queue.popleft()
        
        if current_word == end_word:
            return path_length
        
        # Try changing each character
        for i in range(len(current_word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c == current_word[i]:
                    continue
                
                # Create new word with one character changed
                new_word = current_word[:i] + c + current_word[i+1:]
                
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, path_length + 1))
    
    return 0  # No path found


def word_ladder_path(begin_word: str, end_word: str, word_list: List[str]) -> List[str]:
    word_set = set(word_list)
    
    if end_word not in word_set:
        return []
    
    # BFS with path tracking
    queue = deque([(begin_word, [begin_word])])  # (current_word, path)
    visited = {begin_word}
    
    while queue:
        current_word, path = queue.popleft()
        
        if current_word == end_word:
            return path
        
        # Try changing each character
        for i in range(len(current_word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c == current_word[i]:
                    continue
                
                new_word = current_word[:i] + c + current_word[i+1:]
                
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, path + [new_word]))
    
    return []


def word_ladder_all_paths(begin_word: str, end_word: str, word_list: List[str]) -> List[List[str]]:
    
    word_set = set(word_list)
    
    if end_word not in word_set:
        return []
    
    # BFS to find shortest path length first
    all_paths = []
    shortest_length = float('inf')
    
    # (current_word, path)
    queue = deque([(begin_word, [begin_word])])
    
    # Track visited words at each level to allow multiple paths
    level_visited = {begin_word: 0}  # word -> level at which it was first visited
    
    while queue:
        current_word, path = queue.popleft()
        current_level = len(path)
        
        # If we've exceeded the shortest path, stop
        if current_level > shortest_length:
            break
        
        if current_word == end_word:
            shortest_length = current_level
            all_paths.append(path)
            continue
        
        # Try changing each character
        for i in range(len(current_word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c == current_word[i]:
                    continue
                
                new_word = current_word[:i] + c + current_word[i+1:]
                
                if new_word in word_set:
                    # Allow revisiting if at the same level (for multiple paths)
                    if new_word not in level_visited or level_visited[new_word] >= current_level:
                        level_visited[new_word] = current_level + 1
                        queue.append((new_word, path + [new_word]))
    
    return all_paths


def get_neighbors(word: str, word_set: Set[str]) -> List[str]:
   
    neighbors = []
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if c != word[i]:
                new_word = word[:i] + c + word[i+1:]
                if new_word in word_set:
                    neighbors.append(new_word)
    return neighbors


def bidirectional_word_ladder(begin_word: str, end_word: str, word_list: List[str]) -> int:
    
    word_set = set(word_list)
    
    if end_word not in word_set:
        return 0
    
    # Two sets for bidirectional search
    front = {begin_word}
    back = {end_word}
    visited = set()
    
    length = 1
    
    while front and back:
        # Always expand the smaller set
        if len(front) > len(back):
            front, back = back, front
        
        next_front = set()
        
        for word in front:
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    new_word = word[:i] + c + word[i+1:]
                    
                    if new_word in back:
                        return length + 1
                    
                    if new_word in word_set and new_word not in visited:
                        visited.add(new_word)
                        next_front.add(new_word)
        
        front = next_front
        length += 1
    
    return 0


# Test the solutions
if __name__ == "__main__":
    # Example from the problem
    begin_word = "hit"
    end_word = "cog"
    word_list = ["hot", "dot", "dog", "lot", "log", "cog"]
    
    print("Word Ladder Problem")
    print("=" * 50)
    print(f"Begin word: {begin_word}")
    print(f"End word: {end_word}")
    print(f"Word list: {word_list}")
    print()
    
    # Find shortest path length
    length = word_ladder_length(begin_word, end_word, word_list)
    print(f"Shortest transformation length: {length}")
    
    # Find the actual path
    path = word_ladder_path(begin_word, end_word, word_list)
    print(f"Transformation path: {' -> '.join(path)}")
    
    # Find all shortest paths
    all_paths = word_ladder_all_paths(begin_word, end_word, word_list)
    print(f"\nAll shortest paths ({len(all_paths)} found):")
    for i, p in enumerate(all_paths, 1):
        print(f"  Path {i}: {' -> '.join(p)}")
    
   