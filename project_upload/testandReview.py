#!/usr/bin/env python3
"""
Math Crossword Game - Fill in the grid to match target sums
"""

import random
from typing import List, Tuple, Optional


def generate_random_puzzle(rows: int, cols: int) -> Tuple[List[List[int]], List[int], List[int]]:
    """Generate a random valid puzzle solution and extract sums"""
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Fill with random distinct digits
    available = list(range(1, 10))
    random.shuffle(available)
    
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(available):
                grid[r][c] = available[idx]
                idx += 1
            else:
                grid[r][c] = random.randint(1, 9)
    
    # Calculate row and column sums
    row_sums = [sum(grid[r]) for r in range(rows)]
    col_sums = [sum(grid[r][c] for r in range(rows)) for c in range(cols)]
    
    return grid, row_sums, col_sums


def display_grid(rows: int, cols: int, user_grid: List[List[Optional[int]]], 
                 row_sums: List[int], col_sums: List[int], 
                 show_row_sums: List[bool], show_col_sums: List[bool]):
    """Display the game grid with sums"""
    print("\n" + "="*60)
    print("Math Crossword Puzzle:")
    print("="*60)
    
    # Header with column sums
    print("      ", end="")
    for c in range(cols):
        if show_col_sums[c]:
            print(f"[{col_sums[c]:2d}]", end=" ")
        else:
            print(" ?? ", end=" ")
    print()
    
    print("    " + "----" * cols)
    
    # Rows with data
    for r in range(rows):
        if show_row_sums[r]:
            print(f"[{row_sums[r]:2d}]|", end="")
        else:
            print(" ?? |", end="")
        
        for c in range(cols):
            val = user_grid[r][c]
            if val is None:
                print("  _ ", end="")
            else:
                print(f"  {val} ", end="")
        print()
    
    print("\nLegend: [##] = Target sum, ?? = Hidden sum, _ = Empty cell")
    print("="*60)


def validate_answer(user_grid: List[List[Optional[int]]], 
                    row_sums: List[int], col_sums: List[int],
                    rows: int, cols: int) -> Tuple[bool, List[str]]:
    """Validate user's answer and return errors"""
    errors = []
    all_valid = True
    
    # Check if grid is complete
    for r in range(rows):
        for c in range(cols):
            if user_grid[r][c] is None:
                errors.append(f"Cell ({r},{c}) is empty!")
                all_valid = False
    
    if not all_valid:
        return False, errors
    
    # Validate row sums
    for r in range(rows):
        actual_sum = sum(user_grid[r][c] for c in range(cols))
        if actual_sum != row_sums[r]:
            errors.append(f"❌ Row {r}: Expected sum {row_sums[r]}, got {actual_sum}")
            all_valid = False
    
    # Validate column sums
    for c in range(cols):
        actual_sum = sum(user_grid[r][c] for r in range(rows))
        if actual_sum != col_sums[c]:
            errors.append(f"❌ Column {c}: Expected sum {col_sums[c]}, got {actual_sum}")
            all_valid = False
    
    return all_valid, errors


