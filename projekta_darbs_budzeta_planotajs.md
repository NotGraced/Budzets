# Budžeta plānotājs

## Programmas nosaukums
Budžeta plānotājs

## Mērķis
Projekta mērķis ir izveidot tīmekļa lietotni, kas palīdz lietotājam ērti reģistrēt ienākumus un izdevumus, automātiski aprēķināt bilanci un saglabāt ievadītos datus failā, lai tos varētu izmantot atkārtoti. Lietotne ir veidota kā vienkārša, saprotama un praktiska budžeta pārvaldīšanas sistēma ikdienas finanšu uzskaitei.

## Projekta uzdevumi
Projekta izstrādes laikā tika izvirzīti šādi uzdevumi:

1. Izveidot tīmekļa lietotni ar Flask ietvaru.
2. Nodrošināt iespēju pievienot jaunus ienākumu un izdevumu ierakstus.
3. Saglabāt datus CSV failā un ielādēt tos pēc programmas atkārtotas palaišanas.
4. Aprēķināt kopsummas: kopējos ienākumus, izdevumus un bilanci.
5. Attēlot ievadītos ierakstus pārskatāmā veidā.
6. Iekļaut datu filtrēšanu pēc tipa, mēneša un konta.
7. Nodrošināt ierakstu dzēšanu.
8. Pievienot validāciju nepareizi ievadītiem datiem.
9. Izveidot atsevišķu bilances lapu.
10. Izveidot pievilcīgu CSS dizainu un pārskatāmu lietotāja saskarni.

## Izmantotās tehnoloģijas
- Python
- Flask
- HTML
- CSS
- CSV datu glabāšanai

## Kā lietot programmu
1. Atver projekta mapi terminālī.
2. Palaid programmu ar komandu `python app.py`.
3. Interneta pārlūkā atver adresi `http://127.0.0.1:5000`.
4. Galvenajā lapā aizpildi formu, norādot ieraksta tipu, kontu, summu, aprakstu un datumu.
5. Nospied pogu "Pievienot", lai saglabātu jaunu ierakstu.
6. Lieto filtrus, lai atlasītu tikai ienākumus, tikai izdevumus, konkrētu mēnesi vai noteiktu kontu.
7. Apskati bilances lapu adresē `http://127.0.0.1:5000/bilance`.
8. Ja nepieciešams, dzēs kādu no ierakstiem.

## Ko programma prot
Programma spēj:

- pievienot ienākumus;
- pievienot izdevumus;
- pārvērst ievadīto summu par skaitli;
- pārbaudīt datuma ievadi;
- saglabāt datus CSV failā;
- ielādēt datus no CSV faila;
- aprēķināt kopējos ienākumus, izdevumus un bilanci;
- parādīt ierakstus saraksta veidā;
- filtrēt datus pēc tipa, mēneša un konta;
- dzēst ierakstus;
- parādīt atsevišķu bilances lapu;
- validēt lietotāja ievadītos datus;
- parādīt datus ar modernu dizainu.

## Programmas darbības apraksts
Lietotne darbojas kā budžeta plānošanas sistēma, kurā visi ieraksti tiek glabāti saraksta tipa mainīgajā un saglabāti CSV failā. Kad lietotājs pievieno jaunu ierakstu, programma pārbauda, vai dati ir korekti, pārvērš summu skaitliskā formātā, pārbauda datumu un saglabā ierakstu. Pēc tam visi dati tiek attēloti galvenajā lapā.

Programma automātiski apkopo datus un aprēķina:

- kopējos ienākumus;
- kopējos izdevumus;
- pašreizējo bilanci;
- vidējo ieraksta summu;
- lielāko izdevumu;
- kontu atlikumus;
- mēnešu statistiku grafikiem.

Papildus tam programma nodrošina filtrēšanu, lai lietotājs varētu atlasīt tikai sev vajadzīgos ierakstus. Dati tiek saglabāti failā `dati.csv`, tāpēc, aizverot programmu, informācija nepazūd.

## Galvenās funkcijas un to apraksts

### `parse_amount(value)`
Šī funkcija pārbauda lietotāja ievadīto summu. Tiek aizvietots komats ar punktu, lai summu varētu pārvērst par `float` tipu. Ja summa ir mazāka vai vienāda ar nulli, tiek parādīta kļūda.

### `parse_date(value)`
Šī funkcija pārbauda, vai datums ir ievadīts pareizā formātā `YYYY-MM-DD`. Ja datums nav ievadīts, tiek izmantots šodienas datums.

### `parse_account(value)`
Šī funkcija pārbauda, vai lietotājs ir izvēlējies derīgu kontu no atļauto kontu saraksta.

### `load_data()`
Funkcija ielādē ierakstus no faila `dati.csv`. Ja fails neeksistē, programma izmanto demonstrācijas datus. Tas nodrošina, ka lietotne nestrādā ar tukšu skatu.

### `save_data()`
Funkcija saglabā visus ierakstus CSV failā. Katram ierakstam tiek saglabāts identifikators, tips, summa, apraksts, datums un konts.

