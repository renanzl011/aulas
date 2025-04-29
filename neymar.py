import random


palavras = ['oceano', 'programacao', 'desenvolvimento', 'harry potter', 'computador','microorganismo','O Poderoso Chefão', 'g20']

palavra_secreta = random.choice(palavras)
letras_adivinhadas = set()
tentativas = 8

print("Bem-vindo ao Jogo da Forca!")

while tentativas > 0:
    # Exibir a palavra com letras adivinhadas
    palavra_exibida = ' '.join([letra if letra in letras_adivinhadas else '_' for letra in palavra_secreta])
    print("\nPalavra:", palavra_exibida)
    print(f"Tentativas restantes: {tentativas}")
    
    letra = input("Adivinhe uma letra: ").lower()

    if letra in letras_adivinhadas:
        print("Você já adivinhou essa letra. Tente outra.")
        continue

    letras_adivinhadas.add(letra)

    if letra in palavra_secreta:
        print("Boa! A letra está na palavra.")
    else:
        tentativas -= 1
        print("Ops! A letra não está na palavra.")

    if all(letra in letras_adivinhadas for letra in palavra_secreta):
        print(f"Parabéns! Você adivinhou a palavra: {palavra_secreta}")
        break
else:
    print(f"Você perdeu! A palavra era: {palavra_secreta}")
