# Syntax for specification

$$
\begin{align}
Spec \quad &::= \quad \texttt{Spec\ \{} \quad Configs\quad \texttt\} \\
Configs \quad &::= \quad Entry\quad \texttt,\quad Configs \quad | \quad [] \\
Entry \quad &::= \quad \texttt{'qubit':}\quad \N \\
		&\quad | \quad\ \ \texttt{'initial':} \quad VExpr \\
		&\quad | \quad\ \ \texttt{'final':} \quad VExpr \\
		&\quad | \quad\ \ \texttt{'circuit:'} \quad \mathrm{string} \\
VExpr \quad &::= \quad VExpr \quad + \quad VExpr \\
		&\quad | \quad\ \ VExpr \quad - \quad VExpr \\
		&\quad | \quad\ \ Expr \quad * \quad VExpr \\
		&\quad | \quad\ \ VExpr \quad / \quad Expr \\
		&\quad | \quad\ \ - \quad VExpr \\
		&\quad | \quad\ \ |\N_b\rangle \\
		&\quad | \quad\ \ \texttt( \quad VExpr \quad \texttt) \\
Expr \quad &::= \quad Expr \quad Binop \quad Expr \\
		&\quad | \quad\ \ \texttt( \quad Expr \quad \texttt) \\
		&\quad | \quad\ \ Uniop \quad \texttt( \quad Expr \quad \texttt) \\
		&\quad | \quad\ \ \N \\
		&\quad | \quad\ \ \texttt{exp(} \quad Expr \quad \texttt{)} \\
		&\quad | \quad\ \ \texttt{pi} \quad | \quad \texttt{e} \quad | \quad \texttt{i} \\
\end{align}
$$

 Where

- $LParen$ and $RParen$ are a pair of any brackets (parenthesis, square brackets or curly braces). However, they must come in pairs. 
- $\N$ is any natural number characters, including superscripts and subscripts.
- $Binop$ are the 4 arithmetic operations and power ^
- $Uniop$ are $\sqrt{}$, and trigonometric functions ($\sin$, $\cos$, $\tan$) and their inverses

For example, these are all valid syntax: 

- `¹/√2 |0⟩ + 1/sqrt(2)|1>`
- `sin(π) |0⟩ + cos(pi)|1>`
- `¹/2⁸ + 1/(2 ^ 8)`

