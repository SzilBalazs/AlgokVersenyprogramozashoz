# Bináris keresés
A bináris keresés (angolul binary search) egy gyorsabb keresési módszer, amely során mindig felezzük a keresési intervallumot. Rengeteg alkalmazása van, leggyakrabban rendezett tömbökben egy adott érték megtalálására használjuk.

## Rendezett tömbökben keresés

Az egyik leggyakoribb, bináris kereséssel megoldható probléma a következő: Adott egy rendezett tömb $A_0 \leq A_1 \leq \dots \leq A_{n-1}$, nézzük meg, hogy $k$ benne van-e a tömbben. A legegyszerűbb megoldás, hogy az összes elemen végigmegyünk és összehasonlítjuk őket $k$-val (ez az úgynevezett lineáris keresés). Ez a megoldás $O(n)$ lépést használ, azonban nem használja ki, hogy a tömb rendezett.

Tegyük fel, hogy tudunk két indexet $L\leq{R}$, amikre teljesül, hogy $A_L \leq k \leq A_R$. Mivel a tömb rendezett, ezért tudjuk, hogy ha $k$ előfordul bárhol a tömbben, akkor a $A_L, A_{L+1}, \dots, A_R$ számok közt kell előfordulnia. Válasszunk ki egy $M$ indexet, amire $L \leq M < R$, és nézzük meg, hogy $k$ nagyobb vagy kisebb-e $a_{M}$-nél. Kétféle eset van:

1. $A_L \leq k < A_M$. Ebben az esetben elég folytatnunk a keresést az $[L, R]$ intervallum helyett az $[L, M-1]$ intervallumon.

2. $A_M \leq k \leq A_R$. Ebben az esetben elég folytatnunk a keresést az $[L, R]$ intervallum helyett az $[M, R]$ intervallumon.

Mikor már nem tudunk jó értéket választani $M$-nek, mivel $L=R$, akkor már csak $A_L$-t és $k$-t kell összehasonlítanunk. Egyébként pedig úgy szeretnénk kiválasztani $M$ értékét, hogy a legrosszabb esetben is a lehető leggyorsabban csökkenjen le a szakasz egy elemre.

A legrosszabb eset azt jelenti, hogy az $[L, M-1]$ és az $[M, R]$ intervallumok közül mindig a nagyobb marad meg. így a legrosszabb esetben a intervallum mérete $R-L+1$-ről, $\max(M-L, R-M+1)$-re csökken. Ezt az értéket próbáljuk minimalizálni, legyen ehhez $M \approx \frac{L+R}{2}$, így:
$$M-L \approx \frac{R-L+1}{2} \approx R-M+1$$
Máshogy fogalmazva, ha biztosan gyors keresést akarunk, akkor az optimális, ha mindig az $[L, R]$ intervallum közepében választjuk ki $M$-et. így az aktív intervallum mérete mindig feleződik, egészen addig, amíg el nem éri az $1$-et. Tehát ha a keresés $h$ lépésbe telik, ami alatt az intervallum méretét $R-L+1$-ről, $\frac{R-L+1}{2^h} \approx 1$-re csökkenti, akkor igaz, hogy $2^h \approx R-L+1$.

Ha van egy tulajdonságunk, ami $0$-tól $n-1$-ig kezdetben semmelyik pontra sem teljesül, majd utána mindegyik pontra teljesül, akkor bináris keresés segítségével megmondhatjuk az utolsó pontot, amire még nem teljesül a tulajdonság. Ez különösen hasznos tud lenne, ha a tulajdonság teljesülésének leellenőrzése minden egyes pontra túl sok időt venne igénybe.

Ha a két oldal $2$-es alapú logaritmusát vesszük, akkor $h \approx \log_2(R-L+1)$, vagyis az algoritmus lépésszáma $O(\log n)$, ahol $n$ az eredeti intervallum mérete.

A logaritmus számú lépésszám drasztikusan jobb, mint a lineáris keresesésnél. Például ha $n \approx 2^{20} \approx 10^6$, akkor egy lineáris keresésben nagyjából egymillió lépést kellene megtenni, míg a bináris kereséssel csak körülbelül $20$-at.

