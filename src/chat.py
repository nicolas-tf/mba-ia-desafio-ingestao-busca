from search import search_prompt

def main():
    
    """
    Função principal para executar a interface de chat no terminal.
    
    Permite que o usuário faça perguntas continuamente e receba respostas
    baseadas no conteúdo do PDF ingerido.
    """

    print("=" * 60)
    print("BEM-VINDO AO CHAT DE BUSCA SEMÂNTICA")
    print("=" * 60)
    print("Digite sua pergunta e pressione Enter para obter uma resposta.")
    print("Digite algum dos comandos abaixo para encerrar o chat:")
    print("- sair")
    print("- exit")
    print("- quit")
    print("- Ctrl + C")
    print("")
    
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    while True:
        try:
            # Obter a pergunta do usuário
            question = input("PERGUNTA: ").strip()
            
            # Verificar se o usuário quer sair
            if question.lower() in ["sair", "exit", "quit"]:
                print("")
                print("=" * 60)
                print("CHAT ENCERRADO")
                print("=" * 60)
                break
            
            # Validar pergunta
            if not question:
                print("Por favor, digite uma pergunta válida.\n")
                continue
            
            # Buscar resposta
            print("\nProcessando sua pergunta...")
            answer = chain.invoke(question)
            
            # Exibir a resposta
            print(f"\nRESPOSTA: {answer}\n")
            print("-" * 60 + "\n")
        
        except KeyboardInterrupt:
            print("")
            print("=" * 60)
            print("CHAT ENCERRADO")
            print("=" * 60)
            break
        
        except Exception as error:
            print(f"\nOcorreu um erro: {error}")
            print("Por favor, tente novamente.\n")


if __name__ == "__main__":
    main()