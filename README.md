#  Jezik i alat za kreiranje IF (Interactive Fiction) igara sa grafickim korisnickim interfejsom uz dodatak generisanja slika na osnovu teksta

## Struktura projekta

- `gameFrame.py`: Ova datoteka sadrži kod koji upravlja grafickim interfejsom za igranje igrica.

- `gameInterpreter.py`: U ovom fajlu se kreiraju Python klase interpretiranjem informacije dobijenih parsiranjem igrica napisanih u gameWorldDSL.tx.

- `gui.py`: Ova datoteka sadrži kod za graficki interfejs koji se sastoji od pocetnog ekrana, dela za kreiranje IF, dela za
     ucitavanje koda igrica i izbora igara za igranje.

- `simpleGame.game`: Ovo je primer jedne igre napisane u gameWorldDSL.tx-u.

- `gameWorldDSL.tx`: Ova datoteka sadrži opis Domain-Specific Language (DSL) kojim je moguce pisati igre.

- `dslClasses.py`: Ovaj fajl sadrži Python interpretaciju klasa definisanih u gameWorldDSL.tx formatu.

## Uputstvo za pokretanje projekta

Pokrenuti main.py

## Zavisnosti

- stable-diffusion-v1-5 lokalno instaliran
- Pillow~=10.0.0
- diffusers~=0.19.0
- textX~=3.1.1
- pip install transformers
- pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  (gpu sa CUDA jezgrima)
- pip install accelerate