def main():
    """Main game function"""
    print("\n" + "="*60)
    print("🎮 Math Crossword Game 🎮")
    print("="*60)
    print("\nFill in the grid so that:")
    print("- Each row sums to its target (shown on left)")
    print("- Each column sums to its target (shown on top)")
    print("- Some sums may be hidden (??) - you must figure them out!")
    
    # Get grid size
    while True:
        try:
            rows = int(input("\nEnter number of rows (2-4 recommended): "))
            cols = int(input("Enter number of columns (2-4 recommended): "))
            if 1 <= rows <= 9 and 1 <= cols <= 9:
                break
            print("❌ Error: Grid size must be between 1x1 and 9x9")
        except ValueError:
            print("❌ Error: Please enter valid integers.")
    
    # Generate puzzle
    print("\n🎲 Generating random puzzle...")
    solution_grid, row_sums, col_sums = generate_random_puzzle(rows, cols)
    
    # Decide which sums to hide
    print("\nDo you want to hide some sums? (makes it harder)")
    hide_choice = input("Hide sums? (y/n): ").strip().lower()
    
    show_row_sums = [True] * rows
    show_col_sums = [True] * cols
    
    if hide_choice == 'y':
        # Randomly hide some sums
        num_hide = random.randint(1, min(rows + cols - 1, (rows + cols) // 2))
        hidden = 0
        while hidden < num_hide:
            if random.random() < 0.5 and rows > 0:
                r = random.randint(0, rows - 1)
                if show_row_sums[r]:
                    show_row_sums[r] = False
                    hidden += 1
            else:
                c = random.randint(0, cols - 1)
                if show_col_sums[c]:
                    show_col_sums[c] = False
                    hidden += 1
    
    # Initialize user grid
    user_grid = [[None for _ in range(cols)] for _ in range(rows)]
    
    # Game loop
    attempts = 0
    max_attempts = 20
    
    while attempts < max_attempts:
        display_grid(rows, cols, user_grid, row_sums, col_sums, 
                    show_row_sums, show_col_sums)
        
        print(f"\nAttempt {attempts + 1}/{max_attempts}")
        print("\nOptions:")
        print("  1. Fill a cell")
        print("  2. Clear a cell")
        print("  3. Submit answer")
        print("  4. Show hint")
        print("  5. Give up (show solution)")
        
        choice = input("\nYour choice: ").strip()
        
        if choice == "1":
            # Fill a cell
            try:
                r = int(input("Enter row (0-indexed): "))
                c = int(input("Enter column (0-indexed): "))
                
                if not (0 <= r < rows and 0 <= c < cols):
                    print(f"❌ Error: Cell ({r},{c}) is out of bounds!")
                    continue
                
                val = int(input(f"Enter value for cell ({r},{c}): "))
                
                if not (1 <= val <= 9):
                    print("❌ Error: Value must be between 1 and 9!")
                    continue
                
                user_grid[r][c] = val
                print(f"✓ Set cell ({r},{c}) = {val}")
                
            except ValueError:
                print("❌ Error: Please enter valid integers!")
        
        elif choice == "2":
            # Clear a cell
            try:
                r = int(input("Enter row to clear: "))
                c = int(input("Enter column to clear: "))
                
                if not (0 <= r < rows and 0 <= c < cols):
                    print(f"❌ Error: Cell ({r},{c}) is out of bounds!")
                    continue
                
                user_grid[r][c] = None
                print(f"✓ Cleared cell ({r},{c})")
                
            except ValueError:
                print("❌ Error: Please enter valid integers!")
        
        elif choice == "3":
            # Submit answer
            attempts += 1
            is_valid, errors = validate_answer(user_grid, row_sums, col_sums, rows, cols)
            
            if is_valid:
                print("\n" + "="*60)
                print("🎉 CONGRATULATIONS! 🎉")
                print("="*60)
                print(f"You solved the puzzle in {attempts} attempt(s)!")
                display_grid(rows, cols, user_grid, row_sums, col_sums, 
                           [True]*rows, [True]*cols)
                return
            else:
                print("\n❌ INCORRECT! Errors found:")
                for error in errors:
                    print(f"  {error}")
                print(f"\nYou have {max_attempts - attempts} attempts remaining.")
        
        elif choice == "4":
            # Show hint
            empty_cells = [(r, c) for r in range(rows) for c in range(cols) 
                          if user_grid[r][c] is None]
            
            if empty_cells:
                r, c = random.choice(empty_cells)
                hint_val = solution_grid[r][c]
                print(f"\n💡 Hint: Cell ({r},{c}) = {hint_val}")
            else:
                print("\n💡 No empty cells to hint!")
        
        elif choice == "5":
            # Give up
            print("\n" + "="*60)
            print("Solution:")
            print("="*60)
            display_grid(rows, cols, solution_grid, row_sums, col_sums,
                        [True]*rows, [True]*cols)
            return
        
        else:
            print("❌ Invalid choice!")
    
    print("\n" + "="*60)
    print("❌ GAME OVER - Out of attempts!")
    print("="*60)
    print("\nSolution:")
    display_grid(rows, cols, solution_grid, row_sums, col_sums,
                [True]*rows, [True]*cols)


if __name__ == "__main__":
    main()