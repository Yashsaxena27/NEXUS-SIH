import re
from typing import List, Optional, Dict

class Block:
    def __init__(self, parent_line: str, child_lines: List[str]):
        self.parent_line = parent_line
        self.child_lines = child_lines

    def get_command(self, prefix: str) -> Optional[str]:
        """Find a command in this block that starts with the prefix."""
        for line in self.child_lines:
            line_stripped = line.strip()
            if line_stripped.startswith(prefix):
                return line_stripped
        return None

    def has_command(self, prefix: str) -> bool:
        return self.get_command(prefix) is not None

class IndentBlockParser:
    """Parses configuration where blocks are defined by indentation (e.g. Cisco, Palo Alto)."""
    
    def __init__(self, raw_config: str):
        self.lines = raw_config.splitlines()
        
    def get_block(self, parent_prefix: str) -> Optional[Block]:
        """
        Finds the first line matching parent_prefix and returns it along with all 
        subsequent lines that have a deeper indentation level.
        """
        in_block = False
        parent_line = ""
        child_lines = []
        base_indent = 0
        
        for line in self.lines:
            if not line.strip():
                continue
                
            current_indent = len(line) - len(line.lstrip())
            
            if in_block:
                if current_indent <= base_indent and line.strip() != "!":
                    # End of block
                    break
                child_lines.append(line)
            else:
                if line.lstrip().startswith(parent_prefix):
                    in_block = True
                    parent_line = line.strip()
                    base_indent = current_indent

        if not in_block:
            return None
            
        return Block(parent_line, child_lines)


class KeywordBlockParser:
    """Parses configuration where blocks are defined by keywords (e.g. Fortinet config/end)."""
    
    def __init__(self, raw_config: str, start_keyword: str = "config", end_keyword: str = "end"):
        self.lines = raw_config.splitlines()
        self.start_keyword = start_keyword
        self.end_keyword = end_keyword
        
    def get_block(self, block_name: str) -> Optional[Block]:
        """
        Finds a block starting with 'config <block_name>' and ending with 'end'.
        Supports nested blocks (rudimentary).
        """
        in_block = False
        depth = 0
        parent_line = ""
        child_lines = []
        
        target = f"{self.start_keyword} {block_name}"
        
        for line in self.lines:
            stripped = line.strip()
            if not stripped:
                continue
                
            if in_block:
                if stripped.startswith(self.start_keyword):
                    depth += 1
                elif stripped == self.end_keyword or stripped == "next":
                    if depth == 0:
                        break
                    depth -= 1
                child_lines.append(stripped)
            else:
                if stripped.startswith(target):
                    in_block = True
                    parent_line = stripped
                    depth = 0

        if not in_block:
            return None
            
        return Block(parent_line, child_lines)