### `calculate_totals(records)`
Šī funkcija aprēķina ienākumu un izdevumu kopsummu, kā arī bilanci. Bilance tiek iegūta, no ienākumiem atņemot izdevumus.

### `build_dashboard_data(records)`
Šī funkcija sagatavo datus informācijas panelim un grafikiem. Tiek aprēķināta ienākumu un izdevumu proporcija, ierakstu skaits mēnesī, vidējā summa, lielākais izdevums, kontu kopsavilkums un dati diagrammām.

### `filter_records(...)`
Šī funkcija atlasa ierakstus pēc lietotāja izvēlētajiem filtriem. Ir iespējams filtrēt pēc ieraksta tipa, mēneša un konta.

### `build_history_preview(records)`
Šī funkcija nodala redzamākos jaunākos ierakstus no pārējiem, lai galvenā lapa būtu pārskatāma.

## Programmas lapas

### Galvenā lapa `/`
Galvenajā lapā lietotājs var:

- apskatīt kopsavilkumu par budžetu;
- pievienot jaunu ierakstu;
- filtrēt datus;
- redzēt kontu pārskatu;
- apskatīt darījumu vēsturi;
- redzēt grafikus.

### Pievienošanas darbība `/pievienot`
Šis ceļš apstrādā formu, pievieno jaunu ierakstu un saglabā to failā.

### Dzēšanas darbība `/dzest/<entry_id>`
Šis ceļš ļauj izdzēst konkrētu ierakstu pēc tā identifikatora.

### Bilances lapa `/bilance`
Šajā lapā tiek parādīts pilns bilances pārskats, visi ieraksti un kontu kopsavilkums.

## Validācija un kļūdu apstrāde
Projektā tika ieviesta datu validācija, lai nepieļautu nekorektu datu ievadi. Programma pārbauda:

- vai ieraksta tips ir pareizs;
- vai apraksts nav tukšs;
- vai summa ir skaitlis un lielāka par nulli;
- vai datums ir pareizā formātā;
- vai konts ir izvēlēts no atļautajām vērtībām.

Ja lietotājs ievada kļūdainus datus, programma neatļauj tos saglabāt un parāda kļūdas paziņojumu.

## Dizains
Programmai tika izveidots moderns vizuālais noformējums ar CSS. Saskarnei tika izveidotas:

- galvenes kartītes;
- statistikas bloki;
- filtrēšanas paneļi;
- darījumu saraksts;
- bilances pārskati;
- joslu un līniju grafiku attēlojums;
- personalizēta krāsu tēma violetos toņos.

Tika arī pielāgots fons un kopējais izskats, lai lietotne būtu vizuāli pievilcīga un viegli lietojama.

## Kas tika izdarīts projektā
Projekta izstrādes laikā tika paveikts sekojošais:

1. Izveidota Flask tīmekļa lietotne.
2. Izveidota forma ienākumu un izdevumu pievienošanai.
3. Pievienota summas, datuma un konta validācija.
4. Izveidota datu saglabāšana CSV failā.
5. Izveidota datu ielāde no CSV faila.
6. Izveidota bilances aprēķināšana.
7. Izveidota ierakstu filtrēšana.
8. Pievienota ierakstu dzēšana.
9. Izveidota atsevišķa bilances lapa.
10. Izveidoti kontu pārskati un statistikas bloki.
11. Izveidoti vienkārši grafiki ienākumu un izdevumu attēlošanai.
12. Izveidots moderns dizains ar pielāgotu krāsu tēmu.

## Ekrānattēli
Šajā sadaļā Word dokumentā jāievieto ekrānattēli no programmas. Ieteicams pievienot:

1. Galvenās lapas ekrānattēlu.
2. Ieraksta pievienošanas formas ekrānattēlu.
3. Filtrēšanas sadaļas ekrānattēlu.
4. Darījumu vēstures ekrānattēlu.
5. Bilances lapas ekrānattēlu.
6. Piemēru ar kļūdas paziņojumu, ja ievadīti nepareizi dati.

## Secinājumi
Izstrādājot projektu "Budžeta plānotājs", tika izveidota funkcionējoša tīmekļa lietotne personīgo finanšu uzskaitei. Projekta laikā tika nostiprinātas zināšanas Python programmēšanā, darbā ar Flask ietvaru, HTML un CSS izkārtojumu veidošanā, kā arī datu saglabāšanā failos.

Svarīgākais ieguvums bija tas, ka programma ne tikai pieņem lietotāja ievadi, bet arī apstrādā datus, pārbauda kļūdas, filtrē rezultātus un attēlo pārskatāmu bilanci. Tas padara projektu daudz pilnvērtīgāku nekā vienkāršs saraksts ar ierakstiem.

Nākotnē programmu varētu papildināt ar:

- lietotāju kontiem;
- datubāzi CSV faila vietā;
- diagrammām ar vēl plašāku statistiku;
- kategorijām izdevumiem;
- datu eksportu PDF vai Excel formātā.

Kopumā projekts ir izdevies, jo tas izpilda uzdevumā prasītās funkcijas un piedāvā ērtu, saprotamu un vizuāli pievilcīgu budžeta plānošanas risinājumu.
