def eh_palindromo(palavra):
    """
    Verifica se uma palavra é um palíndromo.
    
    Args:
        palavra (str): A palavra a ser verificada
        
    Returns:
        bool: True se for palíndromo, False caso contrário
    """
    # Remove espaços e converte para minúsculas
    palavra_limpa = palavra.replace(" ", "").lower()
    
    # Inverte a palavra
    palavra_invertida = palavra_limpa[::-1]
    
    # Compara a palavra original com a invertida
    return palavra_limpa == palavra_invertida


# Testando a função
if __name__ == "__main__":
    teste1 = "aba"
    teste2 = "radar"
    teste3 = "python"
    teste4 = "A man a plan a canal Panama"
    
    print(f"'{teste1}' é palíndromo? {eh_palindromo(teste1)}")
    print(f"'{teste2}' é palíndromo? {eh_palindromo(teste2)}")
    print(f"'{teste3}' é palíndromo? {eh_palindromo(teste3)}")
    print(f"'{teste4}' é palíndromo? {eh_palindromo(teste4)}")