## Alsó határ és felső határ

Sokszor szükséges az első olyan elem pozícióját megtalálni, ami nem kisebb mint $k$ (ezt nevezik $k$ alsó határának a tömbben) vagy pedig az első olyan elem pozícióját, ami nagyobb mint $k$. Ezek segítségével meghatározhatjuk, hogy $k$ benne van-e a tömbben, ehhez csupán meg kell néznünk $k$ alsó határát, és ellenőriznünk kell, hogy egyenlő-e $k$-val.

A c++ nyelvben ezekre a keresésekre van beépített függvény, ami az ```<algorithm>``` header fájlben van implementálva. Az alsó határra az ```std::lower_bound```, míg a felső határra a ```std::upper_bound``` függvény.

## Implementáció

A fenti leírás nagyjából elmagyarázza az algoritmus lényeget, azonban az implementációhoz precízebbnek kell lennünk.

Fenntartunk egy $L$ és $R$ változót, úgy hogy $L < R$, és amikre teljesül, hogy $A_L \leq k < A_R$. Ez azt jelenti, hogy jelenleg a keresési intervallum a $[L, R)$ balról zárt, jobbról nyitott intervallum. Az implementáció során nem zárt intervallumokat használnuk, mivel így kevesebb speciális esettel kell foglalkoznunk.

állítsuk be úgy $L$ és $R$ értékét, hogy $L$ a tömb kezdete előtti index legyen, mik $R$ a tömb vége utáni index, így $L=-1$ és $R=n$.

$M$ értékét is meg kell határoznunk pontosan, legyen $M = \lfloor \frac{L+R}{2} \rfloor$.

Ezután a keresés így néz ki:
```
...//  a rendezett tomb elemei a[0], a[1], ..., a[n-1]
int l = -1, r = n;
while(r - l > 1) {
    int m = (l + r) / 2;
    if(k < a[m]) {
        r = m; // a[l] <= k < a[m] <= a[r]
    } else {
        l = m; // a[l] <= a[m] <= k < a[r]
    }
}
```

Az algoritmus végén $L$ az utolsó elem indexe lesz, ami még nem nagyobb mint $k$ (ha nincs ilyen akkor pedig $-1$), $R$ pedig az első olyan elem indexe, ami már nagyobb mint $k$ (ha nincs ilyen, akkor pedig $n$).

## Keresés bármilyen tulajdonságnál

Ha van egy tulajdonságunk, amely a $0$-tól $n-1$-ig pontokon egy pontig minden pontra teljesül, majd utána egyik pontra sem, akkor ezt a választó pontot meg tudjuk találni bináris kereséssel. Ez a módszer akkor hasznos különösen, ha a tulajdonság teljesülésének leelenőrzése sok időbe telik, így nem tehetjük meg minden egyes pontra.

## A válasz bináris keresése

Előfordulhat, hogy valamilyen értéket kell kiszámolnunk, azonban csak azt tudjuk megnézni, hogy a válasz legalább $i$. Például vegyük a következő feladatot: Adott egy táblázat pozitív egész számokkal, mondjuk meg, hogy melyik az a legnagyobb $L$ érték amire létezik olyan $L\times{L}$-es négyzet, ahol minden elem értéke legalább $L$. Itt könnyen látható, hogy ha egy $L$-re teljesül ez a tulajdonság akkor minden nála kisebb $L$-re is teljesül, mígha egy adott $L$-re nem teljesül, akkor semmelyik nála nagyobb $L$-re sem fog. Így a választ kereshetjük binárisan, és a tulajdonság vizsgálatánál megnézünk minden $L\times{L}$-es négyzetet.

## Keresés kettőhatványokkal

Sokszor a tulajdonság teljesülésének leellenőrzése könnyeb, ha mindig kettőhatvánnyokkal növeljük a megnézendő helyet. Ehhez fenntartunk egy $i$ és $k$ változót, ahol $i$ a jelenlegi szám aminél vizsgáljuk, $k$ pedig az épp vizsgált kettőhatvány kitevője. Ha az $i+2^k$-ra sem teljesül a feltétel, akkor ez lesz az új $i$ érték, egyébként marad az eredeti.