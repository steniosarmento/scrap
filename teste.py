# Definir uma função para gerar a sequência de Fibonacci
def fibonacci(n):
  # Inicializar os dois primeiros termos
  a = 1
  b = 1
  # Criar uma lista vazia para armazenar os termos
  lista = []
  # Usar um loop for para iterar n vezes
  for i in range(n):
    # Adicionar o termo atual à lista
    lista.append(a)
    # Atualizar os valores de a e b
    a, b = b, a + b
  # Retornar a lista
  return lista

# Chamar a função com o argumento 15
print(fibonacci(15))