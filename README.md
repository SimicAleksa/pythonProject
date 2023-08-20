# Jezik i alat za kreiranje IF (Interactive Fiction) igara sa grafickim korisnickim interfejsom uz dodatak generisanja slika na osnovu teksta

## Instaliranje
Pre same instalacije ovog alata, potrebno je instalirati PyTorch, koji je neophodan za rad sa modelima vestacke inteligencije. Možete ga instalirati pomocu sledece komande:
`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

``` 
**Napomena**
Neophodno je posedovanje graficke kartice sa CUDA jezgrima  
```

Nakon toga takodje u konzoli pokrecete sledecu komandu:
`pip install if-dsl-gui-ai`


## Inicijalno postavljanje
1. Nakon instalacije, potrebno je da u root direktorijumu svog projekta kreirate direktorijum sa nazivom `if_dsl_gui_ai`.
2. U novokreiranom direktorijumu kreirati jos jedan sa nazivom `games`.  
  *(ostatak je opcionalan ukoliko želite da imate primer igre)*
3. U `games` folderu kreirajte novi folder sa nazivom `simpleGame.game`.
4. U `simpleGame.game` prekopirajte sledece stvari iz `venv/Lib/site-packages/if_dsl_gui_ai`:
    - Slike: `backyard.png`, `entryway.png`, `hallway.png`, `kitchen.png`
    - IF igru: `simpleGame.game`

## Uputstvo za pokretanje projekta
- Importujte `main` iz `if_dsl_gui_ai`.
- U vas kod dodajte `main.App()`.
- Pokrenite vasu aplikaciju.

## Kako i sta?
- Za pregled svih igara i izbor za igranje birate `Library`.
- Za kreiranje novih IF igrica, birate `CreateFiction`.
- Za igranje IF igre, idite u `Library`, izaberite igru, a zatim kliknite dugme `Play`.
- Za kreiranje slika za vasu IF igru, izaberite igru, zatim kliknite dugme `Picture creator`.
- Za pregled koda vase IF igre, idite u `Library`, izaberite igru, a zatim kliknite dugme `Load code`.

## Struktura projekta
- `gameFrame.py`: Ova datoteka sadrži kod koji upravlja grafickim interfejsom za igranje igrica.
- `gameInterpreter.py`: U ovom fajlu se kreiraju Python klase interpretiranjem informacija dobijenih parsiranjem igrica napisanih u `gameWorldDSL.tx`.
- `gui.py`: Ova datoteka sadrži kod za graficki interfejs koji se sastoji od pocetnog ekrana, dela za kreiranje IF, dela za
     ucitavanje koda igrica i izbora igara za igranje, kao i dela za kreiranje slika igre.
- `main.py`: Startni fajl.
- `pictureCreatorFrame.py`: GUI za kreiranje slika IF igre.
- `codeEditorFrame.py`: Code editor za pisanje IF igre.
- `simpleGame.game`: Ovo je primer jedne igre napisane u `gameWorldDSL.tx`-u.
- `gameWorldDSL.tx`: Ova datoteka sadrži opis Domain-Specific Language (DSL) kojim je moguce pisati igre.
- `dslClasses.py`: Ovaj fajl sadrži Python interpretaciju klasa definisanih u `gameWorldDSL.tx` formatu.

##Dodatno
- Za brzi rad aplikacije skinite [*Stable diffusion*](https://huggingface.co/runwayml/stable-diffusion-v1-5) sa sajta [*huggingface*](https://huggingface.co.)
- Zatim je potrebno da kreirate novu *Environment variable*-u sa nazivom `SDV5_MODEL_PATH` i vrednoscu koja predstavlja putanju do *Stable diffusion*-a na vasem racunaru
