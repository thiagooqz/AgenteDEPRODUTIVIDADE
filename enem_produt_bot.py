import time
from datetime import datetime, timedelta
import google.generativeai as genai

API_KEY = "CHAVE API"

def configurar_api():
    genai.configure(api_key=API_KEY)

def mostrar_menu():
    print("\nBem-vindo ao Agente Produtividade!\n")
    print("1. Criar novo plano de estudos com IA")
    print("2. Visualizar agenda")
    print("3. Pedir dicas de produtividade para IA")
    print("4. Iniciar sessão de estudo")
    print("5. Relatório de produtividade")
    print("6. Sair")

def coletar_informacoes_usuario():
    print("\n--- Vamos conhecer melhor seus objetivos e rotina ---")
    info = {}
    
    # Informações básicas
    info['nome'] = input("Qual é o seu nome? ")
    info['idade'] = input("Qual sua idade? ")
    info['objetivo'] = input("Qual seu principal objetivo de estudo? (ex: ENEM, concurso, etc): ")
    
    # Horários disponíveis
    print("\nSobre sua rotina diária:")
    info['hora_acordar'] = input("Que horas você costuma acordar? (formato HH:MM): ")
    info['hora_dormir'] = input("Que horas você costuma dormir? (formato HH:MM): ")
    
    # Compromissos fixos
    info['tem_trabalho'] = input("Você trabalha ou estuda em período fixo? (S/N): ").lower() == 's'
    if info['tem_trabalho']:
        info['hora_trabalho_inicio'] = input("Horário de início: (HH:MM): ")
        info['hora_trabalho_fim'] = input("Horário de término: (HH:MM): ")
    
    # Preferências de estudo
    print("\nSobre suas preferências de estudo:")
    info['periodo_produtivo'] = input("Em qual período você se sente mais produtivo?\n1. Manhã\n2. Tarde\n3. Noite\nEscolha: ")
    info['estilo_aprendizagem'] = input("Como você aprende melhor?\n1. Lendo\n2. Assistindo vídeos\n3. Praticando\n4. Mistura de métodos\nEscolha: ")
    info['materias'] = input("Digite as matérias que precisa estudar (separadas por vírgula): ").split(',')
    
    # Metas e desafios
    print("\nSobre suas metas e desafios:")
    info['horas_disponiveis'] = float(input("Quantas horas por dia você tem disponível para estudar? "))
    info['dias_semana'] = input("Quais dias da semana você pode estudar? (1-Seg, 2-Ter, 3-Qua, 4-Qui, 5-Sex, 6-Sab, 7-Dom)\nDigite os números separados por vírgula: ")
    info['dificuldades'] = input("Quais são suas principais dificuldades nos estudos? ")
    info['prazo'] = input("Qual é o prazo para atingir seu objetivo? (ex: 6 meses, 1 ano): ")
    
    return info

def gerar_agenda_com_ia(info):
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Preparando valores condicionalmente
        trabalho_estuda = f"Sim, das {info['hora_trabalho_inicio']} às {info['hora_trabalho_fim']}" if info['tem_trabalho'] else "Não"
        periodo_produtivo = {"1": "Manhã", "2": "Tarde", "3": "Noite"}[info['periodo_produtivo']]
        estilo_aprendizagem = {"1": "Visual/Leitura", "2": "Audiovisual", "3": "Prático", "4": "Misto"}[info['estilo_aprendizagem']]

        # Criando o prompt para a IA
        prompt = f"""
        Atue como um especialista em produtividade e planejamento de estudos. 
        Crie uma agenda de estudos detalhada e personalizada com base nas seguintes informações:

        Nome: {info['nome']}
        Idade: {info['idade']}
        Objetivo: {info['objetivo']}
        Horário de acordar: {info['hora_acordar']}
        Horário de dormir: {info['hora_dormir']}
        Trabalha/Estuda: {trabalho_estuda}
        Período mais produtivo: {periodo_produtivo}
        Estilo de aprendizagem: {estilo_aprendizagem}
        Matérias: {", ".join(info['materias'])}
        Horas disponíveis por dia: {info['horas_disponiveis']}
        Dias disponíveis: {info['dias_semana']}
        Dificuldades: {info['dificuldades']}
        Prazo: {info['prazo']}
        """
        
        response = model.generate_content(prompt)
        return response.text if response else "Não foi possível gerar o cronograma."
    
    except Exception as e:
        return f"Erro ao consultar a IA: {e}"

def pedir_dicas_ia(info):
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Como especialista em produtividade, forneça dicas personalizadas de estudo para:
        
        Perfil: Estudante de {info['objetivo']}
        Principais dificuldades: {info['dificuldades']}
        Estilo de aprendizagem: {info['estilo_aprendizagem']}
        
        Forneça:
        1. 3 técnicas de estudo específicas para o perfil
        2. 2 sugestões para superar as dificuldades mencionadas
        3. 1 rotina de revisão personalizada
        """
        
        response = model.generate_content(prompt)
        return response.text if response else "Não foi possível gerar dicas."
    
    except Exception as e:
        return f"Erro ao consultar a IA: {e}"

def iniciar_sessao_estudo():
    print("\n=== Iniciar Sessão de Estudo ===")
    duracao = int(input("Digite a duração da sessão em minutos: "))
    cronometrar(duracao)

def cronometrar(minutos):
    print(f"\nCronômetro iniciado por {minutos} minutos.")
    print("Pressione Ctrl+C para interromper")
    try:
        time.sleep(minutos * 60)
        print("\nTempo finalizado! Sessão concluída.")
    except KeyboardInterrupt:
        print("\nSessão interrompida pelo usuário.")

def main():
    configurar_api()
    info_usuario = None
    agenda = None
    
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            info_usuario = coletar_informacoes_usuario()
            print("\nGerando seu cronograma personalizado com IA...")
            agenda = gerar_agenda_com_ia(info_usuario)
            print("\nSeu cronograma personalizado:")
            print(agenda)
        elif opcao == "2":
            if agenda:
                print("\n=== Sua Agenda ===")
                print(agenda)
            else:
                print("\nNenhuma agenda criada ainda. Escolha a opção 1 primeiro.")
        elif opcao == "3":
            if info_usuario:
                print("\nConsultando IA para dicas personalizadas...")
                dicas = pedir_dicas_ia(info_usuario)
                print("\nDicas personalizadas:")
                print(dicas)
            else:
                print("\nPrimeiro crie seu perfil escolhendo a opção 1.")
        elif opcao == "4":
            iniciar_sessao_estudo()
        elif opcao == "5":
            if agenda:
                print("\nRelatório de produtividade em desenvolvimento...")
            else:
                print("\nNenhuma agenda criada ainda. Escolha a opção 1 primeiro.")
        elif opcao == "6":
            print("\nEncerrando Agente Produtividade. Bons estudos!")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
