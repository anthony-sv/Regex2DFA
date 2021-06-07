from Regex import Regex
from Postfix import Postfix
from Tree import Tree
pfr = Postfix(Regex("(a|b)*abb"))
tr = Tree.getSyntaxTree(pfr.getPostfix())
# print(Tree.inorderTraversal(tr))
print(Tree.tryPos(tr))
print(Tree.tryAnulable(tr))
print(Tree.postorderTraversal(tr))
print(tr.getLeft().getNode().getAnulable())