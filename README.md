# computor_V1

## projet
Computor_V1 est un projet du cursus de 42.
Computor V1 est un programme qui permet de resoudre des équations polynomiales. Ce programme est codée en python.
Le sujet est disponible [ici](https://github.com/tarama78/computor_V1/blob/master/computorv1.fr.pdf).

## utilisation
`python computor.py [equation]`

Exemples:

`python computor.py "3 + 2x - 65 + 3x^2 = 3x - 2"`

Retour:
```
Your equation: -62 + 2 * X + 3 * X^2 = -2 + 3 * X
Reduced form:  -60 + -1 * X + 3 * X^2 = 0
Polynomial degree: 2
Solution 1: -4.3086
Solution 2: 4.6419
```

Si on ne lui donne pas d'arguments computor demande d'entrer l'équation après.
