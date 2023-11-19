# Hatvány tábla

A hatvány tábla (angolul Sparse Table) egy adatszerkezet ami intervallum lekérdezések $O(\log N)$ időben való
megválaszolását teszi lehetőve egy állandó tömbön, viszont minimum és
maximum lekérdezésekre $O(1)$ időben is képes választ adni. Frissitéseket 
nem tud elvégezni. 

## Intuíció

Minden $x$ szám megkapható maximum $\log x$ különböző $2$ hatvány összegeként, a szám
bináris alakját tekintve ez az állítás könnyedén látható.
$$
5=(101)_2=4+1 \\\\
13=(1101)_2=8+4+1 \\\\
$$
Ugyanez az ötlet használható intervallumokra is: minden $x$ hosszú intervallum lefedhető
$2$ hatvány hosszú, maximum $\log x$ különböző intervallummal. 

Az algoritmus a következő: $O(N\log N)$ prekalkulációval elvégezzük az összes $2$ hatvány hosszú intervallumon a
műveleteket, utána maximum $O(\log N)$ intervallum összeadásával megkapjuk a
cél intervallumunkat.

## Implementáció

Először választanunk kell egy $K$ értéket amire $2^K >= N$, ha $N <= 10^6$ akkor $K = 25$ meg fog feleni a céljainknak.
Legyen $ht[i][j] = f(a[j], a[j+1], ..., a[j+2^i])$ egy 0-tól indexelt két dimenziós tömb és
$f(x, y) = min(x, y)$. 
A $ht$ értékeit a következő képpen tudjuk kiszámolni, az előző iterációban kiszámolt
értékeket felhasználva:


``` { .prettyprint }

const int MAXN = 1'000'000;
const int K = 25;

int ht[K][MAXN];

int f(int a, int b) {
    return min(a, b);
}

void elokalkulal(int a[], int N) {
    copy(a, a+N, ht[0]);
    for (int i = 1; i < K; i++) {
        for (int j = 0; j + (1 << i) <= N; j++) {
            ht[i][j] = f(ht[i - 1][j], ht[i - 1][j + (1 << (i - 1))]);
        }
    }
}

```
Megjegyzés: A [bit eltolás](https://hu.wikipedia.org/wiki/Bitm%C5%B1velet#Aritmetikai_eltol%C3%A1s) műveletet felhasználva könnyedén ki tudjuk számolni a
kettő hatványokat. $(1<<i) = 2^i$  

### $O(\log N)$ kérdések

Végig iterálunk az összes kettő hatványon legnagyobbtól legkisebbig
és mohón kiválasztjuk az összes intervallumot amit tudunk.

``` {.prettyprint }

int kerdez(int l, int r) {
    int eredmeny = INT_MAX;
    for (int i = K; i >= 0; i--) {
        int hossz = r - l + 1;
        int ketto_hatvany = 1 << i;
        if (hossz >= ketto_hatvany) {
            eredmeny = f(eredmeny, ht[i][l]);
            l += ketto_hatvany;
        }
    }
    return eredmeny;
}

```

### $O(1)$ minimum/maximum kérdések

A minimum és maximum operációra igaz az, hogy egy érték többszöri hozzáadása nem
változtatja az eredményt[^1], formálisan $x \bigotimes y \bigotimes y = x \bigotimes y$.
Ez azt jelenti, hogy a kiválasztott intervallumoknak nem kell diszjunktnak lenniük,
amit kihasználva egy tetszőleges intervallumot le tudunk fedni $2$ intervallummal is.

``` {.prettyprint }
int kerdez(int l, int r) {
    int log2_egesz = log2(r - l + 1);
    int eredmeny = f(ht[log2_egesz][l], ht[log2_egesz][r - (1 << log2_egesz) + 1]);
    return eredmeny;
}
```

## Feladatok

[Cses - Static Range Sum Queries](https://cses.fi/problemset/task/1646)

[Cses - Static Range Minimum Queries](https://cses.fi/problemset/task/1647)

[Cses - Company Queries I](https://cses.fi/problemset/task/1687)

[*Cses - Company Queries II](https://cses.fi/problemset/task/1688)

[^1]: [https://hu.wikipedia.org/wiki/Idempotencia](https://hu.wikipedia.org/wiki/Idempotencia)
*[diszjunktnak]: metszés nélkülinek