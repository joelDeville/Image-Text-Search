#class representing one letter node in trie
class Node:
    def __init__(self, letter):
        self.letter = letter
        self.word = False
        self.children = list()

#trie data structure for storing and retrieving words
class Trie:
    def __init__(self):
        self.root = Node(None)
    
    #determines whether a trie has been generated
    def is_trie_present(self):
        return len(self.root.children) > 0
    
    #build individual path in trie for given word
    def build_trie_path(self, parent, word):
        for letter in word:
            found = False
            
            #searching for letter in children nodes
            for node in parent.children:
                if node.letter == letter:
                    parent = node
                    found = True
                    break
            
            #node not found, add it to trie
            if not found:
                new_node = Node(letter)
                parent.children.append(new_node)
                parent = new_node
            
        #parent will point to node containing final letter, so it is a word
        parent.word = True
    
    #builds trie with list of words
    def build_trie(self, words):
        for word in words:
            self.build_trie_path(self.root, word.lower())
    
    #generates all words stored in trie, stores results into words list
    def traverse_trie(self, trie_node, words, result):
        #reached end of a word
        if trie_node.word and trie_node.letter is not None:
            words.append(result + trie_node.letter)
        
        #root does not have a character assigned, so a check is needed
        if trie_node.letter is not None:
            result = result + trie_node.letter
        
        for node in trie_node.children:
            self.traverse_trie(node, words, result)
    
    def search_trie(self, target):
        parent = self.root
        
        result = ''
        for letter in target:
            found_node = False
            
            #loop through children and see if one matches this letter
            for node in parent.children:
                if node.letter == letter:
                    parent = node
                    found_node = True
                    result += letter
                    break
            
            #if no node matched for this letter, stop searching
            if not found_node:
                break
        
        #start traversing trie at given node if applicable
        matches = list()
        if found_node:
            self.traverse_trie(parent, matches, result[:len(result) - 1])
        else:
            matches.append("No matches found")
        
        matches.sort()
        return matches