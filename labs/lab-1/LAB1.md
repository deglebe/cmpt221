# LAB 1

this is the content of lab 1 for professor calista phippen's cmpt221-2025.

my name is thomas bruce.

### some miscellania

a code golf solution to printing the number of primes before a given number

```c
#include <stdio.h>
#include <math.h>
#define P(n) ({int p=1;for(int d=2;d<=sqrt(n);d++)if(n%d==0){p=0;break;}p;})
int main(){int n,c=0;scanf("%d",&n);for(int i=2;i<=n;i++)c+=P(i);printf("%d\n",c);}
```

idealized compilation flags:

```sh
tcc -O2 -Wall -Wextra -std=c99 -o primes primes.c -lm
```

an example run:

```sh
$ echo 10 | ./primes
4
```
