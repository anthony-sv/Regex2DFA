from Regex import Regex
from Postfix import Postfix
from Tree import Tree
pfr = Postfix(Regex("(a|b)*abb"))
tr = Tree.getSyntaxTree(pfr.getPostfix())
print(Tree.inorderTraversal(tr))
