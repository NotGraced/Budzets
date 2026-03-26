# Budžeta plānotājs

## Programmas nosaukums
Budžeta plānotājs

## Mērķis
Programma palīdz lietotājam reģistrēt ienākumus un izdevumus, automātiski aprēķināt bilanci un saglabāt datus CSV failā, lai tos varētu izmantot atkārtoti.

## Kā lietot programmu
1. Atver termināli projekta mapē.
2. Palaid programmu ar komandu `python app.py`.
3. Pārlūkā atver adresi `http://127.0.0.1:5000`.
4. Ievadi summu, aprakstu, tipu un datumu.
5. Lieto filtrus, lai atlasītu tikai ienākumus, izdevumus vai konkrētu mēnesi.
6. Atver lapu `/bilance`, lai redzētu kopējo pārskatu.
7. Dzēs ierakstus, ja tie vairs nav vajadzīgi.

## Ekrānattēli
Pēc programmas palaišanas ieteicams pievienot:
- sākumlapas ekrānattēlu;
- bilances lapas ekrānattēlu;
- filtra vai validācijas kļūdas piemēra ekrānattēlu.

## Koda apraksts
- `load_data()` ielādē ierakstus no `dati.csv`, ja fails eksistē.
- `save_data()` saglabā visus ierakstus CSV failā.
- `parse_amount()` pārbauda un pārvērš summu par `float`.
- `parse_date()` validē datumu formātā `YYYY-MM-DD`.
- `calculate_totals()` aprēķina ienākumus, izdevumus un bilanci.
- `filter_records()` atlasa ierakstus pēc tipa un mēneša.
- `/` attēlo galveno lapu ar formu, filtriem un tabulu.
- `/pievienot` pievieno jaunu ierakstu.
- `/dzest/<entry_id>` izdzēš izvēlēto ierakstu.
- `/bilance` parāda kopējo bilances pārskatu.

## Secinājumi
Projektā tika izveidota pilnvērtīga Flask tīmekļa lietotne ar datu ievadi, validāciju, filtrēšanu, bilances aprēķinu, saglabāšanu CSV failā un pārskatāmu dizainu. Programmu var viegli paplašināt, piemēram, pievienojot diagrammas vai lietotāja kontus.
